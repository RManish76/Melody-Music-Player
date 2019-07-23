# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 19:53:05 2019

@author: RManish
"""
import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer
import tkinter.messagebox
from mutagen.mp3 import MP3  # to extract the metadata from the mp3 (time duration)
import time
from tkinter import ttk
from ttkthemes import themed_tk as tk
import threading    # to execute two different type of programe at same time


root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
mixer.init()  #initializing the mixer


# Fonts - Arial (corresponds of Helvetical), courier New (Courier), Comic sans MS, Fixedsys,
# MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana
# fg - for font colour and bg - backgroung colour (bg = 'green')
#Styles - normal, bold, roman, italic, underline and overstrike.


statusbar=ttk.Label(root,text="Welcome to Melody",relief = SUNKEN,anchor=W, font='Times 10 italic bold')
statusbar.pack(side="bottom",fill = X)


root.title("Melody")
root.iconbitmap(r'C:\Users\RManish\Desktop\PROJECT\images\favicon.ico')

#Root Window - Statusat, LeftFrame, RightFrame
#LeftFrame - The listbox (playlist)
#RightFrame - TopFrame, MiddleFrame and the BottomFrame

leftframe=Frame(root)
leftframe.pack(side=LEFT, padx=30)

rightframe=Frame(root)
rightframe.pack()

topframe=Frame(rightframe)
topframe.pack()
#creat the menubar

playlistbox=Listbox(leftframe)
playlistbox.pack()

menubar=Menu(root)
root.config(menu=menubar)

#creat the submenu
subMenu=Menu(menubar, tearoff=0)

playlist = []

#playlist - contains the full path + filename
#playlistbox - contains just the filename
#Fullpath + filename is require to play the music inside play_music load funciton

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    #print(filename_path)
    add_to_playlist(filename_path)

addBtn=ttk.Button(leftframe, text="+ Add", command = browse_file)
addBtn.pack(side=LEFT)

def del_song():
     selected_song = playlistbox.curselection() # this line use to get the index of selcted music from playlistbox.
     selected_song=int(selected_song[0])
     playlistbox.delete(selected_song)
     playlist.pop(selected_song)
     
delBtn=ttk.Button(leftframe, text="-Del", command = del_song)
delBtn.pack(side=LEFT)



def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index=0
    playlistbox.insert(index,filename)
    playlist.insert(index,filename_path)
    #print(playlist)
    index +=1


    
menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label='Open',command = browse_file)
subMenu.add_command(label='Exit', command = root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About Melody', 'Melody is a music player build in python')

subMenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label='About us', command=about_us)
subMenu.add_command(label='Online Help')


#root.geometry('500x500')

filelabel=ttk.Label(topframe,text='Lets make some noise')
filelabel.pack()

lengthlabel= ttk.Label(topframe, text = 'Total Lenght : --:--')
lengthlabel.pack(pady=5)

currentlabel= ttk.Label(topframe, text = 'Current Time : --:--', relief = GROOVE)
currentlabel.pack()

playphoto=PhotoImage(file=r"C:\Users\RManish\Desktop\PROJECT\images\play-button.png")
stopphoto=PhotoImage(file=r"C:\Users\RManish\Desktop\PROJECT\images\stop.png")
pausephoto=PhotoImage(file=r"C:\Users\RManish\Desktop\PROJECT\images\pause.png")
rewindphoto=PhotoImage(file=r"C:\Users\RManish\Desktop\PROJECT\images\rewind (1).png")
mutephoto=PhotoImage(file=r"C:\Users\RManish\Desktop\PROJECT\images\002-speaker-1.png")
volumephoto=PhotoImage(file=r"C:\Users\RManish\Desktop\PROJECT\images\001-speaker.png")

'''labelphoto=Label(root, image=playphoto)
labelphoto.pack()
'''

def show_details(play_song):
    filelabel['text']="Playing" + ' ' + '-' + os.path.basename(play_song)

    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio= MP3(play_song)
        total_length=audio.info.length
    else:
        a=mixer.Sound(play_song)
        total_length = a.get_length()

        
    #print(total_length)  
    mins,secs = divmod(total_length,60)   #div - total_lenght/60, mod - total_length%60
    
    mins=(round(mins))
    secs=(round(secs))
    timeformat = '{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text']="Total Length" + ' ' + '-' + ' ' +timeformat

    ''' using threading t1 is the variabel which handel the start count because the start
    will the progrmae in while loop and any other line not going to work since here theading
    is using to run the start_count at same time when other lines are excuting'''
    
    t1= threading.Thread(target=start_count,args=(total_length,))
    t1.start()
    

def start_count(t):
    
    global paused
    
    # mixer.music.get_busy(): -Retrun False when we press the stop button(music stop playin)
    current_time=0
    while current_time<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs = divmod(current_time,60)   #div - total_lenght/60, mod - total_length%60
            mins=(round(mins))
            secs=(round(secs))
            timeformat = '{:02d}:{:02d}'.format(mins,secs)
            currentlabel['text']="Current Time" + ' ' + '-' + ' '+ timeformat 
            time.sleep(1)    #value of time in second
            current_time+=1
            

def play_music():
    global paused
    
    if paused:
        mixer.music.unpause()
        statusbar['text']="Music Resumed"
        paused=FALSE
    
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection() # this line use to get the index of selcted music from playlistbox.
            selected_song=int(selected_song[0])
            play_it=playlist[selected_song]
            mixer.music.load(play_it) # use the word " filename_path " to add from browser without inverted commas
            mixer.music.play()
            statusbar['text']="Playing music" + ' ' + '-' + os.path.basename(play_it)
            #print("hey: This play button works pretty well!")
            show_details(play_it)
        except:
            tkinter.messagebox.showinfo('File not found',"Melody could not find the file: Please check again") #To Error to the user in new window
            #print("Error")


def stop_music():
    mixer.music.stop()
    statusbar['text']='Music is stoped'

paused = FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text']='Music is Paussed'
def rewind_music():
    play_music()
    statusbar['text']='Music is Rewind'
def set_vol(val):
    volume=float(val)/100
    mixer.music.set_volume(volume)

muted = FALSE

def mute_music():
    global muted
    if muted:
        #Unmute the music
        mixer.music.set_volume(30)
        volumeBtn.configure(image=volumephoto)
        scale.set(30)
        muted=FALSE
    else:
        #Mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutephoto)
        scale.set(0)
        muted = TRUE

    # set_volume of mixer takes vlaue only from 0 to 1. Example - 0, 0.1, 0.3

middleframe = Frame(rightframe)  # creating a frame(invisible window inside root) for middle buttons to seprate them  => , relief=RAISED, borderwidth=1
middleframe.pack(pady=10)


playBtn = ttk.Button(middleframe, image=playphoto, command=play_music)
playBtn.grid(row=1,column=0 ,padx=10)

stopBtn = ttk.Button(middleframe, image=stopphoto, command=stop_music)
stopBtn.grid(row=1,column=1,padx=10)

pauseBtn = ttk.Button(middleframe, image=pausephoto, command=pause_music)
pauseBtn.grid(row=1,column=2,padx=10)

# bottomframe for volume botton, rewind botton, volume scale etc.

bottomframe = Frame(rightframe)
bottomframe.pack(pady=10)

rewindBtn= ttk.Button(bottomframe, image=rewindphoto, command=rewind_music)
rewindBtn.grid(row=0,column=0,padx=10)

volumeBtn=ttk.Button(bottomframe, image=volumephoto,command=mute_music)
volumeBtn.grid(row=0,column=1)
# scale is used to make the scale controler like volume scale

scale = ttk.Scale(bottomframe, from_=0, to=100, orient = HORIZONTAL, command = set_vol)
mixer.music.set_volume(0.3)
scale.set(30)
scale.grid(row = 0,column = 2)



def on_closing():
    #tkinter.messagebox.showinfo('prank',"you have been pranked. this window won't close! haaaha")
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
























