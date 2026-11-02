
import sys
import ctypes
from ctypes import wintypes

from PySide6.QtWidgets import (
    QMainWindow,
    QSystemTrayIcon,
    QMenu,
    QApplication,
    QStyle,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QThread, Qt

from gui.chat_widget import ChatWidget
from services.assistant_worker import AssistantWorker
from services.llm_manager import LLMManager
from services.llm_startup_worker import LLMStartupWorker
from services.llm_monitor import LLMMonitor


# Windows global hotkey configuration
HOTKEY_ID = 1
MOD_SHIFT = 0x0004
MOD_NOREPEAT = 0x4000
VK_OEM_PERIOD = 0xBE
WM_HOTKEY = 0x0312


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VoxMate")
        self.resize(1000, 700)
        self.setMinimumSize(700, 500)

        self.shutdown_started = False

        self.llm_available = False
        self.assistant_busy = False

        self.exiting = False
        self.hotkey_registered = False
        self.user32 = None

        self.chat_widget = ChatWidget()
        self.setCentralWidget(self.chat_widget)

        # System tray
        self.setup_tray()

        # Global hotkey
        self.register_global_hotkey()

        # LLM manager
        self.llm_manager = LLMManager()

        # LLM startup thread
        self.startup_thread = QThread(self)
        self.startup_worker = LLMStartupWorker(
            self.llm_manager
        )
        self.startup_worker.moveToThread(
            self.startup_thread
        )

        self.startup_thread.started.connect(
            self.startup_worker.start_server
        )

        self.startup_worker.ready.connect(
            self.on_llm_ready
        )
        self.startup_worker.failed.connect(
            self.on_llm_failed
        )

        self.startup_worker.ready.connect(
            self.startup_thread.quit
        )
        self.startup_worker.failed.connect(
            self.startup_thread.quit
        )

        # Assistant worker thread
        self.worker_thread = QThread(self)
        self.worker = AssistantWorker()
        self.worker.moveToThread(self.worker_thread)

        self.chat_widget.message_submitted.connect(
            self.worker.process_message
        )
        self.chat_widget.voice_requested.connect(
            self.worker.listen_and_process
        )

        self.chat_widget.message_submitted.connect(
            self.on_request_started
        )
        self.chat_widget.voice_requested.connect(
            self.on_request_started
        )

        self.worker.response_ready.connect(
            self.show_response
        )
        self.worker.error_occurred.connect(
            self.show_error
        )
        self.worker.status_changed.connect(
            self.chat_widget.set_status
        )
        self.worker.user_message_ready.connect(
            self.show_user_message
        )

        self.worker_thread.start()

        # LLM monitor thread
        self.monitor_thread = QThread(self)
        self.monitor = LLMMonitor(self.llm_manager)
        self.monitor.moveToThread(self.monitor_thread)

        self.monitor.stop_requested.connect(
            self.monitor.stop_monitoring,
            Qt.ConnectionType.QueuedConnection
        )

        # IMPORTANT:
        # Quit the monitor thread directly from the monitor thread.
        # This avoids blocking the GUI thread during shutdown.
        self.monitor.stopped.connect(
            self.monitor_thread.quit,
            Qt.ConnectionType.DirectConnection
        )

        self.monitor_thread.started.connect(
            self.monitor.start_monitoring
        )

        self.monitor_thread.finished.connect(
            self.monitor.deleteLater
        )

        self.monitor.status_changed.connect(
            self.on_llm_status_changed
        )

        # Initial state
        self.chat_widget.set_busy(True)
        self.chat_widget.set_status("Starting LLM...")

        self.startup_thread.start()

    # --------------------------------------------------
    # SYSTEM TRAY
    # --------------------------------------------------

    def setup_tray(self):
        tray_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_ComputerIcon
        )

        self.tray_icon = QSystemTrayIcon(tray_icon, self)
        self.tray_icon.setToolTip("VoxMate")

        tray_menu = QMenu()

        show_action = QAction("Show VoxMate", self)
        show_action.triggered.connect(self.restore_window)

        exit_action = QAction("Exit VoxMate", self)
        exit_action.triggered.connect(self.exit_application)

        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)

        self.tray_icon.activated.connect(
            self.on_tray_activated
        )

        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon.show()
        else:
            print("System tray is unavailable.")

    def on_tray_activated(self, reason):
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.restore_window()

    def restore_window(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def exit_application(self):
        self.exiting = True
        self.close()

    # --------------------------------------------------
    # GLOBAL HOTKEY: SHIFT + PERIOD
    # --------------------------------------------------

    def register_global_hotkey(self):
        if sys.platform != "win32":
            print("Global hotkey is supported only on Windows.")
            return

        try:
            self.user32 = ctypes.WinDLL(
                "user32",
                use_last_error=True
            )

            self.user32.RegisterHotKey.argtypes = [
                wintypes.HWND,
                ctypes.c_int,
                wintypes.UINT,
                wintypes.UINT,
            ]
            self.user32.RegisterHotKey.restype = wintypes.BOOL

            self.user32.UnregisterHotKey.argtypes = [
                wintypes.HWND,
                ctypes.c_int,
            ]
            self.user32.UnregisterHotKey.restype = wintypes.BOOL

            hwnd = int(self.winId())

            success = self.user32.RegisterHotKey(
                hwnd,
                HOTKEY_ID,
                MOD_SHIFT | MOD_NOREPEAT,
                VK_OEM_PERIOD,
            )

            if success:
                self.hotkey_registered = True
                print("Global hotkey registered: Shift + .")
            else:
                error_code = ctypes.get_last_error()
                print(
                    "Could not register global hotkey. "
                    f"Windows error: {error_code}"
                )

        except Exception as error:
            print(f"Global hotkey setup failed: {error}")

    def nativeEvent(self, event_type, message):
        if event_type == "windows_generic_MSG":
            try:
                msg = wintypes.MSG.from_address(
                    int(message)
                )

                if (
                    msg.message == WM_HOTKEY
                    and msg.wParam == HOTKEY_ID
                ):
                    self.handle_global_hotkey()
                    return True, 0

            except (ValueError, TypeError):
                pass

        return super().nativeEvent(event_type, message)

    def handle_global_hotkey(self):
        if self.exiting:
            return

        if not self.llm_available:
            return

        if self.assistant_busy:
            return

        self.chat_widget.voice_requested.emit()

    def unregister_global_hotkey(self):
        if not self.hotkey_registered or not self.user32:
            return

        try:
            self.user32.UnregisterHotKey(
                int(self.winId()),
                HOTKEY_ID,
            )
            self.hotkey_registered = False
            print("Global hotkey unregistered.")

        except Exception as error:
            print(f"Hotkey cleanup failed: {error}")

    # --------------------------------------------------
    # LLM STATUS
    # --------------------------------------------------

    def on_llm_ready(self):
        self.llm_available = True
        self.update_chat_state()
        self.chat_widget.set_status("Ready")

        if not self.monitor_thread.isRunning():
            self.monitor_thread.start()

    def on_llm_failed(self, error):
        self.llm_available = False
        self.update_chat_state()

        self.chat_widget.add_message(
            "VoxMate",
            f"Could not start the LLM server: {error}"
        )
        self.chat_widget.set_status("LLM startup failed")

    def on_llm_status_changed(self, status):
        if status == "running":
            self.llm_available = True
            self.chat_widget.set_status("LLM connected")

        elif status == "crashed":
            self.llm_available = False
            self.chat_widget.set_status("LLM server crashed")

        else:
            self.llm_available = False
            self.chat_widget.set_status("LLM unavailable")

        self.update_chat_state()

    # --------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------

    def update_chat_state(self):
        self.chat_widget.set_busy(
            not self.llm_available or self.assistant_busy
        )

    def on_request_started(self, *args):
        self.assistant_busy = True
        self.update_chat_state()

    def show_user_message(self, message):
        self.chat_widget.add_message("You", message)

    def show_response(self, response):
        if response:
            self.chat_widget.add_message("VoxMate", response)

        self.assistant_busy = False
        self.update_chat_state()

        if self.llm_available:
            self.chat_widget.set_status("Ready")

    def show_error(self, error):
        self.chat_widget.add_message(
            "VoxMate",
            f"Error: {error}"
        )

        self.assistant_busy = False
        self.update_chat_state()

        if self.llm_available:
            self.chat_widget.set_status("Ready")

    # --------------------------------------------------
    # APPLICATION SHUTDOWN
    # --------------------------------------------------

    def closeEvent(self, event):
        # Normal window close: hide instead of exiting.
        if not self.exiting and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
            return

        # Prevent shutdown from running more than once.
        if self.shutdown_started:
            event.accept()
            return

        self.shutdown_started = True

        print("Shutting down VoxMate...")

        # Unregister global hotkey.
        self.unregister_global_hotkey()

        # Hide system tray icon.
        self.tray_icon.hide()

        # Stop monitor timer in its own thread.
        if self.monitor_thread.isRunning():
            self.monitor.stop_requested.emit()
            self.monitor_thread.wait()

        # Stop startup thread if still running.
        if self.startup_thread.isRunning():
            self.startup_thread.quit()
            self.startup_thread.wait()

        # Stop only the LLM server started by VoxMate.
        self.llm_manager.stop()

        # Stop assistant thread.
        self.worker_thread.quit()
        self.worker_thread.wait()

        print("VoxMate shutdown complete.")

        event.accept()
        
        # Explicitly exit the Qt application event loop.
        QApplication.quit()
