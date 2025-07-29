import asyncio
import ipaddress
import re
import socket
from pathlib import Path
from typing import Literal

import asyncssh
import keyring
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from sshsync.config import Config
from sshsync.schemas import Host, HostAuth, SSHDryRun, SSHResult

console = Console()


def check_path_exists(path: str) -> bool:
    """Check if the given path exists"""
    return Path(path).expanduser().exists()


async def is_host_reachable(host: str, port: int = 80, timeout: int = 2) -> bool:
    """
    Check if a host is reachable by attempting to establish a TCP connection.

    Args:
        host (str): The hostname or IP address to check.
        port (int, optional): The port to attempt to connect to. Defaults to 80.
        timeout (int, optional): Timeout in seconds for the connection attempt. Defaults to 2.

    Returns:
        bool: True if the host is reachable on the specified port, False otherwise.
    """
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except (socket.timeout, socket.error):
        return False


def add_hosts_to_group(group: str) -> list[str]:
    """Prompt for host aliases and return them as a list of non-empty strings"""
    host_input = Prompt.ask(
        f"Enter host aliases to add to group '{group}' (space-separated)"
    )
    return [host.strip() for host in host_input.split() if host.strip()]


def assign_groups_to_hosts(hosts: list[str]) -> dict[str, list[str]]:
    """Prompt the user to assign one or more groups to each host alias and return a mapping"""
    print(
        "Enter group(s) to add to each of the following host aliases (space-separated)"
    )
    host_group_mapping = dict()

    for host in hosts:
        input = Prompt.ask(host)
        groups = [group.strip() for group in input.split() if group.strip()]
        host_group_mapping[host] = groups

    return host_group_mapping


def is_key_private(key_path: str) -> bool:
    """Check if the given ssh key is protected by a passphrase

    Returns:
        bool: True if the ssh key is encrypted, False otherwise
    """
    # Check if key_path is empty or points to a directory
    path = Path(key_path).expanduser()
    if not key_path or not path.exists() or path.is_dir():
        return False  # Cannot be encrypted if it's not a valid file
    try:
        asyncssh.read_private_key(key_path, passphrase=None)
        return False
    except asyncssh.KeyEncryptionError:
        return True
    except ValueError:
        return True
    except Exception:
        return True


def check_key_passphrase(key_path: str, passphrase: str) -> bool:
    """Check if the given passphrase unlocks the SSH key."""
    path = Path(key_path).expanduser()
    if not key_path or not path.exists() or path.is_dir():
        return False
    try:
        asyncssh.read_private_key(key_path, passphrase)
        return True
    except Exception:
        return False


def get_pass(
    host: str, pass_type: Literal["passphrase", "password"], key_path: str = ""
) -> str:
    """Prompt the user for a password or passphrase, validating if needed."""
    while True:
        val = Prompt.ask(f"Please enter {pass_type} for host `{host}`", password=True)
        if not val.strip():
            continue
        if pass_type == "passphrase" and not check_key_passphrase(
            key_path, passphrase=val
        ):
            print("Incorrect passphrase!!!")
            continue
        return val


def set_keyring(host: str, password: str):
    """Store a password in the keyring for a host."""
    keyring.set_password("sshsync", host, password)


def add_auth(hosts: list[dict[str, str]]) -> dict[str, HostAuth]:
    backend = str(keyring.get_keyring())

    if "Plaintext" in backend or "fail" in backend:
        raise Exception(
            "No secure keyring backend found. Please install or configure your system keyring."
        )

    print("Enter password/passphrase for each of the following hosts")

    host_auth: dict[str, HostAuth] = dict()

    for host in hosts:
        alias = host.get("alias", "")
        identity_file = host.get("identity_file")
        if identity_file:
            if is_key_private(identity_file):
                passphrase = get_pass(alias, "passphrase", identity_file)
                set_keyring(alias, passphrase)
                host_auth[alias] = HostAuth("key", True)
            else:
                host_auth[alias] = HostAuth("key", False)
        else:
            auth_method = Prompt.ask(
                f"What auth method does host `{alias}` use", choices=["key", "password"]
            )
            if auth_method == "password":
                password = get_pass(alias, "password")
                set_keyring(alias, password)
                host_auth[alias] = HostAuth("password", None)
            else:
                host_auth[alias] = HostAuth("key", None)

    return host_auth


def is_valid_ip(ip: str) -> bool:
    """Check if the string is a valid ip address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_regex(pattern: str) -> bool:
    "Check if the string is a valid regex pattern"
    try:
        re.compile(pattern)
        return True
    except Exception:
        return False


def get_host_name_or_ip() -> str:
    """Prompt the user to enter a valid hostname or ip address"""
    while True:
        host_input = Prompt.ask("Enter the host name or IP address")

        if is_valid_ip(host_input):
            return host_input

        try:
            socket.gethostbyname(host_input)
            return host_input
        except socket.gaierror:
            console.print(
                f"[bold red]Error:[/bold red] Invalid host name or IP address: [bold]{host_input}[/bold]. Please try again."
            )


def check_file_exists(file_path: str) -> bool:
    """Check if the given path exists and is a valid file"""
    path = Path(file_path).expanduser()
    return path.exists() and path.is_file()


def get_valid_file_path() -> str:
    """Prompt the user to enter a valid file path"""
    while True:
        file_path = Prompt.ask("Enter path to ssh key for this host")
        if check_file_exists(file_path):
            return file_path
        console.log(
            f"[bold red]Error:[/bold red] The file at [bold]{file_path}[/bold] does not exist. Please try again."
        )


def get_valid_username() -> str:
    """Prompt the user to enter a valid username"""
    while True:
        username = Prompt.ask("Enter the SSH username for this server").strip()
        if username:
            break
        console.print(
            "[bold red]Error:[/bold red] Username cannot be empty. Please try again."
        )
    return username


def get_valid_port_number() -> int:
    """Prompt the user to enter a valid port number"""
    while True:
        port_input = Prompt.ask(
            "Enter the port on which the SSH server is running", default="22"
        )
        if port_input.isdigit():
            port = int(port_input)
            if 1 <= port <= 65535:
                return port
        console.print(
            "[bold red]Error:[/bold red] Please enter a valid port number (1–65535)."
        )


def add_group(
    prompt_text: str = "Enter the name(s) of the new group(s) (comma-separated)",
) -> list[str]:
    """Prompt the user for new groups and return a list[str]"""
    group_input = Prompt.ask(prompt_text)
    groups = [group.strip() for group in group_input.split(",")]
    return groups


def add_host() -> Host:
    """Prompt the user for host information and return a Host instance"""
    alias = Prompt.ask("Enter the alias for this host")
    name = get_host_name_or_ip()
    ssh_key_path = get_valid_file_path()
    username = get_valid_username()
    port = get_valid_port_number()
    groups = add_group(
        "Enter the name(s) of the group(s) this host can belong to (comma-separated)"
    )
    return Host(
        alias=alias,
        address=name,
        identity_file=ssh_key_path,
        username=username,
        port=port,
        groups=groups,
    )


def list_configuration(with_status: bool) -> None:
    """
    Display the current SSH configuration including hosts and groups in rich-formatted tables.

    This function retrieves the loaded YAML configuration using the `Config` class,
    and displays:
      - A list of all defined group names.
      - A list of all configured hosts with details like address, username, port, SSH key path,
        group memberships and optionally host reachability.

    Uses the `rich` library to print visually styled tables to the console.

    Returns:
        None: This function prints the results to the console and does not return a value.
    """
    config = Config()

    hosts = config.configured_hosts()

    if hosts:
        host_table = Table(title="Configured Hosts")
        host_table.add_column("Alias", style="purple", no_wrap=True)
        host_table.add_column("Host", style="cyan")
        host_table.add_column("Username", style="green")
        host_table.add_column("Port", style="blue")
        host_table.add_column("SSH Key", style="magenta")
        host_table.add_column("Groups", style="white")
        if with_status:
            host_table.add_column("Status")

        for host in hosts:
            row = [
                host.alias,
                host.address,
                host.username,
                str(host.port),
                host.identity_file,
                ", ".join(host.groups) if host.groups else "-",
            ]
            if with_status:
                row.append(
                    "[bold green]Up[/bold green]"
                    if asyncio.run(is_host_reachable(host.address, host.port))
                    else "[bold red]Down[/bold red]"
                )
            host_table.add_row(*row)

        console.print(host_table)
    else:
        console.print("[bold yellow]No hosts configured.[/bold yellow]")


def print_ssh_results(results: list[SSHResult]) -> None:
    """
    Display SSH command execution results in a formatted table.

    Args:
        results (list[SSHResult | BaseException]): A list containing the results of SSH command
        executions, which may include `SSHResult` objects or exceptions from failed tasks.

    Returns:
        None: This function prints the results to the console and does not return a value.
    """

    table = Table(title="SSHSYNC Results")
    table.add_column("Host", style="cyan", no_wrap=True)
    table.add_column("Status", style="green")
    table.add_column("Exit Code", style="red")
    table.add_column("Output", style="magenta")

    for result in results:
        if result is not None and not isinstance(result, BaseException):
            status = "[green]Success[/green]" if result.success else "[red]Failed[/red]"
            output = f"{result.output.strip()}\n" if result.output else "-"
            exit_status = result.exit_status if result.exit_status else "0"
            table.add_row(result.host, status, str(exit_status), str(output))

    console.print(table)


def print_dry_run_results(tasks: list[SSHDryRun]) -> None:
    """
    Display a dry-run summary for each SSH operation using rich panels.

    Args:
        dry_run_items (list[SSHDryRun]): Simulated SSH operations to preview.
    """
    for task in tasks:
        lines = []

        lines.append(f"[bold]Alias:[/bold] {task.alias}")
        lines.append(f"[bold]User:[/bold] {task.username}")
        lines.append(f"[bold]Operation:[/bold] {task.operation.upper()}")

        if task.operation == "exec" and task.command:
            lines.append(f"[bold]Command:[/bold] {task.command}")

        elif task.operation in ("push", "pull"):
            if task.operation == "pull":
                lines.append(
                    f"[bold]Transfer:[/bold] {task.local_path} <- {task.remote_path}"
                )
            if task.operation == "push":
                lines.append(
                    f"[bold]Transfer:[/bold] {task.local_path} -> {task.remote_path}"
                )

        lines.append(
            f"[bold]Host Reachable:[/bold] {'Yes' if asyncio.run(is_host_reachable(task.host, task.port)) else 'No'}"
        )

        body = "\n".join(lines)
        panel = Panel(
            body,
            title=f"[cyan]{task.host}:{task.port}[/cyan]",
            border_style="white",
            title_align="left",
        )
        console.print(panel)


def print_error(message: str | Exception, exit: bool = False) -> None:
    """
    Display an error message in a styled panel and optionally exit the program.

    Args:
        message (str): The error message to display.
        exit (bool, optional): If True, exits the program with status code 1. Defaults to False.

    Raises:
        typer.Exit: If exit is True, the function raises a typer.Exit with code 1.
    """
    console.print(
        Panel(
            str(message),
            title="Error",
            title_align="left",
            border_style="red",
        ),
        style="bold white",
    )
    if exit:
        raise typer.Exit(1)


def print_message(message: str) -> None:
    """Display an error message in a styled panel"""
    console.print(
        Panel(message, title="Message", title_align="left", border_style="blue"),
        style="bold white",
    )
