#!/usr/bin/env python

import unittest


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

            self.assertIsNotNone(seals_root)

        except ImportError:
            self.fail("Couldn't import seals_data and seals_root like in CL")


if __name__ == "__main__":
    unittest.main()
