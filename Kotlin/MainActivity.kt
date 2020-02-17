package com.example.cleaner

import android.app.Activity
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothSocket
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.bluetooth.BluetoothDevice
import android.graphics.Bitmap
import android.graphics.Color
import kotlinx.android.synthetic.main.activity_main.*
import java.io.*
import android.provider.MediaStore
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.core.graphics.drawable.toBitmap
import java.lang.Exception


class MainActivity : AppCompatActivity() {

    var bluetoothAdapter :BluetoothAdapter? = null // local device Bluetooth adapter for exec tasks
    var clientSocket : BluetoothSocket? = null
    var raspberryDevice : BluetoothDevice? = null
    val REQUEST_ENABLE_BLUETOOTH = 1 //open BT request code
    var client : Client? = null
    var openBTFlag = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        //editText.setBackgroundColor(Color.RED)
        //editText.setTextColor(Color.WHITE)

        open.setOnClickListener {
            openBluetooth()
            Toast.makeText(this,"Bluetooth is open",Toast.LENGTH_LONG).show()

        }

        connect.setOnClickListener {
            connectToRaspberryPi()
            Toast.makeText(this,"Connected to raspberry pi",Toast.LENGTH_LONG).show()
        }

        send.setOnClickListener {
            try {
                //sendImage()
                client!!.message(sendImage(imageView),"reference")
                Toast.makeText(this,"Image has been sent",Toast.LENGTH_LONG).show()
                client!!.message(sendImage(imageView5),"test")
                Toast.makeText(this,"Image has been sent",Toast.LENGTH_LONG).show()
            }
            catch (e:Exception){
                //disconnect()
            }
            finally {
                //disconnect()
            }
        }

        val REQUEST_IMAGE_CAPTURE_REFERENCE = 2
        val REQUEST_IMAGE_CAPTURE_TEST = 3

        takePhoto.setOnClickListener {
            dispatchTakePictureIntent(REQUEST_IMAGE_CAPTURE_REFERENCE)
        }

        takePhoto2.setOnClickListener {
            dispatchTakePictureIntent(REQUEST_IMAGE_CAPTURE_TEST)
        }


    }

    private fun connectToRaspberryPi() {
        raspberryDevice = bluetoothAdapter!!.getRemoteDevice("DC:A6:32:54:8E:B7")
        System.out.println(raspberryDevice!!.name)
        if (raspberryDevice != null) {
            client = Client(raspberryDevice!!,editText)
            client!!.start()

        }else{
            println("No such device")
        }

    }

    // !! throw exception if null otherwise specifies not nullable
    private fun openBluetooth() {
        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter() // get device's local bluetooth
        if(!bluetoothAdapter!!.isEnabled){
            val enableBluetoothIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE) //launch new BT open request
            startActivityForResult(enableBluetoothIntent, REQUEST_ENABLE_BLUETOOTH)
        }
        openBTFlag = 1

    }



    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if(requestCode == REQUEST_ENABLE_BLUETOOTH){
            if(resultCode == Activity.RESULT_OK){
                if(bluetoothAdapter!!.isEnabled){
                    println("BT connected")
                }
            }
        }
        if (requestCode == 2 && resultCode == RESULT_OK) {
            val imageBitmap = data!!.extras!!.get("data") as Bitmap
            imageView.setImageBitmap(imageBitmap)
        }
        if (requestCode == 3 && resultCode == RESULT_OK) {
            val imageBitmap = data!!.extras!!.get("data") as Bitmap
            imageView5.setImageBitmap(imageBitmap)
        }
    }
    private fun disconnect() {
        clientSocket!!.inputStream.close()
        clientSocket!!.outputStream.close()
        clientSocket!!.close()
    }


    private fun dispatchTakePictureIntent(request_code : Int) {
        Intent(MediaStore.ACTION_IMAGE_CAPTURE).also { takePictureIntent ->
            takePictureIntent.resolveActivity(packageManager)?.also {
                startActivityForResult(takePictureIntent, request_code)
            }
        }
    }

    private fun getNum(num:Int) : Int{
        var tmp = num
        var nr = 0
        while( tmp != 0 ){
            nr++
            tmp= tmp / 10
        }
        return nr
    }

    private fun sendImage(imageView: ImageView) : ByteArray{
        var baos = ByteArrayOutputStream()
        var bitmap = imageView.drawable.toBitmap()
        bitmap.compress(Bitmap.CompressFormat.JPEG,100,baos)
        val size = baos.toByteArray().size
        println("Size of image :" + baos.toByteArray().size)
        var list = ArrayList<Byte>()
        list.add(getNum(size).toByte())
        var tmp = size
        var tmpList = ArrayList<Byte>()
        while(tmp!=0){
            tmpList.add((tmp%10).toByte())
            tmp/=10
        }
        list.addAll(tmpList.reversed())
        println(list)
        list.addAll(baos.toByteArray().toList())

        return list.toByteArray()
    }
    fun setText(text:ByteArray?) = editText.setText(text.toString(), TextView.BufferType.EDITABLE)




}





