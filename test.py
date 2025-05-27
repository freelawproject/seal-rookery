import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest import mock

from seal_rookery import _SealRookery, seals_data, seals_root


class SealsDataTests(unittest.TestCase):
    @mock.patch("seal_rookery.open", side_effect=FileNotFoundError)
    def test_data_missing(self, _mock_open):
        out = StringIO()
        rookery = _SealRookery()

        with mock.patch.object(sys, "stdout", new=out):
            data = rookery.seals_data

        self.assertEqual(data, {})
        output = out.getvalue()
        self.assertTrue(
            output.startswith("Seals json missing or not generated yet: ")
        )

    def test_success(self):
        self.assertEqual(
            seals_data["ca1"],
            {
                "has_seal": True,
                "hash": "9cf025a005123030a5adb005c1eb6bf2e6a7de10a1e21f85f48812c85e7e92b0",
                "name": "Court of Appeals for the First Circuit",
                "notes": "Completed as part of initial version.",
            },
        )


class SealsRootTests(unittest.TestCase):
    def test_seals_root(self):
        self.assertIsInstance(seals_root, str)
        path = Path(seals_root)
        self.assertTrue(path.exists())
        self.assertTrue(path.is_dir())
        ca1_svg = path / "orig/ca1.svg"
        self.assertTrue(ca1_svg.exists())
        self.assertGreater(ca1_svg.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
