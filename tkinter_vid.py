import tkinter as tk
from tkVideoPlayer import TkinterVideo

root = tk.Tk()
root.geometry("900x500")

def loopVideo():
    videoplayer.load("vid/think.mp4")
    videoplayer.play()
    root.after(1, loopVideo)

videoplayer = TkinterVideo(master=root, scaled=True)
videoplayer.load("vid/think.mp4")
videoplayer.pack(expand=True, fill="both")
videoplayer.bind('<<Ended>>', lambda event: loopVideo())

videoplayer.play()  # Play the video
root.mainloop()
