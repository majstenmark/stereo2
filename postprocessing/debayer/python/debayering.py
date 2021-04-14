import numpy as np
import cv2 as cv
import argparse
import reader
import glob, os, sys
import gen_table
from input_handler import Runner
import compensate

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('infolder')
    parser.add_argument('-o', '--out', action='store', default='.', help="output folder")
    return parser.parse_args()

def debayer_LUT_8(img, LUT):
    deb = cv.cvtColor(img, cv.COLOR_BayerRG2BGR)
    return LUT[deb[:,:,0], deb[:,:, 1], deb[:,:,2]]

def debayer_LUT_32(img, LUT):
    deb = cv.cvtColor(img, cv.COLOR_BayerRG2BGR)
    b, g, r = cv.split(deb)
    w = np.zeros(b.shape, dtype=np.uint8)
    padded = cv.merge([r, g, b, w])
    rgb = padded.view(np.uint32)
    mapped = np.take(LUT, rgb)
    #mapped.resize(b.shape)
    X = mapped.view(np.uint8)
    #X.resize(padded.shape)
    _, b, g, r = cv.split(X)
    return cv.merge([b, g, r])

def shrink(w, h):
    sz = 640
    if w > h:
        new_w = sz
        new_h = sz*h//w
    else:
        new_h = sz
        new_w = sz*w//h
    return new_h, new_w

def debayer_ximea_file(src, dest, LUT, R, start):
    dims = reader.get_dims(src)
    fps = reader.get_fps(src)
    fourcc = cv.VideoWriter_fourcc(*"mjpg")
    out = cv.VideoWriter(dest, fourcc, fps, dims)
    vals = compensate.compensate(src, fps, start)

    i, tot = 0, reader.get_no_frames(src)
    last = None

    for frame in reader.read_raw(src):
        img = debayer_LUT_32(frame, LUT)
        if vals[i] < 0:
            last = img
            i+= 1
            continue
        if vals[i]:
            L = vals[i]
            if i == 0:
                compensate.fadeIn(img, img, out, L)
            else:
                compensate.fadeIn(last, img, out, L)
        last = img
        out.write(img)
        w, h, _ = img.shape
        img2 = cv.resize(img, shrink(w, h))
        cv.imshow("debayering", img2)
        cv.waitKey(1)
        i+=1
        sys.stdout.write('frame: {} {}\n'.format(i, tot))
        sys.stdout.flush()
        R.handle_cmd()

def int2rgb(n):
    r = (n&0xFF0000) >> 16
    g = (n&0xFF00) >> 8
    b = (n&0xFF)
    return r, g, b

def get_LUT_8():
    LUT = gen_table.get_raw_table()
    LUT.resize((256, 256, 256, 3))
    return LUT
    mapped = LUT[rgb]

def get_LUT_32():
    LUT = gen_table.get_raw_table()
    LUT.resize((256**2, 256, 3))
    b, g, r = cv.split(LUT)
    w = np.zeros(b.shape, dtype=np.uint8)
    LUT = cv.merge([w, b, g, r])
    LUT.resize((256**3, 4))
    LUT = LUT.view(np.uint32)
    LUT.resize((256**3,))
    return LUT

def debayer_all(in_f, out_f):
    in_f = in_f.rstrip('/')
    out_f = out_f.rstrip('/')
    try:
        os.makedirs(out_f)
    except: pass
    files = list(glob.glob('{}/*.avi'.format(in_f))) + list(glob.glob('{}/**/*.avi'.format(in_f)))
    tasks = []
    for f_name in sorted(files):
        suff = f_name[len(in_f) + 1:]
        suff_folder = '/'.join(suff.split('/')[:-1])
        full_suff_folder = '{}/{}'.format(out_f, suff_folder)
        dst = '{}/{}'.format(out_f, suff)
        tasks.append((f_name, dst, full_suff_folder))

    LUT = get_LUT_32()
    R = Runner()
    i, tot = 0, len(tasks)
    for src, dst, folder in tasks:
        start = compensate.get_start('/'.join(src.split('/')[:-1]))
        i += 1
        S = "file: {} {} {}\n".format(i, tot, src)
        sys.stdout.write(S)
        sys.stdout.flush()
        try:
            os.makedirs(folder)
        except: pass
        debayer_ximea_file(src, dst, LUT, R, start)

    


if __name__ == '__main__':
    args = get_args()
    debayer_all(args.infolder, args.out)
