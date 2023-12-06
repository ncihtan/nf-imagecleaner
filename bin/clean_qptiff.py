#!/usr/bin/env python

import sys
import tifftools
import re
import os

input = sys.argv[1]

os.rename(input, input + ".original")

date_pattern = r"(<Date>((\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})(\.\d+)?Z?))</Date>"
date_replacement = "<Date />"


sample_pattern = r"<SampleDescription>.+</SampleDescription>"
sample_replacement = "<SampleDescription />"

qptiff_info = tifftools.read_tiff(input + ".original")

for i, ifd in enumerate(qptiff_info["ifds"]):
    for tag in ifd["tags"]:
        if tag == tifftools.Tag.IMAGEDESCRIPTION:
            old_description = ifd["tags"][tifftools.Tag.IMAGEDESCRIPTION.value]["data"]
            new_description = re.sub(date_pattern, date_replacement, old_description)
            new_description = re.sub(sample_pattern, sample_replacement, new_description)
            if new_description != old_description:
                print(f"Redacting date in IFD {i}, tag {tag}")
                qptiff_info["ifds"][i]["tags"][tifftools.Tag.IMAGEDESCRIPTION.value][
                    "data"
                ] = new_description

tifftools.write_tiff(qptiff_info, input, allowExisting=True)
