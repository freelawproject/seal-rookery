import json
import os

seals_root = os.path.realpath(
    os.path.join(
        os.path.realpath(__file__),
        '../seals'
    )
)

try:
    with open(os.path.join(seals_root, 'seals.json'), 'r') as f:
        seals_data = json.load(f)
except IOError:
    print 'Seals json missing at %s' % (os.path.join(seals_root, 'seals.json'))
    seals_data = json.loads('{}')
