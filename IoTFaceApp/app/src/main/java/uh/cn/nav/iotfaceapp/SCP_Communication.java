package uh.cn.nav.iotfaceapp;

import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Environment;
import android.support.annotation.RequiresApi;
import android.util.Log;
import android.widget.EditText;
import android.widget.ImageView;

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.SftpException;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Created by Nav on 10/16/2017.
 */

public class SCP_Communication extends AsyncTask
{
    static ImageView imgView;
    MainActivity mainActivity;
    String activityType;
    EditText dateText;
    EditText distanceText;
    EditText nameTag;

    String savedImageName = "";
    String identification = "Unknown";
    String lastLogin = "";
    String distanceFromSensor = "";
    String postRefresh = "";
    int currentFrameRate = 0;
    SCP_Communication(ImageView imgView, MainActivity mainActivity, String activityType, EditText dateText, EditText distanceText, EditText nameTag, int currentFrameRate)
    {
        this.imgView = imgView;
        this.mainActivity = mainActivity;
        this.activityType = activityType;
        this.dateText = dateText;
        this.distanceText = distanceText;
        this.nameTag = nameTag;
        this.currentFrameRate = currentFrameRate;
    }

    String regId = "", msg = "";

    public Session connect_Session(Session session, String connection_Method)
    {
        int portSSH = 22;

        JSch ssh = new JSch();
        JSch.setConfig("StrictHostKeyChecking", "no");

        try {
            if (connection_Method.equals("key") || connection_Method.equals("Key")) {
                String server_EC2 = "ec2-54-163-103-176.compute-1.amazonaws.com"; //"ec2-54-236-4-176.compute-1.amazonaws.com";
                String username_EC2 = "ubuntu";

                String privateKeyPath = Environment.getExternalStorageDirectory() + "/Iotapp/EC2_ROG_Converted.ppk";
                ssh.addIdentity(privateKeyPath);
                session = ssh.getSession(username_EC2, server_EC2, portSSH);
            } else {
                String server_UH = "program.cs.uh.edu";
                String username_UH = "npandey";
                String password_UH = "1522324";

                session = ssh.getSession(username_UH, server_UH, portSSH);
                session.setPassword(password_UH);
            }

            session.setConfig("PreferredAuthentications", "publickey,keyboard-interactive,password");
            java.util.Properties config = new java.util.Properties();
            session.setConfig(config);

            session.connect();

        }
        catch (JSchException e)
        {
            e.printStackTrace();
        }

        return session;
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    @Override
    protected Object doInBackground(Object[] params)
    {
        if (activityType.equals("Down") || activityType.equals("down"))
        {
            String filepath = "/Iotapp/";
            savedImageName = "img" + Math.random() + ".jpg";
            try
            {
                String imageName = downloadSCP("ImageName.txt", filepath + "ImageName.txt");
                downloadSCP(imageName, filepath + savedImageName);

                try
                {
                    nameTag.setText(imageName.split(":")[1].split(".")[0]);
                }
                catch(Exception e)
                {

                }
            }
            catch (FileNotFoundException e)
            {
                e.printStackTrace();
            }
        }
        else
        if (activityType.split(":")[0].equals("Up") || activityType.split(":")[0].equals("up"))
        {
            try
            {
                postRefresh = "";
                if (activityType.split(":")[1].equals("poll"))
                {
                    uploadSCP("poll");
                }
                else
                {
                    uploadSCP("refresh");
                    postRefresh = "refresh";
                }
            }
            catch(Exception e)
            {
            }
        }
        return null;
    }

    public void uploadSCP(String actType)
    {
        Session session = null;
        Channel channel = null;

        String remote_file_path = "authenticate.txt";
        String storage_Path = "/Iotapp/authenticate.txt";

        try
        {
            session = connect_Session(session, "Key");

            channel = session.openChannel("sftp");

            channel.connect();
            ChannelSftp sftp = (ChannelSftp) channel;

            String content = "";
            if (actType.equals("poll"))
            {
                String tag = String.valueOf(nameTag.getText());
                if (!tag.substring(tag.length() - 1).equals(":"))
                {
                    try
                    {
                        if(tag.split(":").length == 2) {
                            identification = tag.split(":")[1].trim();
                        }

                        content = "authentication_status: " + activityType.split(":")[2] + "\n" + "tag: " + identification + "\n" + System.currentTimeMillis()/1000 + "\n";
                    }
                    catch(Exception e)
                    {
                        Log.e("Exception", "File write failed: " + e.toString());
                    }
                }

                writeTextFileToDisk(storage_Path, remote_file_path, content);
                sftp.put(Environment.getExternalStorageDirectory() + storage_Path, remote_file_path);
            }
            else
            {
                remote_file_path = "refresh_request.txt";
                storage_Path = "/Iotapp/refresh_request.txt";
                writeTextFileToDisk(storage_Path, remote_file_path,"request : refresh_request");
                sftp.put(Environment.getExternalStorageDirectory() + storage_Path, remote_file_path);
            }

            Log.d("MyApp", "UploadSuccessful");
        }
        catch (JSchException e)
        {
            e.printStackTrace();
        }
        catch (SftpException e)
        {
            e.printStackTrace();
        }
        finally
        {
            if (channel != null)
                channel.disconnect();

            if (session != null)
                session.disconnect();
        }
    }

    public void writeTextFileToDisk(String filepath, String filename, String content)
    {
        try
        {
            String name = Environment.getExternalStorageDirectory() + filepath;
            FileWriter writer = new FileWriter(name);
            writer.write(content);
            writer.flush();
            writer.close();
        }
        catch (IOException e)
        {
            Log.e("Exception", "File write failed: " + e.toString());
        }
        catch (Exception ie)
        {
            Log.e("Exception", "File write failed: " + ie.toString());
        }
        Log.d("MyApp", "file written - success in method");
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public String downloadSCP(String filename, String storage_Path) throws FileNotFoundException
    {
        Session session = null;
        Channel channel = null;
        String ImageName = "";

        try
        {
            session = connect_Session(session, "Key");
            channel = session.openChannel("sftp");

            channel.connect();
            ChannelSftp sftp = (ChannelSftp) channel;
            sftp.get(filename, Environment.getExternalStorageDirectory() + storage_Path);

            if ((filename.split("\\.")[1]).equals("txt"))
            {
                File sdcard = Environment.getExternalStorageDirectory();
                File file = new File(sdcard, storage_Path);
                StringBuilder text = new StringBuilder();

                try
                {
                    BufferedReader br = new BufferedReader(new FileReader(file));
                    String line;
                    int count = 0;
                    while ((line = br.readLine()) != null)
                    {
                        if (count == 0)
                        {
                            String[] content = line.split(":");
                            ImageName = content[1].trim();

                            if (ImageName.contains("_"))
                            {
                                identification = content[1].split("_")[1].split("\\.")[0].trim();
                            }
                        }
                        else
                            if (count == 1)
                            {
                                lastLogin = line;
                            }
                            else if(count == 2)
                            {
                                distanceFromSensor = line;
                            }

                        count++;
                    }
                    br.close();

                } catch (IOException e) {
                    //You'll need to add proper error handling here
                }
            }
        }
        catch (JSchException e)
        {
            e.printStackTrace();
        }
        catch (SftpException e)
        {
            e.printStackTrace();
        }
        finally
        {
            if (channel != null)
                channel.disconnect();

            if (session != null)
                session.disconnect();
        }

        return ImageName;
    }

    @Override
    protected void onPostExecute(Object o)
    {
        super.onPostExecute(o);

        if (activityType.equals("Down") || activityType.equals("down") || ((activityType.equals("Up") || activityType.equals("Up")) && (postRefresh.equals("refresh"))))        {
            try
            {
                if (!identification.equals("Unknown"))
                    nameTag.setText(String.valueOf(nameTag.getText()).split(":")[0] + ": " + identification);

                dateText.setText(String.valueOf(dateText.getText()).split(":")[0] + ": " + lastLogin);
                distanceText.setText(String.valueOf(distanceText.getText()).split(":")[0] + ": " + distanceFromSensor);
            }
            catch(Exception e)
            {
                Log.d("Exxception", "Post Execute String Split Exception");
            }

            File imgFile = new File(String.valueOf(Environment.getExternalStorageDirectory()) + "/Iotapp/" + savedImageName);
            if (imgFile.exists())
            {
                imgView.invalidate();
                imgView.setImageURI(Uri.fromFile(imgFile));
            }
            else
                Log.d("IoTFaceApp", "Image Not Found");
        }
    }
}

//        try
//        {
//            uploadSCP();
//            String imageName = downloadSCP("ImageName.txt", "/Download/ImageName.txt");
//            downloadSCP(imageName, "/Download/Img.jpg");
//        }
//        catch(Exception e)
//        {
//
//        }
//        return null;
//    public void uploadSCP()
//    {
//        Session session = null;
//        Channel channel = null;
//
//        String remote_file_path = "authenticate.jpg";
//        String storage_Path = "/Iotapp/Img.jpg";
//
//        try
//        {
//            session = connect_Session(session, "Key");
//
//            channel = session.openChannel("sftp");
//
//            channel.connect();
//            ChannelSftp sftp = (ChannelSftp) channel;
//
//            sftp.put(Environment.getExternalStorageDirectory() + storage_Path, remote_file_path);
//            Log.d("MyApp", "upload Successful");
//        }
//        catch (JSchException e)
//        {
//            e.printStackTrace();
//        }
//        catch (SftpException e)
//        {
//            e.printStackTrace();
//        }
//        finally
//        {
//            if (channel != null)
//                channel.disconnect();
//
//            if (session != null)
//                session.disconnect();
//        }
//    }