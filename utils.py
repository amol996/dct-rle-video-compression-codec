import numpy as np
import cv2
import os

# vars
BLOCK_SIZE = 8
WIDTH = 800
HEIGHT = 450
NUM_FRAMES = 150

# quantization matrix
Q = np.array([
    [16,11,10,16,24,40,51,61],
    [12,12,14,19,26,58,60,55],
    [14,13,16,24,40,57,69,56],
    [14,17,22,29,51,87,80,62],
    [18,22,37,56,68,109,103,77],
    [24,35,55,64,81,104,113,92],
    [49,64,78,87,103,121,120,101],
    [72,92,95,98,112,100,103,99]
])

def get_quant_matrix(q):
    if q < 50:
        S = 5000.0/q
    else:
        S = 200-2.0*q
    Ts = np.floor((S*Q+50)/100.0)
    Ts[Ts == 0] = 1
    return Ts.astype(int)

Q = get_quant_matrix(50)

def frame_differences(frames):
    cur = np.zeros(frames[0].shape)
    res = []
    for frame in frames:
        res.append(frame-cur)
        cur = frame
    return res

def recon_frame_differences(diffs):
    frames = []
    cur = np.zeros(diffs[0].shape)
    for diff in diffs:
        frames.append(cur+diff)
        cur = frames[-1]
    return frames

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

def compare_frames(ori_filename, recon_filename):
    ori_frames = read_yuv(ori_filename)
    recon_frames = read_yuv(recon_filename)
    mse = []
    for ori, recon in zip(ori_frames, recon_frames):
        mse.append(np.mean((ori-recon)**2))
    return np.mean(mse)

def compare_file_sizes(uncompressed, compressed):
    return os.path.getsize(uncompressed)/float(os.path.getsize(compressed))

def show_frame(filename, i):
    frames = read_yuv(filename)
    cv2.imshow("frame", frames[i])
    cv2.waitKey()
