import re
import json

from argparse import ArgumentParser
from collections import defaultdict

parser = ArgumentParser("Convert vox mom to json")
parser.add_argument("voxmom")
parser.add_argument("json")
args = parser.parse_args()

leads = {}
with open(args.voxmom) as f:
    for line in f:
        name, x, y, z, type_, xi, yi = line.split()
        xi, yi = int(xi), int(yi)
        basename = re.sub("[0-9]", "", name)
        lead = leads.setdefault(basename, 
            {"pairs": [],
             "type": type_,
             "dimensions": [xi, yi],
             "n_groups": 1,
             "contacts": []
             }
        )
        leadnum = int(re.sub("[^0-9]", "", name))
        lead_loc = [
            leadnum / yi + 1,
            leadnum % yi + 1
        ]

        lead["contacts"].append(dict(
            lead_group=0,
            coordinate_spaces={
                "ct_voxel": {
                    "raw": [
                        int(float(x)),
                        int(float(y)),
                        int(float(z))
                    ]
                    }
                },
            lead_loc=lead_loc,
            name=name
            ))
        print(lead)

with open(args.json, 'w') as f:
    json.dump({"leads": leads}, f, indent=2)
