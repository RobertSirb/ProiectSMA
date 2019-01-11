package com.smaproject.ursum.cheatingshazamapp

import android.annotation.SuppressLint
import android.content.Context
import android.os.Bundle
import android.support.v7.widget.LinearLayoutManager
import android.view.LayoutInflater
import com.google.firebase.database.*
import kotlinx.android.synthetic.main.activity_response_songs.*

class FavoritesSongsActivity : BaseMenuActivity() {

    private lateinit var linearLayoutManager: LinearLayoutManager
    private lateinit var userIdDBRef: DatabaseReference

    // Initializing an empty ArrayList to be filled with animals
    private val favoritesSongsList: ArrayList<Song> = ArrayList()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val inflater = this.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
        @SuppressLint("InflateParams")
        val contentView = inflater.inflate(R.layout.activity_response_songs, null, false)
        drawer!!.addView(contentView, 0)
        val extras = intent.extras ?: return
        val userId = extras.getString("USERID")

        userIdDBRef = FirebaseDatabase.getInstance().reference.child("users").child(userId!!)

        // Loads songs into the ArrayList
        val userIdListener = object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                dataSnapshot.children.forEach{
                    val songInfo = it.getValue(String::class.java)
                    favoritesSongsList.add(Song(songInfo!!))
                }

                // Access the RecyclerView Adapter and load the data into it
                rv_songs_list.adapter = FavoritesAdapter(favoritesSongsList, applicationContext)
            }

            override fun onCancelled(databaseError: DatabaseError) {
                println("loadPost:onCancelled ${databaseError.toException()}")
            }
        }
        userIdDBRef.addListenerForSingleValueEvent(userIdListener)

        // Creates a vertical Layout Manager
        linearLayoutManager = LinearLayoutManager(this)
        rv_songs_list.layoutManager = linearLayoutManager

    }
}