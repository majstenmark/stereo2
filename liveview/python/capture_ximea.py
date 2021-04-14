from ximea import xiapi
import sys
import cv2
from collections import deque, defaultdict
from threading  import Thread
import traceback
try:
    from queue import Queue, Empty
    PYV = 3

    print('PVV 3')
except ImportError:
    from Queue import Queue, Empty  # python 2.x
    PYV = 2
    print('PVV 2')

import numpy as np
import timing
from CameraWrapper import CameraWrapper

class Writer:
    def __init__(self, out, log_file):
        self.out = out
        self.log_file = log_file
    def write(self, img, t0, img_t0):
        self.out.write(img)
        open(self.log_file, 'a').write('{} {}\n'.format(t0, img_t0))
    def release(self):
        self.out.release()

class VideoStream:
    def __init__(self,
            cam_id,
            downsample=2,
            exposuretime=10000,
            fps=40.0,
            debug=True,
            t0=0,
            is_master=False,
            convert_id=False):

        #self.cam = cam
        self.convert_id = convert_id
        self.cam_id = cam_id + 1
        self.master = is_master
        self.dt = int(1e6/fps)
        self.fps = 10.**6/self.dt
        self.t0 = t0
        if PYV == 3:
            self.stdout = sys.stdout.buffer
        else:
            self.stdout = sys.stdout

        sys.stdout = sys.stderr
        self.err = sys.stderr
        self.q = Queue()
        def enqueue_input(queue):
            for line in iter(sys.stdin.readline, b''):
                queue.put(line.strip())

        t = Thread(target=enqueue_input, args=(self.q,))
        t.daemon = True
        t.start()
        self.cam = CameraWrapper(cam_id, downsample, exposuretime, is_master, convert_id)
        self.cam.setup()
        self.__log('is_master: {}'.format(is_master))
        self.__log(downsample)
    
    
    def __log(self, s):
        self.err.write('{}: {}\n'.format(self.cam_id, s))
        self.err.flush()

    def handle_cmd(self, cmd):
        cmdarr = cmd.split()
        c = cmdarr[0]
        if c == 'quit':
            self.running = False
            if self.recording:
                self.writer.release()
                self.recording = False
        elif c == 'record':
            if self.recording:
                self.writer.release()
                self.recording = False
            self.recording = True

            self.tstart = int(cmdarr[1])
            self.__log("Starting Recoring in {} ms".format(int(self.tstart - timing.micros())//1000))
            path = ' '.join(cmdarr[2:]).rstrip('/')
            out = cv2.VideoWriter('{}/{}.avi'.format(path, self.cam_id), 0, self.fps, (self.cam.w, self.cam.h), False)
            self.writer = Writer(out, '{}/{}.log'.format(path, self.cam_id))
        elif c == 'stop':
            if self.recording:
                self.recording = False
                self.writer.release()
        elif c == 'exposure':
            self.exposuretime = int(cmdarr[-1])
            self.cam.set_exposure(self.exposuretime)
        elif c == 'downsample':
            if self.recording:
                self.recording = False
                self.writer.release()
            self.downsample = int(cmdarr[-1])
            self.__log("Downsample: {}".format(self.downsample))
            self.cam.restart()
            self.img = xiapi.Image()
        elif c == 'fps':
            if not self.recording:
                self.t0 = int(cmdarr[2])
                self.dt = int(1e6/float(cmdarr[1]))
                self.fps = 10.**6/self.dt
                self.cntr = 0

        else:
            self.__log('Unknown cmd: {}'.format(cmd))

    def send_img(self, img):

        def i2ba(n):
            v = []
            for i in range(4):
                lo = n >> (i*8)
                v.append(lo&255)
            return v

        if PYV == 3:
            self.stdout.write(bytes(i2ba(img.width)))
            self.stdout.write(bytes(i2ba(img.height)))
        else:
            self.stdout.write(''.join(chr(x) for x in i2ba(img.width)))
            self.stdout.write(''.join(chr(x) for x in i2ba(img.height)))

        self.stdout.write(img.get_image_data_raw())
        self.stdout.flush()

    def correct_time(self, t2):
        c = 0
        if self.t0 < t2:
            dx = t2 - self.t0
            rounds = (dx + self.dt - 1)//self.dt
            self.__log('Correcting {}'.format(rounds))
            self.t0 += rounds*self.dt
            self.cntr += rounds
            c += 1
        if t2 < self.t0 - self.dt:
            self.t0 -= self.dt
            self.cntr -= 1
            self.__log("BackCorrecting")
            c += 1
        if c > 1:
            self.__log("Double?! {} {}".format(self.t0, t2))
    
    def read_mail(self):
        try:
            while True:
                line = self.q.get_nowait()
                self.handle_cmd(line)
        except Empty:
            pass


    
    def update(self):
        timeout = 30 if self.master else 100
        try:
            self.img = xiapi.Image()
            self.cntr = 0
            self.running = True
            self.recording = False
            timeout_streak = 0
            while self.running:
                got_img = False
                if self.t0 > timing.micros() + 10**5:
                    timing.sleep_until(self.t0 - 2*10**4)
                if self.master:
                    t1 = timing.wait_until(self.t0)
                    self.cam.set_trigger_software(1)
                try:
                    self.cam.get_image(self.img, timeout=timeout)
                    self.cntr += 1
                    self.t0 += self.dt
                    t2 = int(timing.micros())
                    got_img = True
                    timeout_streak = 0
                except Exception as e:
                    self.__log(traceback.format_exc())
                    timeout_streak += 1
                    self.__log('timeout streak: {}'.format(timeout_streak))
                    if timeout_streak > 10:
                        timeout_streak = 0
                        self.t0 += self.dt*500
                        self.cntr += 500
                        self.cam.restart()
                        self.img = xiapi.Image()
                if got_img:
                    self.correct_time(t2)

                    if self.recording and self.t0 > self.tstart: # and self.t0 - dt < t2:
                        self.writer.write(self.img.get_image_data_numpy(), t2, self.img.tsSec*10**6 + self.img.tsUSec)
                    self.send_img(self.img)

                self.read_mail()

                if self.cntr%(int(self.fps)) == 0 and got_img:
                    self.__log('received {} {} fps {}'.format(t2, self.t0 - self.dt, self.fps))

        except Exception as e:
            self.err.write('{}\n'.format(traceback.format_exc()))

        self.__log('stopping acqusition...')

        self.cam.teardown()
        if self.recording:
            self.recording = False
            self.writer.release()

import argparse
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', type=int, required=True, help="id of camera")
    parser.add_argument('-s', '--start', type=int, help="start time of cameras")
    parser.add_argument('-d', '--downsample', type=int, default=2, help="downsample images")
    parser.add_argument('-e', '--exposure', type=int, default=10000, help="exposure time of cameras in micro seconds")
    parser.add_argument('-f', '--fps', type=int, default=25, help="frames per second of cameras")
    parser.add_argument('--convert_id', action='store_true', help="convert ids with LUT")
    parser.add_argument('--one_master', action='store_true', help="camera 0 is master")
    parser.add_argument('--all_master', action='store_true', help="all master-cam")
    parser.add_argument('--all_slave', action='store_true', help="all slave-cam")
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    if args.start == None:
        args.start = timing.micros() + 10**6
    cnt = 0
    master = False
    if args.one_master:
        cnt += 1
        master = True and args.id == 0
    if args.all_master:
        cnt += 1
        master = True
    if args.all_slave: cnt += 1
    assert cnt == 1

    v = VideoStream(args.id,
            t0=args.start,
            downsample=args.downsample,
            exposuretime=args.exposure,
            is_master=master,
            convert_id=args.convert_id,
            fps=args.fps)
    if not v.cam.open:
        raise ConnectionError('NO CAMERA CONNECTED')
    v.update()


