import subprocess
import time
from shutil import which
from appium.webdriver.appium_service import AppiumService
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

class AppiumRunner:
    def __init__(self, server_url: str, caps: dict):
        self.server = AppiumService()
        self.server_args = {
            'args': ['--address', '127.0.0.1', '--port', '4723']
        }
        self.server_url = server_url
        self.caps = caps
        self.driver = None

    @staticmethod
    def ensure_appium_installed():
        """
        Checks if the Appium CLI and Python client are installed. Installs them if missing.
        """
        # Check Appium CLI
        if which('appium') is None:
            print("Appium CLI not found. Installing via npm...")
            subprocess.run(['npm', 'install', '-g', 'appium'], check=True)
            print("Appium CLI installed successfully.")
        else:
            print("Appium CLI is already installed.")
        # Check Appium Python client
        try:
            import appium
            print("Appium Python client is already installed.")
        except ImportError:
            print("Appium Python client not found. Installing via pip...")
            subprocess.run(['pip', 'install', 'Appium-Python-Client'], check=True)
            print("Appium Python client installed successfully.")

    def start(self):
        # 0) ensure Appium CLI is available
        self.ensure_appium_installed()
        # 1) start Appium server
        self.server.start(**self.server_args)
        if not self.server.is_running:
            raise RuntimeError("Appium server failed to start")
        print("Appium server started")

        # 2) start WebDriver session
        self.driver = webdriver.Remote(self.server_url, self.caps)
        self.driver.implicitly_wait(10)
        print("Appium session started")

    def run_steps(self, steps: list, inputs: dict):
        for step in steps:
            if 'fill' in step:
                config = step['fill']
                element = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, config['selector'])
                element.clear()
                element.send_keys(inputs.get(config['text_from_input'], ''))

            elif 'tap' in step:
                element = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, step['tap'])
                element.click()

            elif 'wait' in step:
                time.sleep(step['wait'])

            elif 'screenshot' in step:
                filename = f"{step['screenshot']}.png"
                self.driver.save_screenshot(filename)
                print(f"Saved screenshot: {filename}")

            else:
                raise ValueError(f"Unknown step: {step}")

    def stop(self):
        if self.driver:
            self.driver.quit()
            print("Appium session quit")
        if self.server.is_running:
            self.server.stop()
            print("Appium server stopped")

