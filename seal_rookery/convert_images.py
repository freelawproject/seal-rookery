import hashlib
import json
import os
import subprocess

from seal_rookery import seals_root, seals_data

os.chdir(os.path.join(seals_root, 'orig'))


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
    for image in os.listdir('.'):
        print "\nProcessing: %s" % image
        court_id = image.split('.')[0]
        final_name = '%s.png' % court_id
        current_hash = get_hash_from_file(image)
        old_hash = get_old_hash(image)
        if current_hash != old_hash:
            # Update the hash
            set_new_hash(court_id, current_hash)

            # Regenerate the images
            for size in ['128', '256', '512', '1024']:
                print "  - Making {size}x{size} image...".format(size=size)
                command = [
                    'convert',
                    '-resize',
                    '%sx%s' % (size, size),
                    '-background',
                    'transparent',
                    image,
                    '../%s/%s' % (size, final_name),
                ]
                subprocess.Popen(command, shell=False).communicate()
        else:
            print ' - Unchanged hash, moving on.'


def save_new_json():
    """Update the JSON object on disk."""
    json.dump(
        seals_data,
        open('../seals.json', 'w'),
        sort_keys=True,
        indent=4,
    )

if __name__ == '__main__':
    convert_images()
    save_new_json()
