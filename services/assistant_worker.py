
from PySide6.QtCore import QObject, Signal, Slot

from agent import Agent
from stt.whisper_stt import WhisperSTT
from tts.tts_engine import TTSEngine


class AssistantWorker(QObject):
    response_ready = Signal(str)
    error_occurred = Signal(str)
    status_changed = Signal(str)
    user_message_ready = Signal(str)

    def __init__(self):
        super().__init__()

        self.agent = None
        self.stt = None
        self.tts = None

    def initialize_agent(self):
        if self.agent is None:
            self.agent = Agent()

    def initialize_tts(self):
        if self.tts is None:
            self.tts = TTSEngine()

    @Slot(str)
    def process_message(self, message):
        self.process_request(message)

    @Slot()
    def listen_and_process(self):
        try:
            self.status_changed.emit("Initializing speech recognition...")

            if self.stt is None:
                self.stt = WhisperSTT()

            self.status_changed.emit("Listening... Speak now.")

            message = self.stt.listen()

            if not message:
                self.status_changed.emit("No speech detected.")
                self.response_ready.emit("")
                return

            self.user_message_ready.emit(message)
            self.process_request(message)

        except Exception as error:
            self.error_occurred.emit(str(error))

    def process_request(self, message):
        try:
            self.status_changed.emit("Thinking...")

            self.initialize_agent()
            response = self.agent.run(message)

            response = str(response)
            self.status_changed.emit("Speaking...")

            self.initialize_tts()
            self.tts.speak(response)

            self.response_ready.emit(response)

        except Exception as error:
            self.error_occurred.emit(str(error))
