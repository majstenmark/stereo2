import java.util.*;
import java.io.*;
import javafx.scene.image.Image;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.FileSystems;
public class ImageMonitor {
    private HashMap<Integer, ImageWrapper> imageWrappers = new HashMap<>();
    boolean running = true;
    CameraReceiver[] crs;
    int[] screen2camera = new int[]{0, 1};
    boolean recording, cross, round;
    String folder_prefix;
    int[] LUT;
    boolean downsampling;
    private int fps = 25;
    public UpdateCamSelect cam_select;
    public ImageMonitor(Defaults d) {
        folder_prefix = d.prefix_save;
        crs = new CameraReceiver[d.no_cams];
        long start = Time.get_time() + 4*1000*1000;
        downsampling = d.downsample == 2;
        this.LUT = d.LUT;
        for(int i = 0; i<d.no_cams; i++) {
            crs[i] = new CameraReceiver(i, this, start, d);
        }
    }
    public synchronized int get_bound_camera(int screen, int curr_cam) throws InterruptedException {
        while(curr_cam == screen2camera[screen] && isRunning()){
            wait();
        }
        return isRunning()? screen2camera[screen] : -1;
    }
    public synchronized boolean bind_camera2screen(int screen, int camera) {
        if(screen2camera[screen] == camera) return true;
        for(int cam : screen2camera) if(cam == camera) return false;
        screen2camera[screen] = camera;
        notifyAll();
        return true;
    }
    public synchronized boolean isRunning() {
        return running;
    }
    public synchronized boolean isActive(int i) {
        return i == screen2camera[0];
    }
    public synchronized void set_prefix(String path) {
        folder_prefix = path;
    }
    public synchronized void setCross(boolean val) {
        cross = val;
    }
    public synchronized boolean getCross() {
        return cross;
    }
    public synchronized void setRound(boolean val) {
        round = val;
    }
    public synchronized boolean ds() {
        return downsampling;
    }
    public synchronized void setDownsample(boolean val) {
        downsampling = val;
        for(CameraReceiver c: crs)
            c.set_downsample(val);
    }
    public synchronized boolean getRound() {
        return round;
    }
    public int[] getLUT() {
        return LUT;
    }
    public synchronized void quit() {
        running = false;
        for(CameraReceiver c: crs) c.quit();
        notifyAll();
    }

    public synchronized ImageWrapper getImageById(int i, ImageWrapper iw) throws InterruptedException {
        while((!imageWrappers.containsKey(i) || imageWrappers.get(i) == iw) && running) {
            this.wait();
        }
        if(!running) return null;
        return imageWrappers.get(i);
    }

    public synchronized ImageWrapper getImageByScreen(int i, ImageWrapper iw) throws InterruptedException {
        while((!imageWrappers.containsKey(screen2camera[i]) || imageWrappers.get(screen2camera[i]) == iw) && running) {
            this.wait();
        }
        if(!running) return null;
        return imageWrappers.get(screen2camera[i]);
    }
    public synchronized void setWrap(int i, ImageWrapper img){
        imageWrappers.put(i, img);
        notifyAll();
    }
    public synchronized void set_exposure(long etime) {
        for(CameraReceiver c: crs)
            c.set_exposure(etime);
    }
    public synchronized int get_fps() {
        return fps;
    }
    public synchronized void set_fps(int fps) {
        if(recording) return;
        if(fps <= 0 || fps > 200) return;
        long start_time = Time.get_time() + 100*1000;
        for(CameraReceiver c: crs) {
            c.set_fps(fps, start_time);
        }
        this.fps = fps;
    }
    public synchronized boolean record() {
        recording = !recording;
        if(!recording) {
            for(CameraReceiver c: crs)
                c.stop_record();
        }else {
            String record_folder = get_and_create_folder(folder_prefix);
            if(record_folder == null) return recording = false;
            long start_time = Time.get_time() + 500*1000; //500 milli second after button pressed.
            for(CameraReceiver c: crs)
                c.start_record(start_time, record_folder);
        }
        return recording;
    }
    private String get_and_create_folder(String prefix) {
        int i = 0;
        while(true) {
            String s = String.format("shot_%05d", i);
            Path p = FileSystems.getDefault().getPath(prefix, s);
            if(Files.notExists(p)) {
                try {
                    Files.createDirectory(p);
                    return String.format("%s/%s", prefix, s);
                }catch(Exception e) {
                    e.printStackTrace();
                    break;
                }
            }
            i += 1;
        }
        return null;
    }
}
