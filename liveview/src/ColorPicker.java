import javafx.scene.Node;
import java.util.*;
public class ColorPicker {
    static ColorPicker self = null;
    public ArrayList<Node> bg = new ArrayList<>();
    public ArrayList<Node> fg = new ArrayList<>();
    
    static ColorPicker get_instance() {
        if(self == null){
            self = new ColorPicker();
        }
        return self;
    }
    public static void add_bg(Node n) {
        get_instance().bg.add(n);
    }
    public static void add_fg(Node n) {
        get_instance().fg.add(n);
    }
    public static String styleStr(String bg, String fg) {
        return String.format("-fx-background-color: %s; -fx-text-fill: %s", bg, fg);
    }
    public static void set(String bg_c, String fg_c){
        String style = styleStr(bg_c, fg_c);
        ColorPicker p = get_instance();
        for(Node node : p.bg) {
            node.setStyle(style);
        }
        for(Node node : p.fg) {
            node.setStyle(style);
        }
    }
}
