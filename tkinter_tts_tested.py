import tkinter as tk
import os
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def record_audio():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Recording Audio")
        audio = recognizer.listen(source)
        print("Audio recording complete")
    
    # save the audio file
    with open("output.wav", "wb") as file:
        file.write(audio.get_wav_data())
    print('File saved to ' + os.getcwd() + '/output.wav')

    try:
        text = recognizer.recognize_google(audio)
        tts_text.insert(tk.END, 'You said: ' + text + '\n')

        # text to speech
        engine.say("You said: " + text)
        engine.runAndWait()
    except:
        tts_text.insert(tk.END, 'Sorry, I did not get that. Please speak again.' + '\n')

root = tk.Tk()
root.geometry('600x400')
root.title('Record, Save, Transcribe and Text to Speech')

record_button = tk.Button(root, text='Record', command=record_audio)
record_button.pack()

tts_text = tk.Text(root, height=10, width=50)
tts_text.pack()

root.mainloop()
