package com.unicitee.tamara;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class MainActivity extends AppCompatActivity {
    private static Python py ;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
        Button btn = findViewById(R.id.btn);
        final TextView textView = findViewById(R.id.textView);
        final EditText editText = findViewById(R.id.editText);
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String txt = editText.getText().toString();
                py = Python.getInstance();
                String pyStr = py.getModule("Phoneme").callAttr("breakdownWord",txt).toString();
                textView.setText(pyStr);
            }
        });
    }
}
