#!/usr/bin/env python

import sys
import io
from Cheetah.Template import Template

TEMPLATE=io.readfile('pds4_policy_template_cheetah.txt')
BASEURL='$HOME/Desktop/Harvest/bundles/'

def main(argv=None):
    if argv is None:
        argv = sys.argv

    basedir = argv[1]
    bundle_id = argv[2]
    collection_ids = argv[3:]
    
    write_policies(basedir, bundle_id, collection_ids)
    
    
def write_policies(basedir, bundle_id, collection_ids):
    '''
    Generates a policy file from the specified parameters. This will also
    automatically determine the output file name from the bundle id.
    '''
    output_file = get_output_file(bundle_id)
    title = get_title(bundle_id)
    values = getValueMap(basedir, bundle_id, collection_ids, title)
    write_policy(output_file, values)
    

def get_output_file(bundle_id):
    return './harvest-policy-' + bundle_id + '.xml'


def get_title(bundle_id):
    return bundle_id + ' package'


def getValueMap(basedir, bundle_id, collection_ids, title):
    '''
    Packages the command parameters into a dictionary that will be fed into the
    cheetah template.
    '''
    return {
            'basedir': basedir, 
            'bundle_id': bundle_id, 
            'title': title, 
            'collection_ids': collection_ids,
            'baseurl' : BASEURL
    }


def write_policy(output_file, values):
    '''
    Applies the supplied values to the cheetah template, and writes the result
    to a file.
    '''
    template = Template(TEMPLATE, values)
    with open(output_file, 'w') as f:
        f.write(template.respond())

if __name__ == '__main__':
    sys.exit(main())
