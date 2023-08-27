package com.hfad.swbs_intergrate_test;


import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

public class MyDatabaseHelper extends SQLiteOpenHelper {
    private static final String DATABASE_NAME = "mydatabase.db";
    private static final int DATABASE_VERSION = 1;

    String[][] message;
    public MyDatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        // 建立資料表
        String createTableQuery = "CREATE TABLE if not exists " +
                " mytable (id INTEGER PRIMARY KEY AUTOINCREMENT, teacher varchar(15), " +
                "fromWhere varchar(15), content TEXT, " +
                "sendtime DATETIME, isNew int)";
        db.execSQL(createTableQuery);


        createTableQuery = "CREATE TABLE if not exists " +
                "initData (id INTEGER PRIMARY KEY AUTOINCREMENT, classNumber varchar(5) UNIQUE, breakHour int, breakStartMinute int, breakEndMinute int)";
        db.execSQL(createTableQuery);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // 更新資料庫
        String dropTableQuery = "DROP TABLE IF EXISTS mytable";
        db.execSQL(dropTableQuery);
        dropTableQuery = "DROP TABLE IF EXISTS initData";
        db.execSQL(dropTableQuery);
        onCreate(db);
    }
    public String getClassNumber() {
        SQLiteDatabase db = getReadableDatabase();
        String query = "SELECT classNumber FROM initData";
        Cursor cursor = db.rawQuery(query, null);
        if (cursor.moveToFirst()){
            while (cursor.moveToNext()) {
                int index = cursor.getColumnIndex("classNumber");
                String classNumber = cursor.getString(index);
                if (classNumber != null) {
                    cursor.close();
                    return classNumber;
                }

            }
        }
        return "-1";
    }
    public boolean isNew() {
        SQLiteDatabase db = getReadableDatabase();
        String search = "SELECT isNew FROM mytable WHERE isNew = 1";
        Cursor cursor = db.rawQuery(search, null);
        if (cursor.moveToFirst() && cursor.getCount() != 0) {
            cursor.close();
            return true;
        }
        else {
            cursor.close();
            return false;
        }
    }

    public void messageDateCheck() {
        SQLiteDatabase db = getReadableDatabase();
        SQLiteDatabase dbd = getWritableDatabase();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String search = "SELECT * FROM mytable";
        Cursor cursor = db.rawQuery(search, null);
        if (cursor.moveToFirst()) {
            do {
                int sendTimeIndex = cursor.getColumnIndex("sendtime");
                String datetime = cursor.getString(sendTimeIndex);

                LocalDateTime dateTime = LocalDateTime.parse(datetime, formatter);
                LocalDate sendtime = dateTime.toLocalDate();
                LocalDate today = LocalDate.now();
                int daysDifference = (int) ChronoUnit.DAYS.between(today, sendtime);
                Log.d("sendtime", ""+daysDifference);
                if (daysDifference > 3) {
                    int idIndex = cursor.getColumnIndex("id");
                    String id = cursor.getString(idIndex);
                    dbd.delete("mytable", "id" +"=?", new String[]{id});
                }
            } while (cursor.moveToNext());
        }
        cursor.close();
    }

    public String[][] getMessage() {
        int count = 0;
        SQLiteDatabase db = getReadableDatabase();
        String search = "SELECT teacher, fromWhere, content, sendtime FROM mytable";
        Cursor cursor = db.rawQuery(search, null);

        message = new String[cursor.getCount()][4];
        if (cursor.moveToFirst()) {
            do {
                int teacherIndex = cursor.getColumnIndex("teacher");
                int fromWhereIndex = cursor.getColumnIndex("fromWhere");
                int contentIndex = cursor.getColumnIndex("content");
                int sendtimeIndex = cursor.getColumnIndex("sendtime");
                String teacher = cursor.getString(teacherIndex);
                String fromWhere = cursor.getString(fromWhereIndex);
                String content = cursor.getString(contentIndex);
                String sendtime = cursor.getString(sendtimeIndex);
                message[count][0] = teacher;
                message[count][1] = fromWhere;
                message[count][2] = content;
                message[count][3] = sendtime;
                count++;
            } while (cursor.moveToNext());
            cursor.close();
            return message;
        } else {
            cursor.close();
            return null;
        }
    }


    public String[][] getNewMessage() {
        int count = 0;
        SQLiteDatabase db = getReadableDatabase();
        String search = "SELECT teacher, fromWhere, content, sendtime, isNew FROM mytable where isNew = 1";
        Cursor cursor = db.rawQuery(search, null);
        if (cursor.getCount() != 0) {
            message = new String[cursor.getCount()][4];
            if (cursor.moveToFirst()) {
                do {
                    int teacherIndex = cursor.getColumnIndex("teacher");
                    int fromWhereIndex = cursor.getColumnIndex("fromWhere");
                    int contentIndex = cursor.getColumnIndex("content");
                    int sendtimeIndex = cursor.getColumnIndex("sendtime");

                    String teacher = cursor.getString(teacherIndex);
                    String fromWhere = cursor.getString(fromWhereIndex);
                    String content = cursor.getString(contentIndex);
                    String sendtime = cursor.getString(sendtimeIndex);
                    message[count][0] = teacher;
                    message[count][1] = fromWhere;
                    message[count][2] = content;
                    message[count][3] = sendtime;
                    count++;


                } while (cursor.moveToNext());
                cursor.close();
                return message;
            } else {
                cursor.close();
                return null;
            }
        } else {
            return null;
        }

    }

    public void haveShowed(String content) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put("isNew", 0);
        db.update("mytable", values, " content = ?", new String[] {content});

        db.close();
    }
}
