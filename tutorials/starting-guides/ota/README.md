# Qualcomm OTA Guide
## Overview
![ai_on_dragonwing_sw_stack](fig/ai_on_dragonwing_sw_stack.png)
- Capsule Update
    - Capsule update uses a UEFI capsule to update firmware on Qualcomm Linux devices. The capsule is downloaded to the EFI partition during normal operation, then applied automatically on the next reboot.

- OSTree Update
    - OSTree provides atomic, version-controlled Linux OS updates. Devices pull filesystem snapshots from a repository, with support for safe rollback if an update fails.

## Capsule Update
### Prepare the .capsule file
Please refer to [Generate Capsule](https://github.com/quic/cbsp-boot-utilities/tree/main/uefi_capsule_generation) for more information.
### Update the .capsule file
Please refer to [Capsule update flow](https://docs.qualcomm.com/doc/80-70020-27/topic/ota_update_for_qualcomm_linux.html#capsule-update-flow) for more information.
> [!NOTE]  
> You can specify the firmware version number using the `-fwver` option in `capsule_creator.py`.
### Verify the update
Assuming you use `-fwver 0.0.0.9527` to specify the firmware version, after updating the capsule, the boot log (accessible through UART) will show the FwVer value as 9527 (0x2537).  
![fwver_bootlog](fig/fwver_bootlog.png)  
After entering the system, you can also run `cat /sys/firmware/efi/esrt/entries/entry0/fw_version` and see the value 9527.  
![fw_version](fig/fw_version.png)

This confirms that the capsule has been successfully updated.
Please refer to [Capsule update logs](https://docs.qualcomm.com/doc/80-70018-4/topic/capsule-update-logs.html), [Capsule update flow](https://docs.qualcomm.com/doc/80-70020-27/topic/ota_update_for_qualcomm_linux.html#capsule-update-flow) for more information.

## OSTree Update
### Prepare & Update the OSTree
Please refer to [Linux OS update flow using OSTree](https://docs.qualcomm.com/doc/80-70020-27/topic/ota_update_for_qualcomm_linux.html#linux-os-update-flow-using-ostree) for more information.

## Reference
[OTA update for Qualcomm Linux](https://docs.qualcomm.com/doc/80-70020-27/topic/ota_update_for_qualcomm_linux.html)
