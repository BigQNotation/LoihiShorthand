package com.example.shorthand;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.DisplayMetrics;


public class WriteActivity extends AppCompatActivity {

    protected void onCreate(Bundle savedInstanceState) {
        FingerView fingerView;
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_draw);
        fingerView = findViewById(R.id.paintView);
        DisplayMetrics metrics = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(metrics);
        fingerView.init(metrics);
    }

}


