#!/usr/bin/env python3

import sys
from jinja2 import Template
import os
import os.path
import itertools

with open('pds4_policy_template_jinja.txt') as template_file:
    TEMPLATE=template_file.read()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if (len(argv) < 4):
        usage()
        return 1
        
    basedir = argv[1]
    baseurl = argv[2]
    bundle_id = argv[3]
    collection_files = discover_collection_files(basedir)
    print(collection_files)
    
    write_policies(basedir, baseurl, bundle_id, collection_files)

def usage():
    print('usage: make_policy.py basedir baseurl bundle_id collection_files...')

def discover_collection_files(basedir):
    files = itertools.chain.from_iterable([[os.path.join(path, filename) for filename in filenames] for path, _, filenames in os.walk(basedir)])
    return [f for f in files if 'collection_' in f and f.endswith('.xml')]
    
def write_policies(basedir, baseurl, bundle_id, collection_files):
    '''
    Generates a policy file from the specified parameters. This will also
    automatically determine the output file name from the bundle id.
    '''
    output_file = get_output_file(bundle_id)
    title = get_title(bundle_id)
    values = getValueMap(basedir, baseurl, bundle_id, collection_files, title)
    write_policy(output_file, values)
    

def get_output_file(bundle_id):
    return './harvest-policy-' + bundle_id + '.xml'


def get_title(bundle_id):
    return bundle_id + ' package'


def getValueMap(basedir, baseurl, bundle_id, collection_files, title):
    '''
    Packages the command parameters into a dictionary that will be fed into the
    cheetah template.
    '''
    return {
            'basedir': basedir, 
            'bundle_id': bundle_id, 
            'title': title, 
            'collection_files': collection_files,
            'baseurl' : baseurl
    }


def write_policy(output_file, values):
    '''
    Applies the supplied values to the cheetah template, and writes the result
    to a file.
    '''
    template = Template(TEMPLATE)
    with open(output_file, 'w') as f:
        f.write(template.render(values))

if __name__ == '__main__':
    sys.exit(main())
