package com.smaproject.ursum.cheatingshazamapp

import android.content.Context
import android.support.v7.widget.RecyclerView
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import kotlinx.android.synthetic.main.song_list_item.view.*

internal class FavoritesAdapter(val items : ArrayList<Song>, val context: Context) : RecyclerView.Adapter<FavoritesAdapter.ViewHolder>() {

    // Gets the number of songs in the list
    override fun getItemCount(): Int {
        return items.size
    }

    // Inflates the item views
    override fun onCreateViewHolder(p0: ViewGroup, p1: Int): FavoritesAdapter.ViewHolder {
        return ViewHolder(LayoutInflater.from(context).inflate(R.layout.song_list_item, p0, false))
    }

    // Binds each song in the ArrayList to a view
    override fun onBindViewHolder(p0: FavoritesAdapter.ViewHolder, p1: Int) {
        val itemSong = items[p1]
        p0.bindItems(itemSong)

    }

    internal inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {

        fun bindItems(song: Song) {
            itemView.tv_song_name.text = song.songInfo
            itemView.btn_add_fav.visibility = View.GONE
        }

    }
}