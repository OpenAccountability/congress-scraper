#!/bin/bash

membersFile=$1
mkdir bills/

jq -r .[].Key $membersFile | parallel --bar wget -O bills/{}.csv 'https://www.congress.gov/quick-search/legislation?wordsPhrases=\&wordVariants=on\&congressGroups%5B%5D=0\&congressGroups%5B%5D=1\&congresses%5B%5D=all\&legislationNumbers=\&legislativeAction=\&sponsor=on\&representative={}\&senator={}\&1ddcb92ade31c8fbd370001f9b29a7d9=628cb5675ff524f3e719b7aa2e88fe3f'
