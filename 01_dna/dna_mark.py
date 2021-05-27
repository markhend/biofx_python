#!/usr/bin/env python3
"""
Author : mhenders <mhenders@localhost>
Date   : 2020-11-08
Purpose: Tetranucleotide frequency
"""

import argparse
import os
from typing import NamedTuple


class Args(NamedTuple):
    """ Command-line arguments """

    dna: str


def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Tetranucleotide frequency",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("dna", metavar="DNA", help="Input a DNA Sequence")

    args = parser.parse_args()

    if os.path.isfile(args.dna):
        args.dna = open(args.dna).read().rstrip()

    return Args(args.dna)


def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    res = ""
    for base in "ACGT":
        res += str(args.dna.count(base)) + ' '
    print(res[:-1])
    # print(args.dna)


if __name__ == "__main__":
    main()
