package com.hfad.swbs_intergrate_test;

import android.annotation.SuppressLint;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link History_message#newInstance} factory method to
 * create an instance of this fragment.
 */
public class History_message extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    int seeing = 0;
    Button next;
    Button prev;
    TextView teacher;
    TextView fromWhere;
    TextView content;
    TextView sendtime;
    TextView page_num;

    public History_message() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment History_message.
     */
    // TODO: Rename and change types and number of parameters
    public static History_message newInstance(String param1, String param2) {
        History_message fragment = new History_message();
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
        View view = inflater.inflate(R.layout.fragment_history_message, container, false);

        MyDatabaseHelper database = new MyDatabaseHelper(requireContext());
        next = view.findViewById(R.id.next);
        prev = view.findViewById(R.id.prev);
        teacher = view.findViewById(R.id.teacher);
        fromWhere = view.findViewById(R.id.fromWhere);
        content = view.findViewById(R.id.content);
        sendtime = view.findViewById(R.id.sendtime);
        page_num = view.findViewById(R.id.page_num);

        String[][] message;
        message = database.getMessage();

        if (message != null) {
            showMessage(message);
        } else{
            content.setText("無訊息紀錄");
        }

        next.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (message != null) {
                    seeing += 1;
                    showMessage(message);
                }


            }
        });

        prev.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (message != null) {
                    seeing -= 1;
                    showMessage(message);
                }

            }
        });

        return view;
    }

    @SuppressLint("SetTextI18n")
    private void showMessage(String[][] message) {
        int len = message.length;
        if (seeing >= len) {
           seeing = 0;
        }
        else if (seeing < 0) {
            seeing = len -1;
        }
        teacher.setText(message[seeing][0]);
        fromWhere.setText(message[seeing][1]);
        content.setText(message[seeing][2]);
        sendtime.setText(message[seeing][3]);
        page_num.setText(seeing + 1 + "/" + message.length);
    }
}