from ximea import xiapi

class CameraWrapper:
    def __init__(self,
            cam_id,
            downsample=2,
            exposuretime=10000,
            is_master=False,
            convert_id=False):

        self.open = False
        self.accing = False
        self.convert_id = convert_id
        self.cam_id = cam_id + 1
        self.master = is_master
        self.downsample = downsample
        self.exposuretime = exposuretime
    
    def set_downsample(self, downsample):
        self.downsample = downsample
        self.restart()

    def set_exposure(self, exptime):
        self.exposuretime = exptime
        self.cam.set_exposure(exptime)

    def setup(self):
        if self.open or self.accing:
            self.teardown()
        self.H, self.W = 2056, 2464
        try:
            if self.convert_id:
                self.cam = xiapi.Camera() 
                cam = self.cam
                cam.set_debug_level('XI_DL_DISABLED')
                from camera_indexing import id_sn
                redo = 0
                while redo < 2:
                    try:
                        sn = id_sn[self.cam_id]
                        cam.open_device_by('XI_OPEN_BY_SN', sn)
                    except:
                        redo += 1
                        if redo >= 2:

                            raise('CANNOT FIND CAMERAS')
                        else:
                            id_sn_cp = update_cameras()
                            if len(id_sn_cp) == 0:
                                raise('CANNOT FIND CAMERAS')
                                

            else:
                self.cam = xiapi.Camera(self.cam_id -1)
                cam = self.cam
                cam.set_debug_level('XI_DL_DISABLED')
                cam.open_device()
            self.open = True
            
        except:
            return
        downsample = self.downsample
        cam.set_downsampling('XI_DWN_{}x{}'.format(downsample, downsample))
        self.h, self.w = self.H//downsample, self.W//downsample
        cam.set_gpi_selector('XI_GPI_PORT1')
        cam.set_gpi_mode('XI_GPI_TRIGGER')
        if self.master:
            cam.set_trigger_source('XI_TRG_SOFTWARE')
            cam.set_gpo_selector('XI_GPO_PORT1')
            cam.set_gpo_mode('XI_GPO_EXPOSURE_ACTIVE')    
        else:
            cam.set_trigger_source('XI_TRG_EDGE_RISING')
            cam.set_gpo_selector('XI_GPO_PORT1')
            cam.set_gpo_mode('XI_GPO_OFF')    

        cam.set_imgdataformat('XI_RAW8')
        cam.set_exposure(self.exposuretime)
        cam.start_acquisition()
        self.accing = True

    def teardown(self):
        if self.accing:
            self.cam.stop_acquisition()
            self.accing = False
        if self.open:
            self.cam.close_device()
            self.open = False

    def restart(self):
        self.teardown()
        self.setup()

    def get_image(self, img, timeout=30):
        if self.accing:
            self.cam.get_image(img, timeout=timeout)
        else:
            raise 'Not in aquiring mode'
    def set_trigger_software(self,i):
        self.cam.set_trigger_software(i)

    def update_cameras():
        from find_cameras import find_devices
        li = find_devices()
        new_id_sn = {}
        with open('camera_indexing.py', 'w+') as fc_file:
            fc_file.write('id_sn = { \n')
            for (k, v) in li:
                fc_file.write("{}: '{}',\n".format(k, v))
                new_id_sn[k] = v
            fc_file.write('}')
        return new_id_sn
    

