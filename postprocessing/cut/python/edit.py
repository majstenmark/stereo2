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
from PIL import ImageFont, ImageDraw, Image  
import numpy as np
import argparse

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

    def get_frame(self, frame_no):
        self.V.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        return self.get_next()


    def set_frame_to(self, frame_no):
        self.V.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        
    def getFPS(self):
        return self.V.get(cv2.CAP_PROP_FPS)

    def get_no_frames(self):
        return int(self.V.get(cv2.CAP_PROP_FRAME_COUNT) + 0.5)
    
    def get_dims(self):

        width  = self.V.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
        height = self.V.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
        return int(width + 0.5), int(height + 0.5)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--input', action='store', required='True', help="folder of video files")
    parser.add_argument('-o', '--out', action='store', required='True', help="out-file")
    return parser.parse_args()


def addText(V, frame_no, text, xys):
    global out_folder, i
    dx = -70
    dy = -20
    ok, frame = V.get_frame(frame_no)
    if not ok:
        return
    pil_im = Image.fromarray(frame)  
    draw = ImageDraw.Draw(pil_im)  
    # use a truetype font  
    #font = ImageFont.truetype("arial.ttf", 60) 
    fontpath_alt = ['FreeMono.ttf', './python/FreeMono.ttf', './cut/python/FreeMono.ttf'] 
    fontpath = ''
    for p in fontpath_alt: 
        if os.path.exists(p): 
            fontpath = p
            break
    



    font = ImageFont.truetype(fontpath, 30)

    # Draw the text  
    draw.text((xys[0][0], xys[0][1]), text[0], font=font)  
    draw.text((xys[1][0], xys[1][1]), text[1], font=font)  
      
    # Get back the image to OpenCV  
    cv2_im_processed = np.array(pil_im)  
    #cv2.imshow('Testing', cv2_im_processed)
    #k = cv2.waitKey(1)
    return cv2_im_processed

def drawText(V, frame_no, text, xys):
    global out_folder, i
    cv2_im_processed = addText(V, frame_no, text, xys)
    #cv2.imshow('Testing', cv2_im_processed)

    old = out_folder + '/tmp{}.jpg'.format(i)
    i += 1
    fname = out_folder + '/tmp{}.jpg'.format(i)
    if path.exists(old):
        os.remove(old)
    
    
    cv2.imwrite(fname, cv2_im_processed)
    sys.stdout.write('text: {}\n'.format(fname))
    sys.stdout.flush()

    k = cv2.waitKey(1)
            
        
#IN  Cut at frame 5 EX  Cut at frame 11 IN  Cut at frame 16
def generate(V, msg, saved, outfolder):
    msg = msg.replace(' Seq from ', '')
    msg = msg.replace('to', '')
    
    li = msg.split()

    tot = V.get_no_frames()
    
    try:
        filename = outfolder + '/generated.avi'
        W, H = V.get_dims()
        fps = V.getFPS()
        codec = 'mjpg'
        out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*codec), fps, (W, H))

        pairs = [(li[3 * i].strip(), int(li[3 * i+1]), int(li[3 * i+2])) for i in range(len(li)//3)]
        
        for inex, start_no, end_no in pairs:
            text = None
            xys = []

            if inex == "IN":
                if end_no in saved:
                    text, xys = saved[end_no]
                    for intermed_frame in range(start_no, end_no + 1):
                
                        frame_with_text = addText(V, intermed_frame, text, xys)
                        out.write(frame_with_text)

                        sys.stdout.write('frame: {}/{}\n'.format(intermed_frame, tot))
                        sys.stdout.flush()
                
                else:
                    V.set_frame_to(start_no)

                    for intermed_frame in range(start_no, end_no + 1):
                        ok, frame = V.get_next()

                        if ok:
                            out.write(frame)

                            sys.stdout.write('frame: {}/{}\n'.format(intermed_frame, tot))
                            sys.stdout.flush()
            
            
            
    except:
        print('Exception')
        pass

    return None
    
def edit_file():
    global input_file
    V = Video(input_file)
    
    CHANGE_FRAME = 10
    CLOSE = 11
    ADD_TEXT= 12
    TEXT_LEFT= 13
    TEXT_RIGHT= 14
    TEXT_UP= 15
    TEXT_DOWN= 16
    TEXT_SAVE = 17

    CHANGE_DOWN = 18
    CHANGE_UP = 19

    TO_GENERATE = 20
    GENERATE = 21
    
    text = ['', '']
    W, H = V.get_dims()
    D = int(0.8 * W)
    H = 1028
    T = H//2 - (H - D)
    M = W//2
    xys = [[M, T], [M, D]]
    X_STEP = 5
    Y_STEP = 5

    even = False
    frame_no = 0
    top = True
    

    R = Runner(running = False)

    while 1:
        R.handle_cmd()
        
        if R.step == CHANGE_FRAME:
            
            frame_no = int(R.msg)
            
            if frame_no in saved:
                text, xys = saved[frame_no]
            else:
                text = ['', ''] if top else ['', '']
                xys = [[M, T], [M, D]]
             
        elif R.step == ADD_TEXT:
            msg = R.msg
            if top:
                text[0] = msg
            else:
                text[1] = msg
            

        elif R.step == TEXT_LEFT:
            if top:
                x, y = xys[0]
                xys[0] = [x - X_STEP, y]
            else:
                x, y = xys[1]
                xys[1] = [x - X_STEP, y]
            

        elif R.step == TEXT_RIGHT:
            if top:
                x, y = xys[0]
                xys[0] = [x + X_STEP, y]
            else:
                x, y = xys[1]
                xys[1] = [x + X_STEP, y]
            

        elif R.step == TEXT_UP:
            if top:
                x, y = xys[0]
                xys[0] = [x, y - Y_STEP]
            else:
                x, y = xys[1]
                xys[1] = [x, y  - Y_STEP]
            

        elif R.step == TEXT_DOWN:
            if top:
                x, y = xys[0]
                xys[0] = [x, y + Y_STEP]
            else:
                x, y = xys[1]
                xys[1] = [x, y  + Y_STEP]
            
        elif R.step == CHANGE_UP:
            top = True

        elif R.step == CHANGE_DOWN:
            top = False

        elif R.step == CLOSE:
        
            cv2.destroyAllWindows()
            k = cv2.waitKey(1)
            
            exit()

        elif R.step == TO_GENERATE:
            generate(V, R.msg, saved, out_folder)
            
            
        saved[frame_no] = text, xys
        drawText(V, frame_no, text, xys)

        R.step = 0
    

if __name__ == '__main__':
    global input_file, out_folder, i, saved
    i = 0
    saved = {} #frame id to text and xys
    arg = get_args()
    input_file, out_folder = arg.input, arg.out
    edit_file()
