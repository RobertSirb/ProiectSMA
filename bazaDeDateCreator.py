import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
bins = [0,10,20,40,80,160,512,1024,2048]
coeficientNumarComune = 0.40
coeficientCoerentaTimp = 0.50
coeficient = 0.3
BazaDeData={}
SongIndexes={}
melodiiSimilare={}
indexUltimaMelodie=0

fisierBazaDate = r"C:\Users\Pita\Desktop\New folder (2)\bazaDateAdrese.pkl"
fisierSongIndexes=r"C:\Users\Pita\Desktop\New folder (2)\bazaDateIndexes.pkl"
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
    listOfSongs=[]
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

    import pickle
    f = open(r"C:\Users\Pita\Desktop\New folder (2)\bazaDateAdrese.pkl","wb")
    pickle.dump(BazaDeData, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    f = open(r"C:\Users\Pita\Desktop\New folder (2)\bazaDateIndexes.pkl","wb")
    pickle.dump(SongIndexes, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    quit()
    
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
    return gasite2



        
def verificaPuncte(mapare):
    for it in range(len(mapare)-1):
        if (mapare[it][0] == mapare[it+1][0]):
            if (mapare[it][1] > mapare[it+1][1]):
                print "MARE PROBLEMA",mapare[it],mapare[it+1],it
        elif mapare[it][0] > mapare[it+1][0]:
            print "MARE PROBLEMA",mapare[it],mapare[it+1],it
    print "OK"
    
def creazaAdrese(puncteFiltrare):
    global indexUltimaMelodie
    for it in range(len(puncteFiltrare)-7):
        ancora = puncteFiltrare[it]
        for jt in range(it+3,it+8):
            deltaTime = puncteFiltrare[jt][0]-ancora[0]
            adresa=(ancora[1],puncteFiltrare[jt][1],deltaTime) 
            if adresa not in BazaDeData:
                BazaDeData[adresa]=[]
            BazaDeData[adresa].append((ancora[0],indexUltimaMelodie))

    indexUltimaMelodie +=1


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
    medieMaxima = 0
    for it in range(len(frecvente)):
        medieL = medieLocala(it,frecvente)
        if medieL >medieMaxima:
            medieMaxima = medieL
    return medieMaxima

def deschideMelodie(melodie):
    wf=wave.open(melodie, 'rb')
    return wf

def executaFFT(melodie):
    frecvente = []
    try:
        chunk = 4096
        window = np.hamming(chunk)
        wf = deschideMelodie(melodie)
        swidth = wf.getsampwidth()
        RATE = wf.getframerate()
        p = pyaudio.PyAudio()
        stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)
        
        data = wf.readframes(chunk)
        while len(data) == chunk*swidth:
            #stream.write(data)
            
            indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),data))
            #plt.plot(indata)
            #plt.show()
            indata2=indata*window
            #plt.plot(indata2)
            #plt.show()
            
            indata=np.fft.fft(indata2)
            #plt.plot(abs(indata))
            #plt.xlim([0,2048])
            #plt.show()
            indata = abs(indata)
            indata = indata[0:2048]
            frecvente.append(indata)
            data = wf.readframes(chunk)
        return frecvente
    except:
        return "Can't fft the song\n"
    

    
def aux(melodie):
    frecvente = executaFFT(melodie)
    
    nume = melodie.split("\\")[-1]
    nume = nume.split(".")[0]
    SongIndexes[indexUltimaMelodie]=nume
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
    plt.xlim([0,20])
    plt.show()
    '''
    verificaPuncte(mapare)
    
    creazaAdrese(mapare)
    #print BazaDeData    
    #print len(BazaDeData)


def getFiles(director):
    import os
    fisiere=[]
    for root, _, filenames in os.walk(director):
        for filename in filenames: 
            fisier=os.path.join(root,filename) 
            if fisier.endswith(".wav"):
                #l=fisier.split("\\")[-1]
                #l=l.split(r".")[0]
                #l=int(l)
                fisiere.append(fisier)
    return fisiere
def aux2():
    fisiere=getFiles(r"C:\Users\PITA\Desktop\muzicaSMA")
    for it in range(len(fisiere)):
        
        print len(fisiere),it
        aux(fisiere[it])
    import pickle
    f = open(r"C:\Users\Pita\Desktop\New folder (2)\bazaDateAdrese.pkl","wb")
    pickle.dump(BazaDeData, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    f = open(r"C:\Users\Pita\Desktop\New folder (2)\bazaDateIndexes.pkl","wb")
    pickle.dump(SongIndexes, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    quit()
    
def aux3():
    import ObtineHash
    import ObtineListaMelodii
    import ExecutaFFT
    init2()
    FFTS ={}
    fisiere =getFiles(r"C:\Users\PITA\Desktop\muzicaSMA")
    for it in range(len(fisiere)):
        listaMelodiiSimilare=[]
        for jt in range(len(fisiere)):
            
            if it==jt:
                continue
            
            melodie1 = fisiere[it].split("\\")[-1]
            melodie1 = melodie1.split(".")[0]
            
            melodie2 = fisiere[jt].split("\\")[-1]
            melodie2 = melodie2.split(".")[0]
            print it , jt
            print melodie1,melodie2  
            if melodie1 not in FFTS:
                valoareReturnata , frecvente1 = ExecutaFFT.executaFFT(fisiere[it])
            
                valoareReturnata , hashuri1 = ObtineHash.obtineHash(frecvente1)
                FFTS[melodie1]=hashuri1
            else:
                hashuri1 = FFTS[melodie1]
            if melodie2 not in FFTS:
                valoareReturnata , frecvente2 = ExecutaFFT.executaFFT(fisiere[jt])
            
                valoareReturnata , hashuri2 = ObtineHash.obtineHash(frecvente2)
                FFTS[melodie2] = hashuri2
            else:
                hashuri2 = FFTS[melodie2]
            id1=-1
            id2 =-1
            for kt,lt in SongIndexes.iteritems():
                if lt == melodie1:
                    id1 = kt
                if lt == melodie2:
                    id2 = kt
                if id1!=-1 and id2 !=-1:
                    break    
            listaMelodiiSimilare.append([id2,ObtineListaMelodii.comparaDouaMelodi(hashuri1,hashuri2)])
        listaMelodiiSimilare.sort(key=lambda x: x[1])
        ids=zip(*listaMelodiiSimilare)[0]
        melodiiSimilare[id1]=ids[0:3]
    print melodiiSimilare
    import pickle
    f = open(r"C:\Users\Pita\Desktop\New folder (2)\melodiiSimilare.pkl","wb")
    pickle.dump(melodiiSimilare, f, pickle.HIGHEST_PROTOCOL)
    f.close()
def deschideFisierBazaDate():
    global fisierBazaDate
    f = open(fisierBazaDate,"rb")
    return f

def deschideFisierSongIndexe():
    global fisierSongIndexes
    f= open(fisierSongIndexes,"rb")
    return f
def init2():
    global BazaDeData
    global SongIndexes
    import pickle
    f=deschideFisierBazaDate()
    BazaDeData = pickle.load(f)
    f.close()
    
    f = deschideFisierSongIndexe()
    SongIndexes = pickle.load(f)
    f.close()        
aux3()