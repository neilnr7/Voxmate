import pyttsx3


class TextToSpeech:
    def __init__(self, rate=175, volume=1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

    def speak(self, text):
        if not text or not text.strip():
            return

        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == "__main__":
    tts = TextToSpeech()
    tts.speak("Hello! VoxMate text to speech is working.")
