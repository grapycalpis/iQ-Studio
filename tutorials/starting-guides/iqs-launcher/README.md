<!--
 Copyright (c) 2025 Innodisk Corp.
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# iqs-launcher architecture guide

This project provides a command-line tool to install and launch iQ-Studio components. It automatically manages dependencies like Docker images and IPK packages by verifying their compatibility with the system's Board Support Package (BSP) version.

## Architecture

![Architecture Diagram](fig/iqs-launcher_flow.png)


## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3 (`python3`, `python3-venv`)
- Docker
- Skopeo
- OPKG Package Manager

This tool also expects a specific directory structure for its components:
- `binaries/docker-images/`: Stores Docker image `.tar` archives.
- `binaries/ipk/`: Stores `.ipk` package files.

## Installation

To install the launcher, run the installation script from the project root directory. This will create a Python virtual environment and create a symbolic link for the launcher in `/usr/local/bin`, making it a global command.

```bash
./install.sh
```

## How to Use

The primary command is `iqs-launcher`. It serves as the main entry point for all operations.

### Arguments

- `--autotag <component_name>`: Finds a compatible Docker image for the specified component, loads it, and then executes its `run.sh` script.
- `--ipk <package_name>`: Finds and installs a compatible `.ipk` package and then executes its `run.sh` script.
- `--other "<args>"`: Passes additional arguments to the component's `run.sh` script.

### How It Works

1.  **Docker Image (`--autotag`)**:
    1.  Checks for a locally available Docker image with a matching BSP version label.
    2.  If not found, it looks for a `{component_name}.tar` archive in the `binaries/docker-images/` directory and checks its BSP version.
    3.  If still not found, it attempts to pull the image from Docker Hub (`innodiskorg/{component_name}:{bsp_version}`).
    4.  Once a compatible image is found, it looks up the component's script in `metadata.json` and executes it, passing the image name as an argument.

2.  **IPK Package (`--ipk`)**:
    1.  Checks if the package is already installed via `opkg`.
    2.  If not, it searches the `binaries/ipk/` directory for an `.ipk` file with a matching package name and BSP version.
    3.  If a compatible package is found, it installs it using `opkg install`.
    4.  Finally, it looks up the component's script in `metadata.json` and executes it.

### Component Script Mapping (`metadata.json`)

The `iqs-launcher` uses a `metadata.json` file to map a component's name to its executable `run.sh` script. This file is the central registry for all runnable components.

#### File Location

The `metadata.json` file must be located at `<project_root>/tutorials/metadata.json`.

#### Format

The file contains a standard JSON object:

*   **Key**: The `component_name` (e.g., `iqs-ubuntu`).
*   **Value**: The path to the component's `run.sh` script, relative to the project root directory (`iQ-Studio__confidential/`).

#### Example

Consider the following directory structure:

```
iQ-Studio__confidential/
├── tutorials/
│   ├── metadata.json
│   └── integrations/
│       └── iqs-ubuntu/
│           └── run.sh
├── iqs-launcher.sh
└── ... (other project files)
```

To allow the launcher to find the `iqs-ubuntu` component, the `tutorials/metadata.json` file must contain:

```json
{
    "iqs-ubuntu": "tutorials/integrations/iqs-ubuntu/run.sh"
}
```

When you execute `iqs-launcher --autotag iqs-ubuntu`, the tool will:
1.  Read `tutorials/metadata.json` from within the project.
2.  Look up the `iqs-ubuntu` key to get the value `"tutorials/integrations/iqs-ubuntu/run.sh"`.
3.  Combine the project's root path with this value to get the final, executable script path.

### How to Write a `run.sh` Script

The `run.sh` script is the entry point for launching your component. After `iqs-launcher` has successfully prepared the dependencies (like pulling a Docker image or installing an IPK package), it executes this script to start your application.

#### Script Location

The path to the script for a component named `<component_name>` must be defined in `tutorials/metadata.json`. The script should be executable (`chmod +x`).

#### Handling Arguments

Your `run.sh` script needs to be able to handle arguments passed by `iqs-launcher`.

*   **For Docker-based Components (`--autotag`)**: The first argument (`$1`) will always be the name of the compatible Docker image found by the launcher. Your script **must** use this argument in the `docker run` command.

*   **For IPK-based Components (`--ipk`)**: No default arguments are passed to the script.

*   **Additional Arguments (`--other`)**: Any arguments provided with the `--other` flag will be passed to your script after the default arguments. You can use `shift` and `$@` to process them.

#### Example `run.sh`

This example can be used as a template for your own Docker-based components.

```bash
#!/bin/bash
# File: tutorials/integrations/hello-test/run.sh

# Exit immediately if a command fails.
set -e

# The first argument ($1) is the Docker image name provided by iqs-launcher.
IMAGE_TO_RUN="$1"

# Use 'shift' to remove the image name from the argument list.
# Now, $@ contains only the arguments passed via the --other flag.
shift

# Execute the container using the provided image name and pass any additional arguments.
echo "Executing docker run on image: $IMAGE_TO_RUN with args: $@"
docker run --rm "$IMAGE_TO_RUN" "$@"
```

### Examples

**Launch a Docker-based component:**

- **Usage:** `iqs-launcher --autotag <component_name> [--other "<args>"]`
- **Example:**
  ```bash
  iqs-launcher --autotag iqs-ubuntu --other "--rm"
  ```

**Install and launch an IPK-based component:**

- **Usage:** `iqs-launcher --ipk <package_name> [--other "<args>"]`
- **Example:**
  ```bash
  iqs-launcher --ipk my-service
  ```
