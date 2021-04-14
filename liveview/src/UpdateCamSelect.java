import javafx.scene.control.Label;
import javafx.application.Platform;
public class UpdateCamSelect {
    private ImageMonitor m;
    private Label l;
    private int screen_id;
    public UpdateCamSelect(ImageMonitor m, Label l, int screen_id) {
        this.m = m;
        this.l = l;
        this.screen_id = screen_id;
        Thread t = new Thread(new Runnable(){
            public void run() {
            int curr = -1;
            do {
                try {
                    curr = m.get_bound_camera(screen_id, curr);
                    final String S = String.format("Camera %d", curr+1);
                    Platform.runLater(new Runnable() {
                    public void run() {
                        l.setText(S);
                    }});
                }catch(Exception e) {
                    e.printStackTrace();
                    break;
                }
            }while(curr != -1);
        }});
        t.start();
    }

}
