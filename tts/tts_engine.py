
import pyttsx3


class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)

    def speak(self, text: str):
        if not text or not text.strip():
            return

        self.engine.say(text)
        self.engine.runAndWait()
