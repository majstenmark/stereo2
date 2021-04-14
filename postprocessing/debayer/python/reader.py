import cv2

def read(vid_file):
    v = cv2.VideoCapture(vid_file)
    ok, frame = v.read()
    while ok:
        yield frame
        ok, frame = v.read()
    v.release()

def read_raw(vid_file):
    for frame in read(vid_file):
        yield frame[:,:,0]

def read_png(folder, cam_id):
    import glob
    import magic
    files = sorted(glob.glob('{}/shot{}.*.png'.format(folder, cam_id)))
    for f in files:
        if 'png' in magic.from_file(f).lower():
            yield cv2.imread(f, False)


def get_dims(vid_file):
    v = cv2.VideoCapture(vid_file)
    t = int(v.get(cv2.CAP_PROP_FRAME_WIDTH)), int(v.get(cv2.CAP_PROP_FRAME_HEIGHT))
    v.release()
    return t

def get_no_frames(vid_file):
    v = cv2.VideoCapture(vid_file)
    t = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
    v.release()
    return t


def get_fps(vid_file):
    v = cv2.VideoCapture(vid_file)
    fps = int(v.get(cv2.CAP_PROP_FPS))
    v.release()
    return fps

def get_no_frames(vid_file):
    v = cv2.VideoCapture(vid_file)
    no = v.get(cv2.CAP_PROP_FRAME_COUNT)
    return int(no)

