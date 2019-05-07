#!/usr/bin/env python3

from jinja2 import Template
from bs4 import BeautifulSoup
import sys
import os
import os.path
import itertools
import re




def main(argv=None):
    if argv is None:
        argv = sys.argv

    if (len(argv) < 3):
        usage()
        return 1

    scriptdir = os.path.dirname(argv[0])        
    basedir = argv[1].rstrip("/") + "/"
    baseurl = argv[2].rstrip("/") + "/"

    make_policy(scriptdir, basedir, baseurl)

def usage():
    print('usage: make_policy.py basedir baseurl')

def make_policy(templatedir, basedir, baseurl):
    with open(os.path.join(templatedir, 'pds4_policy_template_jinja.txt')) as template_file:
        template=template_file.read()
        
    bundle_files = discover_files(basedir, '.*bundle.*\.xml')
    collection_files = discover_files(basedir, '.*collection.*\.xml')

    bundle_file = (bundle_files or collection_files)[0]
    bundle_id = extract_bundle_id(bundle_file)

    template_values = getValueMap(basedir, baseurl, bundle_id, collection_files)

    write_policies(bundle_id, template_values, template)

def discover_files(basedir, regex):
    r = re.compile(regex)
    files = itertools.chain.from_iterable([[os.path.join(path, filename) for filename in filenames] for path, _, filenames in os.walk(basedir)])
    return [f for f in files if r.match(f)]

def extract_bundle_id(bundle_filename):
    with open(bundle_filename, encoding='utf-8') as bundle_file:
        soup = BeautifulSoup(bundle_file, "lxml-xml")
        product = soup.Product_Bundle or soup.Product_Collection
        logical_id = product.Identification_Area.logical_identifier.string
        return logical_id.split(":")[3]

    
def write_policies(bundle_id, template_values, template):
    '''
    Generates a policy file from the specified parameters. This will also
    automatically determine the output file name from the bundle id.
    '''
    output_file = get_output_file(bundle_id)
    write_policy(output_file, template_values, template)
    

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


def write_policy(output_file, values, template):
    '''
    Applies the supplied values to the cheetah template, and writes the result
    to a file.
    '''
    template = Template(template)
    with open(output_file, 'w') as f:
        f.write(template.render(values))

if __name__ == '__main__':
    sys.exit(main())
