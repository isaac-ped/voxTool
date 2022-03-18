#! /usr/bin/env python

__author__ = 'iped'
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
from view.pyloc import PylocControl
import yaml
import argparse

def launch():
    parser = argparse.ArgumentParser(
        "PyLoc",
        description="Extract electrode coordinates from thresholded CT images"
    )
    parser.add_argument(
        "--ct", 
    )
    parser.add_argument(
        "--leads"
    )
    parser.add_argument(
        "--coords"
    )
    args = parser.parse_args()
    
    config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml')))
    controller = PylocControl(config)
    if args.ct is not None:
        controller.load_ct(args.ct)
        
    if args.leads is not None:
        with open(args.leads) as f:
            leads = yaml.load(f)
        
        labels = [lead['label'] for lead in leads]
        types = [lead['type'] for lead in leads]
        dimensions = [(lead['x'], lead['y']) for lead in leads]
        spacings = [config['lead_types'][lead_type]['spacing'] for lead_type in types]
        radii = [config['lead_types'][lead_type]['radius'] for lead_type in types]
        micros = [config['micros'][str(l.get('micro',' None'))] for l in leads]
        controller.set_leads(labels, types, dimensions, radii, spacings,micros)
        

    if args.coords is not None:
        controller.load_coordinate_file(args.coords)
        
    controller.exec_()


if __name__ == '__main__':
    launch()