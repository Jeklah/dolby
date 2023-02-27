# this is a simple command line tool to encode and decode
# dolby digitial files using ffmpeg
# and sox where necessary.

import os
import sys
import argparse
import subprocess


def run_cmd(cmd):
    """
    Function that runs the main command and parses the arguments.
    """
    for line in (subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)).stdout.readlines():
        print(line)
    return (subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)).wait()


def encode(infile, outfile, acodec, abitrate, achannel):
    """
    Encode file as dolby d.
    """
    cmd = f'ffmpeg -i {infile} -acodec {acodec} -ab {abitrate} -ac {achannel} -y {outfile}'
    run_cmd(cmd)


def decode(infile, outfile, acodec, abitrate, achannel):
    """
    Decode file from dolby d.
    """
    cmd = f'ffmpeg -i {infile} -acodec {acodec} -ab {abitrate} -ac {achannel} -y {outfile}'
    run_cmd(cmd)


def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(
        description='Dolby Digital Encoder/Decoder')
    parser.add_argument('-i', '--infile', help='Input File')
    parser.add_argument('-o', '--outfile', help='Output File')
    parser.add_argument('-t', '--type', help='Encode or Decode')
    parser.add_argument('-ac', '--acodec', help='Audio Codec')
    parser.add_argument('-ab', '--abitrate', help='Audio Bitrate')
    parser.add_argument('-ch', '--achannel', help='Audio Channel')
    args = parser.parse_args()
    if args.type == 'encode':
        encode(args.infile, args.outfile, args.acodec,
               args.abitrate, args.achannel)
    elif args.type == 'decode':
        decode(args.infile, args.outfile, args.acodec,
               args.abitrate, args.achannel)
    else:
        print('Invalid Type')
        sys.exit(1)


if __name__ == '__main__':
    main()
