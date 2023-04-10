from psutil import net_connections, Process
from argparse import ArgumentParser
from argparse import Namespace as ArgNamespace
from typing import NamedTuple
import pandas
from sys import argv

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
    scan.set_defaults(func=scan_ports)

    check = functions.add_parser(
        "check",
        description="Checks if the given port is open"
    )
    check.add_argument(
        "-i",
        "--ip",
        type=str,
        help="IP address to scan",
        required=True
    )
    check.add_argument(
        "-p",
        "--port",
        type=int,
        help="Port to check",
        required=True
    )
    check.set_defaults(func=check_port)

    return main_parser.parse_args(arguments)


def scan_ports(args: ArgNamespace) -> None:
    open_ports = net_connections()

    if args.ip:
        open_ports = filter(lambda x: x.laddr.ip == args.ip, open_ports)  # type: ignore

    if args.checkprocess:
        open_ports = map(lambda x: process_data(x.laddr.ip, x.laddr.port, x.pid, Process(x.pid).name()), open_ports)  # type: ignore

    else:
        open_ports = map(lambda x: process_data(
            x.laddr.ip, x.laddr.port, x.pid, ""), open_ports)  # type: ignore

    open_ports = tuple(open_ports)

    if any(open_ports):
        if args.checkprocess:
            print(pandas.DataFrame(open_ports).to_string())

        else:
            print(pandas.DataFrame(open_ports).drop(columns=["pid", "proc_name"]).to_string())

        print(f"Total open ports: {len(open_ports)}")

    else:
        print("No open ports found")


def check_port(args: ArgNamespace) -> None:
    open_ports = net_connections()
    open_port = next(filter(lambda x: x.laddr.ip == args.ip and x.laddr.port == args.port, open_ports), None)  # type: ignore

    if open_port:
        print(process_data(open_port.laddr.ip, open_port.laddr.port, open_port.pid, Process(open_port.pid).name()))


def main(arguments: list[str]) -> None:
    args = define_and_read_args(arguments)
    args.func(args)


if __name__ == "__main__":
    main(argv[1:])
