'''
Created on Nov 3, 2017

@author: Pita
'''
import wave
import numpy as np
RANGE = [40 , 80 , 120 , 180 , 300,880]
def getIndex(freq): 
    jt=0
    for it in range(len(RANGE)-1):
        if freq>=RANGE[it] and freq < RANGE[it+1]:
            break
        jt+=1
    return jt

def deschideMelodie(melodie):
    wf=wave.open(melodie, 'rb')
    return wf
def obtineFrecventeDominante(vectorFFT):
    frecventeDominante=[0]*5
    frecventeDominante=np.array(frecventeDominante)
    magDominant=[0]*5
    magDominant=np.array(magDominant)
    for freq in range(40,880):
        mag=abs(vectorFFT[freq])
        index=getIndex(freq)
        if(mag>magDominant[index]):
            frecventeDominante[index]=freq
            magDominant[index]=mag
    return frecventeDominante
def executaFFT(melodie):
    try:
        chunk = 4096
        wf = deschideMelodie(melodie)
        swidth = wf.getsampwidth()
        #RATE = wf.getframerate()
        data = wf.readframes(chunk)
        frecventeMelodie=[]
        while len(data) == chunk*swidth:
            indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),data))
            indata=np.fft.fft(indata)
            indata = obtineFrecventeDominante(indata)
            frecventeMelodie.append(indata)
            data = wf.readframes(chunk)
        return 1,frecventeMelodie
    except:
        return 0,"Can't fft the song\n"

