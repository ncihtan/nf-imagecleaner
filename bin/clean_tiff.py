#!/usr/bin/env python

import argparse
import tifftools
import os

parser = argparse.ArgumentParser()

parser.add_argument("input")
parser.add_argument("--suffix", default="_cleaned")

args = parser.parse_args()

def split_all_ext(filename):
    basename = filename
    extensions = []
    while "." in basename:
        basename, ext = os.path.splitext(basename)
        extensions.append(ext)
    return basename, "".join(reversed(extensions))

basename, all_ext = split_all_ext(args.input)

new_filename = f"{basename}{args.suffix}{all_ext}"
print(new_filename)

unset_list = [
    "DateTime",
    "NDPI_ScanTime",
    "NDPI_WriteTime",
    "Artist",
    "HostComputer",
    "WangAnnotation",
    "WriterSerialNumber",
    "MDLabName",
    "MDPrepDate",
    "MDSampleInfo",
    "Software",
    "45278",
    "45279",
    "45494"
]

def get_all_ifds(ifds, path=""):
    """
    Recursively get all IFDs and their subIFDs.
    """
    all_ifds = []
    for idx, ifd in enumerate(ifds):
        current_path = f"{path},{idx}" if path else str(idx)
        all_ifds.append(current_path)
        for tag in ifd['tags']:
            if tag == tifftools.constants.Tag.SubIFD:
                subifds = ifd['tags'][tag]['ifds']
                all_ifds.extend(get_all_ifds(subifds, current_path))
    return all_ifds

# Read the TIFF file info
info = tifftools.read_tiff(args.input)

# Get all IFDs and subIFDs
all_ifds = get_all_ifds(info['ifds'])

# Prepare a list of tags to unset from all IFDs
unset_all_ifds = []
for ifd_path in all_ifds:
    for tag in unset_list:
        unset_all_ifds.append(f"{tag},{ifd_path}")

# Modify the TIFF file
tifftools.tiff_set(
    args.input,
    output=new_filename,
    overwrite=False,
    unset=unset_all_ifds
)
