import numpy as np
import cv2
import decode
import math
from utils import *

# get blocked size

def get_actual_size(width, height, block_size=BLOCK_SIZE):
    m, n = width, height
    m, n = float(m), float(n)
    num_blocks_m = int(math.ceil(m/block_size))
    num_blocks_n = int(math.ceil(n/block_size))
    return num_blocks_m*block_size, num_blocks_n*block_size

# uncompresss frames

def uncompress(frame, width=WIDTH, height=HEIGHT):
    tokens = frame.split()
    temp = np.zeros(height*width, dtype=int)
    k, i, x, j = 0, 0, 0, 0
    while k < temp.shape[0]:
        if i >= len(tokens):
            break
        if "-" in tokens[i]:
            temp[k] = -1*int("".join(filter(str.isdigit, tokens[i])))
        else:
            temp[k] = int("".join(filter(str.isdigit, tokens[i])))
        if len(tokens) > i+3:
            j = int(''.join(filter(str.isdigit, tokens[i+3])))
        if j == 0:
            k += 1
        else:
            k += j + 1
        i += 2
    decoded = decode.decode(np.reshape(temp, (height, width)), width, height)
    return decoded

def uncompress_yuv(filename, out_filename, width=WIDTH, height=HEIGHT, frame_diff=False):
    width, height = get_actual_size(width, height)
    frames = None
    with open(filename, "r") as f:
        frames = f.read()
    frames_arr = frames.split("\n")[:-1]
    res = []
    for i, frame in enumerate(frames_arr):
        decoded = uncompress(frame, width, height)
        res.append(decoded[:HEIGHT,:WIDTH])
        print("%s | uncompressed frame %d" % (filename, i))
    if frame_diff:
        res = recon_frame_differences(res)
    cv2.imwrite("compressed_image.bmp", res[0])
    f = open(out_filename, "wb")
    f.write(np.uint8(np.array(res)))
    f.close()
    print("%s saved" % out_filename)
