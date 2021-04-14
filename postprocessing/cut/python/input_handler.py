import time, sys

from threading  import Thread
try:
    from queue import Queue, Empty
    PYV = 3
except ImportError:
    from Queue import Queue, Empty  # python 2.x
    PYV = 2
class Runner:
    def __init__(self, running = True):
        self.Q = Queue()
        self.step = 0
        self.msg = ''
        def enqueue_input(queue):
            for line in iter(sys.stdin.readline, b''):
                queue.put(line.strip())

        t = Thread(target=enqueue_input, args=(self.Q,))
        t.daemon = True
        t.start()
        self.running = running

    def handle_cmd(self):
        while True:
            try:
                line = self.Q.get_nowait()
                self.running = line == '1'
            except:
                break
        while not self.running and self.step == 0:
            line = self.Q.get()
            self.running = line == '1'
            if int(line) > 1:
                self.step = int(line)
                if self.step == 12 or self.step == 10 or self.step == 20:
                    #Add text!
                    self.msg = self.Q.get()
            else:
                self.step = 0


if __name__ == '__main__':
    R = Runner()

    for i in range(1000):
        print('file: x.avi')
        print('frame: {}/{}'.format(i, 999))
        time.sleep(0.5)
        R.handle_cmd()
