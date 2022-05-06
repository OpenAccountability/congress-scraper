#!/bin/bash

rm -r dist/
pip uninstall congress-scraper -y
python -m build
pip install dist/congress_*
cs-members
