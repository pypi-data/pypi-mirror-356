import serial
import json
import time
import requests
from datetime import datetime
from failbot.auth import get_token
from rich import print
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

API_URL = "https://your-backend.fly.dev/api/logs"  # update this!

def stream_logs(robot_id: str, port: str, baudrate: int = 115200, sensor_log: bool = False):
    """Stream real-time logs from serial port"""
    token = get_token()
    if not token:
        print("[red]❌ You must run `failbot-cli login` first[/]")
        return

    console = Console()
    
    try:
        # Open serial connection
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"[green]✔ Connected to {port} at {baudrate} baud[/]")
        print(f"[blue]📡 Streaming logs for robot: {robot_id}[/]")
        print("[yellow]Press Ctrl+C to stop streaming[/]")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Create a buffer for batching logs
        log_buffer = []
        last_send_time = time.time()
        batch_interval = 5  # Send batch every 5 seconds

        def send_batch():
            if log_buffer:
                try:
                    payload = {
                        "robot_id": robot_id,
                        "logs": log_buffer,
                        "sensor_log": sensor_log,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    r = requests.post(API_URL, json=payload, headers=headers)
                    if r.status_code == 200:
                        print(f"[green]✔ Sent {len(log_buffer)} log entries[/]")
                    else:
                        print(f"[red]❌ Failed to send batch: {r.status_code}[/]")
                        
                except Exception as e:
                    print(f"[red]❌ Error sending batch: {e}[/]")
                
                log_buffer.clear()

        try:
            while True:
                if ser.in_waiting:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        timestamp = datetime.utcnow().isoformat()
                        log_entry = {
                            "timestamp": timestamp,
                            "content": line,
                            "type": "sensor" if sensor_log and line.startswith('{') else "log"
                        }
                        
                        log_buffer.append(log_entry)
                        
                        # Display the log line
                        if log_entry["type"] == "sensor":
                            console.print(f"[cyan]{timestamp}[/] [green]SENSOR[/] {line}")
                        else:
                            console.print(f"[cyan]{timestamp}[/] {line}")
                        
                        # Send batch if enough time has passed
                        if time.time() - last_send_time >= batch_interval:
                            send_batch()
                            last_send_time = time.time()
                
                time.sleep(0.1)  # Small delay to prevent CPU spinning
                
        except KeyboardInterrupt:
            print("\n[yellow]Stopping stream...[/]")
            send_batch()  # Send any remaining logs
            print("[green]✔ Stream stopped[/]")
            
    except serial.SerialException as e:
        print(f"[red]❌ Serial port error: {e}[/]")
        print(f"[yellow]Make sure {port} is available and you have permission to access it[/]")
    except Exception as e:
        print(f"[red]❌ Unexpected error: {e}[/]")
    finally:
        if 'ser' in locals():
            ser.close() 