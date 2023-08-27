package com.hfad.swbs_intergrate_test;


import androidx.appcompat.app.AppCompatActivity;
import android.content.ContentValues;
import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Settings;
import android.util.Log;
import android.view.KeyEvent;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    MyDatabaseHelper database = new MyDatabaseHelper(this);
    TextView warning;
    EditText messageView;
    ContentValues values = new ContentValues();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (!Settings.canDrawOverlays(this)) {
            Intent intent = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse("package:"+ getPackageName()));
            startActivityForResult(intent, 100);
        }



        SQLiteDatabase db = database.getReadableDatabase();
        setContentView(R.layout.activity_main);
        //database.onUpgrade(db,1,2);
        String ClassNum = database.getClassNumber();

        if (ClassNum != "-1" && ClassNum != "null") {
            Log.d("Yes", "There are value in Class");
            Log.d("ClassNum", "ClassNumber: "+ ClassNum);
            Intent intent = new Intent(this, update.class);
            startActivity(intent);
        } else {
            Log.d("Class Number ", "There is no value in database");
        }

        messageView = findViewById(R.id.classPin);
        messageView.setOnEditorActionListener( new TextView.OnEditorActionListener() {
            @Override
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                if (actionId == EditorInfo.IME_ACTION_DONE) {
                    String userInput = messageView.getText().toString();
                    Log.d("Enter pressed", "Get Class number" + userInput );
                    checkClassNumber(userInput);
                    return true; // 返回 true 表示已處理此事件
                }
                return false; // 返回 false 表示未處理此事件，繼續處理其他事件
            }
        });

        Button button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                warning = findViewById(R.id.Warning);
                messageView = findViewById(R.id.classPin);
                // 取得輸入數字
                String messageText = messageView.getText().toString();
                Log.d("messageInput", messageText);
                checkClassNumber(messageText);

            }
        });
    }

    private void checkClassNumber (String ClassNumber) {
        Log.d("messageInput", ClassNumber);
        if (!ClassNumber.isEmpty()) {
            try {
                int classNumber = Integer.parseInt(ClassNumber);
                if ((classNumber >= 701 && classNumber <= 705) ||
                        (classNumber >= 801 && classNumber <= 805) ||
                        (classNumber >= 901 && classNumber <= 905) ||
                        (classNumber >= 101 && classNumber <= 106) ||
                        (classNumber >= 111 && classNumber <= 116) ||
                        (classNumber >= 121 && classNumber <= 126)) {

                    SQLiteDatabase initDatabase = database.getReadableDatabase();
                    // 匯入資料庫
                    values.put("id", 1);
                    values.put("classNumber", ClassNumber);
                    initDatabase.insert("initData", null, values);
                    values.clear();
                    for (int j = 8; j < 16; j++) {
                        insertData(j, 0, 10);
                    }
                    // 將班級同步轉換至另一活動
                    Intent intent = new Intent(MainActivity.this, update.class);
//                    intent.setType("text/plain");
//                    intent.putExtra("message", ClassNumber);
                    startActivity(intent);
                } else {
                    warning.setText("班級號碼不在指定範圍內");
                }

            } catch (java.lang.NumberFormatException e)  {
                warning.setText("Please enter a class number");


            }
        } else {
            warning.setText("Please Enter Class number.");
        }
    }


//    private void insertValues (ContentValues values, int breakHour, int breakMinStart, int breakMinEnd) {
//        MyDatabaseHelper database = new MyDatabaseHelper(MainActivity.this);
//        SQLiteDatabase db = database.getWritableDatabase();
//        values.put("fromWhere", fromWere);
//        values.put("content", content);
//        values.put("sendtime", sendtime);
//        values.put("toWho", toWho);
//        db.insert("mytable",null,values);
//    }

    public void insertData(int breakHour, int breakStartMinute, int breakEndMinute) {
        SQLiteDatabase insertData = database.getWritableDatabase();
        values.put("breakHour", breakHour);
        values.put("breakStartMinute", breakStartMinute);
        values.put("breakEndMinute", breakEndMinute);
        Log.d("Put break time in database", values.toString());
        long rowid = insertData.insert("initData", null, values);
        if (rowid != -1) {
            Log.d("Successful insert", Long.toString(rowid));
        } else {
            Log.e("not Successful insert", "Bug");
        }
    }

    @Override
    public void onBackPressed() {
        Toast.makeText(this, "yun'an is what I live for...", Toast.LENGTH_SHORT).show();
    }
}