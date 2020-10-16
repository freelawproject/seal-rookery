#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import subprocess
import unittest
from os import cpu_count

import six
from unittest.mock import patch

from seal_rookery import convert_images


def make_global_args(arguments=[]):
    parser = argparse.ArgumentParser(prog="update-seals")
    parser.add_argument(
        "-f",
        dest="forced",
        default=False,
        action="store_true",
        help="force seal update or regeneration",
    )
    parser.add_argument(
        "-v",
        dest="verbose",
        default=0,
        action="count",
        help="turn on verbose seal generation messages",
    )
    parser.add_argument(
        "-j",
        dest="numprocs",
        type=int,
        default=cpu_count(),
        help="Use multiple processes to convert images.",
    )
    args = parser.parse_args(arguments)
    return args


class PackagingTests(unittest.TestCase):
    """
    Some simple tests to make sure the package works. Does not test functionality.
    """

    def test_does_not_break_cl(self):
        """
        Can we do some import statements like in the CL project? Test if we
        are about to break Courtlistener.
        """
        try:
            # currently from courtlistener.cl.scrapers.tasks
            from seal_rookery import seals_data, seals_root

            self.assertTrue(seals_data["ca1"]["has_seal"])

        except ImportError as e:
            self.fail("Couldn't import seals_data and seals_root like in CL")

    @patch("seal_rookery.convert_images.args", make_global_args([]))
    def test_base_initialization(self):
        """
        Simple test of calling convert_images to make sure things are wired.
        """
        try:
            convert_images.convert_images()
        except Exception as e:
            self.fail("Failed to call convert_images(): %s" % (e,))


class SealGenerationTest(unittest.TestCase):
    """
    Test the ability to generate seals.
    """

    def setUp(self):
        from seal_rookery import seals_data

        hashes = 0
        for seal in seals_data:
            if seals_data[seal]["has_seal"]:
                hashes = hashes + 1
        self.hashes = hashes
        self.total_seals = len(seals_data)
        self.assertTrue(self.hashes > 0)
        self.assertTrue(self.total_seals > 0)

    def test_can_force_regeneration_of_seals(self):
        """
        Test we can force image conversions from the originals
        :return:
        """
        with patch("seal_rookery.convert_images.args", make_global_args([])):
            changed, skipped = convert_images.convert_images()
            self.assertEqual(0, changed, "Without forcing, nothing changes.")

        with patch(
            "seal_rookery.convert_images.args", make_global_args(["-f"])
        ):
            prev_skipped = skipped
            changed, skipped = convert_images.convert_images()
            self.assertEqual(
                prev_skipped, changed, "Forcing regens all hashes."
            )
            self.assertEqual(0, skipped, "Forcing should skip nothing.")

    def test_convert_images_tool_accepts_args(self):
        """
        Test we can pass command line args to the update-seals script.

        Expected output looks like:
            Updating seals: 1 of 249
            ...
            Updating seals: 249 of 249
            Done:
              0 seals updated
              249 seals skipped
            (0, 249)
        :return:
        """
        import re

        updated_pattern = re.compile("(\d+) seals updated")
        skipped_pattern = re.compile("(\d+) seals skipped")

        # run a forced update
        results = subprocess.run(["update-seals", "-f"], capture_output=True)

        changed, skipped = (
            int(updated_pattern.findall(str(results))[0]),
            int(skipped_pattern.findall(str(results))[0]),
        )

        self.assertTrue(changed > 0)
        self.assertTrue(skipped == 0)
        self.assertEqual(0, results.returncode)

        # run a regular update, which should just skip seals just generated
        results = subprocess.run(["update-seals"], capture_output=True)

        changed, skipped = (
            int(updated_pattern.findall(str(results))[0]),
            int(skipped_pattern.findall(str(results))[0]),
        )
        self.assertTrue(changed == 0)
        self.assertTrue(skipped > 0)
        self.assertEqual(0, results.returncode)

    @patch("sys.stdout", new_callable=six.StringIO)
    def test_bad_command_line_args_raise_systemexit(self, mock_stdout):
        """test that garbage input raises SystemExit"""

        with self.assertRaises(SystemExit):
            convert_images.main(argv=["garbage"])

    @patch("sys.stdout", new_callable=six.StringIO)
    @patch("seal_rookery.convert_images.convert_images")
    def test_failure_in_convert_images_returns_non_zero(
        self, mock_convert, mock_stdout
    ):
        """
        Test that any failure in the conversion routine will result in a
        non-zero return code from the interpreter.
        """
        return_code = convert_images.main(argv=[])
        self.assertEqual(1, return_code)
        self.assertTrue("Failed to update seals!" in mock_stdout.getvalue())


class CommandLineTests(unittest.TestCase):
    def test_convert_images_tool_accepts_args(self):
        """
        Test we can pass command line args to the update-seals script.

        Expected output looks like:
            Updating seals: 1 of 249
            ...
            Updating seals: 249 of 249
            Done:
              0 seals updated
              249 seals skipped
            (0, 249)
        :return:
        """
        import re

        updated_pattern = re.compile("(\d+) seals updated")
        skipped_pattern = re.compile("(\d+) seals skipped")

        # run a forced update
        results = subprocess.run(["update-seals", "-f"], capture_output=True)

        changed, skipped = (
            int(updated_pattern.findall(str(results))[0]),
            int(skipped_pattern.findall(str(results))[0]),
        )

        self.assertTrue(changed > 0)
        self.assertTrue(skipped == 0)
        self.assertEqual(0, results.returncode)

        # run a regular update, which should just skip seals just generated
        results = subprocess.run(["update-seals"], capture_output=True)

        changed, skipped = (
            int(updated_pattern.findall(str(results))[0]),
            int(skipped_pattern.findall(str(results))[0]),
        )
        self.assertTrue(changed == 0)
        self.assertTrue(skipped > 0)
        self.assertEqual(0, results.returncode)


if __name__ == "__main__":
    unittest.main()
