import os
import subprocess

operating_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.join(operating_directory, 'orig'))

for image in os.listdir('.'):
    print "Processing: %s" % image
    final_name = image.split('.')[0] + '.png'
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
