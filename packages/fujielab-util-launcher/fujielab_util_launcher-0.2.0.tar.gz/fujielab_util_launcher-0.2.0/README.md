# fujielab-util-launcher

Multiple Program Launcher Utility

[日本語のREADME](README.ja.md)

## Usage

### How to Run

```
fujielab-launcher [options]
```

#### Options

- `-d`, `--debug`: Enable debug mode. Detailed log messages will be displayed.
- `-r`, `--reset-config`: Initialize the launcher to start with no saved settings from the previous session.
- `-c`, `--config`: Start with settings imported from a previously exported configuration file.
- `--version`: Display version information and exit.
- `--lang`: Select UI language (`en` or `ja`). If omitted, the system locale is
  used.
- `--create-shortcut`: (Windows only) Create a shortcut on the Desktop for easy access.
- `-h`, `--help`: Display help message and exit.

### Debug Mode

In debug mode, detailed information about the application's operation is displayed.
Detailed logs are output for operations such as saving and loading configuration files,
changing window states, starting and stopping processes, etc.

This is useful for development and troubleshooting. It is not necessary for normal use.

```bash
# Start in debug mode
fujielab-launcher -d
```

### Using Custom Configuration File

You can start with previously exported settings by using the `-c` or `--config` option.

```bash
fujielab-launcher --config /path/to/your/custom_config.yaml
```

This is useful for switching between different configuration profiles or importing settings from another system.

### Windows-Specific Features

#### Creating Desktop Shortcut

On Windows systems, you can create a Desktop shortcut for easy access:

```cmd
fujielab-launcher --create-shortcut
```

This will create a shortcut on your Desktop that launches the program directly. This option requires the `pywin32` package to be installed:

```cmd
pip install pywin32
```

## Features

- Multiple program launcher with configurable settings
- Support for Python scripts and shell commands
- Ability to pass command line arguments to Python scripts
- Customizable workspace directory settings
- Cross-platform support (Windows, macOS, Linux)

## Installation

### From PyPI

```bash
pip install fujielab-util-launcher
```

### From Source

```bash
git clone https://github.com/fujielab/fujielab-util-launcher.git
cd fujielab-util-launcher
pip install -e .
```

## License

Apache License 2.0
