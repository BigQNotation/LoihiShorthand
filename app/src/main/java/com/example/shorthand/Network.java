package com.example.shorthand;

import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class Network extends IntentService {

    public Network() {
        super("HelloIntentService");
    }

    protected void onHandleIntent(Intent intent) {
        // Normally we would do some work here, like download a file.
        // For our sample, we just sleep for 5 seconds.
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            // Restore interrupt status.
            Thread.currentThread().interrupt();
        }
    }


//    protected void Connect() {
//        Context context = getApplicationContext();
//        CharSequence msg1 = "Network.Connect() running...";
//        int duration = Toast.LENGTH_SHORT;
//
//        Toast.makeText(context, msg1, duration).show();
//    }
}
