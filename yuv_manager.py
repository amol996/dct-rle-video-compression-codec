import cv2
import numpy as np

from utils import *

def read_frame(f, width, height):
    size = width*height
    raw = f.read(size)
    yuv = np.frombuffer(raw, dtype=np.uint8)
    yuv = yuv.reshape((height, width))
    return yuv

def read_yuv(filename, width=WIDTH, height=HEIGHT, n=NUM_FRAMES):
    frames = []
    f = open(filename, "rb")
    for i in range(n):
        print("%s | read frame %d" % (filename, i))
        frames.append(read_frame(f, width, height))
    return frames
