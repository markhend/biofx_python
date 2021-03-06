#!/usr/bin/env python3
""" Open Reading Frames """

import argparse
from typing import NamedTuple, TextIO, List
from Bio import SeqIO, Seq


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Open Reading Frames',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='Input FASTA file',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    for rec in SeqIO.parse(args.file, 'fasta'):
        rna = str(rec.seq).replace('T', 'U')
        orfs = set()

        for seq in [rna, Seq.reverse_complement(rna)]:
            for i in range(3):
                if prot := Seq.translate(truncate(seq[i:], 3), to_stop=False):
                    for orf in find_orfs(prot):
                        orfs.add(orf)

        print('\n'.join(sorted(orfs)))


# --------------------------------------------------
def truncate(seq: str, k: int) -> str:
    """ Truncate a sequence to even division by k """

    length = len(seq)
    end = length - (length % k)
    return seq[:end]


# --------------------------------------------------
def test_truncate() -> None:
    """ Test truncate """

    seq = '0123456789'
    assert truncate(seq, 3) == '012345678'
    assert truncate(seq[1:], 3) == '123456789'
    assert truncate(seq[2:], 3) == '234567'


# --------------------------------------------------
def find_orfs(aa: str) -> List[str]:
    """ Find ORFs in AA sequence """

    # Method 1: Use in/str.index()
    orfs = []
    while 'M' in aa:
        start = aa.index('M')
        if '*' in aa[start + 1:]:
            stop = aa.index('*', start + 1)
            orfs.append(''.join(aa[start:stop]))
            aa = aa[start + 1:]
        else:
            break

    return orfs


# --------------------------------------------------
def test_find_orfs() -> None:
    """ Test find_orfs """

    assert find_orfs('') == []
    assert find_orfs('M') == []
    assert find_orfs('*') == []
    assert find_orfs('M*') == ['M']
    assert find_orfs('MAMAPR*') == ['MAMAPR', 'MAPR']
    assert find_orfs('MAMAPR*M') == ['MAMAPR', 'MAPR']
    assert find_orfs('MAMAPR*MP*') == ['MAMAPR', 'MAPR', 'MP']


# --------------------------------------------------
if __name__ == '__main__':
    main()
