import sys
import cv2
from collections import deque, defaultdict
from threading  import Thread
import traceback
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty  # python 2.x

import numpy as np
import timing
import subprocess

class VideoStream:
    def __init__(self,
            cam_id,
            fps=25.0,
            debug=True):

        self.cam_id = cam_id + 1
        self.finished = False
        self.started = False
        self.dt = int(1e6/fps)
        self.fps = 10.**6/self.dt
        self.debug = debug
        self.sending = False
        self.err = sys.stderr
        self.stdout = sys.stdout
        sys.stdout = sys.stderr
        self.q = Queue()
        def enqueue_input(queue):
            for line in iter(sys.stdin.readline, b''):
                queue.put(line.strip())

        t = Thread(target=enqueue_input, args=(self.q,))
        t.daemon = True
        t.start()
        v = 'rtsp://root:pass@192.168.0.90:554/axis-media/media.amp?videocodec=&camera={}&resolution:640x480'

    def __setup(self):
        h, w = 2056, 2464
        self.h, self.w = h, w
        base_url = 'rtsp://root:pass@192.168.0.90:554/axis-media/media.amp?videocodec=h264'
        self.url = '{}&camera={}&resolution:640x480'.format(base_url, self.cam_id)
        self.subp = None
        self.recording=False

    def __teardown(self):
        self.__log('closing')
        self.__log('closed')
        self.started = False
        self.finished = True

    
    def __log(self, s):
        self.err.write('{}: {}\n'.format(self.cam_id, s))

    def handle_cmd(self, cmd):
        c = cmd[0]
        if c == 'q':
            self.running = False
            if self.recording:
                self.subp.terminate()
                self.recording = False
        elif c == 'r':
            if self.recording:
                self.subp.terminate()
                self.recording = False
            self.recording = True
            cmdarr = cmd.split()

            self.tstart = int(cmdarr[1])
            self.end = int(cmdarr[2])
            path = ' '.join(cmdarr[3:]).rstrip('/')
            w_file = '{}/{}.avi'.format(path, self.cam_id)
            self.subp = subprocess.Popen(['ffmpeg', '-i', self.url, w_file])
            
        elif c == 's':
            if self.recording:
                self.recording = False
                self.subp.terminate()
        elif c == 'a':
            self.sending = True
            self.video = cv2.VideoCapture(self.url)
        elif c == 'd':
            if self.sending:
                self.video.release()
            self.sending = False
        elif c == 'e':
            pass

        else:
            self.__log('Unknown cmd: {}'.format(cmd))

    def send_img(self, img):
        def i2ba(n):
            v = []
            for i in range(4):
                lo = n >> (i*8)
                v.append(lo&255)
            return v
        w, h = img.shape[1], img.shape[0]
        self.stdout.write(''.join(chr(x) for x in i2ba(w)))
        self.stdout.write(''.join(chr(x) for x in i2ba(h)))
        s = img.flatten().tobytes()
        self.stdout.write(s)
        self.stdout.flush()
    
    def update(self):
        self.__setup()
        self.running = True
        if self.finished: return
        try:
            while self.running:
                try:
                    line = self.q.get_nowait()
                    while 1:
                        self.handle_cmd(line)
                        line = self.q.get_nowait()
                except Empty:
                    pass
                if self.sending:
                    ok, img = self.video.read()
                    try:
                        self.send_img(img)
                    except IOError:
                        pass

        except Exception as e:
            self.err.write('{}\n'.format(traceback.format_exc()))

        self.__log('stopping acqusition...')

        self.__teardown()
        if self.recording:
            self.recording = False
            self.out.release()


    def start(self):
        if self.started:
            self.__log("already started!!")
            return None
        if self.finished:
            self.__log("camera finished")
            return None
        self.started = True
        self.update()

import argparse
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', type=int, required=True, help="id of camera")
    parser.add_argument('-e', '--exposure', type=int, required=True, help="exposuretime")
    parser.add_argument('-s', '--start', type=int, required=True, help="starttime")
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    v = VideoStream(args.id)
    v.start()
