#!/usr/bin/env python
import hashlib
import json
import os
import sys
import subprocess
from seal_rookery import seals_root, seals_data

ORIG_DIR = os.path.join(seals_root, 'orig')


def get_old_hash(img):
    """Get the old hash from seals.json"""
    try:
        old_hash = seals_data[img.split('.')[0]]['hash']
    except KeyError:
        old_hash = None
    return old_hash


def get_hash_from_file(img):
    """Get the hash from the current file"""
    with open(img, 'r') as f:
        return hashlib.sha256(f.read()).hexdigest()


def set_new_hash(court_id, new_hash):
    """Update the json object with new values"""
    seals_data[court_id]['hash'] = new_hash


def convert_images():
    for image in os.listdir(ORIG_DIR):
        print "\nProcessing: %s" % image
        court_id = image.split('.')[0]
        final_name = '%s.png' % court_id
        path_to_orig = os.path.join(ORIG_DIR, image)

        current_hash = get_hash_from_file(path_to_orig)
        old_hash = get_old_hash(path_to_orig)

        if current_hash != old_hash:
            # Update the hash
            set_new_hash(court_id, current_hash)

            # Regenerate the images
            for size in ['128', '256', '512', '1024']:
                print "  - Making {size}x{size} image...".format(size=size)
                path_to_output = '%s/%s/%s' % \
                                 (seals_root, size, final_name)
                print '    - writing to %s' % (path_to_output,)
                command = [
                    'convert',
                    '-resize',
                    '%sx%s' % (size, size),
                    '-background',
                    'transparent',
                    path_to_orig,
                    path_to_output,
                ]
                subprocess.Popen(command, shell=False).communicate()
        else:
            print ' - Unchanged hash, moving on.'


def save_new_json():
    """Update the JSON object on disk."""
    json.dump(
        seals_data,
        open(os.path.join(seals_root, 'seals.json'), 'w'),
        sort_keys=True,
        indent=4,
    )


def main(argv=None):
    convert_images()
    save_new_json()


if __name__ == '__main__':
    main(sys.argv)
