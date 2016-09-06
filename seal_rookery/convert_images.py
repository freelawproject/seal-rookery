#!/usr/bin/env python
import argparse
import hashlib
import json
import os
import subprocess
import sys

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
    with open(img, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def set_new_hash(court_id, new_hash):
    """Update the json object with new values"""
    seals_data[court_id]['hash'] = new_hash


def convert_images(verbose=False, forced=False):
    """
    Convert the original seal images to their different scaled outputs for
    use either in CourtListener or another application.

    :param verbose: if True, provides detailed conversion feedback to stdout
    :param forced: if True, ignores unchanged hashes and regenerates images
    :return: tuple (number changed, number skipped)
    """
    images = os.listdir(ORIG_DIR)
    num_images = len(images)
    num_changed = 0
    num_skipped = 0
    for i, image in enumerate(images, 1):
        if verbose:
            sys.stdout.write(u"\nProcessing: %s" % image)
        else:
            sys.stdout.write(u'\rUpdating seals: %s of %s' % (i, num_images))
            sys.stdout.flush()
        court_id = image.split('.')[0]
        final_name = '%s.png' % court_id
        path_to_orig = os.path.join(ORIG_DIR, image)

        current_hash = get_hash_from_file(path_to_orig)
        old_hash = get_old_hash(image)

        if current_hash != old_hash or forced:
            # Update the hash
            set_new_hash(court_id, current_hash)

            # Regenerate the images
            for size in ['128', '256', '512', '1024']:
                if verbose:
                    sys.stdout.write(u"  - Making {size}x{size} image...".format(
                        size=size
                    ))
                path_to_output = '%s/%s/%s' % (seals_root, size, final_name)
                if verbose:
                    sys.stdout.write(
                        u'    - writing to %s' % (path_to_output,)
                    )
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
            num_changed += 1
        else:
            if verbose:
                sys.stdout.write(u' - Unchanged hash, moving on.')
            num_skipped += 1

    if not verbose:
        sys.stdout.write(
            u"\nDone:\n  %s seals updated\n  %s seals skipped\n" % (
                num_changed,
                num_skipped,
            ))

    return num_changed, num_skipped

def save_new_json():
    """Update the JSON object on disk."""
    json.dump(
        seals_data,
        open(os.path.join(seals_root, 'seals.json'), 'w'),
        sort_keys=True,
        indent=4,
    )


def main(argv=None):
    """
    Main function and entry point for console script
    :param argv: list of command line args, probably from sys.argv
    :return: tuple (number of changed images, number of skipped images)
    """
    # when running as a console_script via setuptools, no args are passed,
    # so we need to try grabbing sys.argv
    parser = argparse.ArgumentParser(prog='update-seals')
    parser.add_argument('-f',
                        action='count',
                        help='force seal update or regeneration')
    parser.add_argument('-v',
                        action='count',
                        help='turn on verbose seal generation messages')

    args = parser.parse_args(argv)
    changed, skipped = convert_images(
        verbose=bool(args.v), forced=bool(args.f)
    )

    save_new_json()

    return changed, skipped


if __name__ == '__main__':
    main(sys.argv)
