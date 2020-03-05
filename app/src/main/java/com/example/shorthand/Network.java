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

    public PrintWriter output;
    public BufferedReader input;
    BufferedReader stdIn;
    List<Float> list;
    Socket socket;
    public String response_string = "";

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

    public void getResponseString(){

        new Thread(new GetData()).start();
    }


    class Connect implements Runnable {
        public void run() {


            try {
                socket = new Socket(MainActivity.SERVER_IP, MainActivity.SERVER_PORT);
                output = new PrintWriter(socket.getOutputStream());
                input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    class GetData implements Runnable {

        GetData(){
        }

        @Override
        public void run(){
            try {
                System.out.println("called getData");
                Log.i("network", "called getData");
                if (((response_string = input.readLine()) != null)){

                }

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
