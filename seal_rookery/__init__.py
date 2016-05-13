import json
import os


class _SealRookery(object):
    """
    Wrapper for turning seals information into method-backed properties
    allowing the file system hits to be deferred.
    """

    def __init__(self):
        self._seals_root = None

    @property
    def seals_root(self):
        """
        Figure out the root directory of the seals, if we haven't already
        :return: string path to seals root directory
        """
        if not self._seals_root:
            self._seals_root = os.path.realpath(
                os.path.join(
                    os.path.realpath(__file__),
                    '../seals'
                )
            )
        return self._seals_root

    @property
    def seals_data(self):
        """
        Parse and return the json seals data as a dictionary
        :return: dict of seals.json data, empty dict if not found
        """
        try:
            with open(os.path.join(self.seals_root, 'seals.json'), 'r') as f:
                return json.load(f)
        except IOError:
            print 'Seals json missing or not generated yet.a' % (
            os.path.join(self.seals_root, 'seals.json'))
            return json.loads('{}')


_rookery = _SealRookery()
seals_data = _rookery.seals_data
seals_root = _rookery.seals_root
