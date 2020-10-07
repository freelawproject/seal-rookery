#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from mock import patch
import six

from seal_rookery import convert_images


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
        changed, skipped = convert_images.convert_images()
        self.assertEqual(0, changed, "Without forcing, nothing changes.")

        prev_skipped = skipped
        changed, skipped = convert_images.convert_images(forced=True)
        self.assertEqual(prev_skipped, changed, "Forcing regens all hashes.")
        self.assertEqual(0, skipped, "Forcing should skip nothing.")

    @patch("sys.stdout", new_callable=six.StringIO)
    def test_convert_images_tool_accepts_args(self, mock_stdout):
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
        return_code = convert_images.main(
            argv=[
                "-f",
            ]
        )
        results = mock_stdout.getvalue()

        changed, skipped = (
            int(updated_pattern.findall(results)[0]),
            int(skipped_pattern.findall(results)[0]),
        )

        self.assertTrue(changed > 0)
        self.assertTrue(skipped == 0)
        self.assertEqual(0, return_code)

        # reset the mock stdout buffer
        mock_stdout.seek(0)

        # run a regular update, which should just skip seals just generated
        return_code = convert_images.main(argv=[])
        results = mock_stdout.getvalue()

        changed, skipped = (
            int(updated_pattern.findall(results)[0]),
            int(skipped_pattern.findall(results)[0]),
        )
        self.assertTrue(changed == 0)
        self.assertTrue(skipped > 0)
        self.assertEqual(0, return_code)

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


if __name__ == "__main__":
    unittest.main()
