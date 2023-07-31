import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

def show_gif():
    file_path = "img/owl.gif"  # Replace with the path to your GIF file
    gif = Image.open(file_path)

    gif_frames = [frame.resize((200, 200), Image.ANTIALIAS) for frame in ImageSequence.Iterator(gif)]
    gif_frames = [ImageTk.PhotoImage(frame) for frame in gif_frames]

    def update_frame(frame_num):
        label.config(image=gif_frames[frame_num])
        root.after(100, update_frame, (frame_num + 1) % len(gif_frames))

    label.config(image=gif_frames[0])
    update_frame(1)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("GIF Viewer")

    label = tk.Label(root, compound=tk.CENTER)
    label.pack(padx=10, pady=5)

    show_gif()

    root.mainloop()
