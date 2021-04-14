import numpy as np
import cv2 as cv
import sys
from color_edit import fix_cols
from progress.bar import Bar

def get_raw_table():
    cache_fname = 'raw_table.data'
    def read_table(cache_fname):
        S = open(cache_fname, 'rb').read()
        LUT = np.frombuffer(S, dtype=np.uint8)
        assert LUT.shape == (3*256**3,), "LUT.shape {}".format(LUT.shape)
        return LUT
    try:
        LUT = read_table(cache_fname)
        return LUT
    except:
        gen_raw_table(cache_fname)
        LUT = read_table(cache_fname)
        return LUT

def gen_raw_table(cache_fname):
    f = open(cache_fname, 'wb')
    img = np.zeros((256*256, 256, 3), dtype=np.uint8)
    for b in range(256):
        for g in range(256):
            for r in range(256):
                img[b*256 + g, r, 0] = np.uint8(b)
                img[b*256 + g, r, 1] = np.uint8(g)
                img[b*256 + g, r, 2] = np.uint8(r)
    conv = fix_cols(img)
    f.write(conv.flatten().tobytes())
    f.close()

