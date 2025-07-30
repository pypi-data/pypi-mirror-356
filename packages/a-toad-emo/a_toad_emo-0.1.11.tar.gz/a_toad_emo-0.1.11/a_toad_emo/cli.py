import argparse
from a_toad_emo.emulator_launcher import EmulatorLauncher
from a_toad_emo.config_loader import load_config
from a_toad_emo.app_installer import AppInstaller
from a_toad_emo.app_runner import AppRunner
from a_toad_emo.appium_runner import AppiumRunner

def main():
    parser = argparse.ArgumentParser(description="A Toad Emo - Auto App Demo generate tool.")
    parser.add_argument(
        "--headless",
        type=str.lower,
        choices=["true", "false"],
        default="true",
        help="Run emulator in headless mode (default: true)"
    )
    args = parser.parse_args()
    headless = args.headless == "true"

    config = load_config()
    platform = config.get("platform")
    device_name = config.get("device_name")
    app_path = config.get("app_path")
    install_app = config.get("install_app", True)
    app_id = config.get("app_id")
    inputs = config.get("inputs", {})
    flow_steps = config.get("flow", [])

    # Validate essentials
    if not all([platform, device_name, app_path, flow_steps]):
        raise ValueError("Config must include platform, device_name, app_path, and flow steps.")

    # 1. Launch Emulator
    launcher = EmulatorLauncher()
    launcher.launch(platform=platform, device_name=device_name, headless=headless)

    # 2. Install the target app
    if install_app:
        if not app_path:
            raise ValueError("Config must include 'app_path' when install_app is true.")
        installer = AppInstaller()
        installer.target_app_install(platform=platform, device_name=device_name, app_path=app_path)

    print(f"[INFO] Loaded {len(flow_steps)} flow steps; starting Appium automation...")

    # 3. Run the target app
    runner = AppRunner()
    runner.run_app(platform=platform, app_path=app_path, app_id=app_id)

    # 4. Configure Appium desired capabilities
    caps = {
        'platformName': platform.capitalize(),
        'deviceName': device_name,
        # for IOS
        'automationName': 'XCUITest' if platform.lower() == 'ios' else 'UiAutomator2',
        'app': app_path,
        # for Android:
        **({'appPackage': app_id} if platform.lower() == 'android' else {}),
        **({'appActivity': config.get('app_activity')} if config.get('app_activity') else {}),
        'newCommandTimeout': 300
    }

    # 5. Run the flow via Appium
    appium_url = "http://localhost:4723/wd/hub"
    executor = AppiumRunner(appium_url, caps)
    try:
        executor.start()
        executor.run_steps(flow_steps, inputs)
    finally:
        executor.stop()

if __name__ == "__main__":
    main()