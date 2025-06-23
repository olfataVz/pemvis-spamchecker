import sys
import json
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon, QGuiApplication
from Main.login import LoginWindow
from Main.dashboard import DashboardWindow
from Database.database import init_db

LOGIN_STATE_FILE = "login_state.json"

if __name__ == "__main__":
    init_db()
    
    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")
    app.setWindowIcon(QIcon("Res/mail.png"))

    # Cek apakah ada user yang remembered
    if os.path.exists(LOGIN_STATE_FILE):
        with open(LOGIN_STATE_FILE, "r") as f:
            data = json.load(f)
            if data.get("remember") and data.get("username"):
                window = DashboardWindow(data["username"])
            else:
                window = LoginWindow()
    else:
        window = LoginWindow()

    window.show()
    sys.exit(app.exec())
