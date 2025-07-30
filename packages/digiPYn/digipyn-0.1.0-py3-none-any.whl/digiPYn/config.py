import os
import json
from pathlib import Path

#Define Config Dir and File nama
APP_NAME = "digipin_converter_package_with_geocoding"
CONFIG_DIR_NAME = f".{APP_NAME}"
CONFIG_FILE_NAME = "confiig.json"

def get_config_path():
    """
    Determines the appropriate config file path based on the OS
    Linux/MacOS -> XDG Base Directory Specification
    Windows -> APPDATA
    """

    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / APP_NAME / CONFIG_FILE_NAME
        else:
            return Path.home() / APP_NAME / CONFIG_FILE_NAME

    elif os.name == "posix":
        config_home = os.environ.get("XDG_CONFIG_HOME")
        if config_home:
            return Path(config_home) / APP_NAME / CONFIG_FILE_NAME
        else:
            return Path.home() / CONFIG_DIR_NAME / CONFIG_FILE_NAME
    else:
        return Path.home() / CONFIG_DIR_NAME / CONFIG_FILE_NAME

def load_api_key():
    """
    Loads the API key from configuration file
    returns none if not found
    """
    config_file = get_config_path()
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                return config.get("api_key")
        except json.JSONDecodeError:
            print("Error decoding config file. It might be corrupted.")
            return None
    return None

def save_api_key(key):
    """
    Saves the API key to configuration file
    """
    config_file = get_config_path()
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w") as f:
        json.dump({"api_key": key}, f)

def prompt_for_api_key():
    """
    Prompts the user for API key
    returns none if not found
    """
    print("\nGoogle API Key not found.")
    print("To use this package, you need a Google Geocoding API key.")
    print("You can get one here: https://console.cloud.google.com/apis/credentials")  # Updated link for clarity
    key = input("Please enter your Google API Key: ").strip()
    if key:
        save_api_key(key)
        return key
    else:
        print("No API key provided. Geocoding functionality will be disabled.")
        return None


_api_key = None

def get_api_key():
    """
    Retrieves the API key from configuration file
    prompts user for API key if not found
    main entry point for obtaining the key
    """
    global _api_key
    if _api_key is None:
        # Check environment variable first
        env_api_key = os.getenv("GOOGLE_API_KEY")
        if env_api_key:
            _api_key = env_api_key
            print("API key loaded from environment variable.")
        else:
            _api_key = load_api_key()
            if _api_key is None:
                _api_key = prompt_for_api_key()
    return _api_key

def delete_api_key():
    """
    Deletes the configuration file containing the API key
    """
    config_file = get_config_path()
    if config_file.exists():
        try:
            config_file.unlink()
            try:
                config_file.parent.rmdir()
            except OSError:
                pass
            global _api_key
            _api_key = None
            print("API key configuration file deleted.")
        except OSError as e:
            print(f"Error deleting config file: {e}")