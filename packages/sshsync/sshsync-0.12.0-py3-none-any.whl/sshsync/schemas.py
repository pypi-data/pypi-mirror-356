from dataclasses import asdict, dataclass
from enum import Enum
from typing import Literal

from asyncssh import BytesOrStr


class FileTransferAction(str, Enum):
    """
    Enum representing the types of transfer actions.

    Attributes:
        PUSH (TransferType): Indicates a push action or file action.
        PULL (TransferType): Indicates a pull action or file download action.
    """

    PUSH = "push"
    PULL = "pull"


@dataclass
class Host:
    """
    Represents a host configuration with connection and grouping details.

    Attributes:
        alias (str): The alias used instead of IP address of hostname of the host.
        address (str): The IP address or hostname of the host.
        identity_file (str): The file path to the SSH private key used for authentication.
        username (str): The username used to connect to the host.
        port (int): The SSH port used to connect to the host (typically 22).
        groups (list[str]): A list of group names that this host belongs to.
    """

    alias: str
    address: str
    identity_file: str
    username: str
    port: int
    groups: list[str]


@dataclass
class HostAuth:
    """
    Authentication method and passphrase info for a host.

    Attributes:
        auth (Literal["key", "password"]): Authentication type.
        key_has_passphrase (bool | None): Whether the key has a passphrase.
    """

    auth: Literal["key", "password"]
    key_has_passphrase: bool | None


@dataclass
class YamlConfig:
    """
    Represents the YAML configuration containing a list of hosts and groups.

    Attributes:
        groups (dict[str, list[str]]): A mapping of group names to lists of host aliases.
        host_auth (dict[str, HostAuth]): Mapping of host aliases to authentication info.
    """

    groups: dict[str, list[str]]
    host_auth: dict[str, HostAuth]

    def as_dict(self) -> dict[str, object]:
        """
        Converts the `YamlConfig` instance into a dictionary format.

        Returns:
            dict: A dictionary representation of the `YamlConfig` instance.
        """
        return asdict(self)


@dataclass
class SSHResult:
    """
    Stores the result of an SSH operation.

    Attributes:
        host (str): The remote host's address or hostname.
        exit_status (int | None): The exit status of the operation (None if failed).
        success (bool): Whether the operation was successful.
        output (BytesOrStr | None): The output of the operation (None if no output).
    """

    host: str
    exit_status: int | None
    success: bool
    output: BytesOrStr | None


@dataclass
class SSHDryRun:
    """
    Represents the intended SSH operation during a dry run, without execution or validation.

    Attributes:
        host (str): Target host.
        alias (str): Alias of the host specified in ~/.ssh/config
        username (str): Username
        port (int): Port on which ssh server is running
        operation (Literal["exec", "push", "pull"]): Type of SSH operation.
        command (str | None): Command to be run (for 'exec').
        local_path (str | None): Local file path (used in 'push' or 'pull').
        remote_path (str | None): Remote file path (used in 'push' or 'pull').
    """

    host: str
    alias: str
    username: str
    port: int
    operation: Literal["exec", "push", "pull"]

    # For exec
    command: str | None = None

    # For push/pull
    local_path: str | None = None

    remote_path: str | None = None
