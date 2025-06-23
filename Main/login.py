from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
import json
import os
import sqlite3

from Main.dashboard import DashboardWindow
from Main.signup import SignupWindow
from Database.database import DB_NAME
LOGIN_STATE_FILE = "login_state.json"

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(400, 200, 350, 240)

        self.setup_ui()
        self.check_remembered_user()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Login")
        title.setFont(QFont("Arial", 16))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        pw_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.toggle_pw = QPushButton()
        self.toggle_pw.setIcon(QIcon("Res/eye_closed.png"))
        self.toggle_pw.setCheckable(True)
        self.toggle_pw.setFixedWidth(32)
        self.toggle_pw.clicked.connect(self.toggle_password_visibility)

        pw_layout.addWidget(self.password_input)
        pw_layout.addWidget(self.toggle_pw)
        layout.addLayout(pw_layout)

        self.remember_me = QCheckBox("Ingat saya")  
        self.remember_me.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        layout.addWidget(self.remember_me)

        btn_login = QPushButton("Login")
        btn_login.clicked.connect(self.handle_login)
        layout.addWidget(btn_login)

        btn_signup = QPushButton("Belum punya akun? Daftar di sini")
        btn_signup.setStyleSheet("color: #3498db; background: none; border: none; font-weight: bold;")
        btn_signup.clicked.connect(self.open_signup)
        layout.addWidget(btn_signup)

        self.setLayout(layout)
        self.setStyleSheet("background-color: white;")

    def toggle_password_visibility(self):
        if self.toggle_pw.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_pw.setIcon(QIcon("Res/eye_open.png"))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_pw.setIcon(QIcon("Res/eye_closed.png"))

    def check_remembered_user(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM login_state WHERE remember=1 LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            self.open_dashboard(row[0])
            self.close()

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row and row[0] == password:
            if self.remember_me.isChecked():
                with open(LOGIN_STATE_FILE, "w") as f:
                    json.dump({"username": username, "remember": True}, f)
            self.open_dashboard(username)
        else:
            QMessageBox.warning(self, "Login Gagal", "Username atau password salah!")
            
    def open_dashboard(self, username):
        self.dashboard = DashboardWindow(username)
        self.dashboard.show()
        self.close()

    def open_signup(self):
        self.signup = SignupWindow(parent=self)
        self.hide()
        self.signup.show()

    def set_username(self, username):
        self.username_input.setText(username)

