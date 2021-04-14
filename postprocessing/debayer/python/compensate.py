import numpy as np
import cv2 as cv
import argparse
import reader
import color_edit
import glob, os, sys
import gen_table
from progress.bar import Bar
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder')
    parser.add_argument('-s', '--shift', default='', action='store', help="how2shift")
    return parser.parse_args()


def get_start(folder):
    logs = glob.glob('{}/*.log'.format(folder))
    print(logs, folder)
    start = min([int(open(log, 'r').readline().split()[0]) for log in logs])
    return start

def get_log_file(vid_file):
    return vid_file.replace('.avi', '.log')


def compensate(log_file, fps, start):
    if '.avi' in log_file:
        log_file = get_log_file(log_file)
    dt = int(10**6/fps)
    dt_h = dt//2
    X = open(log_file).read().split('\n')
    v = [int(l.split()[0]) for l in X if l]
    add = 0
    M = 0
    out = {}
    for i in range(len(v)):
        diff = v[i] - start - (i+add)*dt
        old_add = add
        while diff > dt_h:
            add += 1
            diff -= dt
        while diff <= -dt_h:
            add -= 1
            diff += dt
        out[i] =  add-old_add
        M = max(M, abs(diff))
    return out

def fadeIn(img1, img2, out, L=10):
    for IN in range(1,L+1):
        fadein = IN/float(L+1)
        dst = cv.addWeighted( img1, 1-fadein, img2, fadein, 0)
        out.write(dst)

def fix(src, log, dst, shift):
    dims = reader.get_dims(src)
    fps = reader.get_fps(src)
    fourcc = cv.VideoWriter_fourcc(*"X264")
    out = cv.VideoWriter(dst, fourcc, fps, dims)
    vals = compensate(log, fps)
    last = None
    b = Bar(max=len(vals))
    for i, frame in enumerate(reader.read(src)):
        if shift > i: continue
        if vals[i] < 0: continue
        if vals[i]:
            L = vals[i]
            fadeIn(last, frame, out, L)
        last = frame
        out.write(frame)
        b.next()
    b.finish()
    out.release()

def fix_couple(in_f, log_f, out_f, shift_1=0, shift_2=0):
    for i, shift in zip("12", [shift_1, shift_2]):
        src = '{}/{}'.format(in_f, '{}.avi'.format(i))
        log = '{}/{}'.format(log_f, '{}.log'.format(i))
        dst = '{}/{}'.format(out_f, '{}_timealigned.avi'.format(i))
        fix(src, log, dst, shift)



if __name__ == '__main__':
    args = get_args()
    try:
        os.mkdir(args.out)
    except: pass
    shift = args.shift
    shift_l = 0
    shift_r = 0
    if 'l' in shift:
        shift_l = int(shift[1:])
    elif 'r' in shift:
        shift_r = int(shift[1:])
    f = args.folder.rstrip('/')
    fix_couple(f, f, f, shift_l, shift_r)

