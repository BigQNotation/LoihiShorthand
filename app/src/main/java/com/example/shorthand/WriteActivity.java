package com.example.shorthand;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;


public class WriteActivity extends AppCompatActivity {

    FingerView fingerView;
    private BufferedReader input;

    @SuppressLint("ClickableViewAccessibility")
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_draw);
        fingerView = findViewById(R.id.paintView);
        DisplayMetrics metrics = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(metrics);
        fingerView.init(metrics);

        final TextView document_view = findViewById(R.id.DocumentView);

        // handle fingerView draw events
        fingerView.setOnTouchListener(new View.OnTouchListener() {

            @Override
            public boolean onTouch(View view, MotionEvent event) {
                float x = event.getX();
                float y = event.getY();

                switch(event.getAction()) {
                    case MotionEvent.ACTION_DOWN :
                        fingerView.touchStart(x, y);
                        fingerView.invalidate();
                        break;
                    case MotionEvent.ACTION_MOVE :
                        fingerView.touchMove(x, y);
                        fingerView.count++;
                        fingerView.network.send(x,fingerView.y_max - y,fingerView.count);
                        fingerView.invalidate();
                        break;
                    case MotionEvent.ACTION_UP :
                        fingerView.network.send(-1,-1,fingerView.count);
                        fingerView.touchUp();
                        fingerView.invalidate();
                        fingerView.clear();
                        fingerView.count = 0;

                        // append document view with the response from server
                        fingerView.network.getResponseString();
                        final TextView document_view = findViewById(R.id.DocumentView);
                        String text1 = document_view.getText().toString();
                        String text2 = fingerView.network.response_string;
                        String text3 = text1 + text2;
                        document_view.setText(text3);
                        break;
                }

                return true;

            }
        });




    }



}


