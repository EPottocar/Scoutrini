import os
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLineEdit, QTextEdit, QPushButton, QComboBox, QLabel, QFormLayout, QMessageBox, QListWidget, QHBoxLayout
)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt

def get_menu_path():
    if getattr(sys, 'frozen', False):
        # Se eseguibile PyInstaller
        base_path = os.path.dirname(sys.executable)
    else:
        # Da script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "menu.json")

class MenuEdit(QMainWindow):
    def __init__(self, back_callback=None):
        super().__init__()
        self.setWindowTitle("Menu")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #fdf6e3;
                color: #222;
            }
            QLabel {
                color: #222;
                font-size: 18px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #fdf6e3;
                color: #222;
                border: 2px solid #b58900;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #fff;
                color: #222;
                border: 2px solid #b58900;
                border-radius: 12px;
                padding: 8px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #fdf6e3;
                color: #b58900;
                border: 2px solid #b58900;
            }
            QListWidget {
                background-color: #fdf6e3;
                color: #222;
                border: 2px solid #b58900;
                font-size: 16px;
            }
        """)

        self.menu = self.load_menu()
        self.back_callback = back_callback

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Top navigation bar
        top_bar = QHBoxLayout()
        layout.addLayout(top_bar)

        back_button = QPushButton("  ←  ")
        back_button.setStyleSheet("font-size: 25px; padding: 10px;")
        back_button.clicked.connect(self.handle_back)
        top_bar.addWidget(back_button, alignment=Qt.AlignLeft)

        # Dropdown per selezionare la categoria
        self.category_selector = QComboBox()
        self.category_selector.addItems(["Cibo", "Bevanda"])
        self.category_selector.setMinimumWidth(200)
        self.category_selector.view().setMinimumWidth(200)
        self.category_selector.currentTextChanged.connect(self.toggle_fields)

        # Campi di input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome del prodotto")

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Descrizione del cibo")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Prezzo del prodotto")
        self.price_input.setValidator(QDoubleValidator(0.99, 999.99, 2))

        self.description_input.setSizePolicy(self.sizePolicy().Expanding, self.sizePolicy().Preferred)
        self.price_input.setSizePolicy(self.sizePolicy().Expanding, self.sizePolicy().Preferred)

        # Pulsante per aggiungere l'elemento
        self.add_button = QPushButton("Aggiungi al menu")
        self.add_button.clicked.connect(self.add_item_to_menu)

        # Layout del form
        form_layout = QFormLayout()
        form_layout.addRow("Categoria:", self.category_selector)
        form_layout.addRow("Nome:", self.name_input)
        form_layout.addRow("Descrizione:", self.description_input)
        form_layout.addRow("Prezzo:", self.price_input)

        # Lista riepilogo
        self.menu_list = QListWidget()
        self.update_menu_list()

        # Pulsante per rimuovere un elemento
        self.remove_button = QPushButton("Rimuovi selezionato")
        self.remove_button.clicked.connect(self.remove_selected_item)

        # Layout principale
        layout.addLayout(form_layout)
        layout.addWidget(self.add_button)
        layout.addWidget(QLabel("Riepilogo menu:"))
        layout.addWidget(self.menu_list)
        layout.addWidget(self.remove_button)

        # Widget principale
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.toggle_fields()  # Configura i campi inizialmente

    def handle_back(self):
        if self.back_callback:
            self.hide()
            self.back_callback()

    def toggle_fields(self):
        """Abilita/disabilita i campi in base alla categoria selezionata."""
        if self.category_selector.currentText() == "Cibo":
            self.description_input.setEnabled(True)
        else:
            self.description_input.setEnabled(False)
            self.description_input.clear()

    def add_item_to_menu(self):
        """Aggiunge un elemento al menu e lo salva su file."""
        category = self.category_selector.currentText()
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        try:
            price = float(self.price_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Errore", "Il prezzo deve essere un numero valido.")
            return

        if not name:
            QMessageBox.warning(self, "Errore", "Il nome del prodotto non può essere vuoto.")
            return

        item = {"nome": name, "prezzo": price, "quantita": 0}
        if category == "Cibo":
            item["descrizione"] = description

        self.menu[category.lower()].append(item)
        self.save_menu()
        QMessageBox.information(self, "Successo", f"{category} aggiunto al menu.")

        # Reset campi
        self.name_input.clear()
        self.description_input.clear()
        self.price_input.clear()

        self.update_menu_list()

    def remove_selected_item(self):
        """Rimuove l'elemento selezionato dalla lista e dal file JSON."""
        selected_item = self.menu_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Errore", "Seleziona un elemento da rimuovere.")
            return

        item_text = selected_item.text()
        category, item_name = item_text.split(" - ", 1)
        category_key = "cibo" if category == "Cibo" else "bevanda"

        self.menu[category_key] = [item for item in self.menu[category_key] if item["nome"] != item_name]
        self.save_menu()

        QMessageBox.information(self, "Successo", "Elemento rimosso dal menu.")
        self.update_menu_list()

    def update_menu_list(self):
        """Aggiorna la lista riepilogativa del menu."""
        self.menu_list.clear()
        for category, items in self.menu.items():
            category_label = "Cibo" if category == "cibo" else "Bevanda"
            for item in items:
                item_text = f"{category_label} - {item['nome']}"
                self.menu_list.addItem(item_text)

    def load_menu(self):
        """Carica il menu da un file JSON."""
        menu_path = get_menu_path()
        try:
            with open(menu_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"cibo": [], "bevanda": []}

    def save_menu(self):
        """Salva il menu in un file JSON."""
        menu_path = get_menu_path()
        with open(menu_path, "w") as file:
            json.dump(self.menu, file, indent=4)

