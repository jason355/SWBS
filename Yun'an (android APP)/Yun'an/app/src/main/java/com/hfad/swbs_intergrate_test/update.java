package com.hfad.swbs_intergrate_test;

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;
import java.util.Arrays;


public class update extends AppCompatActivity {

    MyDatabaseHelper database = new MyDatabaseHelper(this);
    String[][] message;
    boolean isConnected;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_update);



        Intent serviceIntentWebsocket = new Intent(this, MyForegroundWebsocketService.class);
        this.startForegroundService(serviceIntentWebsocket);


        Intent serviceIntentTimer = new Intent(this, MyForegroundTimerService.class);
        this.startForegroundService(serviceIntentTimer);
        Log.d("Timer", "Started");




    }

    @Override
    public void onStart() {
        super.onStart();
        if (database.isNew()) {
            database.messageDateCheck();
            message = database.getMessage();
            Log.d("message", Arrays.deepToString(message));
            Intent intent = new Intent(this, messageActivity.class);
            intent.putExtra("fragmentTag", "New_message");
            startActivity(intent);
        }
        else {
            Intent intent = new Intent(this, messageActivity.class);
            intent.putExtra("fragmentTag", "History_message");
            startActivity(intent);
        }

    }

    @Override
    public void onBackPressed() {
        Toast.makeText(this, "yun'an is what I live for...", Toast.LENGTH_SHORT).show();
    }

    private void closeActivity() {
        Intent intent = new Intent(Intent.ACTION_MAIN);
        intent.addCategory(Intent.CATEGORY_HOME);
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(intent);
    }
}