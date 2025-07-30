"""
WordNet model browse sample
Author: John McCrae <john@mccr.ae> for original code
Author: Bernard Bou <1313ou@gmail.com> for rewrite and revamp
"""
#  Copyright (c) 2024.
#  Creative Commons 4 for original code
#  GPL3 for rewrite

import argparse
import sys
from glob import glob
from typing import Dict

import yaml


def merge_yaml_files(output_file, files):
    merged_data = {}
    for file in files:
        with open(file) as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict):
                _deep_merge(merged_data, data)
            else:
                print("Cannot merge non dictionaries", file=sys.stderr)
    with open(output_file, 'w') as out:
        yaml.dump(merged_data, out, allow_unicode=True)


def _shallow_merge(target: Dict, source: Dict) -> Dict:
    target.update(source)
    return target


def _deep_merge(base: Dict, incoming: Dict) -> Dict:
    for key, value in incoming.items():
        if isinstance(value, dict) and key in base and isinstance(base[key], dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def main() -> None:
    arg_parser = argparse.ArgumentParser(description="browse")
    arg_parser.add_argument('in_dir', type=str, help='from-dir for yaml/pickle')
    arg_parser.add_argument('out_dir', type=str, help='out-dir for result')
    arg_parser.add_argument('syntagnet', type=str, nargs='?', default='syntagnet.yaml', help='syntagnet data')
    args = arg_parser.parse_args()

    merge_files = glob(f'{args.in_dir}/*.yaml')
    merge_files.append(args.syntagnet)
    merge_yaml_files(f'{args.out_dir}/merged.yaml', merge_files)


if __name__ == '__main__':
    main()
