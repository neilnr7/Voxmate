
from html import escape

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextBrowser,
    QLineEdit,
    QPushButton,
    QLabel,
    QFrame,
)


class ChatWidget(QWidget):
    message_submitted = Signal(str)
    voice_requested = Signal()

    def __init__(self):
        super().__init__()

        self.wave_frames = [
            "▁ ▂ ▃ ▅ ▃ ▂ ▁",
            "▂ ▄ ▆ ▃ ▅ ▄ ▂",
            "▃ ▅ ▂ ▆ ▄ ▂ ▅",
            "▂ ▄ ▅ ▃ ▆ ▄ ▂",
        ]
        self.wave_index = 0

        self.setup_ui()

        self.wave_timer = QTimer(self)
        self.wave_timer.setInterval(180)
        self.wave_timer.timeout.connect(self.animate_wave)

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #101114;
                color: #E8EAF0;
                font-family: "Segoe UI";
            }

            QLabel {
                background: transparent;
            }

            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 13px;
            }

            QPushButton:disabled {
                background-color: #30323A;
                color: #777984;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(36, 24, 36, 24)
        main_layout.setSpacing(16)

        # Header
        header = QHBoxLayout()

        branding = QLabel("VOXMATE")
        branding.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 3px;
            color: #E8EAF0;
        """)

        self.chat_toggle = QPushButton("Open Chat")
        self.chat_toggle.setStyleSheet("""
            QPushButton {
                background-color: #20232B;
                color: #C5C9D3;
                border: 1px solid #343741;
            }
            QPushButton:hover {
                background-color: #2B2F39;
            }
        """)
        self.chat_toggle.clicked.connect(self.toggle_chat)

        header.addWidget(branding)
        header.addStretch()
        header.addWidget(self.chat_toggle)

        main_layout.addLayout(header)

        # Voice area
        voice_area = QVBoxLayout()
        voice_area.setSpacing(18)
        voice_area.addStretch()

        self.status_label = QLabel("Ready when you are")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 500;
            color: #E8EAF0;
        """)

        self.waveform_label = QLabel("▁ ▂ ▃ ▅ ▃ ▂ ▁")
        self.waveform_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.waveform_label.setStyleSheet("""
            font-size: 27px;
            color: #777E91;
            letter-spacing: 5px;
        """)

        self.mic_button = QPushButton("🎙")
        self.mic_button.setFixedSize(112, 112)
        self.mic_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mic_button.setToolTip("Speak to VoxMate")

        self.mic_button.setStyleSheet("""
            QPushButton {
                background-color: #252B3A;
                color: #A9C7FF;
                border: 2px solid #465C83;
                border-radius: 56px;
                font-size: 38px;
            }

            QPushButton:hover {
                background-color: #303C54;
                border: 2px solid #7598D5;
            }

            QPushButton:pressed {
                background-color: #3B5278;
            }

            QPushButton:disabled {
                background-color: #20232B;
                color: #656A78;
                border: 2px solid #343741;
            }
        """)

        mic_container = QHBoxLayout()
        mic_container.addStretch()
        mic_container.addWidget(self.mic_button)
        mic_container.addStretch()

        self.hint_label = QLabel("Press the microphone or use your hotkey")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label.setStyleSheet("""
            font-size: 12px;
            color: #858B9A;
        """)

        voice_area.addWidget(self.status_label)
        voice_area.addWidget(self.waveform_label)
        voice_area.addLayout(mic_container)
        voice_area.addWidget(self.hint_label)
        voice_area.addStretch()

        main_layout.addLayout(voice_area, stretch=1)

        # Expandable chat panel
        self.chat_panel = QFrame()
        self.chat_panel.setStyleSheet("""
            QFrame {
                background-color: #181A20;
                border: 1px solid #30333D;
                border-radius: 12px;
            }
        """)

        chat_layout = QVBoxLayout(self.chat_panel)
        chat_layout.setContentsMargins(12, 12, 12, 12)
        chat_layout.setSpacing(10)

        self.chat_display = QTextBrowser()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextBrowser {
                background-color: #181A20;
                color: #E8EAF0;
                border: none;
                font-size: 13px;
                padding: 8px;
            }
        """)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText(
            "Type a message to VoxMate..."
        )
        self.message_input.setMinimumHeight(42)
        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: #242730;
                color: white;
                border: 1px solid #393D49;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
        """)

        self.send_button = QPushButton("Send")
        self.send_button.setMinimumHeight(42)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #456DAA;
                color: white;
            }
            QPushButton:hover {
                background-color: #5683C7;
            }
        """)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)

        chat_layout.addWidget(self.chat_display)
        chat_layout.addLayout(input_layout)

        self.chat_panel.setMaximumHeight(260)
        self.chat_panel.hide()

        main_layout.addWidget(self.chat_panel)

        # Footer
        footer = QLabel("Your private desktop assistant")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("""
            font-size: 11px;
            color: #626877;
        """)

        main_layout.addWidget(footer)

        # Connections
        self.mic_button.clicked.connect(self.voice_requested.emit)
        self.send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)

        self.add_message(
            "VoxMate",
            "Hello! I'm VoxMate. How can I help you?"
        )

    def toggle_chat(self):
        visible = not self.chat_panel.isVisible()
        self.chat_panel.setVisible(visible)

        self.chat_toggle.setText(
            "Close Chat" if visible else "Open Chat"
        )

    def send_message(self):
        message = self.message_input.text().strip()

        if not message:
            return

        self.add_message("You", message)
        self.message_input.clear()

        self.set_busy(True)
        self.message_submitted.emit(message)

    def add_message(self, sender, message):
        if not message:
            return

        safe_sender = escape(sender)
        safe_message = escape(str(message)).replace("\n", "<br>")

        if sender == "You":
            color = "#83B5FF"
            alignment = "right"
        else:
            color = "#8BD6B0"
            alignment = "left"

        html = f"""
        <div style="margin: 12px 4px; text-align: {alignment};">
            <span style="color: {color}; font-weight: bold;">
                {safe_sender}
            </span>
            <br>
            <span style="color: #E8EAF0;">
                {safe_message}
            </span>
        </div>
        """

        self.chat_display.append(html)

    def set_busy(self, busy):
        self.send_button.setDisabled(busy)
        self.message_input.setDisabled(busy)
        self.mic_button.setDisabled(busy)

        self.send_button.setText("..." if busy else "Send")

    def set_status(self, status):
        self.status_label.setText(status)

        normalized = status.lower()

        if "listening" in normalized:
            self.hint_label.setText("I'm listening...")
            self.start_wave_animation()

        elif "thinking" in normalized or "initializing" in normalized:
            self.hint_label.setText("Processing your request...")
            self.stop_wave_animation()

        elif "speaking" in normalized:
            self.hint_label.setText("VoxMate is responding...")
            self.start_wave_animation()

        elif "error" in normalized or "failed" in normalized:
            self.hint_label.setText("Something needs your attention.")
            self.stop_wave_animation()

        else:
            self.hint_label.setText(
                "Press the microphone or use your hotkey"
            )
            self.stop_wave_animation()

    def start_wave_animation(self):
        if not self.wave_timer.isActive():
            self.wave_timer.start()

    def stop_wave_animation(self):
        self.wave_timer.stop()
        self.waveform_label.setText("▁ ▂ ▃ ▅ ▃ ▂ ▁")
        self.waveform_label.setStyleSheet("""
            font-size: 27px;
            color: #777E91;
            letter-spacing: 5px;
        """)

    def animate_wave(self):
        frame = self.wave_frames[self.wave_index]
        self.wave_index = (
            self.wave_index + 1
        ) % len(self.wave_frames)

        self.waveform_label.setText(frame)
        self.waveform_label.setStyleSheet("""
            font-size: 27px;
            color: #83B5FF;
            letter-spacing: 5px;
        """)
