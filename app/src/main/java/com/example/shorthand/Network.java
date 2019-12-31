package com.example.shorthand;

import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;


public class Network {

    private PrintWriter output;
    private BufferedReader input;

    public Network() {
        Thread Connect = new Thread(new Connect());
        Connect.start();
    }


    public void send(float x, float y) {
        Log.i("Network.send()", "x: " + x + " y: " + y);
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
            output.println(data);
            output.flush();
        }
    }

}
