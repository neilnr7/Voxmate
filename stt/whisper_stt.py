
import os
import tempfile
import wave

import numpy as np
import sounddevice as sd
import torch

from faster_whisper import WhisperModel
from silero_vad import load_silero_vad


class WhisperSTT:
    def __init__(self, model_size="small"):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

        self.vad_model = load_silero_vad()

        self.sample_rate = 16000
        self.silence_duration = 2.0
        self.start_timeout = 5.0
        self.max_duration = 15.0

        # Silero VAD requires 512 samples at 16 kHz.
        self.chunk_size = 512
        self.chunk_duration = self.chunk_size / self.sample_rate

    def listen(self):
        print("Listening...")

        silence_chunks_required = int(
            self.silence_duration / self.chunk_duration
        )

        timeout_chunks = int(
            self.start_timeout / self.chunk_duration
        )

        max_chunks = int(
            self.max_duration / self.chunk_duration
        )

        audio_chunks = []
        speech_started = False
        silence_chunks = 0
        waited_chunks = 0

        self.vad_model.reset_states()

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                blocksize=self.chunk_size
            ) as stream:

                while waited_chunks < max_chunks:
                    chunk, overflowed = stream.read(
                        self.chunk_size
                    )
                    waited_chunks += 1

                    if overflowed:
                        print("Warning: Audio input overflow.")

                    audio = chunk[:, 0].copy()
                    audio_tensor = torch.from_numpy(audio)

                    with torch.inference_mode():
                        speech_probability = self.vad_model(
                            audio_tensor,
                            self.sample_rate
                        ).item()

                    is_speech = speech_probability >= 0.5

                    if not speech_started:
                        if is_speech:
                            speech_started = True
                            print("Speech detected...")
                            audio_chunks.append(audio)
                            continue

                        if waited_chunks >= timeout_chunks:
                            print("No speech detected.")
                            return ""

                        continue

                    audio_chunks.append(audio)

                    if is_speech:
                        silence_chunks = 0
                    else:
                        silence_chunks += 1

                    if silence_chunks >= silence_chunks_required:
                        break

        finally:
            self.vad_model.reset_states()

        if not speech_started or not audio_chunks:
            print("No speech detected.")
            return ""

        audio = np.concatenate(audio_chunks)
        audio = np.clip(audio, -1.0, 1.0)

        audio_int16 = (audio * 32767).astype(np.int16)
        filename = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            ) as temp:
                filename = temp.name

            with wave.open(filename, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_int16.tobytes())

            print("Processing...")

            segments, _ = self.model.transcribe(
                filename,
                language="en",
                beam_size=5,
                vad_filter=True
            )

            return " ".join(
                segment.text.strip()
                for segment in segments
            ).strip()

        finally:
            if filename and os.path.exists(filename):
                os.remove(filename)


if __name__ == "__main__":
    stt = WhisperSTT()
    text = stt.listen()

    if text:
        print("You said:", text)
