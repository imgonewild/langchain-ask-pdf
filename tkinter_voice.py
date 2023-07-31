from gtts import gTTS
import pyglet
import io

def speak_in_spanish(text):
    tts = gTTS(text=text, lang='es')
    tts_file = io.BytesIO()
    tts.write_to_fp(tts_file)
    tts_file.seek(0)

    # Play the audio using pyglet
    audio = pyglet.media.load('tts.mp3', file=tts_file)
    audio.play()

    # Schedule the application exit after the audio duration
    pyglet.clock.schedule_once(lambda dt: pyglet.app.exit(), audio.duration)

    # Start the pyglet event loop
    pyglet.app.run()

if __name__ == "__main__":
    text_to_speak = "Hola, ¿cómo estás? Estoy aprendiendo a hablar en español."
    speak_in_spanish(text_to_speak)
