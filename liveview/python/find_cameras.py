#!/usr/bin/env python3

from ximea import xiapi

def find_devices():
    i = 0
    li = []
    while 1:
        try:
            c = xiapi.Camera(i)
            c.set_debug_level('XI_DL_DISABLED')
            c.open_device()
            li.append((i, c.get_device_sn()))
            c.close_device()
        except:
            break
        i += 1
    return li
    

def main():    
    li= find_devices()
    for i, id, in li:
       print(i, id)
    if len(li) == 0:
        print('NO CAMERAS FOUND')

if __name__ == "__main__":
    main()