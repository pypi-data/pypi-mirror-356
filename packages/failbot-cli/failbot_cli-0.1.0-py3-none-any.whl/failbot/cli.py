import typer
from typing import Optional
from failbot.auth import login as auth_login, get_token
from failbot.config import init_config
from failbot.send import send_log
from failbot.stream import stream_logs

app = typer.Typer()

@app.command()
def login():
    """Authenticate user with Failbot token"""
    auth_login()

@app.command()
def init():
    """Initialize project configuration"""
    init_config()

@app.command()
def upload(
    robot: str = typer.Option(..., "--robot", "-r", help="Robot identifier"),
    logs: str = typer.Option(..., "--logs", "-l", help="Path to log file(s)"),
    sensor_log: bool = typer.Option(False, "--sensor-log", help="Include sensor data logs")
):
    """Upload log files to Failbot"""
    send_log(logs, robot, sensor_log)

@app.command()
def stream(
    robot: str = typer.Option(..., "--robot", "-r", help="Robot identifier"),
    port: str = typer.Option(..., "--port", "-p", help="Serial port (e.g., /dev/ttyUSB0)"),
    sensor_log: bool = typer.Option(False, "--sensor-log", help="Include sensor data logs"),
    baudrate: int = typer.Option(115200, "--baudrate", "-b", help="Serial baudrate")
):
    """Stream real-time logs from serial port"""
    stream_logs(robot, port, baudrate, sensor_log)

# Legacy command for backward compatibility
@app.command()
def send(filepath: str):
    """Send log file to Failbot backend (legacy command)"""
    send_log(filepath) 