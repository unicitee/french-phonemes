package com.unicitee.tamara;

import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.util.HashMap;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {
    private static Python py ;
    private static final String TAG = "TAMARA";
    static TextToSpeech textToSpeech ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
        Button btn = findViewById(R.id.btn);
        Button btn2 = findViewById(R.id.btn2);

        final TextView textView = findViewById(R.id.textView);
        final EditText editText = findViewById(R.id.editText);
        btn2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String txt = editText.getText().toString();
                speak(txt);
            }
        });
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String txt = editText.getText().toString();
                py = Python.getInstance();
                String pyStr = py.getModule("Phoneme").callAttr("breakdownWord",txt).toString();
                textView.setText(pyStr);
            }
        });

        textToSpeech = new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.ERROR) {
                    Log.e(TAG, "TTS init failed");
                } else if (status == TextToSpeech.SUCCESS) {
                    textToSpeech.setOnUtteranceProgressListener(new UtteranceProgressListener() {
                        @Override
                        public void onDone(String utteranceId) {
                            Log.i(TAG, "TTS complete " + utteranceId );
                            textToSpeech.stop();
                        }

                        @Override
                        public void onError(String utteranceId) {
                            Log.e(TAG, "TTS error "+utteranceId);
                        }

                        @Override
                        public void onStart(String utteranceId) {
                            Log.i(TAG, "TTS start "+utteranceId);
                        }
                    });

                    int result = textToSpeech.setLanguage(Locale.FRANCE);
                    if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Log.e(TAG, "This Language is not supported");
                    }

                    speak("");
                }
            }
        });
    }

    private static void speak(String txt) {
        Log.i(TAG,"try speaking "+txt);

        String utteranceId = Integer.toString(txt.hashCode());
        HashMap<String, String> params = new HashMap<String, String>();
        params.put(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, utteranceId);
        int speechStatus = textToSpeech.speak(txt, TextToSpeech.QUEUE_ADD, params);

        if (speechStatus == TextToSpeech.ERROR) {
            Log.e(TAG, "Error in converting Text to Speech!");
        }
    }
}
