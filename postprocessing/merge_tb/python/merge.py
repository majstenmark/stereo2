import numpy as np
import cv2 as cv
import argparse
import reader
import glob, os, sys
import os.path
from os import path
import gen_table
from progress.bar import Bar
from input_handler import Runner
import datetime

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', action='store', required='True', help="folder of video files")
    parser.add_argument('-o', '--out', action='store', required='True', help="out-file")
    parser.add_argument('-s', '--single', action='store', required='True', help="true = merge into singe out file, false = merge into multiple files")
    parser.add_argument('-t', '--top', action='store', default='right', help="right or left, right default")
    
    return parser.parse_args()


def zip(l, r):
    while True:
        try:
            l_out = next(l)
            r_out = next(r)
            yield l_out, r_out
        except: break


def top_bottom(src_r, src_l, R, video, left_top = False):
    i, tot = 0, max(reader.get_no_frames(src_l), reader.get_no_frames(src_r))
    print('HERE')
    for f_r, f_l in zip(reader.read(src_r), reader.read(src_l)):
        f_r = f_r[::2]
        f_l = f_l[::2]
        total = None
        if left_top:
            total = np.vstack((f_l, f_r))
        else:
            total = np.vstack((f_r, f_l))
        video.write(total)
        cv.imshow('Merging ...', total)
        cv.waitKey(1)
        i+=1
        sys.stdout.write('frame: {} {}\n'.format(i, tot))
        sys.stdout.flush()
        R.handle_cmd()

    
def merge_folders(folder, out_folder, single, top):

    out_folder = out_folder.rstrip('/')
    try:
        os.makedirs(out_folder)
    except: pass
    end = 'avi'
    files = sorted(list(glob.glob('{}/**/*.{}'.format(folder, end))) + list(glob.glob('{}/*.{}'.format(folder, end))))
    
    tasks = []
    NO = "out"
    fix_miss = "missing"
    for f_name in files:
        splitted = f_name.split('/')
        video_name = splitted[-1]
        prefix = '/'.join(splitted[0:-1])
        if video_name == '1.' + end:
            dst = 'merged.' + end
            
            tasks.append((prefix, '1.' + end, '2.' + end, dst))

        if video_name == '1_timealigned.' + end:
            tasks.append((prefix, '1_timealigned.' + end, '2_timealigned.' + end, dst))
    i, tot = 0, len(tasks)
    R = Runner()
    
    i, tot = 0, len(tasks)
    video = None
    
    for (prefix, right, left, dst) in tasks:

        i += 1
        src_l =  prefix + '/' + left
        src_r = prefix + '/' + right
        name = prefix.replace('/', '_')

        if name[0] == '_': name = name[1:]
        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d %H.%M.%S")

        dest = out_folder +'/' + now_str + ' ' + dst if single else out_folder +'/' + name + '_' + dst


        if (single and video == None) or not single:
            dims_l, dims_r = map(reader.get_dims, [src_l, src_r])
            fps_l, fps_r = map(reader.get_fps, [src_l, src_r])
            assert dims_l == dims_r
            assert fps_l == fps_r
            w, h = dims_l
            w, h = int(w), int(h)
            video = cv.VideoWriter(dest, cv.VideoWriter_fourcc(*'mjpg'), fps_l, (w, h))
            

    
        i += 1
    
        S = "file: {} {} {}\n".format(i, tot, prefix)
        sys.stdout.write(S)
        sys.stdout.flush()
        top_bottom(src_r, src_l, R, video, top == 'left')
        if not single:
            video.release()
        


if __name__ == '__main__':
    arg = get_args()
    single = arg.single.lower() == 'true'
    merge_folders(arg.folder, arg.out, single, arg.top)
