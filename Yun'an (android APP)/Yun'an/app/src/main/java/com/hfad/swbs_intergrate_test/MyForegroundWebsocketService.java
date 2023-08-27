package com.hfad.swbs_intergrate_test;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.IBinder;
import android.util.Log;

public class MyForegroundWebsocketService extends Service {

    private static final int NOTIFICATION_ID = 1;
    private static final String CHANNEL_ID = "ForegroundWebsocketServiceChannel";
    private websocket webSocketClient;
    boolean isConnected;

    @Override
    public void onCreate() {
        super.onCreate();
        webSocketClient = new websocket(this);
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // 在這裡執行你的背景任務

        // 創建一個通知並將服務設置為前景
        createNotificationChannel();
        Notification notification = buildNotification();
        startForeground(NOTIFICATION_ID, notification);
        webSocketClient.startWebSocket();
        // 返回 START_STICKY，表示 Service 被終止後會自動重啟
        return START_STICKY;
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        // 停止任務，並移除前景狀態
        stopForeground(true);
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    private void createNotificationChannel() {
        NotificationChannel serviceChannel = new NotificationChannel(
                CHANNEL_ID,
                "Foreground Service Channel",
                NotificationManager.IMPORTANCE_DEFAULT
        );
        NotificationManager manager = getSystemService(NotificationManager.class);
        manager.createNotificationChannel(serviceChannel);
    }

    private Notification buildNotification() {
        Notification.Builder builder;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            builder = new Notification.Builder(this, CHANNEL_ID);
        } else {
            builder = new Notification.Builder(this);
        }

        return builder
                .setContentTitle("Foreground Service")
                .setContentText("Running in the background")
                .setSmallIcon(R.mipmap.logo)
                .build();
    }
}
