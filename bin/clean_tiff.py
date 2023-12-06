#!/usr/bin/env python

import argparse
import tifftools
import os

import argparse

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


base_unset_list = [
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

info = tifftools.read_tiff(args.input)
num_ifds = len(info['ifds'])

unset_list_for_all_ifds = []
for ifd in range(num_ifds):
    unset_list_for_ifd = [f"{tag},{ifd}" for tag in base_unset_list]
    unset_list_for_all_ifds.extend(unset_list_for_ifd)

# Call tiff_set only once after all IFD modifications are specified
tifftools.tiff_set(
    args.input,
    output=new_filename,
    overwrite=False,
    unset=unset_list_for_all_ifds
)