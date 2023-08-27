package com.hfad.swbs_intergrate_test;


import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;

import androidx.drawerlayout.widget.DrawerLayout;

import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.annotation.SuppressLint;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.BroadcastReceiver;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;

import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.google.android.material.navigation.NavigationView;

import android.view.MenuItem;
import android.widget.Toast;


public class messageActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {

    MyDatabaseHelper database = new MyDatabaseHelper(this);
    private DrawerLayout drawerLayout;
    private static final String PREFS_NAME = "MyPrefs";
    private static final String Frag_PREF = "fragmentTag";
    private static final String NETWORK_STATUS_KEY = "network_status";
    private static final String Fragment_STATUS_KEY = "fragment_status";

    boolean isConnected;
    private String fragmentTag;
    ImageView NetworkStat;
    ImageButton wifiRefresh;
    ProgressBar roundBar;

    private websocket websocket;

    private  BroadcastReceiver connectionStatusReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (intent.getAction().equals("websocket_connection_status")) {
                roundBar.setVisibility(View.INVISIBLE);
                isConnected = intent.getBooleanExtra("is_connected", false);
                Log.d("isConnected", "connect:"+ isConnected);
                if (isConnected) {
                    NetworkStat.setImageResource(R.mipmap.network_good);
                    wifiRefresh.setVisibility(View.INVISIBLE);
                }else {
                    NetworkStat.setImageResource(R.mipmap.network_error);
                    wifiRefresh.setVisibility(View.VISIBLE);
                }
            }
        }
    };

    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //ImageButton btnHamburger = findViewById(R.id.btn_hamburger);
        // 在您的 Activity 中
        setContentView(R.layout.activity_message);

        IntentFilter intentFilter = new IntentFilter("websocket_connection_status");

        LocalBroadcastManager.getInstance(this).registerReceiver(connectionStatusReceiver, intentFilter);
        websocket = new websocket(this);

        TextView messageView = (TextView)findViewById(R.id.Classtitle);
        String ClassNumber = database.getClassNumber();
        ClassNumber = "Class:" + ClassNumber;
        messageView.setText(ClassNumber);
        NetworkStat = findViewById(R.id.imageView);
        wifiRefresh = findViewById(R.id.refreshWifi);
        roundBar = findViewById(R.id.roundBar);
        //drawerLayout = findViewById(R.id.drawer_layout);


        drawerLayout = findViewById(R.id.drawer_layout);
        NavigationView navigationView = findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(this, drawerLayout, R.string.open_drawer, R.string.close_drawer);
        drawerLayout.addDrawerListener(toggle);
        toggle.syncState();


        wifiRefresh.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                websocket.startWebSocket();
                roundBar.setVisibility(View.VISIBLE);
            }
        });

    }



    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
        // 側邊欄選單項目被點擊時的處理邏輯
        int id = item.getItemId();

        if (id == R.id.nav_New) {
            FragmentManager fragmentManager = getSupportFragmentManager();
            fragmentManager.beginTransaction()
                    .replace(R.id.fragmentContainerView, New_message.class, null)
                    .setReorderingAllowed(true)
                    .addToBackStack(null)
                    .commit();
            fragmentTag = "New_message";



            Log.d("NavigationItem", "New clicked");
        } else if (id == R.id.nav_history) {
            FragmentManager fragmentManager = getSupportFragmentManager();
            fragmentManager.beginTransaction()
                    .replace(R.id.fragmentContainerView, History_message.class, null)
                    .setReorderingAllowed(true)
                    .addToBackStack(null)
                    .commit();
            fragmentTag = "History_message";
            Log.d("NavigationItem", "history clicked");
        }
        drawerLayout.closeDrawers();

        return true;
    }



    @Override
    public void onResume() {
        super.onResume();
        Log.d("NetworkSta", String.valueOf(readNetworkStatusInBackground(this)));
//
//        if (readNetworkStatusInBackground(this)) {
//            NetworkStat.setImageResource(R.mipmap.network_good);
//            wifiRefresh.setVisibility(View.INVISIBLE);
//        } else {
//            NetworkStat.setImageResource(R.mipmap.network_error);
//            wifiRefresh.setVisibility(View.VISIBLE);
//        }
        Intent intent = getIntent();
        FragmentManager fragmentManager = getSupportFragmentManager();
        FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();

        fragmentTag = intent.getStringExtra("fragmentTag");
        Log.d("fragmentTag", fragmentTag);
        if (fragmentTag != null) {
            if (fragmentTag.equals("New_message")){
                fragmentTransaction.replace(R.id.fragmentContainerView, New_message.class, null);

            }
            else if (fragmentTag.equals("History_message")) {
                fragmentTransaction.replace(R.id.fragmentContainerView, History_message.class, null);
            }
        }



        fragmentTransaction.commit();

    }


    @Override
    public void onPause() {
        super.onPause();
        SharedPreferences.Editor editor = getSharedPreferences("fragmentTag", MODE_PRIVATE).edit();
        editor.putString("key", fragmentTag);
        editor.apply();
    }


    @Override
    public void onBackPressed() {
        Toast.makeText(this, "Yun'an is what I live for.", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        LocalBroadcastManager.getInstance(this).unregisterReceiver(connectionStatusReceiver);
    }
    public static boolean readNetworkStatusInBackground(Context context) {

        SharedPreferences sharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);

        return sharedPreferences.getBoolean(NETWORK_STATUS_KEY, true);
    }

    public static String readFragmentTag(Context context) {
        SharedPreferences sharedPreferences = context.getSharedPreferences(Frag_PREF, Context.MODE_PRIVATE);
        return sharedPreferences.getString(Fragment_STATUS_KEY, null);
    }
}