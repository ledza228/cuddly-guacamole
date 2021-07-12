package sample;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.layout.VBox;

public class Controller {

    public Button btn1;
    public VBox VBoxMain;


    public void buttonClicked(){
        System.out.println("HAHAHHAHAHH");
        btn1.setText(String.format("%1$,.2f",Math.random()*100));
    }

}
