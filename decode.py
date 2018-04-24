import cv2
import numpy as np
import math

from zigzag import *
from utils import *

# do inv dct

def decode(frame, width=WIDTH, height=HEIGHT, block_size=BLOCK_SIZE):
    padded_frame = np.zeros((height, width))
    i, j, k = 0, 0, 0
    while i < height:
        j = 0
        while j < width:
            temp_stream = frame[i:i+block_size,j:j+block_size]
            block = inverse_zigzag(temp_stream.flatten(), block_size, block_size)
            quant = np.multiply(block, Q)
            padded_frame[i:i+block_size,j:j+block_size] = cv2.idct(quant)
            j += block_size
        i += block_size
    padded_frame[padded_frame > 255] = 255
    padded_frame[padded_frame < 0] = 0
    return padded_frame
