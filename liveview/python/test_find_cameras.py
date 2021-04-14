from ximea import xiapi

from camera_indexing import id_sn
from find_cameras import find_devices

def update_cameras():
    li = find_devices()
    new_id_sn = {}
    with open('camera_indexing.py', 'w+') as fc_file:
        fc_file.write('id_sn = { \n')
        for (k, v) in li:
            fc_file.write("{}: '{}',\n".format(k, v))
            new_id_sn[k] = v
        fc_file.write('}')
    return new_id_sn
    

def main():
    id_sn_cp = id_sn
    cam = xiapi.Camera()
    redo = 0
    while redo < 2:
        try:
            sn = id_sn_cp[0]
            cam.open_device_by('XI_OPEN_BY_SN', sn)
        except:
            redo += 1
            if redo >= 2:
                print('CANNOT FIND CAMERAS')
            else:
                id_sn_cp = update_cameras()
                if len(id_sn_cp) == 0:
                    print('CANNOT FIND CAMERAS')
                    return
            
       
        #run find_cameras and update camera indexing.

if __name__ == "__main__":
    main()
