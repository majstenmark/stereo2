import javafx.scene.image.Image;
import javafx.scene.image.PixelFormat;
import javafx.scene.image.WritableImage;
import javafx.scene.image.PixelWriter;
public class ImageWrapper {
    byte[] buf;
    int w, h;
    public ImageWrapper(byte[] buf, int w, int h) {
        this.buf = buf;
        this.w = w;
        this.h = h;
    }
    private Image assemble(int[] rgbarr, int w_out, int h_out) {
        WritableImage img = new WritableImage(w_out, h_out);
        PixelWriter pw = img.getPixelWriter();
        pw.setPixels(0, 0, w_out, h_out, PixelFormat.getIntArgbInstance(), rgbarr, 0, w_out);
        return img;
    }
    public Image getThumb(boolean red, int[] LUT) {
        int div = h/200*2;
        int pad = 5;
        int h_out = h/div, w_out = h/div;
        int[] rgbarr = ImageCreator.debayer_thumb(buf, w, h, div, pad, red, false, true, LUT);
        w_out += 2*pad;
        h_out += 2*pad;
        return assemble(rgbarr, w_out, h_out);
    }
    public Image getFull(boolean round, boolean cross, int[] LUT) {
        int w_out = w, h_out = h;
        int[] rgbarr;
        if(true){
            rgbarr = ImageCreator.debayer_full(buf, w, h, cross, round, LUT);
        } else{
            rgbarr = ImageCreator.debayer_half(buf, w, h, cross, round, LUT);
            w_out /= 2;
            h_out /= 2;
        }
        return assemble(rgbarr, w_out, h_out);
    }
}
