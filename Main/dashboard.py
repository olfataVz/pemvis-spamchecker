from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QListWidget, QHBoxLayout,
    QListWidgetItem, QPushButton, QStatusBar, QTabWidget,
    QRadioButton, QButtonGroup, QLineEdit, QFrame, QTextEdit, QMessageBox,
    QMenuBar, QMenu, QFileDialog
)
from PyQt6.QtGui import QFont, QIcon, QAction
from PyQt6.QtCore import Qt

import datetime
import csv
import sqlite3

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from Database.database import DB_NAME
from spam_checker import predict_spam_probability
from Main.spam_ham_tab import SpamHamTab
from Main.classifier_tab import ClassifierTab


emails = [
    {"from": "promo@tokoonline.com", "title": "Diskon besar-besaran!", "body": "Dapatkan diskon hingga 70% hanya hari ini.", "date": "2025-06-21", "category": "Undefined", "probability": 0.0},
    {"from": "noreply@bank.com", "title": "Konfirmasi transfer anda", "body": "Silakan konfirmasi transfer terakhir anda untuk keamanan.", "date": "2025-06-20", "category": "Undefined", "probability": 0.0},
    {"from": "admin@webhosting.com", "title": "Gratis domain setahun", "body": "Dapatkan domain gratis selama 1 tahun untuk setiap hosting.", "date": "2025-06-19", "category": "Undefined", "probability": 0.0},
    {"from": "iklan@travelmurah.com", "title": "Promo liburan!", "body": "Liburan hemat ke Bali dengan harga miring.", "date": "2025-06-18", "category": "Undefined", "probability": 0.0},
    {"from": "info@pinjamanku.id", "title": "Pinjaman cepat cair", "body": "Ajukan pinjaman tanpa jaminan sekarang juga.", "date": "2025-06-17", "category": "Undefined", "probability": 0.0},
    {"from": "rekan@kampus.ac.id", "title": "Tugas akhir revisi", "body": "Silakan periksa hasil revisi tugas akhirmu minggu ini.", "date": "2025-06-16", "category": "Undefined", "probability": 0.0},
    {"from": "teman@whatsapp.com", "title": "Makan malam bareng", "body": "Yuk makan malam di tempat biasa jam 7.", "date": "2025-06-15", "category": "Undefined", "probability": 0.0},
    {"from": "dosen@univ.ac.id", "title": "Pengumuman seminar", "body": "Seminar nasional akan dilaksanakan Jumat depan.", "date": "2025-06-14", "category": "Undefined", "probability": 0.0},
    {"from": "organisasi@himakom.org", "title": "Rapat mingguan", "body": "Rapat rutin hari Kamis pukul 8 malam.", "date": "2025-06-13", "category": "Undefined", "probability": 0.0},
    {"from": "notifikasi@e-learning.id", "title": "Nilai tugas terbaru", "body": "Tugas ke-3 sudah dinilai, silakan cek portal.", "date": "2025-06-12", "category": "Undefined", "probability": 0.0},
]

class DashboardWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowIcon(QIcon("Res/mail.png"))
        self.username = username
        self.setWindowTitle("Spam Checker")
        self.setGeometry(300, 100, 800, 500)
        self.sort_by = "title"
        self.ascending = True
        self.emails = emails  
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        self.menu_bar = QMenuBar()
        file_menu = QMenu("File", self)
        export_pdf_action = QAction("Export as PDF", self)
        export_csv_action = QAction("Export as CSV", self)
        export_pdf_action.triggered.connect(self.export_pdf)
        export_csv_action.triggered.connect(self.export_csv)
        file_menu.addAction(export_pdf_action)
        file_menu.addAction(export_csv_action)

        help_menu = QMenu("Help", self)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        self.menu_bar.addMenu(file_menu)
        self.menu_bar.addMenu(help_menu)

        main_layout.setMenuBar(self.menu_bar)

        top_label = QLabel(f"Selamat datang, {self.username} !")
        top_label.setFont(QFont("Arial", 14))
        top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(top_label)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 5px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab {
                padding: 8px;
                margin-right: 2px;
            }
        """)

        self.list_tab = QWidget()
        self.spam_ham_tab_widget = SpamHamTab(self.emails)  
        self.clf_tab = ClassifierTab()

        self.tabs.addTab(self.list_tab, "List Email")
        self.tabs.addTab(self.spam_ham_tab_widget, "Spam/Ham Email")  
        self.tabs.addTab(self.clf_tab, "Classifier")

        self.init_list_tab()

        main_layout.addWidget(self.tabs)

        self.status = QStatusBar()
        self.status.showMessage("F1D022057 - Lalu Olfata Vedora Zurji")
        main_layout.addWidget(self.status)

        self.setLayout(main_layout)
        self.apply_styles()

    def init_list_tab(self):
        self.list_layout = QHBoxLayout()
        self.email_list_layout = QVBoxLayout()

        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sort By")
        sort_label.setFont(QFont("Arial", 10))
        sort_layout.addWidget(sort_label)

        self.radio_title = QRadioButton("A-Z")
        self.radio_date = QRadioButton("Date")
        self.radio_title.setChecked(True)
        self.sort_group = QButtonGroup()
        self.sort_group.addButton(self.radio_title)
        self.sort_group.addButton(self.radio_date)
        self.sort_group.buttonClicked.connect(self.sort_emails)

        sort_layout.addSpacing(3)
        sort_layout.addWidget(self.radio_title)
        sort_layout.addSpacing(6)
        sort_layout.addWidget(self.radio_date)

        search_container = QFrame()
        search_container.setStyleSheet("QFrame { border: 1px solid #ccc; border-radius: 4px; }")
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(5, 0, 5, 0)
        search_container.setLayout(search_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("cari email..")
        self.search_input.setFont(QFont("Arial", 10))
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self.filter_emails)

        self.search_icon = QLabel()
        self.search_icon.setPixmap(QIcon("Res/search.png").pixmap(16, 16))
        self.search_icon.setStyleSheet("padding: 3px;")
        self.search_icon.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_icon)
        search_container.setFixedWidth(220)
        sort_layout.addSpacing(20)
        sort_layout.addWidget(search_container)

        sort_layout.addStretch()

        self.sort_icon = QPushButton()
        self.sort_icon.setIcon(QIcon("Res/sort-ascending.png"))
        self.sort_icon.setFixedSize(32, 24)
        self.sort_icon.setCheckable(True)
        self.sort_icon.setChecked(True)
        self.sort_icon.clicked.connect(self.toggle_sort_order)
        sort_layout.addWidget(self.sort_icon)

        self.sort_label_status = QLabel("Ascending")
        self.sort_label_status.setFont(QFont("Arial", 10))
        sort_layout.addWidget(self.sort_label_status)

        self.email_list_layout.addLayout(sort_layout)

        self.email_list = QListWidget()
        self.email_list.itemClicked.connect(self.show_email_detail)
        self.email_list_layout.addWidget(self.email_list)

        self.email_detail = QTextEdit()
        self.email_detail.setReadOnly(True)
        self.email_detail.hide()

        self.btn_close_detail = QPushButton("Tutup")
        self.btn_close_detail.clicked.connect(self.hide_email_detail)
        self.btn_close_detail.hide()

        self.btn_check_spam = QPushButton("Check Spam")
        self.btn_check_spam.clicked.connect(self.check_spam_email)
        self.btn_check_spam.hide()  

        self.email_detail_layout = QVBoxLayout()
        self.email_detail_layout.addWidget(self.email_detail)
        self.email_detail_layout.addWidget(self.btn_close_detail)
        self.email_detail_layout.addWidget(self.btn_check_spam)

        self.list_layout.addLayout(self.email_list_layout, 3)
        self.list_layout.addLayout(self.email_detail_layout, 2)

        sidebar_layout = QHBoxLayout()
        btn_export = QPushButton("Export Data")
        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.logout)
        sidebar_layout.addWidget(btn_export)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(btn_logout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.list_layout)
        main_layout.addLayout(sidebar_layout)

        self.list_tab.setLayout(main_layout)
        self.load_emails(self.emails)

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "emails.csv", "CSV Files (*.csv)")
        if path:
            with open(path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["From", "Date", "Title", "Body", "Category", "Probability"])
                for email in self.emails:
                    writer.writerow([
                        email["from"], email["date"], email["title"], email["body"], email["category"], f"{email.get('probability', 0.0)*100:.2f}%"
                    ])

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "emails.pdf", "PDF Files (*.pdf)")
        if path:
            c = canvas.Canvas(path, pagesize=letter)
            width, height = letter
            y = height - 40
            c.setFont("Helvetica-Bold", 10)
            c.drawString(40, y, "From | Date | Title | Category | Probability")
            c.setFont("Helvetica", 9)
            y -= 20
            for email in self.emails:
                line = f"{email['from']} | {email['date']} | {email['title'][:30]} | {email['category']} | {email.get('probability', 0.0)*100:.2f}%"
                c.drawString(40, y, line)
                y -= 15
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 9)
                    y = height - 40
            c.save()

    def show_about(self):
        QMessageBox.about(self, "Tentang Aplikasi", (
            "<b>Spam Checker</b> adalah aplikasi klasifikasi email berbasis machine learning yang membantu menyaring email spam secara otomatis."
            " Aplikasi ini mengelompokkan email menjadi Spam, Ham (bukan spam), atau Undefined sebelum diperiksa."
            "<br><br>Tujuan utama dari aplikasi ini adalah membantu pengguna mengurangi paparan email tidak penting"
            " serta memberikan kemampuan ekspor data hasil klasifikasi ke PDF atau CSV. Pengguna dapat menyeleksi dan memeriksa email dengan mudah melalui tab List Email dan Spam/Ham."
        ))

    def show_email_detail(self, item):
        index = self.email_list.currentRow()
        email = self.emails[index]
        detail = f"Dari: {email['from']}\nTanggal: {email['date']}\nJudul: {email['title']}\n\n{email['body']}"
        self.email_detail.setText(detail)
        self.email_detail.show()
        self.btn_close_detail.show()

    def hide_email_detail(self):
        self.email_detail.hide()
        self.btn_close_detail.hide()
        self.btn_check_spam.hide()  

    def show_email_detail(self, item):
        index = self.email_list.currentRow()
        email = self.emails[index]
        self.selected_index = index  # Simpan index email yang sedang dipilih

        detail = f"Dari: {email['from']}\nTanggal: {email['date']}\nJudul: {email['title']}\n\n{email['body']}"
        self.email_detail.setText(detail)
        self.email_detail.show()
        self.btn_close_detail.show()
        self.btn_check_spam.show()

    def toggle_sort_order(self):
        self.ascending = not self.ascending
        icon = QIcon("Res/sort-ascending.png" if self.ascending else "Res/sort-descending.png")
        self.sort_icon.setIcon(icon)
        self.sort_label_status.setText("Ascending" if self.ascending else "Descending")
        self.sort_emails()

    def sort_emails(self):
        self.sort_by = "title" if self.radio_title.isChecked() else "date"
        reverse = not self.ascending
        sorted_list = sorted(self.emails, key=lambda x: x[self.sort_by].lower() if self.sort_by == "title" else x[self.sort_by], reverse=reverse)
        self.load_emails(sorted_list)

    def filter_emails(self):
        query = self.search_input.text().lower()
        filtered = [e for e in self.emails if query in e['title'].lower() or query in e['from'].lower() or query in e['date']]
        sorted_list = sorted(filtered, key=lambda x: x[self.sort_by].lower() if self.sort_by == "title" else x[self.sort_by], reverse=not self.ascending)
        self.load_emails(sorted_list)

    def load_emails(self, email_list):
        self.email_list.clear()
        for email in email_list:
            item = QListWidgetItem(f"[{email['date']}] {email['title']}")
            self.email_list.addItem(item)

    def check_spam_email(self):
        index = getattr(self, "selected_index", None)
        if index is None:
            return

        email = self.emails[index]
        full_text = f"{email['title']} {email['body']}"
        prob = predict_spam_probability(full_text)
        prob_percent = round(prob * 100, 2)

        result = "Spam" if prob > 0.5 else "Ham"
        QMessageBox.information(self, "Hasil Prediksi", f"Email ini terdeteksi sebagai {result}.\nProbabilitas Spam: {prob_percent}%")

        # Update ke list lokal agar UI tetap bisa refresh
        self.emails[index]['category'] = result
        self.emails[index]['probability'] = prob

        # Simpan ke database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO emails (sender, date, title, body, category, probability)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            email['from'],
            email['date'],
            email['title'],
            email['body'],
            result,
            prob_percent
        ))
        conn.commit()
        conn.close()

        # Refresh tampilan tab Spam/Ham
        if hasattr(self, "spam_ham_tab_widget"):
            self.spam_ham_tab_widget.refresh_lists()

    def logout(self):
        import os
        if os.path.exists("login_state.json"):
            os.remove("login_state.json")
        self.close()
        from Main.login import LoginWindow
        self.login = LoginWindow()
        self.login.show()

    def apply_styles(self):
        self.setStyleSheet("""
            QListWidget {
                background-color: #f7fefc;
                font-size: 14px;
            }
            QPushButton {
                padding: 6px;
                font-size: 14px;
                background-color: #3498db;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
