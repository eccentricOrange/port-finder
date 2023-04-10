from argparse import ArgumentParser
from argparse import Namespace as ArgNamespace
from logging import DEBUG, INFO, FileHandler, Formatter, Logger, getLogger
from colorama import Fore, Style


from psutil import net_connections


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
        required_ports = filter(lambda x: x.laddr.ip == args.ip, open_ports)

        print(*required_ports, sep="\n\n")


def check_port(args: ArgNamespace) -> None:
    pass


def main(arguments: list[str]) -> None:
    args = define_and_read_args(arguments)
    args.func(args)


if __name__ == "__main__":
    main(["scan", "-i", "127.0.0.1"])