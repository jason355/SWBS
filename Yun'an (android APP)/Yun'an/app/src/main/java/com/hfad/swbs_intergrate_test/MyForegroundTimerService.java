package com.hfad.swbs_intergrate_test;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Intent;
import android.os.CountDownTimer;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;
import android.widget.Toast;
import android.database.sqlite.SQLiteDatabase;

public class MyForegroundTimerService extends Service {

    private static final int NOTIFICATION_ID = 2;
    private static final String CHANNEL_ID = "ForegroundTimerServiceChannel";

    int count = 0;
    int result;
    private timer clock;
    boolean canPass = true;
    int delay = 0;
    private CountDownTimer countDownTimer;
    private FloatingViewManager floatingViewManager;
    MyDatabaseHelper database = new MyDatabaseHelper(this);
    private Handler handler = new Handler();

    @Override
    public void onCreate() {
        super.onCreate();
        clock = new timer(this);

    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        createNotificationChannel();
        Notification notification = buildNotification();
        startForeground(NOTIFICATION_ID, notification);


        Log.d("Timer", "Started in onStartCommand");

        runTimer();



        return START_STICKY;

        // 返回 START_STICKY，表示 Service 被終止後會自動重啟

    }

    private void runTimer() {
        //floatingViewManager = new FloatingViewManager(this);
        if (count <= 8 && canPass) {
            result = clock.startClock();
            //Log.d("Timer result", Integer.toString(result));
            if (result == 1) {
                // Context context = getApplicationContext();
                if (database.isNew()){

                   Intent intentCountDownService = new Intent(MyForegroundTimerService.this, CountDown.class);
                   startService(intentCountDownService);

                }


            } else if (result == 0) {
                if (database.isNew()) {
                    Intent intent1 = new Intent(MyForegroundTimerService.this, messageActivity.class);
                    startActivity(intent1);
                }

            } else if (result != -1) {
                canPass = false;
                Log.d("Time result", "result != -1");
                delay = result;
                handler.postDelayed(new Runnable() {
                    @Override
                    public void run() {
                        canPass = true;
                        runTimer();
                    }
                }, delay);
            }
            else {
                handler.postDelayed(new Runnable() {
                    @Override
                    public void run() {

                        runTimer();
                    }
                }, 0);
            }
            count++;
            Log.d("count", Integer.toString(count));
        }
        else {
            Log.d("MyForegroundTimerService", "Closing");
            stopForeground(true);
            stopSelf();
        }
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
        builder = new Notification.Builder(this, CHANNEL_ID);

        return builder
                .setContentTitle("Foreground Service")
                .setContentText("Running in the background")
                .setSmallIcon(R.mipmap.logo)
                .build();
    }
}
