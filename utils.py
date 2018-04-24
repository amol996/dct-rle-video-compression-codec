import numpy as np

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
