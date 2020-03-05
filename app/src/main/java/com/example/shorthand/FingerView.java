package com.example.shorthand;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.util.AttributeSet;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.TextView;

import java.util.ArrayList;


public class FingerView extends View {

    Network network = new Network();
    public static int BRUSH_SIZE = 20;
    public static final int DEFAULT_COLOR = Color.BLACK;
    public static final int BACKGROUND_COLOR = Color.WHITE;
    private static final float TOUCH_TOLERANCE = 4;
    private ArrayList<FingerPath> paths = new ArrayList<>();
    private float mX, mY;
    private Path mPath;
    private Paint mPaint;
    private int currentColor;
    private int backgroundColor = BACKGROUND_COLOR;
    private int strokeWidth;
    private Bitmap mBitmap;
    private Canvas mCanvas;
    private Paint mBitmapPaint = new Paint(Paint.DITHER_FLAG);
    private long timeStart;
    private long timeStop;
    private long timeDelta;
    private double timeInSeconds;
    public int count;

    public FingerView(Context context) {
        this(context, null);
    }

    public FingerView(Context context, AttributeSet attrs) {
        super(context, attrs);
        mPaint = new Paint();
        mPaint.setAntiAlias(true);
        mPaint.setDither(true);
        mPaint.setColor(DEFAULT_COLOR);
        mPaint.setStyle(Paint.Style.STROKE);
        mPaint.setStrokeJoin(Paint.Join.ROUND);
        mPaint.setStrokeCap(Paint.Cap.ROUND);
        mPaint.setXfermode(null);
        mPaint.setAlpha(0xff);

    }

    public void init(DisplayMetrics metrics) {
        int height = metrics.heightPixels;
        int width = metrics.widthPixels;

        mBitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888);
        mCanvas = new Canvas(mBitmap);

        currentColor = DEFAULT_COLOR;
        strokeWidth = BRUSH_SIZE;

        count = 0;
    }


    public void clear() {
        backgroundColor = BACKGROUND_COLOR;
        paths.clear();
        invalidate();
    }

    @Override
    protected void onDraw(Canvas canvas) {
        canvas.save();
        mCanvas.drawColor(backgroundColor);

        for (FingerPath fp : paths) {
            mPaint.setColor(fp.color);
            mPaint.setStrokeWidth(fp.strokeWidth);
            mPaint.setMaskFilter(null);
            mCanvas.drawPath(fp.path, mPaint);

        }

        canvas.drawBitmap(mBitmap, 0, 0, mBitmapPaint);
        canvas.restore();
    }

    public void touchStart(float x, float y) {
        mPath = new Path();
        FingerPath fp = new FingerPath(currentColor, strokeWidth, mPath);
        paths.add(fp);

        mPath.reset();
        mPath.moveTo(x, y);
        mX = x;
        mY = y;
    }

    public void touchMove(float x, float y) {
        float dx = Math.abs(x - mX);
        float dy = Math.abs(y - mY);

        if (dx >= TOUCH_TOLERANCE || dy >= TOUCH_TOLERANCE) {
            mPath.quadTo(mX, mY, (x + mX) / 2, (y + mY) / 2);
            mX = x;
            mY = y;
        }
    }

    public void touchUp() {
        mPath.lineTo(mX, mY);
    }






    /*
    // onTouchEvent has been commented out by Quinn.
    // This function has been moved to WriteActivity.java
    // in order to allow access/modification of other
    // Views (DocumentView) when touch events
    // from FingerView occur.

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        float x = event.getX();
        float y = event.getY();

        switch(event.getAction()) {
            case MotionEvent.ACTION_DOWN :
                touchStart(x, y);
                invalidate();
                break;
            case MotionEvent.ACTION_MOVE :
//                Log.i("onTouchEvent()", "x: " + x + " y: " + y);
//                timeStart = System.nanoTime();
                touchMove(x, y);
//                timeStop = System.nanoTime();
//                timeDelta = timeStop - timeStart;
//                timeInSeconds = timeDelta / 1000.0;
//                Log.i("onTouchEvent()", "timeStamp: " + System.currentTimeMillis() + " currentTimeMillis ");
                count++;
                network.send(x,y,count);
                invalidate();
                break;
            case MotionEvent.ACTION_UP :
                network.send(-1,-1,count);
                touchUp();
                invalidate();
                clear();
                count = 0;
                network.getResponseString();
                System.out.println("Response: " + network.response_string);



                break;
        }

        return true;
    }

     */
}

