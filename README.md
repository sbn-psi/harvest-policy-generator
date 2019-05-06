# Harvest Policy Generator

## Overview

This script will generate a policy file for the PDS4 harvest tool.

## Prerequisites

This script requires the jinja2 templating engine and BeautifulSoup. You can install them by running:

```bash
pip3 install jinja2
pip3 install beautifulsoup4
```

## Usage

```bash
make_policy.py basedir baseurl
```

`basedir` is the root directory of the bundle

`baseurl` is the url of the bundle
