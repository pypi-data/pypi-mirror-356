import subprocess
import xml.etree.ElementTree as ET
import json
import re
import time

class FlowExecutor:
    """
    Executes UI flow steps on iOS or Android by dumping and parsing the live UI hierarchy,
    locating elements by ID/text, then injecting taps and text input at their centers.

    Usage:
        executor = FlowExecutor(platform, device)
        executor.run_steps(steps, inputs)

    - platform: 'ios' or 'android'
    - device: UDID (iOS) or adb device/emulator name (Android)
    """
    def __init__(self, platform: str, device: str):
        self.platform = platform.lower()
        self.device = device

    def run_steps(self, steps: list, inputs: dict) -> None:
        for step in steps:
            if 'fill' in step:
                cfg = step['fill']
                sel = cfg['selector']
                text = inputs.get(cfg['text_from_input'], '')
                # tap field then type
                x, y = self._locate(sel)
                self._tap_coord(x, y)
                self._type_text(text)

            elif 'tap' in step:
                sel = step['tap']
                x, y = self._locate(sel)
                self._tap_coord(x, y)

            elif 'wait' in step:
                time.sleep(step['wait'])

            elif 'screenshot' in step:
                name = f"{step['screenshot']}.png"
                self._screenshot(name)

            else:
                raise ValueError(f"Unknown step: {step}")

    def _locate(self, identifier: str) -> tuple[int,int]:
        """
        Dump and parse the UI tree to find element's center by its ID or label.
        """
        if self.platform == 'android':
            xml = self._dump_ui_android()
            return self._find_element_android(xml, resource_id=identifier)
        else:
            js = self._dump_ui_ios()
            return self._find_element_ios(js, identifier=identifier)

    # --- Android helpers ---
    def _dump_ui_android(self) -> str:
        subprocess.run(['adb', 'shell', 'uiautomator', 'dump', '/sdcard/view.xml'], check=True)
        subprocess.run(['adb', 'pull', '/sdcard/view.xml', '.'], check=True)
        return 'view.xml'

    def _find_element_android(self, xml_path: str, resource_id: str=None, text: str=None) -> tuple[int,int]:
        tree = ET.parse(xml_path)
        for node in tree.findall('.//node'):
            attrs = node.attrib
            if resource_id and attrs.get('resource-id', '').endswith(resource_id):
                return self._center_from_bounds(attrs['bounds'])
            if text and attrs.get('text') == text:
                return self._center_from_bounds(attrs['bounds'])
        raise RuntimeError(f"Android element '{resource_id or text}' not found")

    def _center_from_bounds(self, bounds_str: str) -> tuple[int,int]:
        nums = list(map(int, re.findall(r'\d+', bounds_str)))
        x1,y1,x2,y2 = nums
        return ((x1+x2)//2, (y1+y2)//2)

    # --- iOS helpers ---
    def _dump_ui_ios(self) -> str:
        with open('tree.json', 'w') as f:
            subprocess.run(
                ['xcrun', 'simctl', 'ui', self.device, 'dumpAccessibilityTree'],
                stdout=f, check=True
            )
        return 'tree.json'

    def _find_element_ios(self, json_path: str, identifier: str=None, label: str=None) -> tuple[int,int]:
        data = json.load(open(json_path))
        frame = self._search_tree(data, identifier)
        if not frame:
            raise RuntimeError(f"iOS element '{identifier}' not found")
        return (frame['x'] + frame['width']//2, frame['y'] + frame['height']//2)

    def _search_tree(self, node: dict, identifier: str=None) -> dict|None:
        if node.get('identifier') == identifier or node.get('label') == identifier:
            return node.get('frame')
        for child in node.get('children', []):
            res = self._search_tree(child, identifier)
            if res:
                return res
        return None

    # --- Action injections ---
    def _tap_coord(self, x: int, y: int) -> None:
        if self.platform == 'android':
            subprocess.run(['adb', 'shell', 'input', 'tap', str(x), str(y)], check=True)
        else:
            subprocess.run(['xcrun', 'simctl', 'ui', self.device, 'tap', str(x), str(y)], check=True)

    def _type_text(self, text: str) -> None:
        if not text:
            return
        if self.platform == 'android':
            subprocess.run(['adb', 'shell', 'input', 'text', text], check=True)
        else:
            subprocess.run(['xcrun', 'simctl', 'io', self.device, 'keyboard', 'text', text], check=True)

    def _screenshot(self, filename: str) -> None:
        if self.platform == 'android':
            cmd = f'adb exec-out screencap -p > {filename}'
            subprocess.run(cmd, shell=True, check=True)
        else:
            subprocess.run(['xcrun', 'simctl', 'io', self.device, 'screenshot', filename], check=True)
        print(f"Screenshot saved: {filename}")
