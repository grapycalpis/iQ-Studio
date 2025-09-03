# Copyright (c) 2025 Innodisk Corp.
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import subprocess
import logging

class IPK:
    def __init__(self, args, root_path, bsp_version):
        self.args = args
        self.ipk_dir = os.path.normpath(os.path.join(root_path, 'binaries', 'ipk'))
        self.bsp_version = bsp_version

    def is_installed(self):
        """
        Checks if the package is already installed by parsing the output of 'opkg status'.
        It verifies that the output contains 'Status: install ok installed'.
        """
        ipk_name = self.args.ipk
        logging.info(f"Checking if package '{ipk_name}' is installed...")

        try:
            result = subprocess.run(
                ['opkg', 'status', ipk_name],
                capture_output=True, text=True, check=False # check=False to handle not-found case
            )

            # If opkg fails (e.g., package not found), it often returns a non-zero exit code.
            # We check stdout for the definitive status line.
            if "Status: install ok installed" in result.stdout:
                logging.info(f"Package '{ipk_name}' is already installed.")
                return True
            else:
                logging.info(f"Package '{ipk_name}' is not installed or has an invalid status.")
                return False

        except FileNotFoundError:
            logging.error("'opkg' command not found. Unable to check package status.")
            return False

    def find_compatible_path(self):
        """
        Finds a compatible .ipk file by inspecting its metadata via the 'opkg' command.
        It checks for a matching package name and a version that corresponds to the system's BSP.
        """
        system_bsp = self.bsp_version

        search_dir = self.ipk_dir

        if not os.path.isdir(search_dir):
            logging.error(f"IPK directory does not exist: {search_dir}")
            return None

        for filename in os.listdir(search_dir):
            if not filename.endswith(".ipk"):
                continue

            full_path = os.path.join(search_dir, filename)
            logging.info(f"Checking file: {filename}")

            try:
                # Get Package Name
                pkg_name_cmd = f"opkg info {full_path} | awk -e '/^Package:/{{print $2}}'"
                ipk_name_result = subprocess.run(
                    ['sh', '-c', pkg_name_cmd],
                    check=True, capture_output=True, text=True, encoding='utf-8'
                )
                ipk_name = ipk_name_result.stdout.strip()

                # Get Version (BSP)
                version_cmd = f"opkg info {full_path} | awk -e '/^Version:/{{print $2}}'"
                ipk_version_result = subprocess.run(
                    ['sh', '-c', version_cmd],
                    check=True, capture_output=True, text=True, encoding='utf-8'
                )
                ipk_bsp_version = ipk_version_result.stdout.strip()

                # Compare
                if ipk_name == self.args.ipk and ipk_bsp_version == system_bsp:
                    logging.info(f"Found compatible IPK: {filename} (Package: {ipk_name}, BSP: {ipk_bsp_version})")
                    return full_path

            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                logging.debug(f"Could not get info from {filename} or it's not a match: {e}")
                continue

        logging.error(f"Could not find any package '{self.args.ipk}' compatible with system BSP '{system_bsp}' in {search_dir}")
        return None

    def install(self, file_path):
        """Installs the .ipk file at the given path."""
        if not file_path:
            logging.error("No installation archive path provided.")
            return False
            
        logging.info(f"Ready to install: {file_path}")
        try:
            subprocess.run(
                ['opkg', 'install', file_path],
                check=True, capture_output=True, text=True
            )
            logging.info(f"The package {os.path.basename(file_path)} was installed successfully.")
            return True
        except FileNotFoundError:
            logging.error("'opkg' directive does not exist.")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Package installation failed. Return code: {e.returncode}")
            logging.error(f"Error message:\n{e.stderr}")
            return False