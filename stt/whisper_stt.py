import os
import numpy as np
import sounddevice as sd
import torch

from faster_whisper import WhisperModel
from silero_vad import load_silero_vad


class WhisperSTT:
    def __init__(self, model_size="base"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

        self.vad_model = load_silero_vad()

        self.sample_rate = 16000
        self.silence_duration = 0.7
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

        print("Processing...")

        segments, _ = self.model.transcribe(
            audio,
            language="en",
            beam_size=1
        )

        return " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()


if __name__ == "__main__":
    stt = WhisperSTT()
    text = stt.listen()

    if text:
        print("You said:", text)