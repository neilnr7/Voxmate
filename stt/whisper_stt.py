import sounddevice as sd
import numpy as np
import wave
import tempfile
import os

from faster_whisper import WhisperModel


class WhisperSTT:
    def __init__(self, model_size="small"):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

    def listen(
        self,
        sample_rate=16000,
        max_duration=8,
        silence_duration=1.2,
        threshold=500
    ):
        print("Listening...")

        audio = sd.rec(
            int(max_duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        audio = audio.flatten()

        # Find where speech starts
        volume = np.abs(audio)

        speech_indices = np.where(volume > threshold)[0]

        if len(speech_indices) == 0:
            print("No speech detected.")
            return ""

        start = max(0, speech_indices[0] - int(0.2 * sample_rate))

        # Find where speech ends
        silence_samples = int(silence_duration * sample_rate)

        end = len(audio)

        for i in range(start + silence_samples, len(audio)):
            chunk = audio[i - silence_samples:i]

            if np.max(np.abs(chunk)) < threshold:
                end = i
                break

        audio = audio[start:end]

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp:
            filename = temp.name

        try:
            with wave.open(filename, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio.tobytes())

            segments, _ = self.model.transcribe(
                filename,
                language="en",
                beam_size=5,
                vad_filter=True
            )

            text = " ".join(
                segment.text for segment in segments
            )

            return text.strip()

        finally:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == "__main__":
    stt = WhisperSTT()

    text = stt.listen()

    if text:
        print("You said:", text)