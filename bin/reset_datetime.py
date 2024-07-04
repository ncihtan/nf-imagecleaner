#!/usr/bin/env python

# Source: https://github.com/labsyspharm/ome-tiff-pyramid-tools/blob/master/reset_datetime.py

import argparse
from datetime import datetime
import sys
import tiffsurgeon


# Define a custom argument type for a list of integers
def list_of_ints(arg):
    return list(map(int, arg.split(",")))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Set all specified date tags in a TIFF to one value (in place).",
    )
    parser.add_argument("image_path", help="TIFF file to process")
    parser.add_argument(
        "--datetags",
        help="Space-separated list of tags (integer ids) with dates to replace (default: 306)",
        nargs="+",
        type=int,
        default=[306],
    )
    parser.add_argument(
        "--datetime",
        help="YYYY:MM:DD HH:MM:SS string to replace all DateTime values."
        " Note the use of colons in the date, as required by the TIFF standard."
        " Default: 1970:01:01 00:00:00 (start of Unix epoch).",
        type=str,
        default="1970:01:01 00:00:00",
    )
    argv = sys.argv[1:]
    # Allow date and time to be passed as separate args for convenience.
    if len(argv) == 3:
        argv[1] = " ".join(argv[1:3])
        del argv[2]
    args = parser.parse_args(argv)
    return args


def main():

    args = parse_args()

    try:
        tiff = tiffsurgeon.TiffSurgeon(
            args.image_path, encoding="utf-8", writeable=True
        )
        tiff.read_ifds()
    except (tiffsurgeon.FormatError, UnicodeDecodeError) as e:
        print(f"TIFF format or encoding error: {e}. Trying with Latin-1 encoding.")
        try:
            tiff = tiffsurgeon.TiffSurgeon(
                args.image_path, encoding="latin-1", writeable=True
            )
            tiff.read_ifds()
        except tiffsurgeon.FormatError as e:
            print(f"Error reading IFDs: {e}")
            sys.exit(1)
    except tiffsurgeon.FormatError as e:
        print(f"TIFF format error: {e}")
        sys.exit(1)
    try:
        datetime.strptime(args.datetime, "%Y:%m:%d %H:%M:%S")
    except ValueError as e:
        print(f"Invalid datetime: {e}")
        sys.exit(1)
    new_datetime = args.datetime.encode("ascii")
    assert len(new_datetime) == 19, "length of DateTime string must be exactly 19"

    tiff.read_ifds()

    for tag in args.datetags:
        if not any(tag in i.tags for i in tiff.ifds):
            print(f"Tag {tag} not found in {args.image_path} -- file not modified")
            sys.exit(1)

        subifds = [
            tiff.read_ifd(v)
            for i in tiff.ifds
            if 330 in i.tags
            for v in i.tags[330].value
        ]
        offsets = [
            i.tags[tag].offset_range.start for i in tiff.ifds + subifds if tag in i.tags
        ]

        if offsets:
            for x in offsets:
                tiff.file.seek(x)
                tiff.file.write(new_datetime)
            print(
                f"Successfully replaced {len(offsets)} values of tag {tag} in"
                f" {args.image_path}"
            )
        else:
            print(
                f"No tags with number {tag} found in {args.image_path} -- file not modified"
            )

    tiff.close()


if __name__ == "__main__":
    main()
