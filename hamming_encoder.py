#!/usr/bin/env python3

import sys
import argparse
import numpy as np

h74_encode = [
    [1,1,0,1],
    [1,0,1,1],
    [1,0,0,0],
    [0,1,1,1],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
]

h74_decode = [
    [0,0,1,0,0,0,0],
    [0,0,0,0,1,0,0],
    [0,0,0,0,0,1,0],
    [0,0,0,0,0,0,1]
]

def native_encode(word, _):
    word = np.array([int(ch) for ch in "{0:04b}".format(word)])
    return "".join(["{0:01b}".format(x%2) for x in np.matmul(h74_encode,word)])

def native_decode(word, _):
    word = np.array([int(ch) for ch in "{0:07b}".format(word)])
    return "".join(["{0:01b}".format(x%2) for x in np.matmul(h74_decode,word)])

if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Hamming string encoder.')
    parser.add_argument(
            '-f',
            '--file',
            dest="file",
            type=argparse.FileType('r')
    )
    parser.add_argument(
            '-l', 
            '--use-lib', 
            dest='use_lib', 
            action='store_true',
            default=False
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

    if args.use_lib:
        try:
            import hamming_codec
            local_encode = hamming_codec.encode
            local_decode = hamming_codec.decode
        except:
            print("failed hamm import")
            local_encode = native_encode
            local_decode = native_decode
    else:
        local_encode = native_encode
        local_decode = native_decode


    if args.encode:
        for line in input_stream:
            bin_rep = [format(ord(val), '08b') for val in line[:-1]]

            bin4_rep = []
            for val in bin_rep:
                bin4_rep += [val[:4], val[4:]]

            ham_rep = [local_encode(int(val,2), 4) for val in bin4_rep]
            print(" ".join(ham_rep))

    else:
        for line in input_stream:
            dec_ham = [local_decode(int(val,2), 7) for val in line.split(" ")]

            dec_bin = []
            for ell, arr in zip(dec_ham[::2], dec_ham[1::2]):
                dec_bin += [ell+arr]

            dec_msg = "".join([chr(int(val, 2)) for val in dec_bin])
            print(dec_msg)
