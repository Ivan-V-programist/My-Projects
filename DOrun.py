from tkinter import *
import tkinter as tk
from PIL import ImageTk,Image
from tkinter import filedialog
from pygame import mixer
import time
from mutagen.mp3 import MP3
import librosa
import numpy as np
from scipy.signal import find_peaks
import os

#defining size of the window
global root
root=Tk()
root.geometry('900x500')
root.configure(bg='#262626')
root.resizable(0,0)
current_frame = Frame()


#######################################################################
#________________________________choices______________________________#
#######################################################################


########################################################
#_____________________Home Screen______________________#
def Home_screen():
    global current_frame
    current_frame.destroy()
    f1.destroy()
    frame = Frame(root,width=900,height=500,bg='#262626')
    current_frame = frame
    frame.place(x=175, y=80)
    l1 = Label(frame,text='DOrun',fg='white',bg='#262626')
    l2 = Label(frame, text="run to the beat!", fg="white", bg="#262626")
    l1.config(font=('Comic Sans MS',90))
    l2.config(font=('Harlow solid italic',60))
    l1.pack(expand=True)
    l2.pack(expand=True)
########################################################
#____________________Music Player______________________#
def frame_2():
    global current_frame
    current_frame.destroy()
    f1.destroy()
    frame1 = Frame(root,width=900,height=500,bg='#262626')
    current_frame = frame1
    frame1.place(x=150, y=10)
    
    #initialising pygame mixer
    mixer.init()
    
    

    ################################################################
    #___________________________Functons___________________________#
    
    ################################################################
    #getting length of a song (time)
    def play_time():
        current_time = mixer.music.get_pos() / 1000 #time in seconds
        #convert to time format
        converted_time = time.strftime('%M:%S', time.gmtime(current_time))
        
        #get length of the song
        current_song = song_box.curselection()
        song = song_box.get(current_song)
        song = f"C:/Users/ivanv/Desktop/playlist1/{song}"
        song_mut = MP3(song)
        song_length = song_mut.info.length
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
        
        status_bar.config(text=f'Time elapsed: {converted_time} of {converted_song_length}   ')
        #updating time
        status_bar.after(1000, play_time)
    
    ################################################################
    #add many songs
    def add_many_songs():
        songs = filedialog.askopenfilenames(initialdir="C:", title="choose a song", filetypes=(("mp3 files", "*.mp3"), ("wav files", "*.wav")))
        #loop through all songs selected
        for song in songs:
            song = os.path.basename(song)
            song_box.insert("end", song)
 
    ################################################################
    #stop the song completely
    def stop() :
        mixer.music.stop()
        song_box.selection_clear(ACTIVE)
        status_bar.config(text="")
    
    ################################################################
    #create global pause variable
    is_paused = False
    i = 0
    #pause and unpause the song
    def pause(is_paused, i):
        current_song = song_box.curselection()
        song = song_box.get(current_song)
        song = f"C:/Users/ivanv/Desktop/playlist1/{song}"
        if i ==0:
            mixer.music.load(song)
            mixer.music.play()
            i += 1
        if is_paused == False:
    
            mixer.music.pause()
            is_paused = True
            pause_or_play_button = Button(controls_frame, borderwidth=0,text="play", command=lambda: pause(is_paused, 1))
            pause_or_play_button.grid(row=0, column=2, padx=15)
            print("paused")
            return is_paused
            #call play time function to get the length of a song
            
        else:
            mixer.music.unpause()
            is_paused = False
            song = song_box.get(ACTIVE)
            song = f"C:/Users/ivanv/Desktop/playlist1/{song}"
            pause_or_play_button = Button(controls_frame, borderwidth=0,text="pause", command=lambda: pause(is_paused, 1))
            pause_or_play_button.grid(row=0, column=2, padx=15)
            #call play time function to get the length of a song
            play_time()
            print("playing")
            return is_paused
        #unpause
            
        
    ################################################################
    #next song function
    def next_song():
        #get index of the next song as a tuple
        next = song_box.curselection()
        #add 1 to the current song number
        next = next[0]+1
        #take song's title from the playlist
        song = song_box.get(next)
        #add directory to the name of the song to find it in the files
        song = f"C:/Users/ivanv/Desktop/playlist1/{song}"
        mixer.music.load(song)
        mixer.music.play(loops=0)
        #clear active bar in the playlist 
        song_box.select_clear(0, "end")
        #moving it to the next song
        song_box.activate(next)
        #set active bar to next song
        song_box.selection_set(next, last=None)
        
    
    ################################################################
    #previous song function
    def previous_song():
         #get index of the next song as a tuple
        next = song_box.curselection()
        #subtract 1 to the current song number
        next = next[0]-1
        #take song's title from the playlist
        song = song_box.get(next)
        #add directory to the name of the song to find it in the files
        song = f"C:/Users/ivanv/Desktop/playlist1/{song}"
        mixer.music.load(song)
        mixer.music.play(loops=0)
        #clear active bar in the playlist 
        song_box.select_clear(0, "end")
        #moving it to the next song
        song_box.activate(next)
        #set active bar to next song
        song_box.selection_set(next, last=None)
        
    ################################################################
    #delete song function
    def delete_songs():
        song_box.delete(ANCHOR)
        mixer.music.stop()
    
    
    #creating playlist box where songs will be displayed
    song_box = tk.Listbox(frame1, bg="black", fg="#0f9d9a", width=100, 
    height=20, selectbackground="#0f9d9a", selectforeground='#262626')
    song_box.pack(pady=20)
    
    
    
    #creating player buttons (images)
    #player control frames
    controls_frame = tk.Frame(frame1)
    controls_frame.pack()

    back_button = Button(controls_frame, borderwidth=0, text="back", command=previous_song)
    forward_button = Button(controls_frame, borderwidth=0,text="forward", command= next_song)
    pause_or_play_button = Button(controls_frame, borderwidth=0,text="pause", command=lambda: pause(is_paused, i))
    stop_button = Button(controls_frame, borderwidth=0,text="stop", command=stop)
    add_more_songs = Button(controls_frame, borderwidth=0, text="add song(s) to playlist", command=add_many_songs)
    delete_song = Button(controls_frame, borderwidth=0, text="delete song from  playlist", command=delete_songs)
    

    back_button.grid(row=0, column=0, padx=15)
    forward_button.grid(row=0, column=1, padx=15)
    pause_or_play_button.grid(row=0, column=2, padx=15)
    stop_button.grid(row=0, column=3, padx=15)
    add_more_songs.grid(row=0, column=4, padx=15)
    delete_song.grid(row=0, column=5, padx=15)
 
    status_bar = Label(frame1, text="", bd=1, relief=GROOVE, anchor=E)
    status_bar.pack(fill=X, side=BOTTOM, ipady=2)
    
########################################################
########################################################

def Main_algorithm():
    global current_frame
    current_frame.destroy()
    f1.destroy()
    frame2 = Frame(root,width=900,height=500,bg='#262626')
    current_frame = frame2
    frame2.place(x=150, y=10)
    
    
    FRAME_SIZE = 1024
    HOP_LENGTH = 512
    #loading test audio files
    def add_song():
        #asking for a song                                                                    allowed types of audio
        global music_file
        music_file = filedialog.askopenfilename(initialdir="C:", title="choose a song", filetypes=(("mp3 files", "*.mp3"), ("wav files", "*.wav")))
        audio, sr = librosa.load(music_file, duration=10)
        # Duration of 1 sample
        sample_duration = 1/sr
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
            x = (peaks[i+1] - peaks[i])
            av_diff.append(x)

        mean_diff = np.mean(av_diff)

        time = librosa.frames_to_time(mean_diff)
        #found number of frames between 2 peaks. find number of frames in a minute
        global BPM
        BPM = (60/time)/3
        global half_time
        half_time = []
        while BPM >50:
            half_time.append(round(BPM))
            BPM = BPM/2
        

        #output of BPM
        BPM_label = Label(frame2, borderwidth=0, text=f"BPM: {half_time}")
        BPM_label.place(x=300, y=150)
    
    #output for the user        
    file_btm = Button(frame2, borderwidth=0, text="Choose a song", command=add_song)
    file_btm.place(x=150, y=150)
        
#######################################################################
#######################################################################   




#functions for the menu
def toggle_menu():
    global f1
    f1=Frame(root,width=300,height=500,bg='#12c4c0')
    f1.place(x=0,y=0)


    #buttons
    global options
    def options(x,y,text,bcolor,fcolor,cmd):
        #flashy animations
        global on_enter
        def on_enter(e):
            myButton1['background'] = bcolor #ffcc66
            myButton1['foreground']= '#262626'  #000d33
        #flashy animations pt2
        global on_leave
        def on_leave(e):
            myButton1['background'] = fcolor
            myButton1['foreground']= '#262626'

        myButton1 = Button(f1,text=text,width=42,height=2,
        fg='#262626',border=0,bg=fcolor,activeforeground='#262626'
        ,activebackground=bcolor,command=cmd)                
        myButton1.bind("<Enter>", on_enter)
        myButton1.bind("<Leave>", on_leave)
        myButton1.place(x=x,y=y)

  
  
    #buttons in the menu itself
    options(0,80,'M U S I C  P L A Y E R','#0f9d9a','#12c4c0', frame_2)
    options(0,117,'B E A T  T R A C K E R','#0f9d9a','#12c4c0',Main_algorithm)
    options(0,154,'E Q U A L I S E R','#0f9d9a','#12c4c0',None)
    options(0,191,'H O M E  S C R E E N','#0f9d9a','#12c4c0',Home_screen)
    options(0,228, 'O P T I O N S','#0f9d9a','#12c4c0',None )


    global close
    def close():
        f1.destroy()
    #images for buttons for more aesthetic
    global img2
    img2 = ImageTk.PhotoImage(Image.open("close.png"))

    Button(f1,image=img2,border=0,command=close,bg='#12c4c0',activebackground='#12c4c0').place(x=5,y=10)
    

img1 = ImageTk.PhotoImage(Image.open("open.png"))

Button(root,image=img1,command=toggle_menu,border=0,bg='#262626',activebackground='#262626').place(x=5,y=10)




toggle_menu()
Home_screen()
root.mainloop()
