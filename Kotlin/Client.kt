package com.example.cleaner
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.util.Log
import android.widget.EditText
import java.lang.Exception




class Client(device: BluetoothDevice,editText: EditText): Thread() {

    var MY_UUID = device.uuids[0].uuid
    private var byteArray: ByteArray? = null
    private var byteArray2: ByteArray? = null
    val paramTypes = arrayOf<Class<*>>(Integer.TYPE)
    val m = device.javaClass.getMethod("createRfcommSocket", *paramTypes)
    private var socket = m.invoke(device, 1) as BluetoothSocket
    private var returnedValue : ByteArray? = null
    private val editText = editText

    override fun run() {

        Log.i("client", "Connecting")
        socket.connect()

        Log.i("client", "Sending")
        val outputStream = this.socket.outputStream
        val inputStream = this.socket.inputStream
        try {
            while(true){
                if(byteArray != null)
                    break
            }

            outputStream.write(byteArray)
            outputStream.flush()

            while(true){
                if(byteArray2 != null)
                    break
            }

            outputStream.write(byteArray2)
            outputStream.flush()

            while(!currentThread().isInterrupted()) {
                try {
                    val bytesAvailable = inputStream.available()
                    if (bytesAvailable > 0) {
                        val packetBytes = ByteArray(bytesAvailable)
                        inputStream.read(packetBytes)
                        editText.setText(String(packetBytes))
                    }
                }catch (e:Exception){

                }
            }



            // editText.setText(inputStream.readBytes().toString())

            Log.i("client", "Sent")
        } catch(e: Exception) {
            Log.e("client", "Cannot send", e)
        } finally {
            outputStream.close()
            inputStream.close()
            socket.close()
        }
    }


    fun message(msg : ByteArray, which:String){
        if(which.equals("reference"))
            byteArray = msg
        else if(which.equals("test"))
            byteArray2 = msg
    }

    fun getReturnedValue(): ByteArray? {
        return returnedValue
    }

}