from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import Qt

from spam_checker import predict_spam_probability

class ClassifierTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header layout
        header_layout = QHBoxLayout()

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("Res/mail.png").scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio))
        header_layout.addWidget(icon_label)

        title_label = QLabel("Klasifikasi Pesan")
        title_label.setFont(QFont("Arial", 16))
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Text input
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Silahkan isi dengan text atau pesan untuk klasifikasi..")
        self.text_input.setFont(QFont("Arial", 12))
        layout.addWidget(self.text_input)

        # Check Spam button
        self.check_button = QPushButton("Check Spam")
        self.check_button.clicked.connect(self.check_spam_text)
        layout.addWidget(self.check_button)

        self.setLayout(layout)

    def check_spam_text(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Peringatan", "Silahkan masukkan teks terlebih dahulu.")
            return

        prob = predict_spam_probability(text)
        prob_percent = round(prob * 100, 2)
        result = "Spam" if prob > 0.5 else "Ham"

        QMessageBox.information(
            self,
            "Hasil Klasifikasi",
            f"Pesan ini diklasifikasikan sebagai {result}.\nProbabilitas Spam: {prob_percent}%"
        )
