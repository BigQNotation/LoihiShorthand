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

    public PrintWriter output; //problem child
    public BufferedReader input;
    BufferedReader stdIn;
    List<Float> list;
    Socket socket;
    public String response_string = "";

    public Network() {

        System.out.println("Network()\n");
        Thread Connect = new Thread(new Connect());
        list = new ArrayList<Float>();
        Connect.start();
    }


    public void send(float x, float y, float timeStamp) {

        System.out.println("send(x,y,timeStamp)\n");
        list.clear();
        list.add(x);
        list.add(y);
        list.add(timeStamp);
//        Log.i("Network.send()", "x: " + x + " y: " + y + " timeStamp: " + timeStamp);
        new Thread(new SendData(x)).start();
    }

    public void getResponseString() throws InterruptedException {

        System.out.println("getResponseString()\n");
        Thread response;
        response = new Thread(new GetData());
        response.start();
        response.join();
        return;
    }


    class Connect implements Runnable {
        public void run() {

            System.out.println("Connect run\n");

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
                if (((response_string = input.readLine()) == null)){
                    response_string = "error";
                }

                System.out.println("Check point 1\n");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    class SendData implements Runnable {
        private float data;
        SendData(float data) {
            System.out.println("sendData");
            this.data = data;
        }
        @Override
        public void run() {
            try{
                Log.i("Network.sendData()", "x: " + list.get(0) + " y " + list.get(1));
                output.println(list);
                output.flush();
            }
            catch (Exception e) {
                System.out.println(e);
            }
        }
    }

}
