from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import tkinter.ttk as ttk
import pygame
import time
from mutagen.mp3 import MP3

root = Tk()
root.title('MP3 Player')
root.geometry("550x420")

pygame.mixer.init()

def play_time():
    if stopped:
        return
    
    current_time = pygame.mixer.music.get_pos()/1000
    #slider_label.config(text=f'{int(slider.get())}  -  {int(current_time)}')
    cur_time = time.strftime('%M:%S', time.gmtime(current_time))

    song = playlist.get(ACTIVE)
    song = f'C:/Users/Ideapad/Music/{song}.mp3'
    song_len = MP3(song)
    global song_length
    song_length = song_len.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    current_time +=1

    if int(slider.get()) == int(song_length):
        status_bar.config(text=f'{converted_song_length}  -  {converted_song_length}')

    elif paused:
        pass
    
    elif int(slider.get()) == int(current_time):
        slider_position = int(song_length)
        slider.config(to=slider_position, value=int(current_time))
        
    else:
        slider_position = int(song_length)
        slider.config(to=slider_position, value=int(slider.get()))
        cur_time = time.strftime('%M:%S', time.gmtime(int(slider.get())))
        status_bar.config(text=f'{cur_time}  -  {converted_song_length}')
        next_time = int(slider.get()) + 1
        slider.config(value=next_time)
    
    #status_bar.config(text=f'{cur_time}  -  {converted_song_length}')
    #slider.config(value=int(current_time))
    
    status_bar.after(1000, play_time)

def add_song():
    song = filedialog.askopenfilename(initialdir=r'C:\Users\Ideapad\Music', title="Choose A Song", filetypes=(("mp3 files", "*.mp3"), ))
    song = song.replace("C:/Users/Ideapad/Music/","")
    song = song.replace(".mp3","")
    playlist.insert(END, song)

def delete_song():
    stop()
    playlist.delete(ANCHOR)
    pygame.mixer.music.stop()

def add_many():
    songs = filedialog.askopenfilenames(initialdir=r'C:\Users\Ideapad\Music', title="Choose A Song", filetypes=(("mp3 files", "*.mp3"), ))
    for song in songs:
        song = song.replace("C:/Users/Ideapad/Music/","")
        song = song.replace(".mp3","")
        playlist.insert(END, song)

def delete_all():
    stop()
    playlist.delete(0, END)
    pygame.mixer.music.stop()

def play():
    global stopped
    stopped = False
    song = playlist.get(ACTIVE)
    song = f'C:/Users/Ideapad/Music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()
    #slider_position = int(song_length)
    #slider.config(to=slider_position, value=0)

global stopped
stopped = False
def stop():
    status_bar.config(text='')
    slider.config(value=0)
    pygame.mixer.music.stop()
    playlist.selection_clear(ACTIVE)
    status_bar.config(text='')
    global stopped
    stopped = True

def next_song():
    status_bar.config(text='')
    slider.config(value=0)
    agla = playlist.curselection()
    agla = agla[0]+1
    song = playlist.get(agla)
    song = f'C:/Users/Ideapad/Music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0, END)
    playlist.activate(agla)
    playlist.selection_set(agla, last=None)

def previous_song():
    status_bar.config(text='')
    slider.config(value=0)
    pichla = playlist.curselection()
    pichla = pichla[0]-1
    song = playlist.get(pichla)
    song = f'C:/Users/Ideapad/Music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0, END)
    playlist.activate(pichla)
    playlist.selection_set(pichla, last=None)

global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False

    else:
        pygame.mixer.music.pause()
        paused = True

def slide(X):
    #slider_label.config(text=f'{int(slider.get())}  -  {int(song_length)}')
    song = playlist.get(ACTIVE)
    song = f'C:/Users/Ideapad/Music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))

def volume(X):
    pygame.mixer.music.set_volume(volume_slider.get())

master_frame = Frame(root)
master_frame.pack(pady=20)

playlist=Listbox(master_frame,bg="black",fg="white",width=40,font=('arial',15),selectbackground="blue",selectforeground="black")
playlist.grid(row=0,column=0)

button_frame = Frame(master_frame)
button_frame.grid(row=1, column=0, pady=20)

#play button
play_button=Button(button_frame,text="Play",width =10,command=play)
play_button.grid(row=1,column=0)

#pause button 
pause_button=Button(button_frame,text="Pause/Resume",width =14,command=lambda:pause(paused))
pause_button.grid(row=1,column=1)

#stop button
stop_button=Button(button_frame,text="Stop",width =10,command=stop)
stop_button.grid(row=1,column=2)

#previous button
previous_button=Button(button_frame,text="Previous",width =10,command=previous_song)
previous_button.grid(row=1,column=3)

#nextbutton
next_button=Button(button_frame,text="Next",width =10,command=next_song)
next_button.grid(row=1,column=4)


volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist", command=add_song)
add_song_menu.add_command(label="Add multiple song to playlist", command=add_many)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete the selected song from Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all song from Playlist", command=delete_all)

status_bar = Label(root, text='', relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
slider.grid(row=2, column=0, pady=10)

volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)


#slider_label = Label(root, text="0")
#slider_label.pack(pady=10)

root.mainloop()
