import cv2
import numpy as np
import math

from dahuffman import HuffmanCodec
from zigzag import *
from utils import *

# get run length encoding of flattened matrix

def rle(frame):
    idx = 0
    res = []
    bypass = 0
    stream = ""
    frame = frame.astype(int)
    while idx < frame.shape[0]:
        if frame[idx] != 0:
            res.append((frame[idx], bypass))
            stream += "%s %s " % (str(frame[idx]), str(bypass))
            bypass = 0
        else:
            bypass += 1
        idx += 1
    return stream

# get number of 8 x 8 blocks needed

def number_of_blocks_needed(frame, block_size=BLOCK_SIZE):
    m, n = frame.shape
    m, n = float(m), float(n)

    num_blocks_m = int(math.ceil(m/block_size))
    num_blocks_n = int(math.ceil(n/block_size))
    return num_blocks_m, num_blocks_n

# get the padded image for dct

def get_padded_frame(frame, num_blocks_m, num_blocks_n, block_size=BLOCK_SIZE):
    m = num_blocks_m * block_size
    n = num_blocks_n * block_size

    h, w = frame.shape
    padded_frame = np.zeros((m, n))
    padded_frame[:h,:w] = frame
    return padded_frame

# do the dct on each block

def dct(frame, block_size=BLOCK_SIZE):
    num_blocks_m, num_blocks_n = number_of_blocks_needed(frame)
    padded_frame = get_padded_frame(frame, num_blocks_m, num_blocks_n)

    for i in range(num_blocks_m):
        row_ind_1 = i*block_size
        row_ind_2 = row_ind_1+block_size
        for j in range(num_blocks_n):
            col_ind_1 = j*block_size
            col_ind_2 = col_ind_1+block_size

            block = padded_frame[row_ind_1:row_ind_2,col_ind_1:col_ind_2]
            trans = cv2.dct(block)
            trans_norm = np.divide(trans, Q).astype(int)

            reordered = zigzag(trans_norm)
            reshaped = np.reshape(reordered, (block_size, block_size))

            padded_frame[row_ind_1:row_ind_2,col_ind_1:col_ind_2] = reshaped
    return padded_frame

# dct then rle

def encode(frame, huffman=False):
    dct_frame = dct(frame)
    if not huffman:
        rle_frame = rle(dct_frame.flatten())
        return rle_frame
    else:
        codec = HuffmanCodec.from_data(dct_frame.flatten())
        rle_frame = codec.encode(dct_frame.flatten())
        return rle_frame, codec
