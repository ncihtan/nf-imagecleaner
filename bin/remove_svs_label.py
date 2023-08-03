#!/usr/bin/env python

import sys
import tifftools
import os

input = sys.argv[1]

os.rename(input, input + ".original")

# Read the TIFF
svs_info = tifftools.read_tiff(input + ".original")

# Filter out IFDs where the ImageDescription contains 'label'
filtered_ifds = [
    ifd
    for ifd in svs_info["ifds"]
    if "label" not in ifd["tags"][tifftools.Tag.IMAGEDESCRIPTION.value]["data"]
]

# Overwrite tiff_info['ifds'] with the filtered ones
svs_info["ifds"] = filtered_ifds

# Write the modified TIFF back to a new file
tifftools.write_tiff(svs_info, input, allowExisting=True)
