#!/usr/bin/env python
import os
import shutil
import sys
import urllib2
import tarfile
from seal_rookery import seals_root

PROJECT_NAME = 'seal-rookery'


def download(url):
    """
    Download the tarball at url
    :param url: url to the tarball
    :return: path to downloaded file
    """
    file_path = os.path.join(seals_root, url.split('/')[-1])
    r = urllib2.urlopen(url)
    chunk_size = 1024 * 1024
    with open(file_path, 'wb') as f:
        chunk = r.read(chunk_size)
        while chunk:
            f.write(chunk)
            chunk = r.read(chunk_size)
            sys.stdout.write('.')
            sys.stdout.flush()
        sys.stdout.write('.done\n')
    return file_path


def seal_files(members):
    for tarinfo in members:
        ext = os.path.splitext(tarinfo.name)[1]
        if ext == '.png' or ext == '.json':
            yield tarinfo


if __name__ == '__main__':
    print 'Attempting to download seals to seals_root: ' + seals_root
    url = sys.argv[1]

    print '[Downloading: %s] ' % (url,)
    filename = download(url)
    tar = tarfile.open(name=filename, mode='r:gz')

    print 'Extracting seals...'
    tar.extractall(seals_root, members=seal_files(tar))
    tar.close()

    print 'Moving seals...'
    extract = '%s-%s' % (PROJECT_NAME, url.split('/')[-1].split('.tar.gz')[0])
    print '...extract: ' + extract
    walk_dir = os.path.join(seals_root, extract, 'seals')
    for dir_name, dir_names, file_names\
            in os.walk(walk_dir):
        for subdir in dir_names:
            src_path = os.path.join(dir_name, subdir)
            shutil.move(src_path, os.path.join(seals_root, subdir))
    shutil.copy(os.path.join(walk_dir, 'seals.json'), seals_root)

    try:
        print 'Cleaning up...'
        os.remove(filename)
        shutil.rmtree(os.path.join(seals_root, extract))
    except IOError:
        print 'Unable to delete seals tarfile: %s' % (tarfile,)

