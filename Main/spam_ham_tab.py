from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QGroupBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class SpamHamTab(QWidget):
    def __init__(self, emails):
        super().__init__()
        self.emails = emails
        self.layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Klasifikasi Email: Undefined / Spam / Ham")
        title_label.setFont(QFont("Arial", 12))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)

        # Group Boxes for each category
        self.undefined_box = self.create_email_box("Undefined")
        self.spam_box = self.create_email_box("Spam")
        self.ham_box = self.create_email_box("Ham")

        self.layout.addWidget(self.undefined_box)
        self.layout.addWidget(self.spam_box)
        self.layout.addWidget(self.ham_box)
        self.setLayout(self.layout)

        self.refresh_lists()

    def create_email_box(self, title):
        box = QGroupBox(title)
        box.setFont(QFont("Arial", 10, weight=QFont.Weight.Bold))
        box_layout = QVBoxLayout()
        email_list = QListWidget()
        email_list.setStyleSheet("background-color: #f7fefc;")
        box_layout.addWidget(email_list)
        box.setLayout(box_layout)
        setattr(self, f"{title.lower()}_list", email_list)
        return box

    def refresh_lists(self):
        self.undefined_list.clear()
        self.spam_list.clear()
        self.ham_list.clear()

        for idx, email in enumerate(self.emails):
            item_text = f"{idx+1}. {email['title']}"
            item = QListWidgetItem(item_text)

            if email.get("category") == "Spam":
                self.spam_list.addItem(item)
            elif email.get("category") == "Ham":
                self.ham_list.addItem(item)
            else:
                self.undefined_list.addItem(item)
