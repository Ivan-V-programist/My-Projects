from distutils import command
import librosa
import numpy as np
from scipy.signal import find_peaks
from tkinter.constants import E
from tkinter import Grid, Tk, font, Label, Button, filedialog
import tkinter as tk
from pygame import mixer
import sre_constants


#assigning variables for music player
currentVolume = float(0.5)
# main screen area
HEIGHT = 700
WIDTH = 800
main = Tk()


#assigning variables for main algorithm
FRAME_SIZE = 1024
HOP_LENGTH = 512
#loading test audio files

# Duration of 1 sample

#duration of audio signal in seconds




########################################################################
#==============================Functions===============================#
#____________________________Main Algorithm____________________________#
    

def Main_Algorithm():
    music_file = filedialog.askopenfilename(initialdir="C:/", title="Please select a file")
    audio, sr = librosa.load(music_file, duration=10)
    sample_duration = 1/sr
    duration = sample_duration * len(audio)
    def amplitude_envelope(signal, frame_size, hop_length):
        amplitude_envelope = []
        # calculate AE for each frame
        for i in range(0, len(signal), hop_length):
            currentFrameAmplitude_envelope = max(signal[i:i+frame_size])
            amplitude_envelope.append(currentFrameAmplitude_envelope)
        return np.array(amplitude_envelope)

    ae_audio = amplitude_envelope(audio, frame_size=FRAME_SIZE, hop_length=HOP_LENGTH)

    frames = range(0, ae_audio.size)
    t = librosa.frames_to_time(frames, sr=sr) 

    #finds average parts of a song and puts them into the array
    rms_audio = librosa.feature.rms(audio, frame_length=FRAME_SIZE, hop_length=HOP_LENGTH)[0]
    mean_rms = np.mean(rms_audio)
    #setting min acceptable value as mean value of this array
    peaks, _ = find_peaks(ae_audio, height=mean_rms)

    #finding average difference in frames from the number of peaks
    av_diff = []
    for i in range(0, len(peaks)-1):
        x = (peaks[i+1]-peaks[i])
        av_diff.append(x)
    mean_diff = np.mean(av_diff)
    time = librosa.frames_to_time(mean_diff)
    #found number of frames between 2 peaks. find number of frames in a minute
    BPM = (60/time)/3
  
    half_time = []
    half_time.append(BPM)
    while BPM >50:
        half_time.append(BPM)
        BPM = BPM/2
    
    print("possible BPMs: ", *half_time)

########################################################################
#___________________Functions for music player_________________________#
#function to select song
def play():
    filename = filedialog.askopenfilename(initialdir="C:/", title="Please select a file")
    current_song = filename
    song_name = filename.split("/")
    song_name = song_name[-1]
    print(song_name)
    
    try:
        mixer.init()
        mixer.music.load(current_song)
        mixer.music.set_volume(currentVolume)
        mixer.music.play()
        volume_label.config(fg="green", text="Volume: "+ str(currentVolume))
    
    except Exception as e:
        print(e)
        song_title_label.config(fg="red", text="Error with song file")

#function to reduce volume  
def reduce_volume():
    try:
        global currentVolume
        if currentVolume <= 0:
            volume_label.config(fg="red", text = "Muted")
            return 
        currentVolume = currentVolume - float(0.1)
        currentVolume = round(currentVolume, 1)
        mixer.music.set_volume(currentVolume)
        volume_label.config(fg = "black", text = "Volume: "+str(currentVolume))
    except Exception as e:
        print(e)
        song_title_label.config(fg="red", text= "track Has not been selected")

#function to increase volume 
def increase_volume():
    try:
        global currentVolume
        if currentVolume >= 1:
            volume_label.config(fg="red", text = "Max Volume")
            return 
        currentVolume = currentVolume + float(0.1)
        currentVolume = round(currentVolume, 1)
        mixer.music.set_volume(currentVolume)
        volume_label.config(fg = "black", text = "Volume: "+str(currentVolume))
    except Exception as e:
        print(e)
        song_title_label.config(fg="red", text= "track Has not been selected")

#function to stop song
def stop():
    try:
        mixer.music.pause()
    except Exception as e:
        print(e)    
        song_title_label.config(fg="red", text="track has not been selected yet.")

#function to start song
def unstop():
    try:
        mixer.music.unpause()
    except Exception as e:
        print(e)    
        song_title_label.config(fg="red", text="track has not been selected yet.")

##########################################################################
##########################################################################

#text round the screen/ labels

#main title
Label(main,text="DOrun", font=("Calibri", 15), fg="red").grid(sticky="N", row=0, padx=120)
#text instructions for the user
Label(main,text="select music u  want", font=("Calibri", 12), fg="blue").grid(sticky="N", row=1, padx=120)
#text indicating volume
Label(main,text="Volume", font=("Calibri", 12), fg="black").grid(sticky="N", row=4, padx=120)
#text for song name
song_title_label = Label(main, font=("calibri", 12))
#placing name of the song
song_title_label.grid(stick="N",row=3)
#text for volume
volume_label = Label(main, font=("Calibri", 12))
#placing volume text
volume_label.grid(sticky="N",row=5)

#buttons to press

Button(main, text="Select song", font=("Calibri", 12), command=play).grid(row=2,sticky="N")
Button(main, text="Pause", font=("Calibri", 12), command=stop).grid(row=3,sticky="E")
Button(main, text="Resume", font=("Calibri", 12),command=unstop).grid(row=3,sticky="W")
Button(main, text="+", font=("Calibri", 12),command=increase_volume).grid(row=5,sticky="E")
Button(main, text="-", font=("Calibri", 12),command=reduce_volume).grid(row=5,sticky="W")
Button(main, text="Beats tracker", font=("Calibri", 12), command=Main_Algorithm).grid(row=7, sticky="N")
#start the program
main.mainloop()
































