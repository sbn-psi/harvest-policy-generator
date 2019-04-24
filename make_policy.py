#!/usr/bin/env python3

from jinja2 import Template
from bs4 import BeautifulSoup
import sys
import os
import os.path
import itertools
import re

with open('pds4_policy_template_jinja.txt') as template_file:
    TEMPLATE=template_file.read()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if (len(argv) < 3):
        usage()
        return 1
        
    basedir = argv[1]
    baseurl = argv[2]
    bundle_file = discover_files(basedir, '.*bundle.*\.xml')[0]
    bundle_id = extract_bundle_id(bundle_file)
    collection_files = discover_files(basedir, '.*collection.*\.xml')
    
    write_policies(basedir, baseurl, bundle_id, collection_files)

def usage():
    print('usage: make_policy.py basedir baseurl')

def discover_files(basedir, regex):
    r = re.compile(regex)
    files = itertools.chain.from_iterable([[os.path.join(path, filename) for filename in filenames] for path, _, filenames in os.walk(basedir)])
    return [f for f in files if r.match(f)]

def extract_bundle_id(bundle_filename):
    with open(bundle_filename) as bundle_file:
        soup = BeautifulSoup(bundle_file, "lxml-xml")
        logical_id = soup.Product_Bundle.Identification_Area.logical_identifier.string
        return logical_id.split(":")[3]

    
def write_policies(basedir, baseurl, bundle_id, collection_files):
    '''
    Generates a policy file from the specified parameters. This will also
    automatically determine the output file name from the bundle id.
    '''
    output_file = get_output_file(bundle_id)
    values = getValueMap(basedir, baseurl, bundle_id, collection_files)
    write_policy(output_file, values)
    

def get_output_file(bundle_id):
    return './harvest-policy-' + bundle_id + '.xml'


def getValueMap(basedir, baseurl, bundle_id, collection_files):
    '''
    Packages the command parameters into a dictionary that will be fed into the
    cheetah template.
    '''
    return {
            'basedir': basedir, 
            'bundle_id': bundle_id, 
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
