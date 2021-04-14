import javafx.scene.image.Image;
import java.util.function.Consumer;
class ImageProvider {
    private final Consumer<Image> imgProcessor;
    int screen, id;
    long startTime;
    ImageMonitor m;
    boolean thumb;

    public ImageProvider(Consumer<Image> imgProcessor, int id, ImageMonitor m, boolean thumb) {
        this.imgProcessor = imgProcessor;
        this.screen = id;
        this.id = id;
        this.m = m;
        this.thumb = thumb;
    }

    public void doMachineryWork() {
        ImageWrapper last = null;
        while(m.isRunning()) {
            try {
                ImageWrapper iw = thumb? m.getImageById(id, last) : m.getImageByScreen(screen, last);
                if(iw != null){
                    last = iw;
                    Image img = thumb? iw.getThumb(m.isActive(id), m.getLUT()) : iw.getFull(m.getRound(), m.getCross(), m.getLUT());
                    imgProcessor.accept(img);
                }
            }catch(Exception e) {
                e.printStackTrace();
            }
        }
    }
}
