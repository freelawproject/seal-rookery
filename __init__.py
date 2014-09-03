import json
import os

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'seals.json')) as f:
    seals_data = json.load(f)
