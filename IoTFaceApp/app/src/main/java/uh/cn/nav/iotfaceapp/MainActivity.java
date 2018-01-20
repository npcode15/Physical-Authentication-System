package uh.cn.nav.iotfaceapp;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity implements View.OnClickListener, AdapterView.OnItemSelectedListener
{
    boolean readExtPermGranted = false;
    boolean writeExtPermGranted = false;
    boolean pause = false;

    EditText dateText;
    EditText distanceText;
    EditText nameTag;

    int currentFrameRate = 2;
    SCP_Communication scpcomm;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
//        java.util.logging.Logger.getLogger("com.amazonaws").setLevel(Level.ALL);
        super.onCreate(savedInstanceState);
        currentFrameRate = 0;
        setContentView(R.layout.activity_main);

        Spinner spinner = (Spinner) findViewById(R.id.frameRate);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(MainActivity.this, R.array.framerates, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(adapter);
        spinner.setOnItemSelectedListener(this);
        spinner.setSelection(1);

        final Button btn_refresh = (Button) findViewById(R.id.Refresh);
        btn_refresh.setOnClickListener(this);
        final Button btn_accept = (Button)findViewById(R.id.Btn_Accept);
        btn_accept.setOnClickListener(this);
        final Button btn_reject = (Button)findViewById(R.id.Btn_Reject);
        btn_reject.setOnClickListener(this);

        dateText = (EditText) findViewById(R.id.dateText);
        distanceText = (EditText) findViewById(R.id.distanceText);
        nameTag = (EditText) findViewById(R.id.Name);

        MyFirebaseMessagingService myFirebaseMessagingService = new MyFirebaseMessagingService(MainActivity.this);
        check_and_get_permissions();
    }

    private void check_and_get_permissions()
    {
        Log.d("IOT APP -> ", "Requesting Permissions");
        int requestCodes = 2;

        List<String> permissionsList = new ArrayList<String>();
        permissionsList.add(Manifest.permission.READ_EXTERNAL_STORAGE);
        permissionsList.add(Manifest.permission.WRITE_EXTERNAL_STORAGE);
        String [] permissions = permissionsList.toArray(new String[permissionsList.size()]);

        if (hasAllPermissionsGranted(permissions))
        {
            NextActivity("Down");
        }
        else
            ActivityCompat.requestPermissions(MainActivity.this, permissions, requestCodes);
    }

    public boolean hasAllPermissionsGranted(@NonNull int[] grantResults)
    {
        for (int grantResult : grantResults)
            if (grantResult == PackageManager.PERMISSION_DENIED)
                return false;

        return true;
    }

    public boolean hasAllPermissionsGranted(String[] permissions)
    {
        for (String permission : permissions)
            if (ContextCompat.checkSelfPermission(MainActivity.this, permission) == PackageManager.PERMISSION_DENIED)
                return false;

        return true;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults)
    {
        switch (requestCode)
        {
            case 2:
            {
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED)
                    if (hasAllPermissionsGranted(grantResults))
                        NextActivity("Down");
                break;
            }

            default:
                super.onRequestPermissionsResult(requestCode, permissions, grantResults);

            if (readExtPermGranted && writeExtPermGranted)
            {
                Log.d("IoTApp", "Next Activity Allowed");
                NextActivity("Down");
            }
        }
    }

    void NextActivityBtn(String action)
    {
        try
        {
            ImageView image_View = (ImageView) findViewById(R.id.imageView);

            if (action.equals("Down") || action.equals("down"))
            {
                scpcomm = new SCP_Communication(image_View, MainActivity.this, action, dateText, distanceText, nameTag, currentFrameRate);
            }
            else
            {
                scpcomm = new SCP_Communication(image_View, MainActivity.this, action, dateText, distanceText, nameTag, currentFrameRate);
            }

            scpcomm.execute();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    void NextActivity(String action)
    {
        try
        {
            ImageView image_View = (ImageView) findViewById(R.id.imageView);

            final Handler handler = new Handler();
            handler.postDelayed(new Runnable() {
                public void run()
                {
                    if(pause) {
                        pause = false;
                        handler.removeCallbacks(this);
                    }
//                    else {
//                        handler.postDelayed(this, currentFrameRate * 1000);
//                    }

//                    Toast.makeText(getApplicationContext(), "Refreshing Content...", Toast.LENGTH_SHORT).show();
                    scpcomm = new SCP_Communication(image_View, MainActivity.this, action, dateText, distanceText, nameTag, currentFrameRate);
                    scpcomm.execute();

                    handler.postDelayed(this,(currentFrameRate)*1000 ); //Default rate is 4s
                }
            },  (currentFrameRate)*1000);
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    @Override
    protected void onPause()
    {
        pause = true;
        Toast.makeText(getApplicationContext(), "On pause", Toast.LENGTH_SHORT).show();
        super.onPause();
    }

    @Override
    protected void onResume()
    {
        pause = false;
        Toast.makeText(getApplicationContext(), "On resume", Toast.LENGTH_SHORT).show();
        super.onResume();
    }

    @Override
    public void onClick(View v)
    {
        switch (v.getId())
        {
            case  R.id.Btn_Accept:
            {
                NextActivityBtn("Up:poll:accepted");
                Toast.makeText(MainActivity.this, "User Will be Accepted", Toast.LENGTH_SHORT).show();
                break;
            }

            case R.id.Btn_Reject:
            {
                NextActivityBtn("Up:poll:rejected");
                Toast.makeText(MainActivity.this, "User Will be Rejected", Toast.LENGTH_SHORT).show();
                break;
            }

            case  R.id.Refresh:
            {
                NextActivityBtn("Down");
                Toast.makeText(MainActivity.this, "Refreshing Content", Toast.LENGTH_SHORT).show();
                break;
            }
        }
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id)
    {
        String frameRefreshRate = parent.getItemAtPosition(position).toString();
        currentFrameRate = Integer.parseInt(frameRefreshRate.substring(0, frameRefreshRate.length() - 1 ));

        Toast.makeText(parent.getContext(), "Framerate:" + parent.getItemAtPosition(position).toString() + " Selected", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onNothingSelected(AdapterView<?> parent)
    {

    }

//    void loadImageFromServer(String url, ImageView image_View)
//    {
//        String wurl =  "https://static.pexels.com/photos/92637/pexels-photo-92637.jpeg";
//        Picasso.with(getApplicationContext()).load(url).into(image_View);
//    }
}