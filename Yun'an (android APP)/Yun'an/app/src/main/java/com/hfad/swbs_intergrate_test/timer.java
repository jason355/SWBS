package com.hfad.swbs_intergrate_test;


import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.SystemClock;
import android.util.Log;
import android.os.Handler;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class timer {
    MyDatabaseHelper database;
    String[] projection = {
            "breakHour",
            "breakStartMinute",
            "breakEndMinute"
    };
    int[][] breakTime;
    int delaysec;
    int i = 0;
    int next = 0;
    Handler handler;
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm");
    LocalDateTime currentTime;
    public timer (Context context) {
        database = new MyDatabaseHelper(context);
        getBreakTime();
        //Log.e("Break time", Integer.toString(breakTime[0][0]));
    }

    public int startClock() {
        currentTime = LocalDateTime.now();
        String timeString = currentTime.format(formatter);


        int hour = Integer.parseInt(timeString.split(":")[0]);
        int minute = Integer.parseInt(timeString.split(":")[1]);
        Log.d("now hour", Integer.toString(hour));
        Log.d("now minute", Integer.toString(minute));
        if (next >= 8) {
            next = 7;
        }
        if (hour > breakTime[next][0]) {
            Log.d("timer process", "hour > breakTIme");
            next++;
        }
        else if (hour < breakTime[next][0]) {

            delaysec = (breakTime[next][0] - hour) * 3600;
            delaysec -= (minute - breakTime[next][1]) * 60;
            delaysec *= 1000;
            Log.d("timer process", "delay"+delaysec);
            return delaysec;

        }
        else if (minute >= breakTime[next][2]) {
            Log.d("timer process", "minute >= breakTime");
            next++;
        }
        else {
            if ((breakTime[next][2] - minute) > 2) {
                Log.d("time process", "return 1");
                return 1;
            }
            else {
                Log.d("time process", "return 0");
                return 0;
            }
        }
        Log.d("time process", "return -1");
        return -1;
    }


    public void getBreakTime() {
        SQLiteDatabase readData = database.getReadableDatabase();
        Cursor cursor = readData.query("initData", projection, null, null, null, null, null);
        breakTime = new int[8][3];
        if (cursor.moveToFirst()) {
            while (cursor.moveToNext()) {
                int breakHour = cursor.getInt(cursor.getColumnIndexOrThrow("breakHour"));
                int breakMinStart = cursor.getInt(cursor.getColumnIndexOrThrow("breakStartMinute"));
                int breakMinEnd = cursor.getInt(cursor.getColumnIndexOrThrow("breakEndMinute"));
                Log.d("breakHour", Integer.toString(breakHour));
                Log.d("breakMinuteStart", Integer.toString(breakMinStart));
                Log.d("breakMinuteEnd", Integer.toString(breakMinEnd));
                breakTime[i][0] = breakHour;
                breakTime[i][1] = breakMinStart;
                breakTime[i][2] = breakMinEnd;
                i++;
            }

        }
        cursor.close();

    }
}
