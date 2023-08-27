package com.hfad.swbs_intergrate_test;

import android.content.Context;
import android.graphics.PixelFormat;
import android.os.Build;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.widget.TextView;

public class FloatingViewManager {

    private WindowManager windowManager;
    private View floatingView;
    private TextView textView;

    public FloatingViewManager(Context context) {
        windowManager = (WindowManager) context.getSystemService(Context.WINDOW_SERVICE);
        floatingView = LayoutInflater.from(context).inflate(R.layout.floating_view, null);

        // 可根據需要設置懸浮視窗的位置和大小
        WindowManager.LayoutParams params = new WindowManager.LayoutParams(
                WindowManager.LayoutParams.WRAP_CONTENT,
                WindowManager.LayoutParams.WRAP_CONTENT,
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE | WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
                PixelFormat.TRANSLUCENT
        );
        params.gravity = Gravity.TOP | Gravity.START;
        params.x = 0;
        params.y = 0;

        textView = floatingView.findViewById(R.id.textView);
        windowManager.addView(floatingView, params);
    }

    public void updateText(String text) {
        textView.setText(text);
    }

    public void removeView() {
        if (floatingView != null) {
            windowManager.removeView(floatingView);
            floatingView = null;
        }
    }
}
