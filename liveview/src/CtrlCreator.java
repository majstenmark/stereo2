import javafx.scene.Scene; 
import javafx.geometry.Insets;
import javafx.stage.Stage; 
import javafx.stage.DirectoryChooser;
import java.io.File;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.geometry.Pos;
import javafx.scene.control.CheckBox;
import javafx.scene.control.MenuButton;
import javafx.scene.control.MenuItem;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.layout.Pane;
import javafx.scene.image.ImageView;
import javafx.scene.layout.StackPane;
import javafx.beans.binding.Bindings;
import javafx.scene.layout.Priority;
import javafx.scene.layout.BorderPane;
import javafx.beans.binding.DoubleBinding;

public class CtrlCreator {
    public static void updateStage(Stage stage, ImageMonitor monitor, Defaults def, ImageView screen1, ImageView screen2) {
        stage.setTitle("Surgeon's Perspective");
        stage.setWidth(1800);
        stage.setHeight(1000);
        stage.setMinHeight(500);
        stage.setMinWidth(800);
        BorderPane pane = new BorderPane();
        StackPane holder = new StackPane(pane);
        ColorPicker.add_bg(holder);
        Scene scene = new Scene(holder);

        GridPane top = CtrlCreator.topPanel(monitor, stage, def.prefix_save); 
        GridPane ctrl = CtrlCreator.ctrlPanel(monitor, def.exposure_time, def.no_cams);
        DoubleBinding widthBind = pane.widthProperty().subtract(200).divide(2);
        DoubleBinding heightBind = pane.heightProperty().subtract(top.heightProperty());
        VBox screen1box = CtrlCreator.screen(monitor, screen1, widthBind, heightBind);
        VBox screen2box = CtrlCreator.screen(monitor, screen2, widthBind, heightBind);
        //HBox screeens = new HBox(screen1box, screen2box);
        //screen.setStyle("-fx-border-color: white;");
        HBox.setHgrow(screen1box, Priority.SOMETIMES);
        HBox.setHgrow(screen2box, Priority.SOMETIMES);
        HBox center = new HBox(screen1box, screen2box);

        pane.setTop(top);
        pane.setCenter(center);
        pane.setLeft(ctrl);
        ColorPicker.set("#24292e", "FFFFFF");
        stage.setScene(scene);

    }
    public static ImageView thumbView() {
        ImageView iv = new ImageView();
        iv.setPreserveRatio(true); 
        iv.minWidth(100);
        iv.minHeight(100);
        iv.maxWidth(300);
        iv.maxHeight(300);
        return iv;
    }
    public static ImageView screenView() {
        ImageView iv = new ImageView();
        iv.setPreserveRatio(true); 
        iv.minWidth(0);
        iv.minHeight(0);
        iv.maxWidth(Double.POSITIVE_INFINITY);
        iv.maxHeight(Double.POSITIVE_INFINITY);
        return iv;
    }
    public static GridPane topPanel(ImageMonitor monitor, Stage stage, String prefix) {
        Button quitButton = new Button("Quit");
        quitButton.setOnAction(event -> {
            monitor.quit();
            stage.close();
        });

        Button recordButton = new Button("Record");
        recordButton.setStyle(ColorPicker.styleStr("#00FF00", "#FFFFFF"));
        recordButton.setOnAction(event -> {
            if(monitor.record()){ 
                recordButton.setStyle(ColorPicker.styleStr("#FF0000", "#FFFFFF"));
                recordButton.setText("Stop Recording");
            } else { 
                recordButton.setStyle(ColorPicker.styleStr("#00FF00", "#FFFFFF"));
                recordButton.setText("Record");
            }
        });
        Label destination = new Label(prefix);
        ColorPicker.add_fg(destination);
        Button changedestButton = new Button("Change folder");
            changedestButton.setOnAction(event -> {
                DirectoryChooser chooser = new DirectoryChooser();
                chooser.setTitle("Where should videos be saved");
                File defaultDirectory = new File(destination.getText());
                chooser.setInitialDirectory(defaultDirectory);
                File sel = chooser.showDialog(stage);
            if(sel == null) return;
            destination.setText(sel.getAbsolutePath());
            monitor.set_prefix(sel.getAbsolutePath());
        });

        GridPane ctrlPanel = new GridPane();
        ctrlPanel.setPadding(new Insets(10, 10, 10, 10));
        ctrlPanel.setVgap(10);
        ctrlPanel.setHgap(10);
        ctrlPanel.add(quitButton, 0, 0);
        ctrlPanel.add(recordButton, 1, 0);
        ctrlPanel.add(changedestButton, 2, 0);
        ctrlPanel.add(destination, 2, 1);
        ctrlPanel.setAlignment(Pos.TOP_LEFT);
        return ctrlPanel;
    }
    public static VBox screen(ImageMonitor monitor, ImageView view, DoubleBinding widthProp, DoubleBinding heightProp) {
        //box.setMinSize(480, 300);
        view.fitWidthProperty().bind(widthProp);
        int pad_bot = 50;
        view.fitHeightProperty().bind(heightProp.subtract(pad_bot));
        VBox box = new VBox(view);
        box.setPadding(new Insets(0, 0, pad_bot, 0));
        box.setAlignment(Pos.TOP_CENTER);
        return box;
    }
    public static Pane thumbs(ImageMonitor monitor, ImageView[] views) {
        Pane p = new Pane();
        int[] x = new int[]{120, 240, 180, 60, 0, 60, 180};
        int[] y = new int[]{120, 120, 240, 240, 120, 0, 0};
        int sz = 800;
        p.minWidth(sz);
        p.maxWidth(sz);
        p.minHeight(sz);
        p.maxHeight(sz);
        for(int i = 0; i<views.length; i++) {
            //views[i].setFitWidth(150);
            //views[i].setFitHeight(150);
            ImageButton b = new ImageButton(views[i], monitor, i);
            b.setLayoutX(x[i]);
            b.setLayoutY(y[i]);
            p.getChildren().add(b);
        }
        p.setPadding(new Insets(0, 0, 100, 0));
        

        return p;
        
    }
    public static VBox cameraSelect(int def, int screen_id, int nocams, ImageMonitor monitor) {

        MenuButton screen = new MenuButton("Select Camera");
        Label label = new Label("Camera " + def);
        ColorPicker.add_fg(label);
        for(int i = 0; i<nocams; i++) {
            MenuItem mItem = new MenuItem("Camera " + (i+1));
            final int cam = i;
            mItem.setOnAction(event -> {
                monitor.bind_camera2screen(screen_id, cam);
            });
            screen.getItems().add(mItem);
        }
        VBox box = new VBox(label, screen);
        box.setSpacing(10);
        monitor.cam_select = new UpdateCamSelect(monitor, label, screen_id);

        return box;
    }
    public static GridPane ctrlPanel(ImageMonitor monitor, int exptime, int nocams) {
        Button expButton = new Button("Set Exposure Time");
        TextField expField = new TextField("" + exptime);
        expField.setPrefWidth(expButton.getWidth());
        expField.textProperty().addListener((observable, oldValue, newValue) -> {
            if (!newValue.matches("\\d*")) {
                expField.setText(newValue.replaceAll("[^\\d]", ""));
            }
        });
        expButton.setOnAction(event -> {
            if(expField.textProperty().getValue().length() == 0) return;
            long etime = Long.parseLong(expField.textProperty().getValue());
            System.out.println("Setting exposure time to " + etime);
            monitor.set_exposure(etime);
        });
        Button fpsButton = new Button("Set FPS");
        TextField fpsField = new TextField("" + monitor.get_fps());
        fpsField.setPrefWidth(expButton.getWidth());
        fpsField.textProperty().addListener((observable, oldValue, newValue) -> {
            if (!newValue.matches("\\d*")) {
                fpsField.setText(newValue.replaceAll("[^\\d]", ""));
            }
        });
        fpsButton.setOnAction(event -> {
            if(fpsField.textProperty().getValue().length() == 0) return;
            long fps = Long.parseLong(fpsField.textProperty().getValue());
            System.out.println("Setting fps to " + fps);
            monitor.set_fps((int)fps);
            fpsField.setText("" + monitor.get_fps());
        });
        CheckBox crossCheck = new CheckBox("Crosshair");
        CheckBox roundCheck = new CheckBox("Round");
        CheckBox dsCheck = new CheckBox("Downsample");
        dsCheck.setSelected(monitor.ds());
        crossCheck.selectedProperty().addListener((obs, wasSelected, isSelected) -> monitor.setCross(isSelected));
        roundCheck.selectedProperty().addListener((obs, wasSelected, isSelected) -> monitor.setRound(isSelected));
        dsCheck.selectedProperty().addListener((obs, wasSelected, isSelected) -> monitor.setDownsample(isSelected));
        ColorPicker.add_fg(crossCheck);
        ColorPicker.add_fg(roundCheck);
        ColorPicker.add_fg(dsCheck);

        GridPane ctrlPanel = new GridPane();
        //ctrlPanel.setMinSize(800, 100);
        ctrlPanel.setPadding(new Insets(10, 10, 10, 10));
        ctrlPanel.setVgap(10);
        ctrlPanel.setHgap(10);
        ctrlPanel.add(expField, 0, 0);
        ctrlPanel.add(expButton, 0, 1);
        ctrlPanel.add(fpsField, 0, 2);
        ctrlPanel.add(fpsButton, 0, 3);
        ctrlPanel.add(crossCheck, 0, 4);
        ctrlPanel.add(roundCheck, 0, 5);
        ctrlPanel.add(dsCheck, 0, 6);
        VBox selector = cameraSelect(1, 0, nocams, monitor);
        ctrlPanel.add(selector, 0, 7);
        int len = 8;
        ctrlPanel.add(get_btn("Black",     "#000000", "#FFFFFF"), 0, len++);
        ctrlPanel.add(get_btn("White",     "#FFFFFF", "#000000"), 0, len++);
        ctrlPanel.add(get_btn("DarkGray",  "#24292E", "#FFFFFF"), 0, len++);
        ctrlPanel.add(get_btn("DarkBlue",  "#191970", "#FFFFFF"), 0, len++);
        ctrlPanel.add(get_btn("LightBlue", "#87cefa", "#000000"), 0, len++);
        //ctrlPanel.setAlignment(Pos.CENTER_LEFT);
        return ctrlPanel;

    }
    public static void add_to_grid(GridPane g, int row, String key) {
        Label l = new Label(key);
        ColorPicker.add_fg(l);
        TextField tf = new TextField();
        ColorPicker.add_fg(tf);
        g.add(l, 0, row);
        g.add(tf, 1, row);
    }
    public static Button get_btn(String text, String bg, String fg) {
        Button btn = new Button(text);
        btn.setStyle(ColorPicker.styleStr(bg, fg));
        btn.setOnAction(event -> {
            ColorPicker.set(bg, fg);
        });
        return btn;

    }
    public static GridPane patientPanel() {
        GridPane ctrlPanel = new GridPane();
        //ctrlPanel.setMinSize(800, 100);
        ctrlPanel.setPadding(new Insets(10, 10, 10, 50));
        ctrlPanel.setVgap(10);
        ctrlPanel.setHgap(10);
        String[] fields = new String[]{"Patient", "Age", "Diagnosis", "Operation", "Surgeon", "Assistant Surgeon", "Anesthesia", "Perfusionist"};
        for(int i = 0; i<fields.length; i++) {
            add_to_grid(ctrlPanel, i, fields[i]);
        }

        return ctrlPanel;

    }
}
