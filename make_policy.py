#!/usr/bin/env python3

import sys
import io
from Cheetah.Template import Template

with open('pds4_policy_template_cheetah.txt') as template_file:
    TEMPLATE=template_file.read()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if (len(argv) < 5):
        usage()
        return 1
        
    basedir = argv[1]
    baseurl = argv[2]
    bundle_id = argv[3]
    collection_ids = argv[4:]
    
    write_policies(basedir, baseurl, bundle_id, collection_ids)

def usage():
    print('usage: make_policy.py basedir baseurl bundle_id collection_ids...')
    
    
def write_policies(basedir, baseurl, bundle_id, collection_ids):
    '''
    Generates a policy file from the specified parameters. This will also
    automatically determine the output file name from the bundle id.
    '''
    output_file = get_output_file(bundle_id)
    title = get_title(bundle_id)
    values = getValueMap(basedir, baseurl, bundle_id, collection_ids, title)
    write_policy(output_file, values)
    

def get_output_file(bundle_id):
    return './harvest-policy-' + bundle_id + '.xml'


def get_title(bundle_id):
    return bundle_id + ' package'


def getValueMap(basedir, baseurl, bundle_id, collection_ids, title):
    '''
    Packages the command parameters into a dictionary that will be fed into the
    cheetah template.
    '''
    return {
            'basedir': basedir, 
            'bundle_id': bundle_id, 
            'title': title, 
            'collection_ids': collection_ids,
            'baseurl' : baseurl
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
