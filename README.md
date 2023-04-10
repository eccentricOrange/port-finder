# port-finder
Finds open ports on your system.

## Overview
This is a simple utility that finds open ports on your system.  It is written in Python 3, and uses the `psutil` module to find processes that are listening on ports.

## Installation
You must have a recent Python 3 installation.  You can check your version with `python --version`.  If you don't have Python 3, you can download it from [its official website](https://www.python.org/downloads/).

1.  Clone the repository to your local machine, and change into the directory.
2.  (In a virtual environment, if you like) Install the dependencies.

    ```bash
    python -m pip install -r requirements.txt
    ```

3.  Run the program.

    ```bash
    python main.py
    ```

## Usage
*   This utility follows the [GNU Argument Syntax Conventions](https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html).  This means that you can use either single-dash or double-dash arguments, and you can use either a space or an equals sign to separate the argument from its value.
*   The program offers two main functions: finding open ports (filtered by IP address, if needed), and checking the status of a specific port.
*   You can also kill a process if you like.


### Finding Open Ports
To find open ports, use the `scan` command. Here are the arguments it takes:
```txt
usage: opf scan [-h] [-i IP] [-c] [-j]

Scans for open ports

options:
  -h, --help          show this help message and exit
  -i IP, --ip IP      IP address to scan
  -c, --checkprocess  Check details of the process using the port
  -j, --json          Output the data in JSON format
```

*   The `--ip` argument takes an IP address as a value.  If you don't specify an IP address, the program will scan all IP addresses on your system.
*   The `--checkprocess` argument takes no value.  If you specify it, the program will check the process that is using the port, and display its name and PID.
*   The `--json` argument takes no value.  If you specify it, the program will output the data in JSON format.

### Checking the Status of a Port
To check the status of a port, use the `checkport` command. Here are the arguments it takes:
```txt
usage: opf checkport [-h] -i IP -p PORT [-v]

Checks if the given port is open. Returns a 1 if it is open, 0 if it is closed.

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        IP address to check
  -p PORT, --port PORT  Port to check
  -v, --verbose         Print details of the process using the port
  -k, --kill            Attempt to kill the process using the port. WARNING: This will kill the process without any confirmation.
```

*   The `--ip` argument takes an IP address as a value. **This argument is required.**
*   The `--port` argument takes a port number as a value. **This argument is required.**
*   The `--verbose` argument takes no value.  If you specify it, the program will display the name and PID of the process that is using the port.
*   The `--kill` argument takes no value.  If you specify it, the program will attempt to kill the process that is using the port.  **This will kill the process without any confirmation.**