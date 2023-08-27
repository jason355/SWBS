package com.hfad.swbs_intergrate_test;

import android.annotation.SuppressLint;
import android.companion.WifiDeviceFilter;
import android.content.Context;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.media.MediaPlayer;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.os.CountDownTimer;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.util.Arrays;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link New_message#newInstance} factory method to
 * create an instance of this fragment.
 */
public class New_message extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";


    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    int count = 0;
    TextView teacher;
    TextView fromWhere;
    int color = Color.WHITE;
    TextView content;
    TextView sendtime;
    TextView page_num;
    String[][] message;
    boolean isFirst = true;

    private Handler handler;
    private Runnable updateRunnable;

    private CountDownTimer countDownTimer;
    private LinearLayout progressBarContainer;
    int currentProgressBarIndex = 0;

    private static final int TOTAL_TIME_MS = 10000;  // 進度條總時間（毫秒）
    private static final int INTERVAL_MS = 10;


    public New_message() {
    }


    public static New_message newInstance(String param1, String param2) {
        New_message fragment = new New_message();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        isFirst = true;
        View view = inflater.inflate(R.layout.fragment_new_message, container, false);
        view.setTag("New_message");
        teacher = view.findViewById(R.id.teacher);
        fromWhere = view.findViewById(R.id.fromWhere);
        content = view.findViewById(R.id.content);
        sendtime = view.findViewById(R.id.sendtime);
        page_num = view.findViewById(R.id.page_num);

        MyDatabaseHelper database = new MyDatabaseHelper(requireContext());
        message = database.getNewMessage();



        if (message != null){
            int numberofProgressBar = message.length;
            if (numberofProgressBar != 1) {
                Log.d("New_message", "message = " + numberofProgressBar);

                progressBarContainer = view.findViewById(R.id.progressBarContainer);
                //int fragmentWidth = getResources().getDisplayMetrics().widthPixels;
                //Log.d("fragmentWidth", String.valueOf(fragmentWidth));
                int max_len = (int)(1050 / numberofProgressBar * 80 / 100);
                int space = (int)(max_len /16);


                for (int i = 0; i < numberofProgressBar; i++) {

                    ProgressBar progressBar = new ProgressBar(requireContext(), null, android.R.attr.progressBarStyleHorizontal);
                    progressBar.setVisibility(View.VISIBLE);
                    progressBar.setMax(100);
                    progressBar.setTag(i);
                    progressBar.setProgressTintList(ColorStateList.valueOf(color));
                    LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(
                            max_len,
                            LinearLayout.LayoutParams.WRAP_CONTENT
                    );

                    layoutParams.setMargins(space, 0, space, 0);



                    if (progressBar.getParent() != null) {
                        ((ViewGroup) progressBar.getParent()).removeView(progressBar);
                    }
                    progressBarContainer.addView(progressBar, layoutParams);

                }
                updateMessage(message, database);
                startNextProgressBar(database);


            }
            else {
                updateMessage(message, database);
            }

        }
        else {
            content.setText("無新訊息");
        }
        return view;
    }




    private void startNextProgressBar(MyDatabaseHelper database) {
        int numberofProgressBar = message.length;
        Log.d("currentProgressBarindex", String.valueOf(currentProgressBarIndex));
        countDownTimer = new CountDownTimer(TOTAL_TIME_MS, INTERVAL_MS) {
            ProgressBar currentProgressBar = (ProgressBar) progressBarContainer.getChildAt(currentProgressBarIndex);
            @Override
            public void onTick(long millisUntilFinished) {

                int progress = (int) ((TOTAL_TIME_MS - millisUntilFinished) * 100 / TOTAL_TIME_MS);
                currentProgressBar.setProgress(progress);

            }

            @Override
            public void onFinish() {
                currentProgressBar.setProgress(100);
                currentProgressBarIndex = (currentProgressBarIndex + 1 ) % numberofProgressBar;
                if (currentProgressBarIndex == 0) {
                    resetProgressBar();
                }
                updateMessage(message, database);
                startNextProgressBar(database);

            }

        };
        //
        countDownTimer.start();


    }


    @SuppressLint("SetTextI18n")
    private void updateMessage(String[][] message, MyDatabaseHelper database) {

        int len = message.length;
        if (count < len) {
            teacher.setText(message[count][0]);
            fromWhere.setText(message[count][1]);
            content.setText(message[count][2]);
            sendtime.setText(message[count][3]);
            page_num.setText(count+1 + "/" + message.length);
            if (isFirst) {
                database.haveShowed(message[count][2]);
                Log.d("updateMessage", "wirte" + message[count][2]+"in to 0");
            }
            count++;
        } else {
            count = 0;
            isFirst = false;
            teacher.setText(message[count][0]);
            fromWhere.setText(message[count][1]);
            content.setText(message[count][2]);
            sendtime.setText(message[count][3]);
            page_num.setText(count+1 + "/" + message.length);
            count++;
        }

    }




        private void resetProgressBar() {
            int numberofProgressBar = message.length;

            for (int j = 1; j <= numberofProgressBar;j++) {
                View childView = progressBarContainer.getChildAt(j);
                if (childView instanceof ProgressBar) {
                    ProgressBar progressBar = (ProgressBar) childView;
                    progressBar.setProgress(0);
                }
            }
        }

    @Override
    public void onResume() {
        super.onResume();

    }

    @Override
    public void onPause() {
        super.onPause();
        if (countDownTimer != null)
            countDownTimer.cancel();

    }

}

