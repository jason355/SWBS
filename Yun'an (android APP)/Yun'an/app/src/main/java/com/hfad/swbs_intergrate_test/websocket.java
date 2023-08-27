package com.hfad.swbs_intergrate_test;

import android.content.ContentValues;
import android.content.Intent;
import android.content.SharedPreferences;
import android.media.MediaPlayer;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

public class websocket extends WebSocketListener {
    private WebSocket webSocket;
    private final MyDatabaseHelper database;
    Gson gson = new Gson();
    private final Context context;
    private static final String PREFS_NAME = "MyPrefs";
    private static final String NETWORK_STATUS_KEY = "network_status";
    private MediaPlayer mediaPlayer;
    String ClassNum;
    int retryAttempts = 0;
    int MAX_RETRY_ATTEMPTS = 10;
    int RETRY_DELAY_MS = 600000;
    public websocket(Context context) {
        this.context = context;
        database = new MyDatabaseHelper(context);
    }
    public void startWebSocket() {
        OkHttpClient client = new OkHttpClient();

        Request request = new Request.Builder()
                .url("ws://192.168.0.3:5000")
                .build();


        webSocket = client.newWebSocket(request, this);
//        SharedPreferences sharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
//        SharedPreferences.Editor editor = sharedPreferences.edit();
//        editor.putBoolean(NETWORK_STATUS_KEY, true);
//        editor.apply();
    }

//    public void sendMessage(String message) {
//        webSocket.send(message);
//    }

    public void closeWebSocket() {
        webSocket.close(1000, "WebSocket closed");
    }

    @Override
    public void onOpen(@NonNull WebSocket webSocket, @NonNull Response response) {
//        SQLiteDatabase db = database.getReadableDatabase();
        ClassNum = database.getClassNumber();
        broadcastConnectionStatus(true);
        if (ClassNum != "-1") {
            webSocket.send(ClassNum);

        } else {
            Log.e("Websocket classNum", "Can't Not get class number.");
        }

    }

    Type listType = new TypeToken<List<Message>>(){}.getType();
//    ContentValues values = new ContentValues();

    List<Message> messages = new ArrayList<Message>();
    @Override
    public void onMessage(@NonNull WebSocket webSocket, @NonNull String text) {
        mediaPlayer = MediaPlayer.create(context, R.raw.marimba);
        mediaPlayer.seekTo(0);
        mediaPlayer.start();
        broadcastConnectionStatus(true);
        SQLiteDatabase db = database.getWritableDatabase();
        ContentValues values = new ContentValues();
        Log.d("Get", "Get message"+ text);
        if (text != null) {
            messages = gson.fromJson(text, listType);
            for (Message message: messages) {
                values.put("teacher", message.getTeacher());
                values.put("fromWhere", message.getFromWhere());
                values.put("content", message.getContent());
                values.put("sendtime", message.getSendTime());
                values.put("isNew", message.getIsNew());
                db.insert("mytable", null, values);
            }
        }

        Intent intent = new Intent(context, CountDown.class);
        //intent.putExtra("fragmentTag", "History_message");
        context.startService(intent);

    }



    @Override
    public void onClosing(WebSocket webSocket, int code, String reason) {
        startWebSocket();
    }

    @Override
    public void onClosed(WebSocket webSocket, int code, String reason) {
        Log.d("onClosed", "reason");
    }

    @Override
    public void onFailure(WebSocket webSocket, Throwable t, Response response) {
        Log.e("Error", "some thing went wrong " + t);
//        SharedPreferences sharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
//        SharedPreferences.Editor editor = sharedPreferences.edit();
//        editor.putBoolean(NETWORK_STATUS_KEY, false);
//        editor.apply();
        broadcastConnectionStatus(false);
        if (retryAttempts < MAX_RETRY_ATTEMPTS) {
            retryAttempts++;
            Log.d("Websocket", "Retrying... Attempt: " + retryAttempts);
            mediaPlayer = MediaPlayer.create(context, R.raw.networkerror);
            mediaPlayer.seekTo(0);
            mediaPlayer.start();

            new Handler(Looper.getMainLooper()).post(new Runnable() {
                @Override
                public void run() {
                    Toast.makeText(context, "網路斷線，請檢查網路連線或連繫技術人員.", Toast.LENGTH_SHORT).show();
                }
            });


            // 使用 Handler 進行重試
            new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {
                @Override
                public void run() {
                    // 重新啟動 WebSocket 連接
                    startWebSocket();
                }
            }, RETRY_DELAY_MS);
        } else {
            Log.e("Websocket", "Maximum retry attempts reached. Connection failed.");
            mediaPlayer = MediaPlayer.create(context, R.raw.networkfail);
            mediaPlayer.seekTo(0);
            mediaPlayer.start();
        }
    }

private void broadcastConnectionStatus(boolean isConnected) {
        Intent intent = new Intent("websocket_connection_status");
        intent.putExtra("is_connected", isConnected);
        LocalBroadcastManager.getInstance(context).sendBroadcast(intent);
}
    public static class Message {
        private String teacher;
        private String fromWhere;
        private String content;
        private String sendTime;
        private int isNew;
        public String getTeacher() {
            return teacher;
        }
        public String getFromWhere() {
            return fromWhere;
        }
        public String getContent() {
            return content;
        }
        public String getSendTime() {
            return sendTime;
        }
        public int getIsNew() {
            return isNew;
        }
    }
}
