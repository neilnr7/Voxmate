
from PySide6.QtCore import QObject, Signal, Slot


class LLMStartupWorker(QObject):
    ready = Signal()
    failed = Signal(str)

    def __init__(self, manager):
        super().__init__()
        self.manager = manager

    @Slot()
    def start_server(self):
        try:
            self.manager.start()
            self.ready.emit()

        except Exception as error:
            self.failed.emit(str(error))
