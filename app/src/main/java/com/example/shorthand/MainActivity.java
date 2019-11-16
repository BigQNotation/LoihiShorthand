package com.example.shorthand;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Buttons();
    }

    public void Buttons() {
        findViewById(R.id.connectButton).setOnClickListener(click);

    }

    private View.OnClickListener click = new View.OnClickListener() {

        public void onClick(View view) {
            switch (view.getId()) {
                case R.id.connectButton:
                    startActivity(new Intent(MainActivity.this, WriteActivity.class));
                    break;
            }
        }

    };
}
