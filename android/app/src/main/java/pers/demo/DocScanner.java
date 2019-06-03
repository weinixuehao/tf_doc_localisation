package pers.demo;

import android.content.Context;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.util.Log;

import org.opencv.android.Utils;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.imgproc.Imgproc;
import org.tensorflow.contrib.android.TensorFlowInferenceInterface;

import java.util.ArrayList;
import java.util.List;

import static org.opencv.core.CvType.CV_8UC3;

public class DocScanner {
//    private static final String MODEL_FILE = "file:///android_asset/255X340_frozen_model.pb";
    private static final String MODEL_FILE = "file:///android_asset/frozen_model.pb";
    private static final String INPUT_NODE = "input";
    private static final String OUTPUT_NODE = "heats_map_regression/pred_keypoints/BiasAdd";
    private static DocScanner instance;
    private TensorFlowInferenceInterface tensorFlowInferenceInterface;
    private AssetManager assetManager;
    private int width = 600, height = 800;
    private int outWidth = 19, outHeight = 25;

    public DocScanner(Context context) {
        this.assetManager = context.getAssets();
        tensorFlowInferenceInterface = new TensorFlowInferenceInterface(assetManager, MODEL_FILE);
    }

    static {
        System.loadLibrary("opencv_java3");
        System.loadLibrary("tensorflow_inference");
    }

    public static synchronized DocScanner getInstance(final Context context) {
        if (instance == null) {
            instance = new DocScanner(context.getApplicationContext());
        }
        return instance;
    }

    public void inference(Bitmap bitmap) {
        int[] intValues = new int[width * height];
        float[] floatValues = new float[width * height * 3];
        bitmap.getPixels(intValues, 0, bitmap.getWidth(), 0, 0, bitmap.getWidth(), bitmap.getHeight());
        for (int i = 0; i < intValues.length; ++i) {
            final int val = intValues[i];
            // bitwise shifting - without our image is shaped [1, 168, 168, 1] but we need [1, 168, 168, 3]
//            floatValues[i * 3 + 2] = Color.red(val);
//            floatValues[i * 3 + 1] = Color.green(val);
//            floatValues[i * 3] = Color.blue(val);
            floatValues[i * 3] = Color.red(val);
            floatValues[i * 3 + 1] = Color.green(val);
            floatValues[i * 3 + 2] = Color.blue(val);
        }
        long[] dims = {1, height, width, 3};
        tensorFlowInferenceInterface.feed(INPUT_NODE, floatValues, dims);
        tensorFlowInferenceInterface.run(new String[]{OUTPUT_NODE});
        float[] outputs = new float[outHeight * outWidth * 4];
        tensorFlowInferenceInterface.fetch(OUTPUT_NODE, outputs);
        Mat dummy = new Mat(outHeight, outWidth, CvType.CV_32FC4);
        List<Mat> heatmaps_activations = new ArrayList<>();
        Core.split(dummy, heatmaps_activations);
        Mat p1 = heatmaps_activations.get(0);
        Mat p2 = heatmaps_activations.get(1);
        Mat p3 = heatmaps_activations.get(2);
        Mat p4 = heatmaps_activations.get(3);
        Mat tmpMat = new Mat();
        Core.add(p1, p2, tmpMat);
        Core.add(tmpMat, p3, tmpMat);
        Core.add(tmpMat, p4, tmpMat);
        Mat grayscale = new Mat();
        tmpMat.convertTo(grayscale, CV_8UC3 , 255, 0);
        Mat _heatmap = new Mat();
        Imgproc.applyColorMap(grayscale, _heatmap, Imgproc.COLORMAP_JET);
        Bitmap bmp = Bitmap.createBitmap(_heatmap.cols(), _heatmap.rows(), Bitmap.Config.ARGB_8888);
        Utils.matToBitmap(_heatmap, bmp);

        Log.i("sss", "sss");
    }
}
