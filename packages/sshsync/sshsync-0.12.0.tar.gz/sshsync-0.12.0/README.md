# sshsync ⚡🔐

**sshsync** is a fast, minimal CLI tool to run shell commands across multiple remote servers via SSH. Easily target all servers or just a specific group, great for sysadmins, developers, and automation workflows.

> **IMPORTANT**:
> 
> 1. sshsync uses asyncssh for SSH connections. If you use passphrase-protected SSH keys, you MUST have your ssh-agent running with the keys added via ssh-add. sshsync will rely on SSH agent forwarding to authenticate with protected keys.
> 2. Throughout this documentation, whenever "host" is mentioned, it refers to the SSH alias defined by the `Host` directive in your `~/.ssh/config` file, not the actual hostname (`HostName` directive). sshsync uses these aliases for all operations.

## Features ✨

- 🔁 Run shell commands on **all hosts** or **specific groups**
- 🚀 Executes commands **concurrently** across servers
- 🧠 Group-based configuration for easy targeting
- 🕒 Adjustable SSH timeout settings
- 📁 **Push/pull files** between local and remote hosts
- 📊 Operation history and logging
- 🔍 **Dry-run mode** to preview actions before execution

## Demo 📽️

![Demo](./demo.gif)

## Installation 📦

### Requirements

- Python 3.10 or higher

### Install with pip

```bash
pip install sshsync
```

### Manual Installation

Clone and install manually:

```bash
git clone https://github.com/Blackmamoth/sshsync.git
cd sshsync
pipx install .
```

## Usage 🚀

```bash
sshsync [OPTIONS] COMMAND [ARGS]...
```

**Global Options:**

- `--install-completion` - Install completion for the current shell
- `--show-completion` - Show completion for the current shell
- `--help` - Show help message and exit

## Commands & Usage 🛠️

```bash
sshsync [OPTIONS] COMMAND [ARGS]...
```

### Running Commands on Servers

#### Execute on All Hosts

```bash
sshsync all [OPTIONS] CMD
```

**Options:**

- `--timeout INTEGER` - Timeout in seconds for SSH command execution (default: 10)
- `--dry-run` - Show command and host info without executing

**Examples:**

```bash
# Check disk space on all servers with a 20 second timeout
sshsync all --timeout 20 "df -h"

# Preview which hosts would receive the command without executing
sshsync all --dry-run "systemctl restart nginx"
```

#### Execute on a Specific Group

```bash
sshsync group [OPTIONS] NAME CMD
```

**Options:**

- `--timeout INTEGER` - Timeout in seconds for SSH command execution (default: 10)
- `--dry-run` - Show command and host info without executing
- `--regex` - Filter group members by matching alias with a regex pattern

**Examples:**

```bash
# Restart web services on production servers
sshsync group web-servers "sudo systemctl restart nginx"

# Preview the command execution on database servers without executing
sshsync group db-servers --dry-run "service postgresql restart"
```

### File Transfer Operations

#### Push Files to Remote Hosts

```bash
sshsync push [OPTIONS] LOCAL_PATH REMOTE_PATH
```

**Options:**

- `--all` - Push to all configured hosts
- `--group TEXT` - Push to a specific group of hosts
- `--regex` - Filter group members by matching alias with a regex pattern (can only be used with `--group`)
- `--host TEXT` - Push to a single specific host
- `--recurse` - Recursively push a directory and its contents
- `--dry-run` - Show transfer and host info without executing

**Examples:**

```bash
# Push configuration file to all hosts
sshsync push --all ./config.yml /etc/app/config.yml

# Push directory to web-servers group recursively
sshsync push --group web-servers --recurse ./app/ /var/www/app/

# Preview file transfer to a specific host without executing
sshsync push --host staging-db --dry-run ./db-config.json /etc/postgres/conf.d/
```

#### Pull Files from Remote Hosts

```bash
sshsync pull [OPTIONS] REMOTE_PATH LOCAL_PATH
```

**Options:**

- `--all` - Pull from all configured hosts
- `--group TEXT` - Pull from a specific group of hosts
- `--regex` - Filter group members by matching alias with a regex pattern (can only be used with `--group`)
- `--host TEXT` - Pull from a single specific host
- `--recurse` - Recursively pull a directory and its contents
- `--dry-run` - Show transfer and host info without executing

**Examples:**

```bash
# Pull log files from all database servers
sshsync pull --group db-servers /var/log/mysql/error.log ./logs/

# Pull configuration directory from a specific host
sshsync pull --host prod-web-01 --recurse /etc/nginx/ ./backups/nginx-configs/

# Preview which files would be pulled without executing
sshsync pull --group web-servers --dry-run /var/log/nginx/access.log ./logs/
```

### Configuration Management

#### Add Hosts to Groups

```bash
sshsync gadd [OPTIONS] GROUP
```

**Arguments:**

- `GROUP` - The group to add hosts to (required)

**Example:**

```bash
# Add hosts to the 'web' group
sshsync gadd web
```

#### Add a Host to SSH Config

```bash
sshsync hadd [OPTIONS]
```

This command interactively adds a new host to your SSH config file.

**Example:**

```bash
# Add a new host to your SSH configuration
sshsync hadd
```

#### Synchronize Ungrouped Hosts

```bash
sshsync sync [OPTIONS]
```

This command prompts for group assignments for all ungrouped hosts and updates the config.

**Example:**

```bash
# Assign groups to all ungrouped hosts
sshsync sync
```

#### List Configured Hosts and Groups

```bash
sshsync ls [OPTIONS]
```

**Options:**

- `--with-status` - Show whether a host is reachable

**Example:**

```bash
# List all hosts with their connection status
sshsync ls --with-status
```

#### Show Version

```bash
sshsync version
```

## Configuration 🔧

> sshsync stores its configuration in a YAML file located at `~/.config/sshsync/config.yaml`. It uses your existing SSH configuration from `~/.ssh/config` for host connection details and stores only group information in its own config file. Before running other commands, it's recommended to run `sshsync sync` to assign hosts to groups for easier targeting.
> 
> **Note about hosts**: sshsync uses the SSH alias (the `Host` directive) from your `~/.ssh/config` file, not the actual hostname. This means when you specify a host in any sshsync command, you're referring to the SSH alias that you've defined in your SSH config.

### Configuration File Structure

```yaml
groups:
  dev:
  - example.site
  work:
  - work.dev
  - ssh.work.dev
  web:
  - cloudmesh
  - example.com
```

You can edit this file manually or use the built-in commands to manage groups and hosts.

> **Note**: sshsync leverages your existing SSH configuration for host details, making it easier to maintain a single source of truth for SSH connections.

## Logging 📝

sshsync now includes operation history and logging functionality. Logs are stored in platform-specific locations:

- **Windows**: `%LOCALAPPDATA%\sshsync\logs`
- **macOS**: `~/Library/Logs/sshsync`
- **Linux**: `~/.local/state/sshsync`

These logs track command executions, file transfers, and any errors that occur during operations.

## Examples 🧪

```bash
# Check disk space on all servers
sshsync all "df -h"

# View memory usage on all database servers with increased timeout
sshsync group db-servers --timeout 30 "free -m"

# Preview a potentially destructive command without execution
sshsync all --dry-run "sudo apt update && sudo apt upgrade -y"

# Push configuration files to production servers recursively
sshsync push --group production --recurse ./configs/ /etc/app/configs/

# Pull log files from all web servers
sshsync pull --group web-servers /var/log/nginx/error.log ./logs/

# Preview file transfers to validate paths before execution
sshsync push --all --dry-run ./sensitive-config.json /etc/app/config.json

# Add hosts to the dev group
sshsync gadd dev

# Add a new host to your SSH configuration
sshsync hadd

# Assign groups to all ungrouped hosts
sshsync sync

# Check if hosts are reachable
sshsync ls --with-status
```

## Upcoming Features 🛣️

- Live results display (--live flag) to show command outputs as they complete
- Performance optimizations for large server fleets
- Support for additional authentication methods
- Automated versioning using release-please for streamlined releases

## License 📄

MIT License
