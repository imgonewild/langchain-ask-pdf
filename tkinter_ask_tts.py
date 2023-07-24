import tkinter as tk
from tkinter import *
from tkinter_ask_tts_api import *
import sounddevice as sd
from scipy.io.wavfile import write
load_dotenv()
vector_folder = os.getenv('VECTOR_PATH')
embeddings = OpenAIEmbeddings()

try:
    file = sys.argv[1]
except:
    file = "BioRem-2000-Surface-Cleaner MSDS.pdf"

default = "What is this?"

def record():
    # set the sample rate and duration
    sample_rate = 44100  # in Hz
    duration = 5.0  # in seconds

    print("Recording Audio")
    my_audio = sd.rec(int(sample_rate * duration), 
                    samplerate=sample_rate, channels=2)
    sd.wait()  # wait for the recording to finish
    print("Audio recording complete , Play Audio")
    sd.play(my_audio, sample_rate)
    sd.wait()  # wait for the audio to play back
    print("Play Audio Complete")

    # save the audio file
    write('output.wav', sample_rate, my_audio)  # save as .wav file

    print('File saved to ' + os.getcwd() + '/output.wav')

def default_msg():
    ChatBox.config(state=NORMAL)
    ChatBox.config(foreground="#446665", font=("Verdana", 12 ))
    knowledge_base = FAISS.load_local(f"{vector_folder}\{file}", embeddings)
    msg = default
    res = ask_pdf(msg, knowledge_base)
    ChatBox.insert(END, res + '------------------------------------------------\n')
    ChatBox.config(state=DISABLED)
    ChatBox.yview(END)

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    # EntryBox.delete("0.0",END)

    if msg != '':
        ChatBox.config(state=NORMAL)
        ChatBox.insert(END, "You: " + msg +'\n')
        ChatBox.config(foreground="#446665", font=("Verdana", 12 ))
        knowledge_base = FAISS.load_local(f"{vector_folder}\{file}", embeddings)
        res = ask_pdf(msg, knowledge_base)
        # res = msg
        ChatBox.insert(END, "Bot: " + res + '------------------------------------------------\n')            
        ChatBox.config(state=DISABLED)
        ChatBox.yview(END)

root = tk.Tk()
root.title(file)
root.resizable(True, True)
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
w = 367/1600*ws # width for the Tk root

h = hs # height for the Tk root
x = ws-w #(ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

ChatBox = Text(root, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatBox.config(state=DISABLED)

scrollbar = Scrollbar(root, command=ChatBox.yview, cursor="heart")
ChatBox['yscrollcommand'] = scrollbar.set

EntryBox = Text(root ,bd=0, bg="white",width="29", height="5", font="Arial")
EntryBox.insert(INSERT, "What is the waste procedure?")
EntryBox.bind('<Return>', lambda event: send())

SendButton = Button(root, font=("Verdana",12,'bold'), text="Send", width="8", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )
RecordButton = Button(root, font=("Verdana",12,'bold'), text="Record", width="8", height=5,
                    bd=0, bg="red", activebackground="#3c9d9b",fg='#ffffff',
                    command= record )

# add_heigh = 740-386
add_heigh = 0
scrollbar.place(x=340,y=6, height=386+add_heigh)
ChatBox.place(x=6,y=6, height=386+add_heigh, width=348) #h:740
EntryBox.place(x=6, y=401+add_heigh, height=90, width=248)
SendButton.place(x=256, y=401+add_heigh, height=90, width=100)
RecordButton.place(x=256, y=401+add_heigh+90, height=90, width=100)
# default_msg()
root.mainloop()