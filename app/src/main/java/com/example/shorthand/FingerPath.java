package com.example.shorthand;


import android.graphics.Path;

public class FingerPath {

    public int color;
    public int strokeWidth;
    public Path path;

    public FingerPath(int color, int strokeWidth, Path path) {
        System.out.println("FingerPath(color,strokeWidth,path)\n");
        this.color = color;
        this.strokeWidth = strokeWidth;
        this.path = path;
    }
}