package com.smaproject.ursum.cheatingshazamapp

import android.Manifest
import android.os.Bundle
import android.content.Intent
import android.os.CountDownTimer
import android.view.animation.AnimationUtils
import android.widget.ImageView
import com.google.firebase.FirebaseApp
import android.widget.Toast
import com.google.firebase.database.*
import android.annotation.SuppressLint
import android.content.Context
import android.graphics.Typeface
import android.util.Log
import android.view.LayoutInflater
import kotlinx.android.synthetic.main.activity_main_page.*
import android.support.v4.app.ActivityCompat
import android.content.pm.PackageManager
import android.os.Build




class MainActivity : BaseMenuActivity(){

    val recorder : RecorderHelper = RecorderHelper(null, null, false)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        FirebaseApp.initializeApp(this)

        database = FirebaseDatabase.getInstance().reference
        songModelDBRef = database.child("song")

        //verifyUserIsSignedIn()
        super.auth.addAuthStateListener {
            if (auth.currentUser == null)
                startActivity(Intent(this, SignInActivity::class.java))
        }

        val inflater = this.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
        @SuppressLint("InflateParams")
        val contentView = inflater.inflate(R.layout.activity_main_page, null, false)
        drawer!!.addView(contentView, 0)

        text_timer.setTypeface(null, Typeface.BOLD_ITALIC)
        text_timer.text = "Waiting"

        val songListener = object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                if (dataSnapshot.exists()) {
                    val songModel = dataSnapshot.getValue(SongModel::class.java)
                    songResponse = songModel!!.response
                    songMatchings = songModel.matchings
                    songStatus = songModel.status
                    if (songStatus.equals("Finish")){
                        val responseIntent = Intent(applicationContext, ResponseSongsActivity::class.java)
                        responseIntent.putExtra("RESPONSE", songResponse)
                        responseIntent.putExtra("MATCHINGS", songMatchings)
                        startActivity(responseIntent)
                    }else{
                        text_timer.text = songStatus
                    }
                }
            }

            override fun onCancelled(databaseError: DatabaseError) {
                println("loadPost:onCancelled ${databaseError.toException()}")
            }
        }
        songModelDBRef.addValueEventListener(songListener)

        btn_listen.setOnClickListener {
            if(isPermissionGranted()) {
                recorder.startRecording()

                object : CountDownTimer(10000, 1000) // Wait 10 secs, tick every 1 sec
                {
                    override fun onTick(millisUntilFinished: Long) {
                        text_timer.text = ((millisUntilFinished * .001f).toInt()).toString()
                        shake()
                    }

                    override fun onFinish() {
                        recorder.stopRecording()
                        text_timer.text = songStatus
                    }
                }.start()
            }
            else
                Toast.makeText(this, "App failed because you refused permission!", Toast.LENGTH_SHORT).show()
        }

    }

    fun shake() {
        // Create pulse effect from xml shake resource
        val shake = AnimationUtils.loadAnimation(applicationContext, R.anim.shake)
        // View element to be shaken
        val s = findViewById<ImageView>(R.id.app_logo)
        // Perform animation
        s.startAnimation(shake)
    }

    fun isPermissionGranted(): Boolean {

        if (Build.VERSION.SDK_INT >= 23) {
            if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
                Log.v(MainActivity::class.java.canonicalName, "Permission is granted")
                return true
            } else {
                ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.RECORD_AUDIO), requestAudioRecord)
                return false
            }
        } else { //permission is automatically granted on sdk<23 upon installation
            Log.v(MainActivity::class.java.canonicalName, "Permission is granted")
            return true
        }

    }

    companion object {
        private lateinit var database: DatabaseReference

        private lateinit var songModelDBRef: DatabaseReference

        private val requestAudioRecord = 1234
        private var songResponse : String? = "initial str"
        private var songMatchings: String? = "initial match"
        private var songStatus : String? = "Waiting"

        fun saveData(sData: String){
            val newSong = songModelDBRef.child("newSong")
            //then, we used the reference to set the value on that ID
            newSong.setValue(sData)
            val newStatus = songModelDBRef.child("status")
            newStatus.setValue("new")
        }
    }

}
