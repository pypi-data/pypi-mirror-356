import json
import requests
import os
from pathlib import Path
from failbot.auth import get_token
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

API_URL = "https://your-backend.fly.dev/api/logs"  # update this!

def send_log(filepath: str, robot_id: str = None, sensor_log: bool = False):
    token = get_token()
    if not token:
        print("[red]❌ You must run `failbot-cli login` first[/]")
        return

    # Use robot_id parameter or try to get from config
    if not robot_id:
        try:
            with open("failbot.config.json") as f:
                config = json.load(f)
                robot_id = config.get("device_id")
        except:
            print("[red]❌ Robot ID required. Use --robot flag or run `failbot-cli init`[/]")
            return

    # Handle multiple files or directories
    file_paths = []
    if os.path.isdir(filepath):
        for ext in ['.log', '.txt', '.json', '.csv']:
            file_paths.extend(Path(filepath).glob(f"*{ext}"))
    else:
        file_paths = [Path(filepath)]

    if not file_paths:
        print(f"[red]❌ No valid log files found at: {filepath}[/]")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Uploading logs...", total=len(file_paths))

        for file_path in file_paths:
            try:
                with open(file_path, "r") as f:
                    log_content = f.read()

                payload = {
                    "robot_id": robot_id,
                    "log": log_content,
                    "filename": file_path.name,
                    "sensor_log": sensor_log
                }

                r = requests.post(API_URL, json=payload, headers=headers)

                if r.status_code == 200:
                    print(f"[green]✔ Uploaded: {file_path.name}[/]")
                else:
                    print(f"[red]❌ Failed to upload {file_path.name}: {r.status_code} {r.text}[/]")

            except Exception as e:
                print(f"[red]❌ Could not read file {file_path}: {e}[/]")

            progress.advance(task)

    print("[green]✔ Upload complete![/]")
    print("🔗 View logs at: https://failbot.com/dashboard") 