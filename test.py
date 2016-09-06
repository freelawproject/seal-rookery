#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from mock import patch
from StringIO import StringIO
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
            self.assertTrue(seals_data['ca1']['has_seal'])

        except ImportError as e:
            self.fail("Couldn't import seals_data and seals_root like in CL")

    def test_base_initialization(self):
        """
        Simple test of calling convert_images to make sure things are wired.
        """
        try:
            convert_images.convert_images()
        except Exception as e:
            self.fail('Failed to call convert_images(): %s' % (e,))


class SealGenerationTest(unittest.TestCase):
    """
    Test the ability to generate seals.
    """

    def setUp(self):
        from seal_rookery import seals_data
        hashes = 0
        for seal in seals_data:
            if seals_data[seal]['has_seal']:
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
        self.assertEquals(0, changed, 'Without forcing, nothing changes.')

        prev_skipped = skipped
        changed, skipped = convert_images.convert_images(forced=True)
        self.assertEquals(prev_skipped, changed, 'Forcing regens all hashes.')
        self.assertEquals(0, skipped, 'Forcing should skip nothing.')

    @patch('sys.stdout', new_callable=StringIO)
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
        changed, skipped = convert_images.main(argv=['-f',])
        results = mock_stdout.buflist[-1]
        self.assertTrue(changed > 0)
        self.assertTrue(skipped == 0)
        self.assertTrue(('%s seals updated' % (changed,)) in results)
        self.assertTrue(('%s seals skipped' % (skipped,)) in results)

        changed, skipped = convert_images.main()
        results = mock_stdout.buflist[-1]
        self.assertTrue(('%s seals updated' % (changed,)) in results)
        self.assertTrue(('%s seals skipped' % (skipped,)) in results)


if __name__ == '__main__':
    unittest.main()
