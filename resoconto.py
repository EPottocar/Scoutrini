import json
import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

def get_menu_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "menu.json")

class ResocontoScreen(QWidget):
    def __init__(self, back_callback=None):
        super().__init__()
        self.setWindowTitle("Scoutini - Resoconto")
        self.setGeometry(120, 120, 900, 700)
        self.setStyleSheet("background-color: #fdf6e3;")
        self.back_callback = back_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Top navigation bar con freccia indietro
        if self.back_callback:
            top_bar = QHBoxLayout()
            back_button = QPushButton("  ←  ")
            back_button.setFont(QFont("Arial", 20))
            back_button.setStyleSheet("""
                QPushButton {
                    background-color: #fff;
                    color: #222;
                    border: 2px solid #b58900;
                    font-size: 25px;
                    border-radius: 12px;
                    padding: 8px;
            }
                QPushButton:hover {
                    background-color: #fdf6e3;
                    color: #b58900;
                    border: 2px solid #b58900;
            }
            """)
            back_button.clicked.connect(self.go_back)
            top_bar.addWidget(back_button, alignment=Qt.AlignLeft)
            top_bar.addStretch()
            layout.addLayout(top_bar)

        # Titolo
        title = QLabel("Resoconto Vendite")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #b58900; margin-bottom: 20px;")
        layout.addWidget(title)

        # Scroll area per i prodotti
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(10)

        self.incasso_totale = 0
        self.labels = []

        menu = self.carica_menu()
        for categoria in menu:
            cat_label = QLabel(f"{categoria.capitalize()}")
            cat_label.setFont(QFont("Arial", 16, QFont.Bold))
            cat_label.setStyleSheet("color: #b58900; margin-top: 10px;")
            scroll_layout.addWidget(cat_label)

            for item in menu[categoria]:
                nome = item.get("nome", "")
                prezzo = item.get("prezzo", 0)
                quantita = item.get("quantita", 0)
                incasso = prezzo * quantita
                self.incasso_totale += incasso

                row = QHBoxLayout()
                row.setSpacing(20)
                nome_lbl = QLabel(f"{nome}")
                nome_lbl.setFont(QFont("Arial", 14))
                nome_lbl.setMinimumWidth(200)
                quantita_lbl = QLabel(f"{quantita} venduti")
                quantita_lbl.setFont(QFont("Arial", 14))
                incasso_lbl = QLabel(f"{nome}: €{prezzo:.2f} x {quantita} = <b>€{incasso:.2f}</b>")
                incasso_lbl.setFont(QFont("Arial", 14))
                incasso_lbl.setStyleSheet("color: #859900;")
                row.addWidget(nome_lbl)
                row.addWidget(quantita_lbl)
                row.addWidget(incasso_lbl)
                row.addStretch()
                frame = QFrame()
                frame.setLayout(row)
                scroll_layout.addWidget(frame)
                self.labels.append((quantita_lbl, incasso_lbl, item))

        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Incasso totale
        self.totale_label = QLabel(f"Incasso totale: <b>€{self.incasso_totale:.2f}</b>")
        self.totale_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.totale_label.setAlignment(Qt.AlignCenter)
        self.totale_label.setStyleSheet("color: #268bd2; margin-top: 10px;")
        layout.addWidget(self.totale_label)

        # Bottone resetta
        btn_reset = QPushButton("Resetta Resoconto")
        btn_reset.setFont(QFont("Arial", 18))
        btn_reset.setStyleSheet("""
            QPushButton {
                background-color: #fff;
                color: #dc322f;
                border: 2px solid #dc322f;
                border-radius: 20px;
                padding: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #fdf6e3;
                color: #fff;
                background-color: #dc322f;
            }
        """)
        btn_reset.clicked.connect(self.resetta_resoconto)
        layout.addWidget(btn_reset)

        

        self.setLayout(layout)

    def carica_menu(self):
        with open(get_menu_path(), "r", encoding="utf-8") as f:
            return json.load(f)

    def salva_menu(self, menu):
        with open(get_menu_path(), "w", encoding="utf-8") as f:
            json.dump(menu, f, ensure_ascii=False, indent=4)

    def resetta_resoconto(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Conferma")
        msg.setText("Sei sicuro di voler azzerare tutte le quantità?")
        msg.setIcon(QMessageBox.Question)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #fdf6e3;
            }
            QLabel {
                color: #222;
                font-size: 16px;
            }
            QPushButton {
                background-color: #fff;
                color: #b58900;
                border: 2px solid #b58900;
                border-radius: 10px;
                padding: 6px 18px;
                min-width: 80px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #b58900;
                color: #fff;
            }
        """)
        yes_button = msg.addButton("Sì", QMessageBox.YesRole)
        no_button = msg.addButton("No", QMessageBox.NoRole)
        msg.setIcon(QMessageBox.Question)
        msg.exec_()
        if msg.clickedButton() == yes_button:
            menu = self.carica_menu()
            for categoria in menu:
                for item in menu[categoria]:
                    item["quantita"] = 0
            self.salva_menu(menu)
            # Aggiorna la schermata
            for quantita_lbl, incasso_lbl, item in self.labels:
                quantita_lbl.setText("0 venduti")
                incasso_lbl.setText(f"€{item['prezzo']:.2f} x 0 = <b>€0.00</b>")
            self.totale_label.setText("Incasso totale: <b>€0.00</b>")

    def go_back(self):
        self.hide()
        if self.back_callback:
            self.back_callback()

# Per test rapido:
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    w = ResocontoScreen()
    w.show()
    sys.exit(app.exec_())