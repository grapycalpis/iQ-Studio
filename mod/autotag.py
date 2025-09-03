# Copyright (c) 2025 Innodisk Corp.
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import subprocess
import json
import logging

class AUTOTAG:
    def __init__(self, args, root_path, bsp_version):
        self.args = args
        self.image_name = self.args.autotag
        self.docker_image_dir = os.path.normpath(os.path.join(root_path, 'binaries', 'docker-images'))
        self.bsp_version = bsp_version

    def _check_local_image(self, bsp_version):
        """
        Checks for a compatible image by first filtering all images with the correct
        BSP label, and then filtering that list in Python for the correct name.
        This is more robust than relying on Docker's multi-filter logic.
        """
        logging.info("Step 1: Check if your local Docker image is compatible...")
        try:
            # Step 1: Get all images that match the BSP version label.
            result = subprocess.run(
                ['docker', 'images',
                 '--filter', f'label=BSP_VERSION={bsp_version}',
                 '--format', '{{.Repository}}:{{.Tag}}'],
                check=True, capture_output=True, text=True
            )
            compatible_images = result.stdout.strip().splitlines()

            if not compatible_images:
                logging.info("There is no local image with a bsp label that matches the system.")
                return None

            # Step 2: Filter the list in Python to find the desired image name.
            for image in compatible_images:
                if self.image_name in image:
                    logging.info(f"Success: Found a local compatible image: {image}")
                    return image
            
            logging.info(f"Found {len(compatible_images)} bsp matching images, but none of them have the name '{self.image_name}'.")
            return None

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logging.error(f"Error checking local image: {e}")
            return None

    def _check_tar_archive(self, bsp_version):
        logging.info("Step 2: Check the .tar archive...")
        tar_path = os.path.join(self.docker_image_dir, f'{self.image_name}.tar')

        if not os.path.isfile(tar_path):
            logging.info(f"Could not find .tar archive at {tar_path}.")
            return None

        logging.info(f"Found .tar archive: {tar_path}, checking with skopeo...")
        try:
            result = subprocess.run(
                ['skopeo', 'inspect', f'docker-archive:{tar_path}'],
                check=True, capture_output=True, text=True
            )
            img_data = json.loads(result.stdout)
            label_bsp = img_data.get('Labels', {}).get('BSP_VERSION')

            if label_bsp == bsp_version:
                logging.info(f"Success: BSP version ({label_bsp}) of .tar archive matches, loading...")
                subprocess.run(['docker', 'load', '-i', tar_path], check=True)
                # Assume the loaded image will have the ':latest' tag.
                loaded_image_name = f"{self.image_name}:latest"
                logging.info(f"The image file has been loaded successfully, assuming the name is: {loaded_image_name}")
                return loaded_image_name
            else:
                logging.warning(f"BSP version of .tar archive ({label_bsp}) does not match system ({bsp_version}).")
                return None
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error checking or loading .tar archive: {e}")
            return None

    def _pull_from_hub(self, bsp_version):
        logging.info("Step 3: Try downloading from Docker Hub...")
        image_to_pull = f"innodiskorg/{self.image_name}:{bsp_version}"
        logging.info(f"PULL: {image_to_pull}")
        try:
            subprocess.run(['docker', 'pull', image_to_pull], check=True)
            logging.info("Success: The image has been downloaded from Docker Hub.")
            return image_to_pull
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logging.error(f"Pull from Docker Hub failed: {e}")
            return None

    def ensure_compatible_image_exists(self):
        system_bsp = self.bsp_version

        if (found_image := self._check_local_image(system_bsp)):
            return found_image
        
        if (found_image := self._check_tar_archive(system_bsp)):
            return found_image

        if (found_image := self._pull_from_hub(system_bsp)):
            return found_image

        logging.info("--- All methods failed ---")
        return None