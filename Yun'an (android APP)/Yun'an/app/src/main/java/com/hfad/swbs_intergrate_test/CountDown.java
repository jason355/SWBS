package com.hfad.swbs_intergrate_test;

import android.annotation.SuppressLint;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.PixelFormat;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.CountDownTimer;
import android.os.IBinder;
import android.provider.Settings;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.TextView;

public class CountDown extends Service {

    TextView textView;
    CountDownTimer countDownTimer;
    private MediaPlayer mediaPlayer;

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }


    @Override
    public void onCreate() {
        super.onCreate();




        WindowManager windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);
        LayoutInflater layoutInflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View floatingView = layoutInflater.inflate(R.layout.activity_count_down, null);

        // 在這裡設置你的懸浮視窗的內容
        WindowManager.LayoutParams parms = new WindowManager.LayoutParams(
                WindowManager.LayoutParams.MATCH_PARENT,
                WindowManager.LayoutParams.WRAP_CONTENT,
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY, // 設定浮動視窗的類型
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
                PixelFormat.TRANSLUCENT
        );
        parms.gravity = Gravity.LEFT;
        parms.alpha = 0.9f;
        textView = floatingView.findViewById(R.id.countdown);
        textView.setText("60秒後顯示");
        textView.setTextSize(30);
        textView.setTextColor(Color.WHITE);
        Button floatingButton = floatingView.findViewById(R.id.delay);
        floatingButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                windowManager.removeView(floatingView);
                countDownTimer.cancel();
                CountDownTimer countDownTimerDelay = new CountDownTimer(7000, 1000) {
                    @SuppressLint("SetTextI18n")
                    @Override
                    public void onTick(long l) {
                        long secondsLeft = l / 1000;
                        Log.d("Countdown", "Seconds left:" + secondsLeft);
                    }

                    @Override
                    public void onFinish() {
                        mediaPlayer = MediaPlayer.create(CountDown.this, R.raw.marimba);
                        mediaPlayer.seekTo(0);
                        mediaPlayer.start();
                        Intent intent1 = new Intent(CountDown.this, messageActivity.class);
                        intent1.putExtra("fragmentTag", "New_message");
                        startActivity(intent1);
                        stopSelf();
                    }
                }.start();
            }
        });

        windowManager.addView(floatingView, parms);

        countDownTimer = new CountDownTimer(5000, 1000) {
            @SuppressLint("SetTextI18n")
            @Override
            public void onTick(long l) {
                long secondsLeft = l / 1000;
                Log.d("Countdown", "Seconds left:" + secondsLeft);
                textView.setText(secondsLeft+"秒後顯示");
            }

            @Override
            public void onFinish() {
                windowManager.removeView(floatingView);
                mediaPlayer = MediaPlayer.create(CountDown.this, R.raw.marimba);
                mediaPlayer.seekTo(0);
                mediaPlayer.start();
                Intent intent1 = new Intent(CountDown.this, messageActivity.class);
                intent1.putExtra("fragmentTag", "New_message");
                startActivity(intent1);
                stopSelf();
            }
        }.start();
    }
}