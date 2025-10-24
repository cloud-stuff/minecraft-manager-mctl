![banner.png](assets/banner.png)

# 🧱 mctl — Minecraft Server Manager CLI

`mctl` is a command-line interface for managing multiple Minecraft servers with ease. It helps you **initialize environments**, **install or remove servers**, **start or stop them**, and **configure server properties** directly from your terminal. The tool is designed to automate repetitive administrative tasks, making Minecraft server management faster, cleaner, and more consistent across environments.

![Python Version](https://img.shields.io/badge/python-≥3.9-blue.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

## 📦 Installation

You will need Poetry if you want to install the project from the repo, or any other 
package manager when installed from PyPi.

Clone the repository and install the dependencies:

```bash
git clone git@github.com:cloud-stuff/minecraft-manager-mctl.git
cd mctl
poetry install
```

Run the CLI using:

```bash
python src/mctl/cli/main.py --help
```

Or make it globally available:

```bash
alias mctl="python /path/to/cli/main.py"
```

---

## ⚙️ Global Usage

```bash
Usage: mctl [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell.
  --help                Show this message and exit.

Commands:
  init      Initialise the mctl environment.
  server    Manage Minecraft server instances.
  start     Start a specific server instance.
  stop      Stop a running server instance.
  config    Manage server configuration (get/set).
```

---

## 🧩 Commands

### 🏗️ `init`

Initialise the environment where `mctl` will store servers, configs, and downloads.

```bash
mctl init [OPTIONS]
```

**Options:**

| Option            | Description                    | Default    |
| ----------------- | ------------------------------ | ---------- |
| `-p, --path PATH` | Path to initialize environment | `~/.mcman` |
| `-f, --force`     | Override existing directories  | `False`    |

**Example:**

```bash
mctl init --path ~/minecraft-env --force
```

**Output:**

```
Environment initialized at /home/user/minecraft-env
```

---

### 🧱 `server`

Manage Minecraft server instances.

#### ➕ `install`

Install a new Minecraft server.

```bash
mctl server install [OPTIONS] NAME
```

**Options:**

| Option          | Description                                            | Default   |
| --------------- | ------------------------------------------------------ | --------- |
| `-t, --type`    | Type of server software (e.g., vanilla, paper, spigot) | `vanilla` |
| `-v, --version` | Minecraft version or `latest`                          | `latest`  |
| `-m, --memory`  | Maximum server memory                                  | `2G`      |
| `--eula-accept` | Automatically accept Mojang's EULA                     | —         |
| `--first-start` | Run once to generate world/configs, then exit          | —         |

**Example:**

```bash
mctl server install survival-base -t paper -v 1.21.1 --memory 4G --eula-accept
```

**Output:**

```
✅ Installed server 'survival-base' (type=paper, version=1.21.1)
```

---

#### 🗑️ `remove`

Remove an existing server.

```bash
mctl server remove NAME
```

**Example:**

```bash
mctl server remove survival-base
```

**Output:**

```
Removed server 'survival-base'
```

---

#### ℹ️ `info`

Display server information.

```bash
mctl server info NAME
```

**Example:**

```bash
mctl server info survival-base
```

**Output:**

```
Server: survival-base
Type: paper
Version: 1.21.1
Memory: 4G
Status: stopped
```

---

### 🚀 `start`

Start a Minecraft server.

```bash
mctl start NAME
```

**Example:**

```bash
mctl start survival-base
```

**Output:**

```
Starting server 'survival-base'...
Server running on port 25565
```

---

### 🛑 `stop`

Stop a running Minecraft server.

```bash
mctl stop NAME
```

**Example:**

```bash
mctl stop survival-base
```

**Output:**

```
Stopping server 'survival-base'... Done.
```

---

### ⚙️ `config`

Manage server properties.

#### ✏️ `set`

Set a configuration value in `server.properties`.

```bash
mctl config set SERVER KEY VALUE
```

**Example:**

```bash
mctl config set survival-base motd "Welcome to Survival!"
```

**Output:**

```
Updated 'motd' = "Welcome to Survival!" in survival-base/server.properties
```

---

#### 🔍 `get`

Retrieve a configuration value.

```bash
mctl config get SERVER KEY
```

**Example:**

```bash
mctl config get survival-base max-players
```

**Output:**

```
max-players = 20
```

---

## 🔄 Common Scenarios

### 1. **Initial Setup**

```bash
mctl init
mctl server install base --eula-accept
```

Creates a full environment and installs the latest vanilla server.

---

### 2. **Testing a New Version**

```bash
mctl server install test -v 1.21.1 --first-start
mctl config set test online-mode false
mctl start test
```

Sets up a test server, disables online mode, and starts it for testing.

---

### 3. **Managing Multiple Servers**

```bash
mctl start creative
mctl start survival
mctl config get survival motd
mctl stop creative
```

Allows parallel management of different servers from one CLI.

---

### 4. **Server Maintenance**

```bash
mctl stop survival
mctl config set survival max-players 10
mctl start survival
```

Stops, updates, and restarts a production server safely.

---

🧾 License

MIT License © 2025
See [LICENSE](LICENSE) for details.

