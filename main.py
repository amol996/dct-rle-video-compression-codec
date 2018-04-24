import numpy as np
import compress
import uncompress
import argparse

from utils import *

def experiment_data_gen():
    files = [
        "../bunny/bunny.450p.yuv",
        "../tractor/tractor.450p.yuv",
        "../pinwheel/pinwheel.450p.yuv",
        "../candle/candle.450p.yuv",
        "../jellyfish/jellyfish.450p.yuv"
    ]
    print(Q)
    data = {"huff_frame_dif": {}, "huff": {}, "rle_frame_diff": {}, "rle": {}}
    for f in files:
        # huffman no frame diff
        fileprefix = os.path.basename(f)

        model = compress.compress_yuv_using_huffman(f, fileprefix+".huf.dat", frame_diff=False)
        uncompress.uncompress_yuv_using_huffman(fileprefix+".huf.dat", fileprefix+".hufrecon.dat", model, frame_diff=False)
        mse = compare_frames(f, fileprefix+".hufrecon.dat")
        ratio = compare_file_sizes(f, fileprefix+".huf.dat")
        data["huff"][f] = {"mse": mse, "ratio": ratio}

        # huffman frame diff
        model = compress.compress_yuv_using_huffman(f, fileprefix+".fhuf.dat", frame_diff=True)
        uncompress.uncompress_yuv_using_huffman(fileprefix+".fhuf.dat", fileprefix+".fhufrecon.dat", model, frame_diff=True)
        mse = compare_frames(f, fileprefix+".fhufrecon.dat")
        ratio = compare_file_sizes(f, fileprefix+".fhuf.dat")
        data["huff_frame_dif"][f] = {"mse": mse, "ratio": ratio}

        compress.compress_yuv(f, fileprefix+".rle.dat", frame_diff=False)
        uncompress.uncompress_yuv(fileprefix+".rle.dat", fileprefix+".rlerecon.dat", frame_diff=False)
        mse = compare_frames(f, fileprefix+".rlerecon.dat")
        ratio = compare_file_sizes(f, fileprefix+".rle.dat")
        data["rle"][f] = {"mse": mse, "ratio": ratio}

        compress.compress_yuv(f, fileprefix+".frle.dat", frame_diff=True)
        uncompress.uncompress_yuv(fileprefix+".frle.dat", fileprefix+".frlerecon.dat", frame_diff=True)
        mse = compare_frames(f, fileprefix+".frlerecon.dat")
        ratio = compare_file_sizes(f, fileprefix+".frle.dat")
        data["rle_frame_diff"][f] = {"mse": mse, "ratio": ratio}

    for key in data:
        print(key)
        print(data[key])
        print("------------")
    print(Q)

if __name__ == "__main__":
    # experiment_data_gen()
    parser = argparse.ArgumentParser()
    parser.add_argument("compression_type")
    parser.add_argument("frame_differences_flag")
    parser.add_argument("input_filename")

    args = parser.parse_args()
    flag = False if args.frame_differences_flag == "n" else True

    if args.compression_type == "huff":
        model = compress.compress_yuv_using_huffman(args.input_filename, "hufcompressed.dat", frame_diff=flag)
        uncompress.uncompress_yuv_using_huffman("hufcompressed.dat", "recon.dat", model, frame_diff=flag)
        mse = compare_frames(args.input_filename, "recon.dat")
        show_frame(args.input_filename, 0)
        show_frame("recon.dat", 0)
        print(mse, compare_file_sizes(args.input_filename, "hufcompressed.dat"))
    elif args.compression_type == "rle":
        scompress.compress_yuv(args.input_filename, "rlecompressed.dat", frame_diff=flag)
        uncompress.uncompress_yuv("rlecompressed.dat", "rlerecon.dat", frame_diff=flag)
        mse = compare_frames(args.input_filename, "rlerecon.dat")
        show_frame("recon.dat", 0)
        show_frame("rlerecon.dat", 0)
        print(mse, compare_file_sizes(args.input_filename, "rlecompressed.dat"))
