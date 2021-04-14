import time, sys

from threading  import Thread
try:
    from queue import Queue, Empty
    PYV = 3
except ImportError:
    from Queue import Queue, Empty  # python 2.x
    PYV = 2
class Runner:
    def __init__(self):
        self.Q = Queue()
        def enqueue_input(queue):
            for line in iter(sys.stdin.readline, b''):
                queue.put(line.strip())

        t = Thread(target=enqueue_input, args=(self.Q,))
        t.daemon = True
        t.start()
        self.running = True     

    def handle_cmd(self):
        while True:
            try:
                line = self.Q.get_nowait()
                self.running = line == '1'
            except:
                break
        while not self.running:
            line = self.Q.get()
            self.running = line == '1'

if __name__ == '__main__':
    R = Runner()

    for i in range(1000):
        print('file: x.avi')
        print('frame: {}/{}'.format(i, 999))
        time.sleep(0.5)
        R.handle_cmd()
