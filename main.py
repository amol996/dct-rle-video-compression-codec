import numpy as np
import compress
import uncompress
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("compress_flag")
    parser.add_argument("frame_differences_flag")
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")

    args = parser.parse_args()
    flag = False if args.frame_differences_flag == "n" else True
    if args.compress_flag == "c":
        compress.compress_yuv(args.input_filename, args.output_filename, frame_diff=flag)
    else:
        uncompress.uncompress_yuv(args.input_filename, args.output_filename, frame_diff=flag)
