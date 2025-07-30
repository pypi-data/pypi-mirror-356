import os
import yaml

def load_config() -> dict:
    """Loads the first YAML config file in the current directory that ends with 'atdm_flow.yaml'.

    Returns:
        dict: Parsed YAML configuration.

    Raises:
        FileNotFoundError: If no matching config file is found.
    """
    for file in os.listdir(os.getcwd()):
        if file.endswith("atdm_flow.yaml"):
            with open(file, "r") as f:
                config = yaml.safe_load(f)
                return config

    raise FileNotFoundError(
        "No config file found ending with 'atdm_flow.yaml' in the project root."
    )

def get_flow_steps(config: dict) -> list:
    """Extracts the flow steps from the loaded config.

    Args:
        config (dict): The full configuration dictionary.

    Returns:
        list: A list of flow step dictionaries.
    """
    return config.get("flow", [])
