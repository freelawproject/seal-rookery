#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
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
            self.fail("Coudln't import seals_data and seals_root like in CL")

    def test_base_initialization(self):
        """
        Simple test of calling convert_images to make sure things are wired.
        """
        try:
            convert_images.convert_images()
        except Exception as e:
            self.fail('Failed to call convert_images(): %s' % (e,))


if __name__ == '__main__':
    unittest.main()
