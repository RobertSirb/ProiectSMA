package com.smaproject.ursum.cheatingshazamapp

import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import java.nio.charset.Charset
import kotlin.experimental.and

class RecorderHelper(var recorder: AudioRecord?, var recordingThread: Thread?, var isRecording:Boolean) {

    val bufferSize = AudioRecord.getMinBufferSize(
        RECORDER_SAMPLERATE,
        RECORDER_CHANNELS,
        RECORDER_AUDIO_ENCODING
    )

    fun startRecording(){

            recorder = AudioRecord(
                MediaRecorder.AudioSource.MIC,
                RECORDER_SAMPLERATE, RECORDER_CHANNELS,
                RECORDER_AUDIO_ENCODING, BufferElements2Rec * BytesPerElement
            )

            recorder!!.startRecording()

            isRecording = true

            recordingThread = Thread(Runnable { addRegistrationContent() }, "AudioRecorder Thread")
            recordingThread!!.start()

    }

    private fun addRegistrationContent(){
        val sData = ShortArray(BufferElements2Rec)
        var totalData = String()
        while (isRecording) {
            recorder!!.read(sData, 0, BufferElements2Rec)
            val byteArray = short2byte(sData)
            val stringData = String(byteArray, Charset.forName("UTF-16"))
            totalData+=stringData
        }
        MainActivity.saveData(totalData)
    }

    //Conversion of short to byte
    private fun short2byte(sData: ShortArray): ByteArray {
        val shortArrsize = sData.size
        val bytes = ByteArray(shortArrsize * 2)

        for (i in 0 until shortArrsize) {
            bytes[i * 2] = (sData[i] and 0x00FF).toByte()
            bytes[i * 2 + 1] = sData[i].toLong().shr(8).toByte()
            sData[i] = 0
        }
        return bytes
    }

    fun stopRecording() {
        // stops the recording activity

        if (null != recorder) {
            isRecording = false


            recorder!!.stop()
            recorder!!.release()

            recorder = null
            recordingThread = null
        }
    }
    companion object {

        private val RECORDER_SAMPLERATE = 44100

        private val RECORDER_CHANNELS = AudioFormat.CHANNEL_IN_MONO

        private val RECORDER_AUDIO_ENCODING = AudioFormat.ENCODING_PCM_16BIT

        internal var BufferElements2Rec = 1024
        internal var BytesPerElement = 2 // 2 bytes in 16bit format
    }

}