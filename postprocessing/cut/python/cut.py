import numpy as np
import cv2 as cv
import cv2
import argparse
import reader
import glob, os, sys
import os.path
from os import path
import gen_table
from progress.bar import Bar
from input_handler import Runner
import datetime

class Video:
    def __init__(self, uri):
        self.V = cv2.VideoCapture(uri)

    def get_next(self):
        ok, frame = self.V.read()
        return ok, frame


    def get_current(self):
        f_i = int(self.V.get(cv2.CAP_PROP_POS_FRAMES))
        self.V.set(cv2.CAP_PROP_POS_FRAMES, f_i -1)
        ok, frame = self.V.read()
        return ok, frame
    
    def get_previous(self):
        
        f_i = int(self.V.get(cv2.CAP_PROP_POS_FRAMES))
        f = max(0, f_i -2)
        self.V.set(cv2.CAP_PROP_POS_FRAMES, f)
        ok, frame = self.V.read()
        return ok, frame

    def back(self):
        f_i = int(self.V.get(cv2.CAP_PROP_POS_FRAMES))
        B = max(0, f_i - 2)
        self.V.set(cv2.CAP_PROP_POS_FRAMES, B)
    
    def frameNo(self):
        return max(0, int(self.V.get(cv2.CAP_PROP_POS_FRAMES)) -1)

    def getFPS(self):
        return self.V.get(cv2.CAP_PROP_FPS)

    def get_no_frames(self):
        return int(self.V.get(cv2.CAP_PROP_FRAME_COUNT) + 0.5)

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--input', action='store', required='True', help="folder of video files")
    parser.add_argument('-o', '--out', action='store', required='True', help="out-file")
    
    return parser.parse_args()


def zip(l, r):
    while True:
        try:
            l_out = next(l)
            r_out = next(r)
            yield l_out, r_out
        except: break


def quit():
    global cuts
    
    log = open(log_file, 'w+')
    for cut in cuts:
        log.write('{} {}\n'.format(cut[0], cut[1]))
    log.close()
    exit()

    
def cut_file(inputfile, out_folder):
    
    out_folder = out_folder.rstrip('/')
    try:
        os.makedirs(out_folder)
    except: pass
    V = Video(inputfile)
    log_file = "temp_log.log"
    pause = False
    #ok = True
    cuts = []
    R = Runner()
    tot = V.get_no_frames()
    last_cut = 0

    fps = int(V.getFPS() + 0.5)

    while 1:
        if not pause:
                
            ok, frame = V.get_next()
            if not ok: break
            i =V.frameNo()
            cv2.putText(frame, str(i), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
            cv2.imshow('frame', frame)

            sys.stdout.write('frame: {} {}\n'.format(i, tot))
            sys.stdout.flush()
            k = cv2.waitKey(1)
        #sys.stdout.write('frame: {} {}\n'.format(0, tot))
        #sys.stdout.flush()
        R.handle_cmd()
        if R.step > 0:
            # Handle step!
            
            if R.step == 2:
                #back

                ok, frame = V.get_previous()
                if not ok: break
                i =V.frameNo()
                cv2.putText(frame, str(i), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
                cv2.imshow('frame', frame)

                sys.stdout.write('frame: {}\n'.format(i, tot))
                sys.stdout.flush()
                k = cv2.waitKey(1)
                

            elif R.step == 3:
                #forward

                ok, frame = V.get_next()
                if not ok: break
                i = V.frameNo()
                cv2.putText(frame, str(i), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
                cv2.imshow('frame', frame)

                sys.stdout.write('frame: {} {}\n'.format(i, tot))
                sys.stdout.flush()
                k = cv2.waitKey(1)
            elif R.step == 4:
                #add cut!
                ok, frame2 = V.get_current()
                if not ok: break
                now = datetime.datetime.now()
        
                now_str = now.strftime("%Y-%m-%d %H.%M.%S")
                i = V.frameNo()
                dest = out_folder +'/cut_{}.jpg'.format(i)

                cv2.imwrite(dest, frame2)
                sys.stdout.write('image: {}\n'.format(dest))
                sys.stdout.flush()
                #write down
            elif R.step == 5:
                 cv2.destroyAllWindows()
                 exit()



            R.step = 0
            pause = True
        else:
            pause = False

    

if __name__ == '__main__':
    arg = get_args()
    cut_file(arg.input, arg.out)
