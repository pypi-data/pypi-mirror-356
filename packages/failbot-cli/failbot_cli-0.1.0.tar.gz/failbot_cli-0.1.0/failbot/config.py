import json
from rich import print

def init_config():
    config = {
        "project": input("Project name: "),
        "device_id": input("Device ID: "),
        "log_type": "file"  # could support serial later
    }
    with open("failbot.config.json", "w") as f:
        json.dump(config, f, indent=2)
    print("[green]✔ Config created[/]") 