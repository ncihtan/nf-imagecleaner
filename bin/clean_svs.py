#!/usr/bin/env python

import sys
import tifftools
import re
import os

input = sys.argv[1]

os.rename(input, input + '.original')

pattern = r'\|(Date|Time Zone|ScanScope ID|User|Time|DSR ID) = ([^\|]+)'

replacement = ""

svs_info = tifftools.read_tiff(input + '.original')

for i, ifd in enumerate(svs_info['ifds']):
    for tag in ifd['tags']:
        if tag == tifftools.Tag.IMAGEDESCRIPTION:
            old_description = ifd['tags'][tifftools.Tag.IMAGEDESCRIPTION.value]['data']
            new_description = re.sub(pattern, replacement, old_description)
            if new_description != old_description:
                print(f'Redacting date in IFD {i}, tag {tag}')
                svs_info['ifds'][i]['tags'][tifftools.Tag.IMAGEDESCRIPTION.value]['data']= new_description

tifftools.write_tiff(svs_info, input, allowExisting=True)