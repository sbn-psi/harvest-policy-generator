# Harvest Policy Generator

## Overview

This script will generate a policy file for the PDS4 harvest tool.

## Prerequisites

This script has the following dependencies:

* [jinja2](http://jinja.pocoo.org/)
* [beautiful soup](https://www.crummy.com/software/BeautifulSoup/)
* [lxml](https://lxml.de/)

You can install them by running:

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
make_policy.py basedir baseurl
```

`basedir` is the root directory of the bundle

`baseurl` is the url of the bundle
