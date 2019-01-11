package com.smaproject.ursum.cheatingshazamapp

import android.annotation.SuppressLint
import android.content.Context
import android.os.Bundle
import android.support.v7.widget.LinearLayoutManager
import android.view.LayoutInflater
import kotlinx.android.synthetic.main.activity_response_songs.*

class ResponseSongsActivity: BaseMenuActivity() {

    private lateinit var linearLayoutManager: LinearLayoutManager

    // Initializing an empty ArrayList to be filled with animals
    val songsList: ArrayList<Song> = ArrayList()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val inflater = this.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
        @SuppressLint("InflateParams")
        val contentView = inflater.inflate(R.layout.activity_response_songs, null, false)
        drawer!!.addView(contentView, 0)
        val extras = intent.extras ?: return
        val response = extras.getString("RESPONSE")
        val matchings = extras.getString("MATCHINGS")

        // Loads songs into the ArrayList
        loadSongs(response, matchings)

        // Creates a vertical Layout Manager
        linearLayoutManager = LinearLayoutManager(this)
        rv_songs_list.layoutManager = linearLayoutManager

        // Access the RecyclerView Adapter and load the data into it
        rv_songs_list.adapter = SongsAdapter(songsList, this, auth.currentUser!!.uid)

    }

    // Adds songs to list-> maybe creating it different for 2 activities
    private fun loadSongs(songResponse:String?, songMatchings: String?) {

        val matchings = songMatchings!!.split(";")

        //take care on first pos 0 to have something not important
        songsList.add(Song("The song matches with:"))
        songResponse?.let { songsList.add(Song(it)) }
        //take care pos 2 is also special
        songsList.add(Song("Cheating songs are:"))
        matchings.forEach { matching -> songsList.add(Song(matching)) }
    }
}