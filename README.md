# COMP 590 Lossy Video Compression

This is a class assignment for comp590 at unc-chapel hill. main.py uses the discrete cosine transform (dwt) and run-length encoding (rle) to compress yuv video files. See below for easy instructions on use.

## Usage
You can compress and uncompress files with or without making using frame differences.
* python main.py <compress_flag (c/n)> <frame_diff_flag (y/n)> <input_filename> <output_filename>

### Example
Compressing a yuv file without using frame differences
* python main.py c n bunny.450p.yuv bunny.450p.compressed.txt
Uncompressing the same file
* python main.py n n bunny.450p.compressed.txt bunny.450p.recon.dat
