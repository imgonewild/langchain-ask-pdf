import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter_ask_tts_api import *
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import speech_recognition as sr
from PIL import Image, ImageTk, ImageSequence
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import queue, threading, os, sys
from tkVideoPlayer import TkinterVideo
from gtts import gTTS
import pyglet, io

load_dotenv()
vector_folder = os.getenv('VECTOR_PATH')
parent_folder = os.getcwd() + "/"
image_folder = parent_folder + 'img/'
video_folder = parent_folder + 'vid/'

embeddings = OpenAIEmbeddings()
# lang_code = 'en'
lang = 'English'
try:
    file = sys.argv[1]
except:
    file = "BioRem-2000-Surface-Cleaner MSDS.pdf"

class AudioRecorderApp:
    def __init__(self, root):
        self.root = root
        self.is_recording = False
        self.audio_queue = queue.Queue()

        self.mic_image_path = image_folder + "mic.ico"  # Replace with the actual path to your mic image file
        self.square_image_path = image_folder + "square-128.ico"  # Replace with the actual path to your square image file
        
        self.img_mic = Image.open(self.mic_image_path)
        self.img_square = Image.open(self.square_image_path)

        self.img_mic = self.img_mic.resize((25, 25), Image.LANCZOS)  # Resize the mic image to fit the button
        self.img_square = self.img_square.resize((25, 25), Image.LANCZOS)  # Resize the square image to fit the button
        
        self.photo_mic = ImageTk.PhotoImage(self.img_mic)
        self.photo_square = ImageTk.PhotoImage(self.img_square)

        self.record_btn = ttk.Button(root, image=self.photo_mic,
            command=self.toggle_recording)
        self.record_btn.place(x=256, y=465 + m_height, height=40, width=100)

        self.record_btn.config(state=tk.NORMAL, cursor="hand2")

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
            self.record_btn.config(image=self.photo_square)  # Change to square icon
        else:
            self.stop_recording()
            self.record_btn.config(image=self.photo_mic)  # Change back to mic icon

    def start_recording(self):
        self.is_recording = True
        self.record_audio = []
        self.recording_thread = threading.Thread(target=self.record_audio_thread)
        self.recording_thread.start()

    def stop_recording(self):
        self.is_recording = False

    def record_audio_thread(self):
        def audio_callback(indata, frames, time, status):
            if self.is_recording:
                self.audio_queue.put(indata.copy())

        with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100):
            while self.is_recording:
                sd.sleep(100)

        self.record_btn.config(text="Record", state=tk.NORMAL)
        self.save_audio_to_wav()
        self.wav_to_text()
        send()

    def save_audio_to_wav(self):
        wav_file = "recorded_audio.wav"
        while not self.audio_queue.empty():
            self.record_audio.extend(self.audio_queue.get())

        self.record_audio = np.array(self.record_audio)
        scaled_data = np.int16(self.record_audio * 32767)  # Scale to 16-bit integer range

        wavfile.write(wav_file, 44100, scaled_data)

    def wav_to_text(self):
        r = sr.Recognizer()
        hellow=sr.AudioFile('recorded_audio.wav')
        with hellow as source:
            audio = r.record(source)
        try:
            self.lang = options_dict[selected_option.get()]
            s = r.recognize_google(audio, language = self.lang)
            EntryBox.delete("1.0", tk.END)
            EntryBox.insert(INSERT, s)
            print("Text: "+s)
        except Exception as e:
            print("Exception: "+str(e))

def record():
    EntryBox.delete("1.0", tk.END)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Talk")
        try:
            audio_text = r.listen(source, timeout=5)  # Adjust the timeout value as needed
            print("Time over, thanks")
            try:
                # Using Google speech recognition
                recognized_text = r.recognize_google(audio_text)
                print("Text: " + recognized_text)
                EntryBox.insert(tk.END, recognized_text)
            except sr.UnknownValueError:
                print("Sorry, I could not understand.")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")

def on_entry_change(event):
    entry_text = EntryBox.get("1.0",'end-1c').strip()
    if entry_text:
        SendButton.config(state=tk.NORMAL, cursor="hand2")
    else:
        SendButton.config(state=tk.DISABLED, cursor="arrow")


def send():
    msg = EntryBox.get("1.0",'end-1c').strip()

    if msg != '':
        ChatBox.config(state=NORMAL)
        ChatBox.insert(END, "You: " + msg +'\n', "user")
        ChatBox.tag_configure("user", foreground="red")
        ChatBox.config(foreground="#446665", font=("Verdana", 12 ))        
        knowledge_base = FAISS.load_local(f"{vector_folder}\{file}", embeddings)

        videoplayer.load(video_folder + "answer2.mp4")
        res = ask_pdf(msg, knowledge_base, selected_option.get())
        ChatBox.insert(END, "Fox: " + res + '\n------------------------------------------------', "bot")            
        ChatBox.tag_configure("bot", foreground="black")
        ChatBox.config(state=DISABLED)
        ChatBox.yview(END)
        threading.Thread(target=lambda: tts(res)).start()        
        
def tts(speech):    
    tts_lang = options_dict[selected_option.get()]
    tts = gTTS(text=speech, lang=tts_lang)
    tts_file = io.BytesIO()
    tts.write_to_fp(tts_file)
    tts_file.seek(0)

    # Play the audio using pyglet
    audio = pyglet.media.load('tts.mp3', file=tts_file)
    audio.play()
    pyglet.clock.schedule_once(lambda dt: pyglet.app.exit(), audio.duration)
    pyglet.app.run()
    videoplayer.load(video_folder+"wait.mp4")

root = tk.Tk()
root.title(file)
root.resizable(True, True)
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
option_menu  = 367/1600*ws # width for the Tk root

h = hs # height for the Tk root
x = ws-option_menu  #(ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (option_menu , 710, x, y))

def loop_play_wait(event):
    print("loop")
    videoplayer.play()

videoplayer = TkinterVideo(master=root, scaled=True)
videoplayer.load(video_folder+"wait.mp4")
videoplayer.bind('<<Ended>>', loop_play_wait)
videoplayer.play()

ChatBox = Text(root, bd=0, bg="white", height="10", width="50", font="Arial")
ChatBox.config(state=DISABLED)

scrollbar = Scrollbar(root, command=ChatBox.yview, cursor="heart")
ChatBox['yscrollcommand'] = scrollbar.set

EntryBox = Text(root ,bd=0, bg="white",width="29", height="5", font="Arial")
EntryBox.insert(INSERT, "What is the waste procedure?")
EntryBox.bind('<Return>', lambda event: send())
EntryBox.bind("<KeyRelease>", on_entry_change)
        
send_button_image = Image.open(image_folder+"telegram-128.ico")
send_button_image = send_button_image.resize((25, 25), Image.LANCZOS)  # Resize the image if necessary
send_button_image = ImageTk.PhotoImage(send_button_image)

SendButton = ttk.Button(root, image=send_button_image, command=send, )#state=tk.DISABLED
SendButton.image = send_button_image  # Keep a reference to the image to prevent garbage collection
SendButton.config(state=tk.NORMAL, cursor="hand2")
SendButton.pack()

options_dict = {
    "English": "en",
    "Spanish": "es"
}
options = list(options_dict.keys())
selected_option = tk.StringVar()
selected_option.set(options[0])
# option_menu = ttk.Combobox(root, selected_option, *options)
option_menu = ttk.Combobox(root, values=options, textvariable=selected_option, state="readonly",justify="center")
option_menu.config(cursor="hand2")

m_height = 200
scrollbar.place(x=340,y=5 + m_height, height=386)
ChatBox.place(x=6,y=5 + m_height, height=386, width=348) #h:740

separator = ttk.Separator(root, orient="horizontal")
separator.place(x=0, y=395 + m_height, relwidth=1)

EntryBox.place(x=6, y=400 + m_height, height=105, width=248)
option_menu.place(x=256, y=395+m_height, height=30, width=100)

SendButton.place(x=256, y=425 + m_height, height=40, width=100)
videoplayer.place(x=0, y=0, height=200, width=350)

app = AudioRecorderApp(root)

# default_msg()
root.mainloop()