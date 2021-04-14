import javafx.scene.control.Button;
import javafx.scene.image.ImageView;
import javafx.scene.input.MouseEvent;
import javafx.event.EventHandler;

public class ImageButton extends Button {
    
    private final String STYLE_NORMAL = "-fx-background-color: transparent; -fx-padding: 5, 5, 5, 5;";
    private final String STYLE_PRESSED = "-fx-background-color: transparent; -fx-padding: 6 4 4 6;";
    
    private ImageMonitor m;
    private int id;
    public ImageButton(ImageView view, ImageMonitor m, int id) {
        this.m = m;
        this.id = id;
        setGraphic(view);
        setStyle(STYLE_NORMAL);
        
        setOnMousePressed(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                setStyle(STYLE_PRESSED);
                m.bind_camera2screen(0, id);
            }            
        });
        
        setOnMouseReleased(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
               setStyle(STYLE_NORMAL);
            }            
        });
    }
    
}
