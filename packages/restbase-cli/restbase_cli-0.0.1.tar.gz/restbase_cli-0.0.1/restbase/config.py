import yaml
import os
from restbase.config_generator import main as run_config_builder

CONFIG_FILE = "config.yaml"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print("'config.yaml' not found.")
        print(" Launching interactive config builder...\n")
        run_config_builder()

    else:
        choice = input(" Do you want to regenerate 'config.yaml'? (y/n): ").strip().lower()
        if choice == 'y':
            run_config_builder()

    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)

    required_api_keys = ["base_url", "endpoints"]
    required_pg_keys = ["host", "port", "dbname", "user", "password"]

    for key in required_api_keys:
        if key not in config.get("api", {}):
            raise ValueError(f"Missing API config key: {key}")
    for key in required_pg_keys:
        if key not in config.get("postgres", {}):
            raise ValueError(f"Missing PostgreSQL config key: {key}")

    return config