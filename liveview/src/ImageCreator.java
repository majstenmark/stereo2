public class ImageCreator {
    private static class Counter {
        private int x;
        synchronized void add() {
            x += 1;
            notifyAll();
        }
        synchronized void wait_until(int y) throws Exception {
            while(y != x) {
                wait();
            }
        }
    }
    public static int b2int(byte b) {
        return ((int)(b) + 256)%256;
    }
    private static int get_alpha_round(int d, int r, boolean round) {
        if(!round || d <= r - 256) return 0xFF000000;
        if(d > r) return 0;
        int x = r-d;
        return x << 24;
    }
    public static void set_cross(int[] rgbarr, int w_out, int h_out, boolean round) {
        int mx = w_out/2, my = h_out/2;
        int r2 = Math.min(mx*mx, my*my);
        for(int w = 0; w<w_out; w++) {
            int dx = Math.abs(w - mx);
            rgbarr[(my-1)*w_out + w] = get_alpha_round(dx*dx, r2, round) + 0xFF0000;
            rgbarr[my*w_out + w] = get_alpha_round(dx*dx, r2, round) + 0xFF0000;
            rgbarr[(my+1)*w_out + w] = get_alpha_round(dx*dx, r2, round) + 0xFF0000;
        }
        for(int h= 0; h<h_out; h++) {
            int dy = Math.abs(h-my);
            rgbarr[h*w_out + mx - 1] = get_alpha_round(dy*dy, r2, round) + 0xFF0000;
            rgbarr[h*w_out + mx] = get_alpha_round(dy*dy, r2, round) + 0xFF0000;
            rgbarr[h*w_out + mx + 1] = get_alpha_round(dy*dy, r2, round) + 0xFF0000;
        }
    }
    public static int[] debayer_thumb(byte[] buf, int W, int H, int div, int pad, boolean red, boolean cross, boolean round, int[] LUT) {
        int TH = Math.min(H, W)/div;
        int sz = TH + 2*pad;
        int[] rgbarr = new int[sz*sz];
        int mx = W/(2*div), my = H/(2*div);
        int r2 = Math.min(mx*mx, my*my);
        int r3 = Math.min((mx+pad)*(mx+pad), (my+pad)*(my+pad));
        int RR = red? r3 : r2;
        int ddiff = (W - H)/(2*div); //used to center thumbnails
        for(int w = 0; w < sz; w++) {
            for (int h = 0; h < sz; h++) {
                int dx = Math.abs(w - pad - my), dy = Math.abs(h - pad - my);
                int Radi = dx*dx + dy*dy;
                if(pad <= w && w < sz - pad && pad <= h && h < sz-pad){
                    int b = (h-pad)*div*W + (w-pad + ddiff)*div;
                    int g1 = b + 1;
                    int g2 = b + W;
                    int r = g2 + 1;
                    int v = b2int(buf[r])*0x10000 + 0x100*((b2int(buf[g1]) + b2int(buf[g2]))>>1) + b2int(buf[b]);
                    rgbarr[h*sz + w] = get_alpha_round(Radi, RR, round) + LUT[v]; //c_b(b2int(buf[b])) + //blue
                }
                if(r2 <= Radi && Radi < r3) {
                    rgbarr[h*sz + w] = red? get_alpha_round(Radi, r3, round) + 0xFF0000 : 0;
                }
            }
        }
        if(cross) {
            set_cross(rgbarr, sz, sz, round);
        }
        return rgbarr;
    }
    static int get_blue(byte[] buf, int h, int w, int H, int W) {
        int X = h*W + w;
        if(h%2 == 0 && w%2 == 0) {
            return b2int(buf[X]);
        } else if(h%2 == 0 && w%2 == 1) {
            return (b2int(buf[X-1]) + b2int(buf[X+1]))/2;
        }else if(h%2 == 1 && w%2 == 0) {
            return (b2int(buf[X-W]) + b2int(buf[X+W]))/2;
        }else {
            return (b2int(buf[X-1-W]) + b2int(buf[X+1-W]) + b2int(buf[X-1+W]) + b2int(buf[X+1+W]))/4; 
        }
    }
    static int get_red(byte[] buf, int h, int w, int H, int W) {
        int X = h*W + w;
        if(h%2 == 0 && w%2 == 0) {
            return (b2int(buf[X-1-W]) + b2int(buf[X+1-W]) + b2int(buf[X-1+W]) + b2int(buf[X+1+W]))/4; 
        } else if(h%2 == 0 && w%2 == 1) {
            return (b2int(buf[X-W]) + b2int(buf[X+W]))/2;
        }else if(h%2 == 1 && w%2 == 0) {
            return (b2int(buf[X-1]) + b2int(buf[X+1]))/2;
        }else {
            return b2int(buf[X]);
        }
    }
    static int get_green(byte[] buf, int h, int w, int H, int W) {
        int X = h*W + w;
        if(h%2 == 0 && w%2 == 0) {
            return (b2int(buf[X-1]) + b2int(buf[X+1]) + b2int(buf[X-W]) + b2int(buf[X+W]))/4; 
        } else if(h%2 == 0 && w%2 == 1) {
            return b2int(buf[X]);
        }else if(h%2 == 1 && w%2 == 0) {
            return b2int(buf[X]);
        }else {
            return (b2int(buf[X-1]) + b2int(buf[X+1]) + b2int(buf[X-W]) + b2int(buf[X+W]))/4; 
        }
    }
    public static int[] debayer_full(byte[] buf, int W, int H, boolean cross, boolean round, int[] LUT) {
        int[] startX = new int[]{1, 1, 1, 1, H/4, H/4, H/4, H/4, H/2, H/2, H/2, H/2, 3*H/4, 3*H/4, 3*H/4, 3*H/4};
        int[] startY = new int[]{1, W/4, W/2, 3*W/4, 1, W/4, W/2, 3*W/4, 1, W/4, W/2, 3*W/4, 1, W/4, W/2, 3*W/4};
        int[] endX = new int[]{H/4, H/4, H/4, H/4, H/2, H/2, H/2, H/2, 3*H/4, 3*H/4, 3*H/4, 3*H/4, H-1, H-1, H-1, H-1};
        int[] endY = new int[]{W/4, W/2, 3*W/4, W-1, W/4, W/2, 3*W/4, W-1, W/4, W/2, 3*W/4, W-1, W/4, W/2, 3*W/4, W-1};
        int[] rgbarr = new int[W*H];
        int mx = W/2;
        int my = H/2;
        int r2 = Math.min(mx*mx, my*my);
        Counter COUNTER = new Counter();
        for(int i = 0; i<startX.length; i++) {
            final int x = i;
            Thread t = new Thread(new Runnable(){
                public void run() {
                    for (int h = startX[x]; h < endX[x]; h++) {
                        for(int w = startY[x]; w < endY[x]; w++) {
                            int dx = Math.abs(w - mx), dy = Math.abs(h-my);
                            int v = 0x10000*get_red(buf, h, w, H, W) + 0x100*get_green(buf, h, w, H, W) + get_blue(buf, h, w, H, W);
                            rgbarr[h*W + w] = get_alpha_round(dx*dx + dy*dy, r2, round) + LUT[v];
                        }
                    }
                    COUNTER.add();

                }
            });
            t.start();
        }
        try {
            COUNTER.wait_until(startX.length);
        }catch(Exception e) {}

        if(cross) {
            set_cross(rgbarr, W, H, round);
        }
        return rgbarr;
    }

    public static int[] debayer_half(byte[] buf, int W, int H, boolean cross, boolean round, int[] LUT) {
        int div = 2;
        int w_out = W/div, h_out = H/div;
        int startX [] = new int[]{0,       0,       h_out/2, h_out/2},  startY [] = new int[]{0,       w_out/2, 0,       w_out/2};
        int endX [] = new int[]{  h_out/2, h_out/2, h_out-1, h_out-1},  endY [] = new int[]{  w_out/2, w_out-1, w_out/2, w_out-1};
        int[] rgbarr = new int[w_out*h_out];
        int mx = w_out/2, my = h_out/2;
        int r2 = Math.min(mx*mx, my*my);
        Counter COUNTER = new Counter();
        for(int i = 0; i<startX.length; i++) {
            final int x = i;
            Thread t = new Thread(new Runnable() {
                public void run() {
                    for (int h = startX[x]; h < endX[x]; h++) {
                        for(int w = startY[x]; w < endY[x]; w++) {
                            int dx = Math.abs(w - mx), dy = Math.abs(h-my);
                            int b = h*div*W + w*div;
                            int g1 = b + 1;
                            int g2 = b + W;
                            int r = g2 + 1;
                            int v = 0x10000*b2int(buf[r]) + 0x100 * ((b2int(buf[g1]) + b2int(buf[g2]))>>1) + b2int(buf[b]);
                            rgbarr[h*w_out + w] = get_alpha_round(dx*dx + dy*dy, r2, round) + LUT[v];
                        }
                    }
                    COUNTER.add();
                }
            });
            t.start();
        }
        try {
            COUNTER.wait_until(startX.length);
        }catch(Exception e) {}
        if(cross) {
            set_cross(rgbarr, w_out, h_out, round);
        }
        return rgbarr;
    }
}
