import numpy as np
import encode
import yuv_manager
from utils import *

def compress_yuv(filename, out_filename, frame_diff=False):
    frames = yuv_manager.read_yuv(filename)
    if frame_diff:
        frames = frame_differences(frames)
    rle = ""
    for i, frame in enumerate(frames):
        rle += encode.encode(frame) + "\n"
        print("%s | encoded frame %d" % (filename, i))
    f = open(out_filename, "w")
    f.write(rle)
    f.close()
    print("%s saved" % out_filename)
