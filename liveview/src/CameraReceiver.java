import java.util.*;
import java.io.*;
import javafx.scene.image.Image;
import javafx.scene.image.WritableImage;
import javafx.scene.image.PixelWriter;
import javafx.scene.image.PixelFormat;
import javafx.scene.image.ImageView;
public class CameraReceiver {
    private int id;
    private ImageMonitor m;
    private BufferedWriter out;
    private boolean sentquit = false;
    ReaderThread r;
    boolean accuiring = false;
    boolean recording_here = false;
    private boolean recording = false;
    private String path;
    private int no;
    private void inheritIO(final InputStream src, final PrintStream dest) {
        new Thread(new Runnable() {
            public void run() {
                BufferedReader br = new BufferedReader(new InputStreamReader((src)));
                try{
                    String line;
                    while((line = br.readLine()) != null){
                        dest.println(line);
                        //if(!m.isRunning()) break;
                    }
                }catch(Exception e) {}
            }
        }).start();
    }
    
    public CameraReceiver(int id, ImageMonitor m, long startTime, Defaults d) {
        this.id = id;
        this.m = m;
        String cmd = String.format(d.command, id, startTime, d.downsample, d.exposure_time);
        try {
            Process p = Runtime.getRuntime().exec(cmd);
            InputStream inp = p.getInputStream();
            out = new BufferedWriter( new OutputStreamWriter(p.getOutputStream()));
            inheritIO(p.getErrorStream(), System.err);
            r = new ReaderThread(id, m, inp, d.debayer, d.LUT);
            r.start();
        }catch(IOException e){
            e.printStackTrace();
        }
    }

    private void send_cmd(String cmd) {
        if(sentquit) return;
        try{
            out.write(cmd + "\n");
            out.flush();
        } catch(IOException e) {
            e.printStackTrace();
        }
    }

    public void quit() {
        send_cmd("quit");
        sentquit = true;
    }
    public void set_exposure(long e) {
        send_cmd(String.format("exposure %d", e));
    }
    public void set_downsample(boolean d){
        send_cmd(String.format("downsample %d", d? 2: 1));
    }
    public void set_fps(int fps, long t0){
        send_cmd(String.format("fps %d %d", fps, t0));
    }
    public void start_record(long start, String folder) {
        if(recording_here) {
            path = folder;
            no = 0;
            recording = true;
        } else {
            send_cmd(String.format("record %d %s", start, folder));
        }
    }
    public void stop_record() {
        if(recording_here) {
            recording = false;
        } else {
            send_cmd("stop");
        }
    }

    private class ReaderThread extends Thread {
        private int id;
        private ImageMonitor m;
        private InputStream in;
        public ReaderThread(int id, ImageMonitor m, InputStream in, boolean debayering, int[] LUT) {
            this.id = id;
            this.m = m;
            this.in = in;
        }
        private void read(int sz, byte[] buf) throws Exception{
            int read = 0;
            while(read < sz) {
                read += in.read(buf, read, sz-read);
            }
        }
        private boolean handle_img() throws Exception {
            int w = get_int(in), h = get_int(in);
            if(w <= 1 || h <= 1 || w > 10000 || h > 10000) {
                System.out.println(w + " " + h);
                return false;
            }
            //boolean thumb = w < 600;
            byte[] bf = new byte[h*w];
            read(h*w, bf);
            ImageWrapper iw = new ImageWrapper(bf, w, h);
            m.setWrap(id, iw);

            // If we want to save from java Thread. Not very nice.
            if(recording) {
                String out = String.format("%s/cam_%d_%d", path, id, no++);
                Thread t = new Thread(new Runnable(){
                    public void run() {
                        try (FileOutputStream fos = new FileOutputStream(out)) {
                            fos.write(bf);
                        } catch (IOException ioe) {
                            ioe.printStackTrace();
                        }
                    }
                });
                t.start();
            }
            return true;
        }
        public void run() {
            while(m.isRunning()) {
                try {
                    if(!handle_img()) break;
                }catch(Exception e) {
                    e.printStackTrace();
                    break;
                }
            }
            try{
                in.close();
            }catch(Exception e) {e.printStackTrace();}
        }
        private int b2int(byte b) {
            return ((int)(b) + 256)%256;
        }
        private int get_int(InputStream inp) throws Exception {
            byte[] b = new byte[4];
            inp.read(b);
            return b2int(b[0]) + b2int(b[1])*(1<<8) + b2int(b[2])*(1<<16) + b2int(b[3])*(1<<24);
        }
    }
}
