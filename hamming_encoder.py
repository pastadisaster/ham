#!/usr/bin/env python3

import sys
import hamming_codec
import argparse


if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Hamming string encoder.')
    parser.add_argument(
            '-f',
            '--file',
            dest="file",
            type=argparse.FileType('r')
    )
    encoding_parser = parser.add_mutually_exclusive_group(required=False)
    encoding_parser.add_argument(
            '-e', 
            '--encode', 
            default=True, 
            action='store_true'
    )
    encoding_parser.add_argument(
            '-d', 
            '--decode', 
            dest='encode', 
            action='store_false'
    )

    args = parser.parse_args()

    # use stdin if it's full                                                        
    if args.file:
        input_stream = args.file
    else:
        input_stream = sys.stdin

    if args.encode:
        for line in input_stream:
            bin_rep = [format(ord(val), '08b') for val in line[:-1]]

            bin4_rep = []
            for val in bin_rep:
                bin4_rep += [val[:4], val[4:]]

            ham_rep = [hamming_codec.encode(int(val,2), 4) for val in bin4_rep]
            print(" ".join(ham_rep))

    else:
        for line in input_stream:
            dec_ham = [hamming_codec.decode(int(val,2), 7) for val in line.split(" ")]

            dec_bin = []
            for ell, arr in zip(dec_ham[::2], dec_ham[1::2]):
                dec_bin += [ell+arr]

            dec_msg = "".join([chr(int(val, 2)) for val in dec_bin])
            print(dec_msg)
