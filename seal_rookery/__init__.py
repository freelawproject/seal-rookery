import json
import os

seals_root = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(seals_root, '../seals.json')) as f:
    seals_data = json.load(f)

