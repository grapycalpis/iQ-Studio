import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import MagicMock, patch


CLI_PATH = Path(__file__).resolve().parent.parent / "cli.py"
CLI_SPEC = importlib.util.spec_from_file_location("cv_cli", CLI_PATH)
cli = importlib.util.module_from_spec(CLI_SPEC)
assert CLI_SPEC.loader is not None
CLI_SPEC.loader.exec_module(cli)


class CliParseTests(unittest.TestCase):
    def test_help_includes_configure_and_omits_removed_flags(self) -> None:
        buf = io.StringIO()
        with patch.object(sys, "argv", ["cli.py", "--help"]):
            with redirect_stdout(buf), self.assertRaises(SystemExit) as exc:
                cli.parse_args()

        self.assertEqual(exc.exception.code, 0)
        help_text = buf.getvalue()
        self.assertIn("--configure", help_text)
        self.assertNotIn("--type", help_text)
        self.assertNotIn("  --adb ", help_text)
        self.assertNotIn("  --image ", help_text)
        self.assertNotIn("--fp-head", help_text)
        self.assertNotIn("--qc-head", help_text)

    def test_mode_and_configure_are_mutually_exclusive(self) -> None:
        with patch.object(sys, "argv", ["cli.py", "--mode", "qc", "--configure", "qc"]):
            with self.assertRaises(SystemExit) as exc:
                cli.parse_args()

        self.assertEqual(exc.exception.code, 2)

    def test_removed_type_flag_is_rejected(self) -> None:
        with patch.object(
            sys,
            "argv",
            ["cli.py", "--mode", "qc", "--type", "yolov26", "--model", "m.pt"],
        ):
            with self.assertRaises(SystemExit) as exc:
                cli.parse_args()

        self.assertEqual(exc.exception.code, 2)


class CliConfigureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.tmpdir.name) / "config.json"
        self.model_pt = Path(self.tmpdir.name) / "model.pt"
        self.model_pt.write_text("pt", encoding="utf-8")
        self.model_tflite = Path(self.tmpdir.name) / "model.tflite"
        self.model_tflite.write_text("tflite", encoding="utf-8")
        self.alt_model_tflite = Path(self.tmpdir.name) / "alt_model.tflite"
        self.alt_model_tflite.write_text("alt", encoding="utf-8")
        self.yaml_file = Path(self.tmpdir.name) / "coco.yaml"
        self.yaml_file.write_text("names: []", encoding="utf-8")
        self.ann_file = Path(self.tmpdir.name) / "ann.json"
        self.ann_file.write_text("{}", encoding="utf-8")
        self.image_dir = Path(self.tmpdir.name) / "images"
        self.image_dir.mkdir()
        self.calib_dir = Path(self.tmpdir.name) / "calib"
        self.calib_dir.mkdir()

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_configure_qc_saves_json(self) -> None:
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            sys, "argv", ["cli.py", "--configure", "qc"]
        ), patch(
            "builtins.input",
            side_effect=[str(self.model_pt), str(self.calib_dir)],
        ):
            cli.main()

        saved = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["qc"]["model"], str(self.model_pt.resolve()))
        self.assertEqual(saved["qc"]["calib_dir"], str(self.calib_dir.resolve()))

    def test_configure_current_prints_saved_config(self) -> None:
        self.config_path.write_text(
            json.dumps(
                {
                    "qc": {"model": "/tmp/model.pt"},
                    "mAP": {},
                    "test": {},
                    "shared": {"adb_serial": "device123"},
                }
            ),
            encoding="utf-8",
        )
        buf = io.StringIO()
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            sys, "argv", ["cli.py", "--configure", "current"]
        ), redirect_stdout(buf):
            cli.main()

        output = buf.getvalue()
        self.assertIn("saved config", output)
        self.assertIn("device123", output)

    def test_configure_qc_can_keep_existing_paths(self) -> None:
        self.config_path.write_text(
            json.dumps(
                {
                    "qc": {
                        "model": str(self.model_pt.resolve()),
                        "calib_dir": str(self.calib_dir.resolve()),
                    },
                    "mAP": {},
                    "test": {},
                    "shared": {},
                }
            ),
            encoding="utf-8",
        )
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            sys, "argv", ["cli.py", "--configure", "qc"]
        ), patch(
            "builtins.input",
            side_effect=["y", "y"],
        ):
            cli.main()

        saved = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["qc"]["model"], str(self.model_pt.resolve()))
        self.assertEqual(saved["qc"]["calib_dir"], str(self.calib_dir.resolve()))

    def test_configure_qc_existing_path_requires_explicit_yes_no(self) -> None:
        self.config_path.write_text(
            json.dumps(
                {
                    "qc": {
                        "model": str(self.model_pt.resolve()),
                        "calib_dir": str(self.calib_dir.resolve()),
                    },
                    "mAP": {},
                    "test": {},
                    "shared": {},
                }
            ),
            encoding="utf-8",
        )
        buf = io.StringIO()
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            sys, "argv", ["cli.py", "--configure", "qc"]
        ), patch(
            "builtins.input",
            side_effect=["", "y", "y"],
        ), redirect_stdout(buf):
            cli.main()

        output = buf.getvalue()
        self.assertIn("existing the QC model file (.pt) path:", output)
        self.assertIn(str(self.model_pt.resolve()), output)
        self.assertIn("[error] enter y or n", output)

    def test_configure_map_with_zero_devices_keeps_existing_serial(self) -> None:
        self.config_path.write_text(
            json.dumps(
                {
                    "qc": {},
                    "mAP": {},
                    "test": {},
                    "shared": {"adb_serial": "keepme"},
                }
            ),
            encoding="utf-8",
        )
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            cli, "_list_authorized_adb_devices", return_value=[]
        ), patch.object(
            sys, "argv", ["cli.py", "--configure", "mAP"]
        ), patch(
            "builtins.input",
            side_effect=[
                str(self.ann_file),
                str(self.image_dir),
                str(self.model_pt),
                str(self.model_tflite),
            ],
        ):
            cli.main()

        saved = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["shared"]["adb_serial"], "keepme")

    def test_configure_test_with_one_device_can_replace_existing_serial(self) -> None:
        self.config_path.write_text(
            json.dumps(
                {
                    "qc": {},
                    "mAP": {},
                    "test": {},
                    "shared": {"adb_serial": "old-device"},
                }
            ),
            encoding="utf-8",
        )
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            cli, "_list_authorized_adb_devices", return_value=["device123"]
        ), patch.object(
            sys, "argv", ["cli.py", "--configure", "test"]
        ), patch(
            "builtins.input",
            side_effect=[
                str(self.model_tflite),
                str(self.yaml_file),
                str(self.image_dir),
                "n",
                "device123",
            ],
        ):
            cli.main()

        saved = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["shared"]["adb_serial"], "device123")

    def test_configure_test_with_multiple_devices_uses_existing_when_accepted(self) -> None:
        self.config_path.write_text(
            json.dumps(
                {
                    "qc": {},
                    "mAP": {},
                    "test": {},
                    "shared": {"adb_serial": "device2"},
                }
            ),
            encoding="utf-8",
        )
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            cli, "_list_authorized_adb_devices", return_value=["device1", "device2"]
        ), patch.object(
            sys, "argv", ["cli.py", "--configure", "test"]
        ), patch(
            "builtins.input",
            side_effect=[
                str(self.model_tflite),
                str(self.yaml_file),
                str(self.image_dir),
                "y",
            ],
        ):
            cli.main()

        saved = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["shared"]["adb_serial"], "device2")

    def test_configure_test_with_multiple_devices_reprompts_until_valid_serial(self) -> None:
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            cli, "_list_authorized_adb_devices", return_value=["device1", "device2"]
        ), patch.object(
            sys, "argv", ["cli.py", "--configure", "test"]
        ), patch(
            "builtins.input",
            side_effect=[
                str(self.model_tflite),
                str(self.yaml_file),
                str(self.image_dir),
                "bad-device",
                "device2",
            ],
        ):
            cli.main()

        saved = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["shared"]["adb_serial"], "device2")


class CliDispatchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.tmpdir.name) / "config.json"

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_qc_dispatch_uses_saved_config(self) -> None:
        self.config_path.write_text(
            json.dumps(
                {
                    "qc": {"model": "/saved/model.pt", "calib_dir": "/saved/calib"},
                    "mAP": {},
                    "test": {},
                    "shared": {},
                }
            ),
            encoding="utf-8",
        )
        pipe = MagicMock()
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            cli, "YoloV26Pipeline", return_value=pipe
        ), patch.object(
            sys,
            "argv",
            ["cli.py", "--mode", "qc", "--output", "/tmp/out.tflite"],
        ):
            cli.main()

        pipe.quantize_convert.assert_called_once_with(
            model_path="/saved/model.pt",
            out_tflite="/tmp/out.tflite",
            calib_dir="/saved/calib",
            max_calib=200,
            qc_head="one2many",
            qc_quant_scheme="mse",
        )

    def test_map_dispatch_uses_saved_config_and_shared_runtime_knobs(self) -> None:
        self.config_path.write_text(
            json.dumps(
                {
                    "qc": {},
                    "mAP": {
                        "annotations": "/saved/ann.json",
                        "images": "/saved/images",
                        "fp_model": "/saved/model.pt",
                        "int_model": "/saved/model.tflite",
                    },
                    "test": {},
                    "shared": {
                        "adb_serial": "saved-device",
                        "qnn_lib": "/saved/libQnn.so",
                    },
                }
            ),
            encoding="utf-8",
        )
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            cli, "run_fp_int_pair_map_eval"
        ) as runner, patch.object(
            sys,
            "argv",
            ["cli.py", "--mode", "mAP", "--output_text", "/tmp/report.txt"],
        ):
            cli.main()

        runner.assert_called_once_with(
            fp_model="/saved/model.pt",
            int_model="/saved/model.tflite",
            annotations="/saved/ann.json",
            images="/saved/images",
            output_text="/tmp/report.txt",
            conf=0.25,
            nms=0.7,
            max_det=300,
            max_images=300,
            adb_serial="saved-device",
            qnn_lib="/saved/libQnn.so",
        )

    def test_test_mode_cli_paths_override_saved_config(self) -> None:
        self.config_path.write_text(
            json.dumps(
                {
                    "qc": {},
                    "mAP": {},
                    "test": {
                        "model": "/saved/model.tflite",
                        "yaml": "/saved/coco.yaml",
                        "images": "/saved/images",
                    },
                    "shared": {"adb_serial": "saved-device"},
                }
            ),
            encoding="utf-8",
        )
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch(
            "tool.inference.run_test_inference_adb"
        ) as runner, patch.object(
            sys,
            "argv",
            [
                "cli.py",
                "--mode",
                "test",
                "--images",
                "/cli/images",
                "--adb-serial",
                "cli-device",
                "--out",
                "/tmp/outdir",
            ],
        ):
            cli.main()

        runner.assert_called_once_with(
            model_path="/saved/model.tflite",
            yaml_path="/saved/coco.yaml",
            output_dir="/tmp/outdir",
            conf_thres=0.25,
            iou_thres=0.6,
            topk=300,
            max_det=100,
            image_dir="/cli/images",
            adb_serial="cli-device",
            qnn_lib="/usr/lib/libQnnTFLiteDelegate.so",
        )

    def test_missing_required_error_mentions_configure_mode(self) -> None:
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            sys, "argv", ["cli.py", "--mode", "test"]
        ):
            with self.assertRaises(SystemExit) as exc:
                cli.main()

        self.assertEqual(
            str(exc.exception),
            "[error] test requires --model (INT .tflite) or run: python3 cli.py --configure test",
        )

    def test_invalid_config_json_is_rejected(self) -> None:
        self.config_path.write_text("{bad json", encoding="utf-8")
        with patch.object(cli, "CONFIG_PATH", self.config_path), patch.object(
            sys, "argv", ["cli.py", "--mode", "qc"]
        ):
            with self.assertRaises(SystemExit) as exc:
                cli.main()

        self.assertEqual(
            str(exc.exception),
            "[error] config.json is invalid. Re-run --configure <mode>.",
        )


if __name__ == "__main__":
    unittest.main()
