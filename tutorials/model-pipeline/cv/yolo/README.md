# Model Pipeline: End-to-end guides for converting, optimizing, and deploying AI models on the target platform.

This iQ-Studio tutorial is a simple YOLO26 workflow for Qualcomm Dragonwing IQ9. It shows how to quantize, convert, quality check, and run inference with the default pipeline.

<div align="center"><img src="./img/readme_1.png" alt="Model pipeline overview" width="100%"></div>

## Overview

This guide follows a straightforward end-to-end flow:

1. Quantize the FP32 YOLO26 `.pt` model.
2. Convert it to a quantized `.tflite` model with Qualcomm AI Hub.
3. Compare FP and quantized quality with mAP.
4. Run inference on Qualcomm Dragonwing IQ9 through ADB.

This tutorial focuses on the default YOLO26 path only.

## Requirements

- Ubuntu 22.04 host
- Qualcomm Dragonwing IQ9 target
- USB connection for ADB-based execution

## Step 1. Connect Device

Connect the Qualcomm Dragonwing IQ9 target to the host with a USB-C cable.

<div align="center"><img src="./img/readme_2.png" alt="Host to target USB-C connection" width="80%"></div>

## Step 2. Source `setup.sh`

Source the setup script from this tutorial directory:

```bash
$ source setup.sh
```

This prepares the Python environment, installs the required host packages, and checks ADB access.

## Step 3. QAI Hub Authentication

Log in to the [Qualcomm AI Hub Workbench](https://aihub.qualcomm.com/).

Navigate to `Account -> Settings -> API Token` to find your unique key.

Configure the host with your API token:

```bash
$ qai-hub configure --api_token YOUR_API_TOKEN
```

## Step 4. Use the Modes

### QC

Configure the required paths for `qc`, then run the mode:

```bash
$ python3 cli.py --configure qc
$ python3 cli.py --mode qc
```

### mAP

Configure the required paths for `mAP`, then run the mode:

```bash
$ python3 cli.py --configure mAP
$ python3 cli.py --mode mAP
```

For a smaller validation run, you can limit the number of images:

```bash
$ python3 cli.py --mode mAP --max-images 5
```

`mAP` compares the FP model and the quantized model at mAP@0.5.

### Test

Configure the required paths for `test`, then run the mode:

```bash
$ python3 cli.py --configure test
$ python3 cli.py --mode test
```

`test` runs YOLO26 inference on Qualcomm Dragonwing IQ9 through ADB.

## Output

Generated outputs are written to these directories:

- `out/model/yolov26/`
- `out/mAP_results/yolov26/`
- `out/test/yolov26/`

> 💡 **Tip:** To review the currently saved mode paths, run `python3 cli.py --configure current`.
