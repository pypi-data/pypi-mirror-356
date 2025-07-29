import importlib.metadata

import typer

from sshsync.client import SSHClient
from sshsync.config import Config, ConfigError
from sshsync.schemas import FileTransferAction
from sshsync.utils import (
    add_auth,
    add_host,
    add_hosts_to_group,
    assign_groups_to_hosts,
    check_path_exists,
    is_valid_regex,
    list_configuration,
    print_dry_run_results,
    print_error,
    print_message,
    print_ssh_results,
)

app = typer.Typer(
    name="sshsync",
    help="A fast, minimal SSH tool for running commands and syncing files across multiple servers.",
)


@app.command(help="Run a shell command on all configured hosts concurrently.")
def all(
    cmd: str = typer.Argument(..., help="The shell command to execute on all hosts."),
    timeout: int = typer.Option(
        10, help="Timeout in seconds for SSH command execution."
    ),
    dry_run: bool = typer.Option(
        False, help="Show command and host info without executing."
    ),
):
    """
    Run a shell command on all configured hosts concurrently.

    Args:
        cmd (str): The shell command to execute remotely.
        timeout (int): Timeout (in seconds) for SSH command execution.
        dry_run (bool): Show command and host info without executing.
    """

    try:
        config = Config()

        if not config.hosts:
            print_error("No hosts", True)

        ssh_client = SSHClient()
        if dry_run:
            dry_run_results = ssh_client.begin_dry_run_exec(
                cmd, config.configured_hosts(), "exec"
            )
            print_dry_run_results(dry_run_results)
        else:
            results = ssh_client.begin(cmd, config.configured_hosts(), timeout)
            print_ssh_results(results)
    except ConfigError as e:
        print_error(e, True)


@app.command(
    help="Run a shell command on all hosts within the specified group concurrently."
)
def group(
    name: str = typer.Argument(..., help="Name of the host group to target."),
    cmd: str = typer.Argument(..., help="The shell command to execute on the group."),
    regex: str = typer.Option(
        "", help="Filter group members by matching alias with a regex pattern."
    ),
    timeout: int = typer.Option(
        10, help="Timeout in seconds for SSH command execution."
    ),
    dry_run: bool = typer.Option(
        False, help="Show command and host info without executing."
    ),
):
    """
    Run a shell command on all hosts within the specified group concurrently.

    Args:
        name (str): The name of the host group to target.
        cmd (str): The shell command to execute remotely.
        regex (str): Filter group members by matching alias with regex pattern.
        timeout (int): Timeout (in seconds) for both SSH connection and command execution.
        dry_run (bool): Show command and host info without executing.
    """
    try:
        if regex and not is_valid_regex(regex):
            print_error("Invalid regex", True)

        config = Config()
        hosts = config.get_hosts_by_group(name, regex)

        if not hosts:
            print_error("Invalid group", True)

        ssh_client = SSHClient()
        if dry_run:
            dry_run_results = ssh_client.begin_dry_run_exec(cmd, hosts, "exec")
            print_dry_run_results(dry_run_results)
        else:
            results = ssh_client.begin(cmd, hosts, timeout)
            print_ssh_results(results)
    except ConfigError as e:
        print_error(e, True)


@app.command(help="Add hosts to a specified group.")
def gadd(group: str):
    """
    Add one or more hosts to the specified group.

    Args:
        group (str): The group to add hosts to.
    """
    try:
        config = Config()

        hosts = add_hosts_to_group(group)

        if not hosts:
            return print_error("No hosts provided")

        config.add_hosts_to_group(group, hosts)
        print_message(f"Hosts added to group {group}")
    except ConfigError as e:
        print_error(e, True)


@app.command(help="Add a host to your SSH config.")
def hadd():
    """
    Add a single host entry to your ~/.ssh/config file.
    """
    try:
        config = Config()

        config.add_new_host(add_host())
        print_message("Host added")
    except ConfigError as e:
        print_error(e, True)


@app.command(
    help="Prompt for group assignments for all ungrouped hosts and update the config."
)
def sync():
    """
    Prompt for group assignments for all ungrouped hosts and update the config.
    """
    try:
        config = Config()

        hosts = config.get_ungrouped_hosts()
        if not hosts:
            return print_message("All hosts are already assigned to groups")

        host_group_mapping = assign_groups_to_hosts(hosts)

        config.assign_groups_to_hosts(host_group_mapping)
        print_message("All ungrouped hosts have been assigned to the specified groups")
    except ConfigError as e:
        print_error(e, True)


@app.command(help="Set authentication method for one or more unconfigured hosts.")
def set_auth():
    """
    Set authentication method for one or more unconfigured hosts.
    """
    try:
        config = Config()
        hosts = config.get_unconfigured_hosts()
        host_auth = add_auth(hosts)
        config.save_host_auth(host_auth)
        print_message("Authentication methods for hosts have been saved to config")
    except Exception as e:
        print_error(e, True)


@app.command(help="Push a file to remote hosts using SCP.")
def push(
    local_path: str = typer.Argument(
        ..., help="The local path to the file or directory to be pushed."
    ),
    remote_path: str = typer.Argument(
        ..., help="The remote destination path where the file/directory will be placed."
    ),
    all: bool = typer.Option(False, help="Push to all configured hosts."),
    group: str = typer.Option("", help="Push to a specific group of hosts."),
    regex: str = typer.Option(
        "", help="Filter group members by matching alias with a regex pattern."
    ),
    host: str = typer.Option("", help="Push to a single specific host."),
    recurse: bool = typer.Option(
        False, help="Recursively push a directory and its contents."
    ),
    dry_run: bool = typer.Option(
        False, help="Show transfer and host info without executing."
    ),
):
    """
    Push a local file to remote destination over SSH.

    You must specify exactly one of the following options to determine where to push:
    --all (to all hosts), --group (to a group), or --host (to a specific host).

    Args:
        local_path (str): The local file or directory to push.
        remote_path (str): The destination path on the remote host(s).
        all (bool): Push to all hosts.
        group (str): Push to a specified group of hosts.
        regex (str): Filter group members by matching alias with regex pattern.
        host (str): Push to a specified individual host.
        recurse (bool): If True, recursively push a directory and all its contents.
        dry_run (bool): Show transfer and host info without executing.
    """
    has_all = all
    has_group = bool(group != "")
    has_host = bool(host != "")
    has_regex = bool(regex != "")

    if has_regex and not is_valid_regex(regex):
        print_error("Invalid regex", True)

    options = [has_all, has_group, has_host]

    if sum(options) != 1:
        print_error(
            "You must specify exactly one of --all, --group, or --host.",
            True,
        )

    if has_regex and not has_group:
        print_error(
            "--regex can only be used with --group.",
            True,
        )

    if not check_path_exists(local_path):
        print_error(f"Path ({local_path}) does not exist", True)

    try:
        config = Config()
        ssh_client = SSHClient()

        host_obj = config.get_host_by_name(host)
        hosts = (
            config.configured_hosts()
            if all
            else (
                config.get_hosts_by_group(group, regex)
                if group
                else [host_obj]
                if host_obj is not None
                else []
            )
        )

        if not hosts:
            return print_error("Invalid host or group")

        if dry_run:
            results = ssh_client.begin_dry_run_transfer(
                hosts, local_path, remote_path, "push"
            )
            print_dry_run_results(results)
        else:
            results = ssh_client.begin_transfer(
                local_path, remote_path, hosts, FileTransferAction.PUSH, recurse
            )

            print_ssh_results(results)
    except ConfigError as e:
        print_error(e, True)


@app.command(help="Pull a file from remote hosts using SCP.")
def pull(
    remote_path: str = typer.Argument(
        ..., help="The remote path to the file or directory to be pushed."
    ),
    local_path: str = typer.Argument(
        ..., help="The local destination path where the file/directory will be placed."
    ),
    all: bool = typer.Option(False, "--all", help="Pull from all configured hosts."),
    group: str = typer.Option("", help="Pull from a specific group of hosts."),
    regex: str = typer.Option(
        "", help="Filter group members by matching alias with a regex pattern."
    ),
    host: str = typer.Option("", help="Pull from a single specific host."),
    recurse: bool = typer.Option(
        False, help="Recursively pull a directory and its contents."
    ),
    dry_run: bool = typer.Option(
        False, help="Show transfer and host info without executing."
    ),
):
    """
    Pull a remote file to local destination over SSH.

    You must specify exactly one of the following options to determine where to pull from:
    --all (to all hosts), --group (to a group), or --host (to a specific host).

    Args:
        remote_path (str): The remote file path.
        local_path (str): The local file path.
        all (bool): Pull from all hosts.
        group (str): Pull from a specified group of hosts.
        regex (str): Filter group members by matching alias with regex pattern.
        host (str): Pull from a specified individual host.
        recurse (bool): If True, recursively pull directories and all their contents.
        dry_run (bool): Show transfer and host info without executing.
    """
    has_all = all
    has_group = bool(group != "")
    has_host = bool(host != "")
    has_regex = bool(regex != "")

    if has_regex and not is_valid_regex(regex):
        print_error("Invalid regex", True)

    options = [has_all, has_group, has_host]

    if sum(options) != 1:
        print_error(
            "You must specify exactly one of --all, --group, or --host.",
            True,
        )

    if has_regex and not has_group:
        print_error(
            "--regex can only be used with --group.",
            True,
        )

    if not check_path_exists(local_path):
        print_error(f"Path ({local_path}) does not exist", True)

    try:
        config = Config()
        ssh_client = SSHClient()

        host_obj = config.get_host_by_name(host)
        hosts = (
            config.configured_hosts()
            if all
            else (
                config.get_hosts_by_group(group, regex)
                if group
                else [host_obj]
                if host_obj is not None
                else []
            )
        )

        if not hosts:
            return print_error("Invalid host or group")

        if dry_run:
            results = ssh_client.begin_dry_run_transfer(
                hosts, local_path, remote_path, "pull"
            )
            print_dry_run_results(results)
        else:
            results = ssh_client.begin_transfer(
                local_path,
                remote_path,
                hosts,
                FileTransferAction.PULL,
                recurse,
            )

            print_ssh_results(results)
    except ConfigError as e:
        print_error(e, True)


@app.command(help="List all configured host groups and hosts.")
def ls(
    with_status: bool = typer.Option(
        False, "--with-status", help="Show whether a host is reachable"
    ),
):
    """
    List all configured host groups and hosts.

    Args:
        with_status (bool): Whether to include network reachability status for each host.
    """
    try:
        list_configuration(with_status)
    except ConfigError as e:
        print_error(e, True)


@app.command(help="Display the current version of sshsync.")
def version():
    """
    Display the current version.
    """
    typer.echo(importlib.metadata.version("sshsync"))
