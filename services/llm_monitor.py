
from PySide6.QtCore import QObject, Signal, Slot, QTimer


class LLMMonitor(QObject):
    status_changed = Signal(str)

    stop_requested = Signal()
    stopped = Signal()

    def __init__(self, manager):
        super().__init__()

        self.manager = manager
        self.timer = None
        self.previous_status = None

    @Slot()
    def start_monitoring(self):
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.check_status)

        self.check_status()
        self.timer.start()

    @Slot()
    def check_status(self):
        status = self.manager.get_status()

        if status != self.previous_status:
            self.previous_status = status
            self.status_changed.emit(status)

    @Slot()
    def stop_monitoring(self):
        if self.timer and self.timer.isActive():
            self.timer.stop()

        self.stopped.emit()
