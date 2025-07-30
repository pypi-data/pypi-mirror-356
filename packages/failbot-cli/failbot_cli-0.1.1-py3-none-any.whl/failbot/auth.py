import os
from rich import print

AUTH_FILE = os.path.expanduser("~/.failbot_auth")

def login():
    print("[bold cyan]Login with your Failbot token:[/]")
    token = input("Token: ").strip()
    with open(AUTH_FILE, "w") as f:
        f.write(token)
    print("[green]✔ Token saved![/]")

def get_token():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE) as f:
            return f.read().strip()
    return None 