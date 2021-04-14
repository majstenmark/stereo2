import javafx.application.Application;
import javafx.scene.image.ImageView;
import javafx.stage.Stage; 
import javafx.application.Platform;


public class App extends Application {
    @Override
    public void start(Stage stage) {
        Defaults def = Defaults.get(getParameters().getRaw());
        ImageMonitor monitor = new ImageMonitor(def);
        stage.setOnCloseRequest(event -> {
                monitor.quit();
                Platform.exit();
            });
        ImageView iv0 = CtrlCreator.screenView();
        ImageProvider m0 = new ImageProvider(img ->
            Platform.runLater(() -> iv0.setImage(img)), 0, monitor, false);
        ImageView iv1 = CtrlCreator.screenView();
        ImageProvider m1 = new ImageProvider(img ->
            Platform.runLater(() -> iv1.setImage(img)), 1, monitor, false);

        CtrlCreator.updateStage(stage, monitor, def, iv0, iv1);
        stage.show();
        new Thread(m0::doMachineryWork).start();
        new Thread(m1::doMachineryWork).start();
    }
    public static void main(String[] args) {
        Util.ensure_LUT();
        Application.launch(args);
    }
}

