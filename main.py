"""finds open ports on your system
- scan for open ports
- check if a given port is open
- get details of the process using the port"""

from psutil import net_connections, Process
from argparse import ArgumentParser
from argparse import Namespace as ArgNamespace
from typing import NamedTuple
import pandas
from sys import argv

# using a named tuple hels with type annotations and formatting for the user
process_data = NamedTuple(
    "process_data", [
        ("ip", str),
        ("port", int),
        ("pid", int),
        ("proc_name", str)
    ]
)


def define_and_read_args(arguments: list[str]) -> ArgNamespace:
    """configure parsers
    - define the main parser for the application executable
    - define subparsers (one for each functionality)
    - parse the arguments"""

    main_parser = ArgumentParser(
        prog="opf",
        description="Finds open ports on your system"
    )
    functions = main_parser.add_subparsers(required=True)

    scan = functions.add_parser(
        "scan",
        description="Scans for open ports"
    )
    scan.add_argument(
        "-i",
        "--ip",
        type=str,
        help="IP address to scan",
        required=False
    )
    scan.add_argument(
        "-c",
        "--checkprocess",
        action="store_true",
        help="Check details of the process using the port",
        required=False
    )
    scan.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Output the data in JSON format",
        required=False
    )
    scan.set_defaults(func=scan_ports)

    check = functions.add_parser(
        "checkport",
        description="Checks if the given port is open. Returns a 1 if it is open, 0 if it is closed."
    )
    check.add_argument(
        "-i",
        "--ip",
        type=str,
        help="IP address to check",
        required=True
    )
    check.add_argument(
        "-p",
        "--port",
        type=int,
        help="Port to check",
        required=True
    )
    check.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print details of the process using the port",
    )
    check.add_argument(
        "-k",
        "--kill",
        action="store_true",
        help="Attempt to kill the process using the port. WARNING: This will kill the process without any confirmation.",
    )
    check.set_defaults(func=check_port)

    return main_parser.parse_args(arguments)


def scan_ports(args: ArgNamespace) -> None:
    """scan for open ports
    - filter by IP address, if specified
    - check the process using the port, if specified"""

    # we start with all the data and then filter down as we go
    open_ports = net_connections()

    # filter by IP address, if specified
    if args.ip:
        open_ports = filter(lambda x: x.laddr.ip == args.ip, open_ports)  # type: ignore

    # format to the named tuple
    # add on the process names, if specified
    if args.checkprocess:
        open_ports = tuple(process_data(
            port.laddr.ip,  # type: ignore
            port.laddr.port,  # type: ignore
            port.pid,  # type: ignore
            Process(port.pid).name()
        ) for port in open_ports)

    else:
        open_ports = tuple(process_data(
            port.laddr.ip,  # type: ignore
            port.laddr.port,  # type: ignore
            port.pid,  # type: ignore
            ""
        ) for port in open_ports)

    # pandas is being used just to format the data
    if any(open_ports):
        df = pandas.DataFrame(open_ports, columns=["IP", "Port", "PID", "Process Name"])

        # drop empty columns, if not checking the process names
        if not args.checkprocess:
            df = df.drop(columns=["PID", "Process Name"])

        # print the data in the specified format
        if args.json:
            print(df.to_json(orient="records", indent=4))

        else:
            print(df.to_string(index=False))
            print(f"Total open ports: {len(open_ports)}")


    else:
        print("No open ports found")


def check_port(args: ArgNamespace) -> None:
    """check if a given port is open
    - check if the port is open
    - get details of the process using the port"""

    open_ports = net_connections()
    open_port = next(filter(lambda x: x.laddr.ip == args.ip and x.laddr.port == args.port, open_ports), None)  # type: ignore

    if not args.verbose:
        print(1 if open_port else 0)
        return

    # print the details of the process using the port only if asked for it
    if open_port:
        print("Port is open")
        print(process_data(
            open_port.laddr.ip,  # type: ignore
            open_port.laddr.port,  # type: ignore
            open_port.pid,  # type: ignore
            Process(open_port.pid).name()
        ))

    else:
        print("Port is closed")

    # attempt to kill the process using the port, if asked for it
    if args.kill and open_port:
        try:
            Process(open_port.pid).kill()

        except PermissionError:
            print("You do not have permission to kill this process")


def main(arguments: list[str]) -> None:
    """main function
    - run the application"""

    args = define_and_read_args(arguments)
    args.func(args)


if __name__ == "__main__":
    main(argv[1:])
