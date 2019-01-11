package com.smaproject.ursum.cheatingshazamapp

import android.content.Context
import android.support.v7.widget.RecyclerView
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import kotlinx.android.synthetic.main.song_list_item.view.*
import com.google.firebase.database.FirebaseDatabase
import kotlinx.android.synthetic.main.song_list_header.view.*


class SongsAdapter(val items : ArrayList<Song>, val context: Context, val childName: String) : RecyclerView.Adapter<RecyclerView.ViewHolder>() {
    companion object {
        const val TYPE_HEADER = 0
        const val TYPE_SONG = 1
    }
    private var favoritesDbRef = FirebaseDatabase.getInstance().reference.child("users")

    // Gets the number of songs in the list
    override fun getItemCount(): Int {
        return items.size
    }

    // Inflates the item views
    override fun onCreateViewHolder(p0: ViewGroup, p1: Int): RecyclerView.ViewHolder {
        if (p1 == TYPE_HEADER)
            return HeaderViewHolder(LayoutInflater.from(context).inflate(R.layout.song_list_header, p0, false))

        return SongViewHolder(LayoutInflater.from(context).inflate(R.layout.song_list_item, p0, false))
    }

    // Binds each song in the ArrayList to a view
    override fun onBindViewHolder(p0: RecyclerView.ViewHolder, p1: Int) {
        val itemSong = items[p1]
        if (p0 is HeaderViewHolder) {
            p0.bindHeader(itemSong)
        } else if (p0 is SongViewHolder) {
            p0.bindSong(itemSong, childName)
        }
    }

    override fun getItemViewType(position: Int): Int {
        return if (isPositionHeader(position)) TYPE_HEADER else TYPE_SONG
    }

    private fun isPositionHeader(position: Int): Boolean {
        //return position == 0
        return position == 0 || position == 2
    }


    inner class SongViewHolder(v: View) : RecyclerView.ViewHolder(v) {
        // Holds the TextView that will add each song to
        private var view: View = v
        private var song: Song? = null

        fun bindSong(song: Song, childName: String) {
            this.song = song
            view.tv_song_name.text = song.songInfo
            view.btn_add_fav.setOnClickListener {
                favoritesDbRef.child(childName).push().setValue(song.songInfo)
            }
        }
    }

    inner class HeaderViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {

            fun bindHeader(song: Song) {
                itemView.header_id.text = song.songInfo
            }

   }

}