#!/bin/bash

SUBJDIR="$1"
if [[ ! -d "$SUBJDIR" ]]; then
    exit 1
fi

VOXMOM="$SUBJDIR/VOX_coords_mother.txt"
JSON="$SUBJDIR/voxel_coordinates.json"
python vox_mom_to_json.py "$VOXMOM" "$JSON"
SCAN=$SUBJDIR/*.nii.gz

./launch_pyloc.py --ct $SCAN --leads leads.yml --coords "$JSON"
