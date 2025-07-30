# failbot-cli

A Python CLI tool for uploading robot logs to the Failbot backend. Supports both file uploads and real-time streaming from serial ports.

## Installation

```bash
pip install failbot-cli
```

Or install from source:
```bash
git clone <repository-url>
cd failbot-cli
pip install -e .
```

## Quick Start

1. **Login with your token:**
   ```bash
   failbot-cli login
   ```

2. **Upload log files:**
   ```bash
   failbot-cli upload --robot atlas-01 --logs /var/log/robot.log
   ```

3. **Stream real-time logs:**
   ```bash
   failbot-cli stream --robot atlas-01 --port /dev/ttyUSB0
   ```

## Commands

### `failbot-cli login`
Authenticate with your Failbot token. The token is saved locally for future use.

### `failbot-cli upload`
Upload log files to Failbot.

**Options:**
- `--robot, -r`: Robot identifier (required)
- `--logs, -l`: Path to log file(s) or directory (required)
- `--sensor-log`: Include sensor data logs

**Examples:**
```bash
# Upload a single file
failbot-cli upload --robot atlas-01 --logs /var/log/robot.log

# Upload all log files in a directory
failbot-cli upload --robot atlas-01 --logs /var/logs/

# Upload with sensor data
failbot-cli upload --robot atlas-01 --logs /var/log/robot.log --sensor-log
```

### `failbot-cli stream`
Stream real-time logs from a serial port.

**Options:**
- `--robot, -r`: Robot identifier (required)
- `--port, -p`: Serial port (e.g., /dev/ttyUSB0) (required)
- `--baudrate, -b`: Serial baudrate (default: 115200)
- `--sensor-log`: Include sensor data logs

**Examples:**
```bash
# Basic streaming
failbot-cli stream --robot atlas-01 --port /dev/ttyUSB0

# With custom baudrate
failbot-cli stream --robot atlas-01 --port /dev/ttyUSB0 --baudrate 9600

# Include sensor logs
failbot-cli stream --robot atlas-01 --port /dev/ttyUSB0 --sensor-log
```

### `failbot-cli init`
Initialize project configuration (legacy command).

## Supported File Types

- `.log` - Log files
- `.txt` - Text files
- `.json` - JSON data
- `.csv` - CSV data

## Sensor Log Format

For sensor data, use JSON format:
```json
{"sensor": "battery", "voltage": 4.2}
{"sensor": "temperature", "value": 25.5}
```

## Configuration

The CLI uses a simple token-based authentication system. Your token is stored in `~/.failbot_auth`.

## Troubleshooting

- **Serial port access denied**: Make sure you have permission to access the serial port
- **Upload failed**: Check your internet connection and token validity
- **No logs found**: Verify the file path and supported file extensions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 