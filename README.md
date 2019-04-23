# Harvest Policy Generator

## Overview

This script will generate a policy file for the PDS4 harvest tool.

## Prerequisites

This script requires the jinja2 templating engine. You can install it by running:

```bash
pip3 install jinja2
```

## Usage

```bash
make_policy.py basedir baseurl bundleid collectionids...
```

`basedir` is the root directory of the bundle

`baseurl` is the url of the bundle

`bundleid` is the id of the bundle. This is the fourth component of the logical id.

`collectionids` these are the ids of the collections within the bundle. They are the fifth component of the logical id.
