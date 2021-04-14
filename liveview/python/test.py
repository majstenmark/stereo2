from ximea import xiapi
import sys
import cv2
from collections import deque, defaultdict
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
from CameraWrapper import CameraWrapper

print('Imported')