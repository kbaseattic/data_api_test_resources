#!/usr/bin/env python
"""
Rename datatypes in dumped msgpack files.
"""
import argparse
import json
import os
import sys
#
import msgpack

changeme = 'Prototype'

def warn(msg):
    sys.stderr.write('Warning: {}\n'.format(msg))

def rename_directory(dirname, new_name='', dry_run=False):
    """Rename all files in a directory, `d`.
    Return number of things renamed.
    """
    rename = 0
    for fname in os.listdir(dirname):
        path = os.path.join(dirname, fname)
        if not os.path.isfile(path):
            continue
        try:
            f = open(path)
        except:
            warn('skipping file "{}", cannot open for reading'.format(path))
            continue
        try:
            obj = msgpack.load(f)
        except:
            warn('skipping file "{}", msgpack decoding failed'.format(path))
            continue
        f.close()
        orig_type = obj['type']
        if changeme not in orig_type:
            continue
        try:
            ws, rest = orig_type.split('.', 1)
        except ValueError:
            warn('skipping file "{}", type name "{}" has no workspace part'.format(path, orig_type))
        try:
            name, version = rest.split('-', 1)
        except ValueError:
            warn('skipping file "{}", type name "{}" has no version part'.format(path, rest))
        new_type = new_name + '.' + name + '-1.0'
        print('Renaming "{}" => "{}"'.format(orig_type, new_type))
        obj['type'] = new_type
        if not dry_run:
            with open(path, 'w') as f:
                msgpack.dump(obj, f)
        rename += 1
    return rename
    
def main():
    p = argparse.ArgumentParser(description='Rename a given type in all files in a directory')
    p.add_argument('--ns', dest='new_name', required=True, help='new namespace')
    p.add_argument('--dir', dest='directory', help='directory (default=current)', default='.')
    p.add_argument('--dry-run', '-n', dest='dry_run', action='store_true', help='just print what you would do')
    args = p.parse_args()    
    num = rename_directory(args.directory, new_name=args.new_name, dry_run=args.dry_run)
    print("Renamed {:d} objects".format(num))
    sys.exit(0)
    
if __name__ == '__main__':
    main()
        