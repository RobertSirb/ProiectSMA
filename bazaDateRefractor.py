'''
Created on Dec 20, 2018

@author: Pita
'''
import pickle

coeficientNumarComune = 0.40
BazaDeData={}
SongIndexesData={}
melodiiSimilare={}
fisierBazaDate = r"C:\Users\Pita\Desktop\New folder (2)\bazaDateAdrese.pkl"
fisierSongIndexes=r"C:\Users\Pita\Desktop\New folder (2)\bazaDateIndexes.pkl"
fisiereMelodiiSimilare=r"C:\Users\Pita\Desktop\New folder (2)\melodiiSimilare.pkl"
def filtreazaNumarComune(adreseComune,numarNote):
    listOfSongs = {}
    for cuplu,adrese in adreseComune.iteritems():
        if cuplu[1] not in listOfSongs:
            listOfSongs[cuplu[1]]=0
        listOfSongs[cuplu[1]]+=adrese[1]
    adreseComune2={}
    listOfSongs2=[]
    for song,_ in listOfSongs.iteritems():
        if listOfSongs[song] > numarNote * coeficientNumarComune:
            if song not in listOfSongs2:
                listOfSongs2.append(song)
    for cuplu,valoare in adreseComune.iteritems():
        if cuplu[1] in listOfSongs2:
            adreseComune2[cuplu]=valoare
    return adreseComune2

def filtreazaCoerentaTimp(adreseComune,adreseInregistrare,numarNote):
    listOfDelta = {}
    deltaSong = {}
    for cuplu,adrese in adreseComune.iteritems():
        for adresa in adrese[0]:
            for ancora in adreseInregistrare[adresa]:
                delta = ancora - cuplu[0]
                if cuplu[1] not in listOfDelta:
                    listOfDelta[cuplu[1]]={}
                if delta not in listOfDelta[cuplu[1]]:
                    listOfDelta[cuplu[1]][delta]=0
                listOfDelta[cuplu[1]][delta]+=1
    for song,_ in listOfDelta.iteritems():
        deltaMaxim = 0
        for delta,_ in listOfDelta[song].iteritems():
            if listOfDelta[song][delta] > deltaMaxim:
                deltaMaxim = listOfDelta[song][delta]
        deltaSong[song]=deltaMaxim
    songM = -1
    deltaM = -1
    for song,delta in deltaSong.iteritems():
        if delta > deltaM:
            songM = song
    return songM
    

def cautaInBazaDate(adreseInregistrare,numarNote):
    gasite = {}
    gasite2 = {} 
    for adresa,_ in adreseInregistrare.iteritems():
        if adresa in BazaDeData:
            for jt in BazaDeData[adresa]:
                if jt not in gasite:
                    gasite[jt]=[[],0]
                gasite[jt][1]+=1
                gasite[jt][0].append(adresa)
    for cuplu,_ in gasite.iteritems():
        if gasite[cuplu][1]>5:
            gasite2[cuplu]=gasite[cuplu]
    gasite2 = filtreazaNumarComune(gasite2,numarNote)
    gasite2 = filtreazaCoerentaTimp(gasite2,adreseInregistrare,numarNote)
    if gasite2 == -1:
        return 0
    return gasite2

def deschideFisierBazaDate():
    global fisierBazaDate
    f = open(fisierBazaDate,"rb")
    return f

def deschideFisierSongIndexe():
    global fisierSongIndexes
    f= open(fisierSongIndexes,"rb")
    return f

def deschideFisierMelodiiSimilare():
    global fisiereMelodiiSimilare
    f=open(fisiereMelodiiSimilare,"rb")
    return f
def getSongName(index):
    return SongIndexesData[index]
def getSimilarSongs(songId):
    return melodiiSimilare[songId]
def init():
    global BazaDeData
    global SongIndexesData
    global melodiiSimilare
    
    f=deschideFisierBazaDate()
    BazaDeData = pickle.load(f)
    f.close()
    
    f = deschideFisierSongIndexe()
    SongIndexesData = pickle.load(f)
    f.close()
    
    f= deschideFisierMelodiiSimilare()
    melodiiSimilare = pickle.load(f)
    f.close()