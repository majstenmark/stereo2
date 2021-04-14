import sys
import cv2
from threading  import Thread
import traceback
try:
    from queue import Queue, Empty
    PYV = 3
except ImportError:
    from Queue import Queue, Empty  # python 2.x
    PYV = 2

import numpy as np
import timing

class VideoStream:
    def __init__(self,
            cam_id,
            output_prefix,
            formt='XI_RAW8',
            codec='RAW',
            downsample=2,
            exposuretime=10000,
            fps=25.0,
            debug=True,
            t0=0):

        self.cam_id = cam_id + 1
        self.exposuretime = exposuretime
        self.t0 = t0
        self.dt = int(1e6/fps)
        self.fps = 10.**6/self.dt
        self.err = sys.stderr
        if PYV == 3:
            self.stdout = sys.stdout.buffer
        else:
            self.stdout = sys.stdout
        self.sending = False
        sys.stdout = sys.stderr
        self.q = Queue()
        def enqueue_input(queue):
            for line in iter(sys.stdin.readline, b''):
                queue.put(line.strip())

        t = Thread(target=enqueue_input, args=(self.q,))
        t.daemon = True
        t.start()

    def __setup(self):
        pass
        

    def __teardown(self):
        self.__log('closed')
    
    def __log(self, s):
        self.err.write('{}: {}\n'.format(self.cam_id, s))

    def handle_cmd(self, cmd):
        c = cmd[0]
        if c == 'q':
            self.running = False
        elif c == 'r':
            self.__log("got cmd: record")
        elif c == 's':
            self.__log("got cmd: stop record")
        elif c == 'a':
            self.sending = True
        elif c == 'd':
            self.sending = False
        elif c == 'e':
            self.__log("got cmd: ch exptime")
        else:
            self.__log('Unknown cmd: {}'.format(cmd))


    def send(self, img):
        def i2ba(n):
            v = []
            for i in range(4):
                lo = n >> (i*8)
                v.append(lo&255)
            return v
        w, h = img.shape[1], img.shape[0]
        if PYV == 3:
            self.stdout.write(bytes(i2ba(w)))
            self.stdout.write(bytes(i2ba(h)))
        else:
            self.stdout.write(''.join(chr(x) for x in i2ba(w)))
            self.stdout.write(''.join(chr(x) for x in i2ba(h)))
        s = img.flatten().tobytes()
        assert len(s) == w*h
        self.stdout.write(s)
        self.stdout.flush()

    
    def update(self):
        self.__setup()
        names = ['R', 'L']
        vid_file = "mock-stream/cam_{}.mp4".format(names[self.cam_id - 1])
        v = cv2.VideoCapture(vid_file)
        cnt = 0
        try:
            dt = self.dt
            have_fst = True
            self.running = True
            self.recording = False
            timeout_streak = 0
            while self.running:
                try:
                    line = self.q.get_nowait()
                    while 1:
                        self.handle_cmd(line)
                        line = self.q.get_nowait()
                except Empty:
                    pass
                t1 = timing.wait_until(self.t0)
                self.t0 += dt
                try:
                    ok, img = v.read()
                    if not ok:
                        v.release()
                        v = cv2.VideoCapture(vid_file)
                        ok, img = v.read()
                    self.send(img[:,:,0])
                except IOError:
                    pass

                cnt += 1

        except Exception as e:
            self.err.write('{}\n'.format(traceback.format_exc()))

        self.__log('stopping acqusition...')

        self.__teardown()


    def start(self):
        self.update()

import argparse
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', type=int, help="id of camera")
    parser.add_argument('-s', '--start', type=int, help="start time of cameras")
    parser.add_argument('-d', '--downsample', type=int, default=2, help="start time of cameras")
    parser.add_argument('-e', '--exposure', type=int, default=10000, help="exposure time fo cameras in micro seconds")
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    v = VideoStream(args.id, 'out', t0=args.start, downsample=args.downsample, exposuretime=args.exposure)
    v.start()


