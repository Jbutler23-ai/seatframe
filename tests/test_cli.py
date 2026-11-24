import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from tests.test_geometry import synthetic_arena


ROOT = Path(__file__).resolve().parents[1]
SVG_NAMESPACE = {"svg": "http://www.w3.org/2000/svg"}


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "arena.json"
        self.source.write_text(json.dumps(synthetic_arena()), encoding="utf-8")

    def run_cli(self, output, *extra):
        return subprocess.run(
            [sys.executable, "-m", "seatframe", str(self.source), "--section", "101",
             "--row", "4", "--seat", "8", "--output", str(output), *map(str, extra)],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=30,
        )

    def test_game_and_concert_svg_views_preserve_the_same_seat_camera(self):
        before = self.source.read_bytes()
        metadata = {}
        contents = {}
        for layout in ("game", "concert"):
            output = self.root / f"{layout}.svg"
            result = self.run_cli(output, "--layout", layout)
            self.assertEqual(result.returncode, 0, result.stderr)
            root = ET.parse(output).getroot()
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
            element = root.find("svg:metadata", SVG_NAMESPACE)
            self.assertIsNotNone(element)
            metadata[layout] = json.loads(element.text)
            self.assertIs(metadata[layout]["synthetic"], True)
            self.assertEqual(metadata[layout]["layout"], layout)
            self.assertEqual((metadata[layout]["section"], metadata[layout]["row"], metadata[layout]["seat"]),
                             (101, 4, 8))
            self.assertEqual(metadata[layout]["viewport"], [960, 540])
            self.assertIn("FICTIONAL GEOMETRY", " ".join(root.itertext()).upper())
            contents[layout] = output.read_text(encoding="utf-8")
        self.assertEqual(metadata["game"]["eye"], metadata["concert"]["eye"])
        self.assertEqual(metadata["game"]["target"], metadata["concert"]["target"])
        self.assertEqual(metadata["game"]["vertical_fov_degrees"], metadata["concert"]["vertical_fov_degrees"])
        for actual, expected in zip(metadata["game"]["eye"], (-0.26, -20.55, 3.55)):
            self.assertAlmostEqual(actual, expected, places=11)
        self.assertNotEqual(contents["game"], contents["concert"])
        self.assertEqual(self.source.read_bytes(), before)

    def test_existing_output_and_source_are_never_overwritten(self):
        output = self.root / "existing.svg"
        output.write_bytes(b"keep existing output")
        result = self.run_cli(output)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(output.read_bytes(), b"keep existing output")
        before = self.source.read_bytes()
        result = self.run_cli(self.source)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.source.read_bytes(), before)

    def test_invalid_requests_and_malformed_input_create_no_output(self):
        output = self.root / "invalid.svg"
        for extra in (("--row", "0"), ("--section", "999"), ("--fov", "nan")):
            with self.subTest(extra=extra):
                result = self.run_cli(output, *extra)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse(output.exists())
        missing = self.root / "missing" / "view.svg"
        result = self.run_cli(missing)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(missing.parent.exists())
        self.source.write_text('{"version":1,"version":1}', encoding="utf-8")
        result = self.run_cli(output)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
