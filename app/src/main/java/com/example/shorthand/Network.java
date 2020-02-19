package com.example.shorthand;

import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;


public class Network {

    private PrintWriter output;
    private BufferedReader input;
    List<Float> list;

    public Network() {
        Thread Connect = new Thread(new Connect());
        list = new ArrayList<>();
        Connect.start();
    }


    public void send(float x, float y, float timeStamp) {
        list.clear();
        list.add(x);
        list.add(y);
        list.add(timeStamp);
//        Log.i("Network.send()", "x: " + x + " y: " + y + " timeStamp: " + timeStamp);
        new Thread(new SendData(x)).start();
    }


    class Connect implements Runnable {
        public void run() {
            Socket socket;
            try {
                socket = new Socket(MainActivity.SERVER_IP, MainActivity.SERVER_PORT);
                output = new PrintWriter(socket.getOutputStream());
                input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    class SendData implements Runnable {
        private float data;
        SendData(float data) {
            this.data = data;
        }
        @Override
        public void run() {
//            Log.i("Network.sendData()", "x: " + list.get(0) + " y " + list.get(1));
            output.println(list);
            output.flush();
        }
    }

}
