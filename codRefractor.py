'''
Created on Dec 20, 2018

@author: Pita
'''
import pyrebase
import numpy as np
import struct
import matplotlib.pyplot as plt
import bazaDateRefractor
config = {
  "apiKey": "AIzaSyDD7YuNHf8_VPGdFMfaaA7l7qWnvQHD97Y",
  "authDomain": "cheatingshazamapp.firebaseapp.com",
  "databaseURL": "https://cheatingshazamapp.firebaseio.com",
  "storageBucket": "cheatingshazamapp.appspot.com"
}
bins = [0,10,20,40,80,160,512,1024,2048]
coeficient = 0.3
db=""
def verificaPuncte(mapare):
    for it in range(len(mapare)-1):
        if (mapare[it][0] == mapare[it+1][0]):
            if (mapare[it][1] > mapare[it+1][1]):
                print "MARE PROBLEMA",mapare[it],mapare[it+1],it
        elif mapare[it][0] > mapare[it+1][0]:
            print "MARE PROBLEMA",mapare[it],mapare[it+1],it
    print "OK"
    
def creazaAdrese(puncteFiltrare):
    adrese={}
    numarNote = 0
    for it in range(len(puncteFiltrare)-7):
        ancora = puncteFiltrare[it]
        for jt in range(it+3,it+8):
            deltaTime = puncteFiltrare[jt][0]-ancora[0]
            adresa=(ancora[1],puncteFiltrare[jt][1],deltaTime)
            if adresa not in adrese:
                adrese[adresa]=[]
            adrese[adresa].append(ancora[0])
            numarNote+=1 
            #adrese.append([adresa ,ancora[0]])
    return adrese,numarNote

def executaMapare(medieMaxima,frecvente):
    global coeficient
    mapare = []
    for it in range(len(frecvente)):
        for jt in range(len(bins)-1):
            frecventa,valoare = dominantaInBins(jt, it,frecvente)
            if valoare> medieMaxima*coeficient:
                mapare.append([it,frecventa])
    return mapare
def dominantaInBins(idx,timp,frecvente):
    it1 = bins[idx]
    it2 = bins[idx+1]
    maxim = -1
    for it in range(it1,it2):
        if frecvente[timp][it]>maxim:
            maxim = frecvente[timp][it]
            jt = it
    return jt,maxim

def medieLocala(timp,frecvente):
    medie = 0
    for it in range(len(bins)-1):
        index,maximBin = dominantaInBins(it, timp,frecvente)
        medie+=maximBin
    return medie/8

def aflaMedia(frecvente):
    medieMaxima = -1
    for it in range(len(frecvente)):
        medieL = medieLocala(it,frecvente)
        if medieL >medieMaxima:
            medieMaxima = medieL
    return medieMaxima



def initFirebase():
    global config
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    auth.sign_in_with_email_and_password("sirb.robert@yahoo.com", "clasa12b")
    db = firebase.database()
    return db

def getStringValues(dataIn):
    nou2 = dataIn.encode("utf-16")
    nou5 = struct.unpack('>'+'h'*(len(nou2)//2),nou2)
    return nou5

def obtineFrecvente(data):
        frecvente = []
        chunk = 4096
        window = np.hamming(chunk)
        chunkIdx = 0
        while len(data) - (chunkIdx+1)*chunk >=0:
            it = chunk*chunkIdx
            jt = chunk*(chunkIdx+1)
            
            indata = data[it:jt]
            #if len(indata) != chunk*2:
            #    break
            #indata = np.array(struct.unpack("%dh"%(len(indata)/2),indata))
            indata2=indata*window
            indata=np.fft.fft(indata2)
            indata = abs(indata)
            indata = indata[0:2048]
            frecvente.append(indata)
            
            chunkIdx+=1
        return frecvente
    
    
def getMatchingSong(data):
    frecvente = obtineFrecvente(data)
    db.child("song").child("status").set("Creating Spectrogram")
    medieMaxima = aflaMedia(frecvente)
    mapare = executaMapare(medieMaxima,frecvente)
    print len(mapare)
    '''
    mapare2={}
    for it in mapare:
        if it[0] not in mapare2:
            mapare2[it[0]]=[]
        mapare2[it[0]].append(it[1])
    
    for key in mapare2:
    
        plt.scatter([key]*len(mapare2[key]), mapare2[key], label=key)
    
    plt.legend()
    plt.show()
    '''
    db.child("song").child("status").set("Creating FingerPrint")
    verificaPuncte(mapare)
    
    adrese,numarNote = creazaAdrese(mapare)

    print len(adrese) ,numarNote   
    songIndex = bazaDateRefractor.cautaInBazaDate(adrese,numarNote)
    songName = bazaDateRefractor.getSongName(songIndex)
    return songName,songIndex
    
    
def runServer(db):
    vechi = ""
    while(1):
        nou = db.child("song").child("newSong").get()
        nou=nou.val()
        if nou!= vechi and nou!="":
            db.child("song").child("status").set("In_Queue")
            vechi = nou
            data = getStringValues(nou)
            matchingSong ,songIndex = getMatchingSong(data)
            db.child("song").child("response").set(matchingSong)
            
            similarSongs = bazaDateRefractor.getSimilarSongs(songIndex)
            str2=""
            for it in range(3):
                
                str2+=bazaDateRefractor.getSongName(similarSongs[it])+" ;"
            db.child("song").child("matchings").set(str2)
            db.child("song").child("status").set("Finished")
            db.child("song").child("status").set("Waiting")
            print matchingSong,str2
            #db.child("nouaMelodie").set("")
  
def initLocalDatabase():
    bazaDateRefractor.init()
          
def mainScript():
    global db
    db = initFirebase()
    initLocalDatabase()
    runServer(db)
    
mainScript()