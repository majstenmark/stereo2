from reader import *
from color_edit import debayer_ximea
import numpy as np
import cv2 as cv
import argparse
import subprocess
import os
from compensate import fix_couple
#p3 synchronize.py --right /Users/maj/Desktop/tmp/1.avi --left /Users/maj/Desktop/tmp/2.avi

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--left', required=True, action='store', help="left-video")
    parser.add_argument('-r', '--right', required=True, action='store', help="right-video")
    parser.add_argument('-s', '--shift', action='store', default=0, help="shift left")
    parser.add_argument('-x', '--ximea', action='store_true', help="input type")
    parser.add_argument('-d', '--ds', type=int, action='store', default=1, help="input type")
    return parser.parse_args()

def zip(l, r):
    while True:
        try:
            l_out = next(l)
            r_out = next(r)
            yield l_out, r_out
        except: break

def generate_ximea(src_l, src_r):
    for f_l, f_r in zip(read_raw(src_l), read_raw(src_r)):
        yield debayer_ximea(f_l), debayer_ximea(f_r)

def generate_regular(src_l, src_r, shift):
    #shift = 0
    fs = []
    for i, (f_l, f_r) in enumerate(zip(read_from(src_l, shift), read(src_r))):
        #fs.append((i, f_r))
        #if len(fs) > shift + 1:
        #    fs = fs[1:]
        yield (i + shift, f_l), (i, f_r)

def regenerate_regular(src_l, src_r, shift, start):
    #shift = 0
    fs = []
    for i, (f_l, f_r) in enumerate(zip(read_from(src_l, start+shift), read_from(src_r, start))):
        
        yield (start + i + shift, f_l), (start + i, f_r)

def side_by_side(src_l, src_r, ximea, ds, shift):
    dims_l, dims_r = map(get_dims, [src_l, src_r])
    fps_l, fps_r = map(get_fps, [src_l, src_r])
    assert dims_l == dims_r
    assert fps_l == fps_r
    w, h = dims_l
    
    w, h = int(w)//ds, int(h)//ds
    ow, oh = w*2, h
    if ximea:
        itr = generate_ximea(src_l, src_r)
    else:
        itr = generate_regular(src_l, src_r, shift)

    pause = False
    while True:
    #for (iL, f_l), (iR, f_r) in itr:
        def one_frame():
            
            values = next(itr, None)
            if values == None: 
                return
            (iL, f_l), (iR, f_r) = values
            
            f_l = cv2.resize(f_l, (w, h))
            f_r = cv2.resize(f_r, (w, h))
            cv.putText(f_l, 'Frame {}'.format(iL), (10,25), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 8);
            cv.putText(f_r, 'Frame {}'.format(iR), (10,25), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 8);
            total = np.hstack((f_l, f_r))
            cv.imshow('sbs', total)
            return iR, iL


        iR, iL = one_frame()
        if not pause:
            k = cv.waitKey(1)
            if k == ord(' '):
                pause = True
            if k == ord('q'):
                exit()
        while pause:
            k = cv.waitKey()
            if k == ord('q'):
                exit()
            if k == ord(' '):
                pause = False
            elif k == ord('a'):
                shift -= 1
                if iR + shift <= 0:
                    shift = 0
                itr = regenerate_regular(src_l, src_r, shift, iR)
                iR, iL = one_frame()
            elif k == ord('s'):
                shift += 1
                itr = regenerate_regular(src_l, src_r, shift, iR)
                iR, iL = one_frame()
            elif k == ord('b'):
                if iR + shift <= 0:
                    shift = 0

                itr = regenerate_regular(src_l, src_r, shift, iR-1)
                iR, iL = one_frame()
            elif k == ord('n'):
                itr = regenerate_regular(src_l, src_r, shift, iR + 1)
                iR, iL = one_frame()
            elif k == ord('v'):
                shift = max(0, shift)
                itr = regenerate_regular(src_l, src_r, shift, iR-10)
                iR, iL = one_frame()
            elif k == ord('m'):
                itr = regenerate_regular(src_l, src_r, shift, iR + 10)
                iR, iL = one_frame()
            elif k == ord('g'):
                in_f = os.path.dirname(src_l) 
                fix_couple(in_f, in_f, in_f, shift, 0)
            elif k == 3:
                break
            



if __name__ == '__main__':
    args = get_args()
    side_by_side(args.left, args.right, args.ximea, args.ds, max(0, int(args.shift)))



