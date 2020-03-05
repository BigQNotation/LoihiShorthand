package com.example.shorthand;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;


public class MainActivity extends AppCompatActivity {

    EditText etIP, etPort;
    public static String SERVER_IP;
    public static int SERVER_PORT;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        GetIP();
    }


    public void GetIP() {
        etIP = findViewById(R.id.etIP);
        etPort = findViewById(R.id.etPort);
        findViewById(R.id.connectButton).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Context context = getApplicationContext();
                CharSequence msg1 = "Connecting to ";
                int duration = Toast.LENGTH_SHORT;
                SERVER_IP = etIP.getText().toString().trim();
                SERVER_PORT = Integer.parseInt(etPort.getText().toString().trim());
                Toast.makeText(context, msg1 + SERVER_IP + ":" + SERVER_PORT, duration).show();
                startActivity(new Intent(MainActivity.this, WriteActivity.class));
            }

        });
    }

}
