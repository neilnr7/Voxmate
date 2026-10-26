import threading
import pyttsx3
import pythoncom


class TTSEngine:
    def __init__(self):
        self._lock = threading.Lock()

    def speak(self, text: str):
        if not text or not text.strip():
            return

        def speak_worker():
            with self._lock:
                engine = None

                try:
                    # Initialize COM for this worker thread
                    pythoncom.CoInitialize()

                    engine = pyttsx3.init("sapi5")
                    engine.setProperty("rate", 175)
                    engine.setProperty("volume", 1.0)

                    engine.say(text)
                    engine.runAndWait()

                except Exception as e:
                    print(f"TTS Error: {e}")

                finally:
                    if engine is not None:
                        try:
                            engine.stop()
                        except Exception:
                            pass

                    # Release COM on the same thread
                    try:
                        pythoncom.CoUninitialize()
                    except Exception:
                        pass

        worker = threading.Thread(target=speak_worker)
        worker.start()
        worker.join()