import json

class ConfigLoader:
    def __init__(self, config_path="config.json"):
        """
        Initialize the ConfigLoader with the path to the JSON configuration file.

        Args:
        - config_path (str, optional): Path to the JSON configuration file. Default is "config.json".
        """
        self.config_path = config_path
        self.config = None

    def load(self):
        """
        Load the configuration from the JSON file.

        Returns:
        - dict: Loaded configuration dictionary.

        Raises:
        - Exception: If there is an error loading the configuration file.
        """
        try:
            with open(self.config_path, 'r') as file:
                self.config = json.load(file)
            return self.config
        except Exception as e:
            raise Exception(f"Error loading configuration: {e}")
