# Unofficial Netcup CLI

[![netcup.com](https://www.netcup.com/uploads/netcup_set_C_728x90_b94e135b39.png)](https://www.mihnea.dev/netcup-vouchers)

^^ Click to support me AND redeem a netcup DISCOUNT VOUCHER on [www.mihnea.dev](https://www.mihnea.dev/)

A simple CLI tool for interacting with the Netcup Webservice (based on [`netcup_webservice`](https://github.com/mihneamanolache/netcup-webservice))

## Installation
You can install the CLI tool using pip:
```bash
pip install netcup-cli
```

## Usage
### 1. Setup Login Credentials
Before using any of the commands, you need to log in and save your credentials.
```bash
netcup-cli login 
```
If you don't provide the --user and --password arguments, the CLI will prompt you to input them.
### 2. Available Commands
**Get Commands**
Use the `get` command to retrieve information from the Netcup Webservice. Available resources:
- `vservers`: Get the list of all vServers.
- `vserver_nickname`: Get the nickname of a specific vServer.
- `vserver_state`: Get the state of a specific vServer (running, stopped, etc.).
- `vserver_uptime`: Get the uptime of a specific vServer.
- `vserver_update_notification`: Get the update notifications for a specific vServer.
- `vserver_stat_token`: Get the stat token for a specific vServer.
- `vserver_traffic_of_day`: Get the daily traffic usage for a specific vServer.
- `vserver_traffic_of_month`: Get the monthly traffic usage for a specific vServer.
- `vserver_information`: Get detailed information for a specific vServer.
- `vserver_ips`: Get the IPs assigned to a specific vServer.

Example usage:
```bash
# Get the list of all vServers
netcup-cli get vservers

# Get the state of a specific vServer
netcup-cli get vserver_state --vserver_name YOUR_VSERVER_NAME
```

**Set Commands**
Use the `set` command to update information in the Netcup Webservice. Available resources:
- `vserver_nickname`: Set a new nickname for a specific vServer.
- `password`: Change the user password.
- `panel_settings`: Update panel settings.

Example usage:
```bash
# Set a new nickname for a specific vServer
netcup-cli set vserver_nickname --vserver_name YOUR_VSERVER_NAME --nickname NEW_NICKNAME

# Change the user password
netcup-cli set password --new_password NEW_PASSWORD
```

**Start/Stop/Poweroff Commands**
You can manage the state of your vServers using the following commands:
```bash
# Start a specific vServer
netcup-cli start --vserver_name YOUR_VSERVER_NAME

# Stop a specific vServer
netcup-cli stop --vserver_name YOUR_VSERVER_NAME

# Power off a specific vServer
netcup-cli poweroff --vserver_name YOUR_VSERVER_NAME
```

**Project Commands**
You can organize vServers into projects stored locally in a SQLite database.
```bash
# Create a project
netcup-cli project create myproject

# Add all servers with a nickname matching 'web-' to the project
netcup-cli project add --project myproject --nick '^web-'

# List projects and assigned servers
netcup-cli project list
```

## Disclaimer
This package is not affiliated with, endorsed, or sponsored by Netcup GmbH. It is an independent project and is maintained solely by its contributors.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

