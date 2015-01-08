import hashlib
import json
import os
import subprocess

seals_json = json.load(open('seals.json', 'r'))

operating_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.join(operating_directory, 'orig'))


def get_old_hash(img):
    """Get the hash from seals.json"""
    try:
        hash = seals_json[img.split('.')[0]]['hash']
    except KeyError:
        hash = None
    return hash


def get_hash_from_file(img):
    """Get the hash from the current file"""
    with open(img, 'r') as f:
        return hashlib.sha256(f.read()).hexdigest()


def set_new_hash(court_id, hash):
    """Update the json object with new values"""
    seals_json[court_id]['hash'] = hash


def convert_images():
    for image in os.listdir('.'):
        print "Processing: %s" % image
        court_id = image.split('.')[0]
        final_name =  '%s.png' % court_id
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
                print "done."


def save_new_json():
    """Update the JSON object on disk."""
    json.dump(seals_json, '../seals.json', sort_keys=True)

if __name__ == '__main__':
    convert_images()
    save_new_json()
