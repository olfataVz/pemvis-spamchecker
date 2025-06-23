from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QHBoxLayout
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
import json
import os
import sqlite3

from Database.database import DB_NAME

USERS_FILE = "users.json"

class SignupWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Signup")
        self.setGeometry(450, 220, 350, 250)
        self.parent = parent
        if self.parent:
            self.parent.hide()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Sign Up")
        title.setFont(QFont("Arial", 16))
        title.setStyleSheet("""
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #ffffff,
                stop:0.5 #add8e6,
                stop:1 #87ceeb
            );
            padding: 8px;
            border-radius: 6px;
            color: #1c4966;
            font-weight: bold;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        pw_layout1 = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.toggle_pw1 = QPushButton()
        self.toggle_pw1.setIcon(QIcon("Res/eye_closed.png"))
        self.toggle_pw1.setCheckable(True)
        self.toggle_pw1.setFixedWidth(32)
        self.toggle_pw1.clicked.connect(self.toggle_password_visibility1)
        pw_layout1.addWidget(self.password_input)
        pw_layout1.addWidget(self.toggle_pw1)
        layout.addLayout(pw_layout1)

        pw_layout2 = QHBoxLayout()
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Konfirmasi Password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.toggle_pw2 = QPushButton()
        self.toggle_pw2.setIcon(QIcon("Res/eye_closed.png"))
        self.toggle_pw2.setCheckable(True)
        self.toggle_pw2.setFixedWidth(32)
        self.toggle_pw2.clicked.connect(self.toggle_password_visibility2)
        pw_layout2.addWidget(self.confirm_input)
        pw_layout2.addWidget(self.toggle_pw2)
        layout.addLayout(pw_layout2)

        btn_signup = QPushButton("Daftar")
        btn_signup.clicked.connect(self.handle_signup)
        layout.addWidget(btn_signup)

        btn_back_to_login = QPushButton("Sudah punya akun? Kembali")
        btn_back_to_login.setStyleSheet("color: #3498db; background: none; border: none; font-weight: bold;")
        btn_back_to_login.clicked.connect(self.back_to_login)
        layout.addWidget(btn_back_to_login)

        self.setLayout(layout)
        self.setStyleSheet("background-color: white;")

    def back_to_login(self):
        self.close()
        if self.parent:
            self.parent.show()

    def toggle_password_visibility1(self):
        if self.toggle_pw1.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_pw1.setIcon(QIcon("Res/eye_open.png"))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_pw1.setIcon(QIcon("Res/eye_closed.png"))

    def toggle_password_visibility2(self):
        if self.toggle_pw2.isChecked():
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_pw2.setIcon(QIcon("Res/eye_open.png"))
        else:
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_pw2.setIcon(QIcon("Res/eye_closed.png"))

    def handle_signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if not username or not password or not confirm:
            QMessageBox.warning(self, "Peringatan", "Semua kolom harus diisi!")
            return

        if password != confirm:
            QMessageBox.critical(self, "Kesalahan", "Password tidak cocok!")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            QMessageBox.warning(self, "Gagal", "Username sudah digunakan.")
            conn.close()
            return

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Berhasil", "Akun berhasil dibuat! Silakan login.")

        # 🌟 Kembali ke Login dan isi username
        if self.parent:
            self.parent.set_username(username)  # isi field username di login
            self.parent.show()
        self.close()

