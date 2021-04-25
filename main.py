#!/usr/bin/python3

import wavio
import numpy as np
import argparse

# Parameters
rate = 44100    # samples per second
pitchStandard = 440.0
volume = 0.5

# ompute Waveform samples
def createWave(freq,T):
    t = np.linspace(0, T, int(T*rate), endpoint=False)
    x = np.sin(2*np.pi * freq * t)
    return x

def createNote(n,T,attack=0.01,release=0.5):
    if attack+release > 1.0 :
        raise Exception(" attack and release shouldnt be greater than 1")
    f = pitchStandard * ( 2 ** (n/12))
    wave = createWave(f,T)
    attackArray = np.linspace(0.0,1.0,int(T*rate*attack),endpoint=False)
    releaseArray = np.linspace(1.0,0.0,int(T*rate*release),endpoint=False)
    sustainArray = np.full(len(wave)-(len(attackArray)+len(releaseArray)),1.0)
    mask = np.concatenate((attackArray,sustainArray,releaseArray),axis=0)
    return np.multiply(wave,mask)

def createRandomNoteArray(time):
    a = np.random.random(10)
    a /= a.sum()
    a *= time
    wave = np.empty(shape=1,dtype=float)
    for i in a:
        n = np.random.randint(7)
        mu,sigma = 0,0.1
        attack = abs(np.random.normal(mu,sigma))
        release = abs(np.random.normal(mu,sigma))
        noteWave = createNote(n,i,attack,release)
        wave = np.append(wave,noteWave)
    return wave

def parseArguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n","--name",default="sine.wav")
    args = ap.parse_args()
    return args

if __name__ == "__main__":
    args = parseArguments()
    # Write the samples to a file
    wave = createRandomNoteArray(20)
    wave *= volume
    wavio.write("data/"+args.name, wave, rate, sampwidth=3)
