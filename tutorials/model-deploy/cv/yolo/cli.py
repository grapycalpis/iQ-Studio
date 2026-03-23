#!/usr/bin/env python3
# Copyright (c) 2025 Innodisk Corp.
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from tool.test_map import run_fp_int_pair_map_eval
from yolo_models.yolov26 import YOLOV26_TEST_DEFAULTS, YoloV26Pipeline

YOLO26_MODEL_TYPE = "yolov26"
YOLO26_QC_HEAD = "one2many"
YOLO26_QC_QUANT_SCHEME = "mse"
YOLO26_QC_MAX_CALIB = 200
DEFAULT_MAP_RESULTS_DIR = Path(__file__).resolve().parent / "out" / "mAP_results"
DEFAULT_QC_RESULTS_DIR = Path(__file__).resolve().parent / "out" / "model"
DEFAULT_TEST_RESULTS_DIR = Path(__file__).resolve().parent / "out" / "test"
DEFAULT_QNN_LIB = "/usr/lib/libQnnTFLiteDelegate.so"
CONFIG_PATH = Path(__file__).resolve().parent / "config.json"
ANSI_RESET = "\033[0m"
ANSI_YELLOW = "\033[33m"
ANSI_GREEN = "\033[32m"
ANSI_RED = "\033[31m"


def _print_colored_error(message: str) -> None:
    print(f"{ANSI_RED}{message}{ANSI_RESET}")


def _print_colored_warn(message: str) -> None:
    print(f"{ANSI_YELLOW}{message}{ANSI_RESET}")


def parse_args() -> argparse.Namespace:
    mode_help = (
        "Top-level usage:\n"
        "\n"
        "Configure a mode\n"
        "  python3 cli.py --configure qc\n"
        "  python3 cli.py --configure mAP\n"
        "  python3 cli.py --configure test\n"
        "  python3 cli.py --configure current\n"
        "\n"
        "Run a mode\n"
        "  python3 cli.py --mode qc\n"
        "  python3 cli.py --mode mAP\n"
        "  python3 cli.py --mode test\n"
        "\n"
        "Mode-specific requirements:\n"
        "\n"
        "QC Mode\n"
        "  Required:\n"
        "    --mode qc --model --calib_dir\n"
        "  Optional:\n"
        "    --output\n"
        "\n"
        "mAP Mode\n"
        "  Required:\n"
        "    --mode mAP --annotations --images --fp-model --int-model\n"
        "  Optional:\n"
        "    --output_text --conf --nms --max-det --max-images\n"
        "    --adb-serial --qnn-lib\n"
        "\n"
        "Test Mode\n"
        "  Required:\n"
        "    --mode test --model --yaml --images\n"
        "  Optional:\n"
        "    --out/--output --conf --nms --topk --max-det\n"
        "    --adb-serial --qnn-lib\n"
    )

    parser = argparse.ArgumentParser(
        "qualcomm_ai_hub_model_utility",
        formatter_class=argparse.RawTextHelpFormatter,
        allow_abbrev=False,
        description=(
            "YOLO26 mode overview:\n"
            "  qc   : quantize/convert a model to TFLite\n"
            "  mAP  : evaluate FP vs INT mAP@0.5 pair\n"
            "  test : run int8 inference via adb\n"
            "  configure : save per-mode paths for later runs"
        ),
        epilog=mode_help,
    )

    common = parser.add_argument_group("Global")
    common.add_argument(
        "--mode",
        choices=["qc", "test", "mAP"],
        help="Execution mode",
    )
    common.add_argument(
        "--configure",
        choices=["qc", "mAP", "test", "current"],
        help="Interactively save mode paths or print the current saved config",
    )
    common.add_argument(
        "--model",
        help="Model path\nRequired in: qc (.pt), test (.tflite)",
    )

    shared = parser.add_argument_group("Shared Optional")
    shared.add_argument(
        "--images",
        help="Image directory\nRequired in: mAP and test",
    )
    shared.add_argument(
        "--conf",
        type=float,
        default=None,
        help="Optional: confidence threshold",
    )
    shared.add_argument(
        "--nms",
        type=float,
        default=None,
        help="Optional: NMS IoU threshold",
    )
    shared.add_argument(
        "--max-det",
        dest="max_det",
        type=int,
        default=None,
        help="Optional: max detections per image",
    )
    shared.add_argument(
        "--adb-serial",
        default=None,
        help="Optional: ADB device serial for target device",
    )
    shared.add_argument(
        "--qnn-lib",
        dest="qnn_lib",
        default=None,
        help=(
            "Optional: QNN delegate library path on device "
            f"(default: {DEFAULT_QNN_LIB})"
        ),
    )

    qc = parser.add_argument_group("QC Args (--mode qc)")
    qc.add_argument(
        "--calib_dir",
        default=None,
        help="Required: calibration image folder",
    )
    qc.add_argument(
        "--output",
        help=(
            "Optional: output .tflite path\n"
            "Default: out/model/yolov26/yolov26_int8_<timestamp>.tflite"
        ),
    )

    map_eval = parser.add_argument_group("mAP Args (--mode mAP)")
    map_eval.add_argument(
        "--annotations",
        help=(
            "Required: COCO annotations JSON or custom annotation directory "
            "with labels in 'txt' or 'xml' format"
        ),
    )
    map_eval.add_argument(
        "--fp-model",
        dest="fp_model",
        help="Required: FP .pt model path",
    )
    map_eval.add_argument(
        "--int-model",
        dest="int_model",
        help="Required: INT .tflite model path",
    )
    map_eval.add_argument(
        "--output_text",
        help=(
            "Optional: output text report path\n"
            "Default: out/mAP_results/yolov26/yolov26_mAP_result_<timestamp>.txt"
        ),
    )
    map_eval.add_argument(
        "--max-images",
        dest="max_images",
        type=int,
        default=300,
        help="Optional: number of images to process (default: 300)",
    )

    test = parser.add_argument_group("Test Args (--mode test)")
    test.add_argument(
        "--yaml",
        help="Required: class names yaml path",
    )
    test.add_argument(
        "--out",
        dest="output",
        help="Optional: alias of --output for test output directory",
    )
    test.add_argument(
        "--topk",
        type=int,
        default=None,
        help="Optional: top-k before NMS (default: 300)",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        raise SystemExit(0)

    args = parser.parse_args()
    if bool(args.mode) == bool(args.configure):
        parser.error("choose exactly one of --mode or --configure")
    return args


def _default_config() -> dict:
    return {"qc": {}, "mAP": {}, "test": {}, "shared": {}}


def _load_config() -> dict:
    if not CONFIG_PATH.exists():
        return _default_config()

    try:
        raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(
            "[error] config.json is invalid. Re-run --configure <mode>."
        ) from exc

    if not isinstance(raw, dict):
        raise SystemExit("[error] config.json is invalid. Re-run --configure <mode>.")

    config = _default_config()
    for section in config:
        value = raw.get(section, {})
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise SystemExit(
                "[error] config.json is invalid. Re-run --configure <mode>."
            )
        config[section] = dict(value)
    return config


def _save_config(config: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=CONFIG_PATH.parent,
        prefix="config.",
        suffix=".tmp",
        delete=False,
    ) as tmp_file:
        json.dump(config, tmp_file, indent=2, sort_keys=True)
        tmp_file.write("\n")
        tmp_path = Path(tmp_file.name)
    tmp_path.replace(CONFIG_PATH)


def _print_saved_config() -> None:
    if not CONFIG_PATH.exists():
        print(f"[info] no saved config found at {CONFIG_PATH}")
        return
    config = _load_config()
    print(f"[info] saved config: {CONFIG_PATH}")
    print(json.dumps(config, indent=2, sort_keys=True))


def resolve_default_qc_output_path(output_override: str | None) -> str:
    if output_override:
        return output_override
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return str(
        DEFAULT_QC_RESULTS_DIR
        / YOLO26_MODEL_TYPE
        / f"{YOLO26_MODEL_TYPE}_int8_{ts}.tflite"
    )


def resolve_default_output_text(output_text_override: str | None) -> str:
    if output_text_override:
        return output_text_override
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return str(
        DEFAULT_MAP_RESULTS_DIR
        / YOLO26_MODEL_TYPE
        / f"{YOLO26_MODEL_TYPE}_mAP_result_{ts}.txt"
    )


def resolve_default_test_output_path(output_override: str | None) -> str:
    if output_override:
        return output_override
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return str(
        DEFAULT_TEST_RESULTS_DIR
        / YOLO26_MODEL_TYPE
        / f"{YOLO26_MODEL_TYPE}_inference_{ts}"
    )


def resolve_default_map_conf(conf_override: float | None) -> float:
    return conf_override if conf_override is not None else 0.25


def resolve_default_map_nms(nms_override: float | None) -> float:
    return nms_override if nms_override is not None else 0.7


def resolve_default_map_max_det(max_det_override: int | None) -> int:
    return max_det_override if max_det_override is not None else 300


def _normalize_path(raw_value: str) -> str:
    return str(Path(raw_value).expanduser().resolve())


def _validate_existing_file(
    raw_value: str, label: str, required_suffixes: tuple[str, ...] | None = None
) -> str:
    path = Path(_normalize_path(raw_value))
    if not path.is_file():
        raise ValueError(f"{label} not found: {path}")
    if required_suffixes and path.suffix.lower() not in required_suffixes:
        suffix_text = ", ".join(required_suffixes)
        raise ValueError(f"{label} must end with {suffix_text}: {path}")
    return str(path)


def _validate_existing_dir(raw_value: str, label: str) -> str:
    path = Path(_normalize_path(raw_value))
    if not path.is_dir():
        raise ValueError(f"{label} not found: {path}")
    return str(path)


def _validate_annotations(raw_value: str) -> str:
    path = Path(_normalize_path(raw_value))
    if not path.exists():
        raise ValueError(f"annotations not found: {path}")
    if not path.is_file() and not path.is_dir():
        raise ValueError(f"annotations must be a file or directory: {path}")
    return str(path)


def _prompt_path(
    prompt_label: str, current_value: str | None, validator
) -> str:
    while True:
        if current_value:
            print(f"[info] existing {prompt_label} path:")
            print(f"  {current_value}")
            if _prompt_yes_no(
                f"Would you like to use the existing {prompt_label} path?",
                default=None,
            ):
                try:
                    return validator(current_value)
                except ValueError as exc:
                    _print_colored_warn(f"[warn] {exc}")

        user_value = input(
            f"{ANSI_YELLOW}Enter the path for {prompt_label}:{ANSI_RESET} "
        ).strip()
        if not user_value:
            _print_colored_error("[error] path input is required")
            continue
        try:
            return validator(user_value)
        except ValueError as exc:
            _print_colored_error(f"[error] {exc}")


def _prompt_yes_no(question: str, default: bool | None = True) -> bool:
    if default is None:
        suffix = f" [{ANSI_GREEN}y{ANSI_RESET}/{ANSI_RED}n{ANSI_RESET}]"
    else:
        suffix = (
            f" [{ANSI_GREEN}Y{ANSI_RESET}/{ANSI_RED}n{ANSI_RESET}]"
            if default
            else f" [{ANSI_GREEN}y{ANSI_RESET}/{ANSI_RED}N{ANSI_RESET}]"
        )
    while True:
        raw = input(f"{ANSI_YELLOW}{question}{ANSI_RESET}{suffix}: ").strip().lower()
        if not raw:
            if default is None:
                _print_colored_error("[error] enter y or n")
                continue
            return default
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        _print_colored_error("[error] enter y or n")


def _list_authorized_adb_devices() -> list[str]:
    adb_bin = shutil.which("adb")
    if adb_bin is None:
        return []

    result = subprocess.run(
        [adb_bin, "devices"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []

    devices: list[str] = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    return devices


def _prompt_adb_serial(devices: list[str]) -> str:
    while True:
        serial = input(f"{ANSI_YELLOW}Enter the ADB serial:{ANSI_RESET} ").strip()
        if not serial:
            _print_colored_error("[error] adb-serial is required")
            continue
        if serial not in devices:
            _print_colored_error(
                f"[error] adb-serial must match one of: {', '.join(devices)}"
            )
            continue
        return serial


def _configure_adb_serial(config: dict) -> None:
    devices = _list_authorized_adb_devices()
    shared = config["shared"]
    existing = str(shared.get("adb_serial", "") or "")

    if not devices:
        print("[info] no ADB target detected. Keeping existing adb-serial unchanged.")
        return

    if len(devices) == 1 and not existing:
        print(
            "[info] one ADB target detected. Leaving adb-serial empty to use the default single-device flow."
        )
        print(f"[info] connected device: {devices[0]}")
        return

    print("[info] connected ADB devices:")
    for serial in devices:
        print(f"  - {serial}")

    if existing:
        print(f"[info] existing adb-serial: {existing}")
        if existing in devices:
            print("[info] existing adb-serial is currently connected")
        else:
            _print_colored_warn(
                "[warn] existing adb-serial is not in the current connected device list"
            )
        if _prompt_yes_no(f"Use existing adb-serial '{existing}'?", default=True):
            return

    shared["adb_serial"] = _prompt_adb_serial(devices)


def _configure_mode(mode: str) -> None:
    config = _load_config()
    section = config[mode]

    if mode == "qc":
        section["model"] = _prompt_path(
            "the QC model file (.pt)",
            section.get("model"),
            lambda value: _validate_existing_file(value, "qc model", (".pt",)),
        )
        section["calib_dir"] = _prompt_path(
            "the QC calibration images folder",
            section.get("calib_dir"),
            lambda value: _validate_existing_dir(value, "qc calibration directory"),
        )
    elif mode == "mAP":
        section["annotations"] = _prompt_path(
            "the mAP annotations file or folder",
            section.get("annotations"),
            _validate_annotations,
        )
        section["images"] = _prompt_path(
            "the mAP images folder",
            section.get("images"),
            lambda value: _validate_existing_dir(value, "mAP image directory"),
        )
        section["fp_model"] = _prompt_path(
            "the mAP FP model file (.pt)",
            section.get("fp_model"),
            lambda value: _validate_existing_file(value, "mAP fp model", (".pt",)),
        )
        section["int_model"] = _prompt_path(
            "the mAP INT model file (.tflite)",
            section.get("int_model"),
            lambda value: _validate_existing_file(
                value, "mAP int model", (".tflite",)
            ),
        )
        _configure_adb_serial(config)
    elif mode == "test":
        section["model"] = _prompt_path(
            "the test model file (.tflite)",
            section.get("model"),
            lambda value: _validate_existing_file(value, "test model", (".tflite",)),
        )
        section["yaml"] = _prompt_path(
            "the test class YAML file",
            section.get("yaml"),
            lambda value: _validate_existing_file(value, "test yaml"),
        )
        section["images"] = _prompt_path(
            "the test images folder",
            section.get("images"),
            lambda value: _validate_existing_dir(value, "test image directory"),
        )
        _configure_adb_serial(config)
    else:
        raise SystemExit(f"[error] unsupported configure mode: {mode}")

    _save_config(config)
    print(f"[ok] saved {mode} config to {CONFIG_PATH}")


def _resolve_cli_or_saved(
    cli_value: str | None, saved_value: str | None
) -> str | None:
    if cli_value not in (None, ""):
        return cli_value
    if saved_value not in (None, ""):
        return saved_value
    return None


def _require_cli_or_saved(
    cli_value: str | None, saved_value: str | None, error_message: str, mode: str
) -> str:
    resolved = _resolve_cli_or_saved(cli_value, saved_value)
    if resolved in (None, ""):
        raise SystemExit(
            f"[error] {error_message} or run: python3 cli.py --configure {mode}"
        )
    return str(resolved)


def _run_qc_mode(args: argparse.Namespace, config: dict) -> None:
    effective_model = _require_cli_or_saved(
        args.model, config["qc"].get("model"), "qc requires --model", "qc"
    )
    effective_calib_dir = _require_cli_or_saved(
        args.calib_dir,
        config["qc"].get("calib_dir"),
        "qc requires --calib_dir (calibration image folder)",
        "qc",
    )

    effective_output = resolve_default_qc_output_path(args.output)
    Path(effective_output).parent.mkdir(parents=True, exist_ok=True)
    try:
        YoloV26Pipeline().quantize_convert(
            model_path=effective_model,
            out_tflite=effective_output,
            calib_dir=effective_calib_dir,
            max_calib=YOLO26_QC_MAX_CALIB,
            qc_head=YOLO26_QC_HEAD,
            qc_quant_scheme=YOLO26_QC_QUANT_SCHEME,
        )
    except (
        FileNotFoundError,
        PermissionError,
        ValueError,
        KeyError,
        RuntimeError,
        OSError,
    ) as exc:
        raise SystemExit(f"[error] {exc}") from exc
    print(f"[ok] wrote: {effective_output}")


def _run_map_mode(args: argparse.Namespace, config: dict) -> None:
    effective_annotations = _require_cli_or_saved(
        args.annotations,
        config["mAP"].get("annotations"),
        "mAP requires --annotations",
        "mAP",
    )
    effective_images = _require_cli_or_saved(
        args.images, config["mAP"].get("images"), "mAP requires --images", "mAP"
    )
    effective_fp_model = _require_cli_or_saved(
        args.fp_model,
        config["mAP"].get("fp_model"),
        "mAP requires --fp-model",
        "mAP",
    )
    effective_int_model = _require_cli_or_saved(
        args.int_model,
        config["mAP"].get("int_model"),
        "mAP requires --int-model",
        "mAP",
    )

    effective_output_text = resolve_default_output_text(args.output_text)
    effective_conf = resolve_default_map_conf(args.conf)
    effective_nms = resolve_default_map_nms(args.nms)
    effective_max_det = resolve_default_map_max_det(args.max_det)
    effective_adb_serial = _resolve_cli_or_saved(
        args.adb_serial, config["shared"].get("adb_serial")
    )
    effective_qnn_lib = _resolve_cli_or_saved(
        args.qnn_lib, config["shared"].get("qnn_lib")
    ) or DEFAULT_QNN_LIB

    try:
        run_fp_int_pair_map_eval(
            fp_model=effective_fp_model,
            int_model=effective_int_model,
            annotations=effective_annotations,
            images=effective_images,
            output_text=effective_output_text,
            conf=effective_conf,
            nms=effective_nms,
            max_det=effective_max_det,
            max_images=args.max_images,
            adb_serial=(
                None if effective_adb_serial in (None, "") else str(effective_adb_serial)
            ),
            qnn_lib=str(effective_qnn_lib),
        )
    except (
        FileNotFoundError,
        PermissionError,
        ValueError,
        KeyError,
        RuntimeError,
        OSError,
    ) as exc:
        raise SystemExit(f"[error] {exc}") from exc
    print(f"[ok] wrote: {effective_output_text}")


def _run_test_mode(args: argparse.Namespace, config: dict) -> None:
    from tool.inference import run_test_inference_adb

    effective_model = _require_cli_or_saved(
        args.model,
        config["test"].get("model"),
        "test requires --model (INT .tflite)",
        "test",
    )
    effective_yaml = _require_cli_or_saved(
        args.yaml, config["test"].get("yaml"), "test requires --yaml", "test"
    )
    effective_images = _require_cli_or_saved(
        args.images, config["test"].get("images"), "test requires --images", "test"
    )

    effective_output = resolve_default_test_output_path(args.output)
    effective_conf = (
        args.conf
        if args.conf is not None
        else YOLOV26_TEST_DEFAULTS["conf_thres"]
    )
    effective_nms = (
        args.nms if args.nms is not None else YOLOV26_TEST_DEFAULTS["iou_thres"]
    )
    effective_topk = (
        args.topk if args.topk is not None else YOLOV26_TEST_DEFAULTS["topk"]
    )
    effective_max_det = (
        args.max_det
        if args.max_det is not None
        else YOLOV26_TEST_DEFAULTS["max_det"]
    )
    effective_adb_serial = _resolve_cli_or_saved(
        args.adb_serial, config["shared"].get("adb_serial")
    )
    effective_qnn_lib = _resolve_cli_or_saved(
        args.qnn_lib, config["shared"].get("qnn_lib")
    ) or DEFAULT_QNN_LIB

    try:
        run_test_inference_adb(
            model_path=effective_model,
            yaml_path=effective_yaml,
            output_dir=effective_output,
            conf_thres=effective_conf,
            iou_thres=effective_nms,
            topk=effective_topk,
            max_det=effective_max_det,
            image_dir=effective_images,
            adb_serial=(
                None if effective_adb_serial in (None, "") else str(effective_adb_serial)
            ),
            qnn_lib=str(effective_qnn_lib),
        )
    except (
        FileNotFoundError,
        PermissionError,
        ValueError,
        KeyError,
        RuntimeError,
        OSError,
    ) as exc:
        raise SystemExit(f"[error] {exc}") from exc
    print(f"[ok] wrote: {effective_output}")


def main() -> None:
    args = parse_args()
    if args.configure == "current":
        _print_saved_config()
        return
    if args.configure in {"qc", "mAP", "test"}:
        _configure_mode(args.configure)
        return

    config = _load_config()
    if args.mode == "qc":
        _run_qc_mode(args, config)
        return
    if args.mode == "mAP":
        _run_map_mode(args, config)
        return
    if args.mode == "test":
        _run_test_mode(args, config)
        return


if __name__ == "__main__":
    main()
