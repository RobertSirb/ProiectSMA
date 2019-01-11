package com.smaproject.ursum.cheatingshazamapp

import android.os.Parcel
import android.os.Parcelable

data class Song(var songInfo: String):Parcelable{

    constructor(parcel: Parcel) : this(
        parcel.readString()!!)

    override fun describeContents(): Int {
        return 0
    }

    override fun writeToParcel(dest: Parcel?, flags: Int) {
        dest!!.writeString(songInfo)
    }

    companion object CREATOR : Parcelable.Creator<Song> {
        override fun createFromParcel(parcel: Parcel): Song {
            return Song(parcel)
        }

        override fun newArray(size: Int): Array<Song?> {
            return arrayOfNulls(size)
        }
    }

}