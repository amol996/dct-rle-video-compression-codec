# COMP 590 Lossy Video Compression

This is a class assignment for comp590 at unc-chapel hill. The main.py uses the discrete cosine transform (dwt) and run-length encoding (rle) or huffman (huff) to compress yuv video files. See below for easy instructions on use.

## Usage
You can compress and uncompress files with or without making use of frame differences.
* python main.py <huff/rle> <frame_diff_flag (y/n)> <input_filename>
* The compressed.dat file and the recon.dat file will be saved in the working directory.

### Example
* Compressing a yuv file without use of frame differences
* python main.py huff n bunny.450p.yuv
