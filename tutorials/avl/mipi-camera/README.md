# MIPI Camera

MIPI CSI-2 is a widely adopted camera interface standard designed for high-bandwidth, low-power, and low-latency transmission between image sensors and processing SoCs.

It supports multi-gigabit throughput per lane, enabling high-resolution and high-frame-rate video pipelines for modern imaging applications.

With its mature ecosystem and broad sensor compatibility, MIPI CSI-2 is commonly used in autonomous driving, industrial automation, robotics, medical imaging, and AI edge devices.

> 💡 **Tip:** You can check out **[iQS-Streampipe](../../applications/iqs-streampipe/README.md)** to see how to run multi-stream applications on our platform.

## Supported Components

To build a MIPI vision system, the following components are required:

- **Cameras**: [EVDM-OOM1](https://www.innodisk.com/en/products/camera/mipi-csi-2/evdm-oom1-rhcf), [EV2M-OOM3](https://www.innodisk.com/en/products/camera/mipi-csi-2/ev2m-oom3-rhcf), [EV8M-OOM1](https://www.innodisk.com/en/products/camera/mipi-csi-2/ev8m-oom1-rhcf)
- **Evaluation Kits**: [EXEC-Q911](https://www.innodisk.com/cht/products/computing/qualcomm-solution/EXEC-Q911), [iQ-9075 EVK](https://www.qualcomm.com/developer/hardware/qualcomm-iq-9075-evaluation-kit-evk)
- **Operating Systems**: [Yocto Linux 1.6](https://docs.qualcomm.com/doc/80-70022-254/topic/build_addn_info.html?product=895724676033554725&version=1.6), [Ubuntu 24.04 (x07)](https://people.canonical.com/~platform/images/qualcomm-iot/ubuntu-24.04/ubuntu-24.04-x07/)

## Camera Matrix

Specific connection procedures vary depending on the target platform. Follow the instructions below for your specific hardware.

### 1. Connecting to EXEC-Q911

| Module    | Support Platform | Support OS                          | CN_CSI1 | CN_CSI2 | Resolution, Frame Rate |
| --------- | ---------------- | ----------------------------------- | ------- | ------- | ---------------------- |
| EVDM-OOM1 | EXEC-Q911        | Yocto Linux 1.6, Ubuntu 24.04 (x07) | ✅      | ✅      | 1920x1080, 30 FPS      |
| EV2M-OOM3 | EXEC-Q911        | Yocto Linux 1.6, Ubuntu 24.04 (x07) | ✅      | ✅      | 1920x1080, 30 FPS      |
| EV8M-OOM1 | EXEC-Q911        | Yocto Linux 1.6, Ubuntu 24.04 (x07) | ✅      | ✅      | 1920x1080, 30 FPS      |

> ✅ Supported | ❌ Not supported | ☑️ Coming soon

<div align="center">
  <img src="./fig/911-mipi.png" width="80%">
</div>

To connect the camera to the EXEC-Q911, follow these steps:

1. Use a 22-pin to 22-pin MIPI cable (A-B style) to connect `CN_CSIx` to the camera. This specific cable type is essential for correct CSI lane alignment.
2. Power on the EXEC-Q911.

<br />
<br />

### 2. Connecting to iQ-9075 EVK

| Module    | Support Platform | Support OS                          | JCAM0 | JCAM1 | JCAM2 | JCAM3 | Resolution, Frame Rate |
| --------- | ---------------- | ----------------------------------- | ----- | ----- | ----- | ----- | ---------------------- |
| EVDM-OOM1 | iQ-9075 EVK      | Yocto Linux 1.6, Ubuntu 24.04 (x07) | ✅    | ✅    | ✅    | ✅    | 1920x1080, 30 FPS      |
| EV2M-OOM3 | iQ-9075 EVK      | Yocto Linux 1.6, Ubuntu 24.04 (x07) | ✅    | ✅    | ✅    | ✅    | 1920x1080, 30 FPS      |
| EV8M-OOM1 | iQ-9075 EVK      | Yocto Linux 1.6, Ubuntu 24.04 (x07) | ✅    | ✅    | ✅    | ✅    | 1920x1080, 30 FPS      |

> ✅ Supported | ❌ Not supported | ☑️ Coming soon

<div align="center">
  <img src="./fig/evk-mipi.png" width="80%">
</div>

To connect the camera to the iQ-9075 EVK, follow these steps:

1. Use a 22-to-30 pin adapter to connect the 22-pin to 22-pin MIPI cable (A-A style). 
2. Connect `JCAMx` to the camera. This cable type is required for proper CSI lane alignment.
3. Power on the iQ-9075 EVK.

## How to Deploy

To deploy the camera drivers and configuration, follow these steps:

1. Copy the `.tar.gz` release package to the target platform:
    ```bash
    scp release/<module_name>.tar.gz <target_ip>:/home/root/
    ```
    
2. Install the package based on your operating system and reboot:

### Yocto Linux 1.6
1. Remount the filesystem as read-write and extract the package:
    ```bash
    mount -o rw,remount /usr
    tar -xzvf release/<module_name>.tar.gz -C /usr/lib/camera
    reboot
    ```
            
### Ubuntu 24.04 (x07)
1. Configure the package sources for version x07:
    ```bash
    sudo sed -i 's|URIS: https://ppa.launchpadcontent.net/ubuntu-qcom-iot/qcom-ppa/ubuntu|URIS: https://ppa.launchpadcontent.net/ubuntu-qcom-iot/qcom-ppa-snapshot-x07/ubuntu|' /etc/apt/sources.list.d/ubuntu-qcom-iot-ubuntu-qcom-ppa-noble.sources
    ```
2. Update the system and install the required samples:
    ```bash
    sudo apt update -y && sudo apt upgrade -y
    sudo apt install gstreamer1.0-qcom-sample-apps -y
    ```
3. Extract the release package to the camera library directory:
    ```bash
    sudo tar -xzvf release/<module_name>.tar.gz -C /usr/lib/camera
    sudo reboot
    ```

## How to Use

If the camera is properly connected and the required drivers are installed, you can use GStreamer to interact with the camera streams.

> 🔔 **Note:** For **Yocto Linux**, suppress kernel messages before running pipelines: `echo 0 > /proc/sys/kernel/printk`

To capture a single stream and encode it to MP4:

```bash
pkill cam-server && sleep 5
gst-launch-1.0 -e qtiqmmfsrc exposure-mode=off manual-exposure-time=10000000000 name=camsrc camera=0 ! \
'video/x-raw,width=1920,height=1080,framerate=30/1' ! \
videoconvert ! v4l2h264enc ! h264parse ! mp4mux ! filesink location=test.mp4
```

<div align="center">
  <img src="./fig/mpipi.gif" width="80%">
</div>