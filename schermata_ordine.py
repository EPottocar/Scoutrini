import os
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame, QLineEdit, QSpinBox, QDialog, QTextEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from escpos.printer import Usb

Customer_Name = None

def get_menu_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "menu.json")

class ConfirmDialog(QDialog):
    def __init__(self, item_name, item_price, item_descript):
        super().__init__()
        self.setWindowTitle("Conferma")
        self.setGeometry(300, 200, 900, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #fdf6e3;
                color: #222;
                           
            }
            QSpinBox {
                background-color: #fdf6e3;
                color: #222;
                border: 4px solid #b58900;
                border-radius: 8px;
                font-size: 16px;
            }
            QLabel 
            {
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
        """)

        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Item details
        details_layout = QHBoxLayout()
        self.item_label = QLabel(f"{item_name}")
        self.item_label.setFont(QFont("Arial", 20, QFont.Bold))
        details_layout.addWidget(self.item_label)

        self.price_label = QLabel(f"{item_price}")
        self.price_label.setFont(QFont("Arial", 16))
        details_layout.addWidget(self.price_label)
        layout.addLayout(details_layout)

        # Description section
        description_label = QLabel("Descrizione:")
        description_label.setFont(QFont("Arial", 12))
        layout.addWidget(description_label)

        self.description_field = QTextEdit()
        self.description_field.setReadOnly(True)
        self.description_field.setText(f"{item_descript}.")  # Placeholder
        layout.addWidget(self.description_field)

        # Notes section
        notes_label = QLabel("Note:")
        notes_label.setFont(QFont("Arial", 16))
        layout.addWidget(notes_label)

        self.notes_field = QTextEdit()
        layout.addWidget(self.notes_field)

        # Quantity section
        quantity_layout = QHBoxLayout()
        quantity_label = QLabel("Quantità:")
        quantity_label.setFont(QFont("Arial", 16))
        quantity_layout.addWidget(quantity_label)

        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setMinimum(1)
        self.quantity_spinbox.setValue(1)
        quantity_layout.addWidget(self.quantity_spinbox)
        layout.addLayout(quantity_layout)

        # Buttons
        buttons_layout = QHBoxLayout()

        self.confirm_button = QPushButton("Conferma")
        self.confirm_button.setStyleSheet("background-color: green; color: white; font-size: 14px; padding: 10px;")
        buttons_layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Cancella")
        self.cancel_button.setStyleSheet("background-color: red; color: white; font-size: 14px; padding: 10px;")
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        # Connect buttons
        self.confirm_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_order_details(self):
        return {
            "notes": self.notes_field.toPlainText(),
            "quantity": self.quantity_spinbox.value()
        }

class Insert_Name_Order(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inserisci Nome Ordine")
        self.setGeometry(300, 200, 400, 300)
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
        """)

        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Notes section
        notes_label = QLabel("Inserisci Nome Ordine:")
        notes_label.setFont(QFont("Arial", 16))
        layout.addWidget(notes_label)

        self.notes_field = QTextEdit()
        layout.addWidget(self.notes_field)

        # Buttons
        buttons_layout = QHBoxLayout()

        self.confirm_button = QPushButton("Conferma")
        self.confirm_button.setStyleSheet("background-color: green; color: white; font-size: 14px; padding: 10px;")
        buttons_layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Cancella")
        self.cancel_button.setStyleSheet("background-color: red; color: white; font-size: 14px; padding: 10px;")
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        # Connect buttons
        self.confirm_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_name(self):
        # Method to retrieve the customer name after dialog acceptance
        return self.notes_field.toPlainText()

class SchermataOrdine(QMainWindow):
    def __init__(self, back_callback=None):
        super().__init__()
        self.setWindowTitle("Ordine")
        self.setGeometry(100, 100, 900, 600)
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
            QTableWidget {
                background-color: #fdf6e3;
                color: #222;
                font-size: 16px;
            }
        """)

        self.menu_items = []
        self.beverage_items = []
        self.back_callback = back_callback
        self.order_notes = []  # Lista parallela per le note

        self.load_menu_data()
        self.initUI()

    def aggiorna_quantita_menu(self, order_items):
        """Aggiorna le quantità in menu.json in base agli item dell'ordine."""
        menu_path = get_menu_path()
        with open(menu_path, "r", encoding="utf-8") as f:
            menu = json.load(f)
        conteggi = {}
        for item in order_items:
            nome = item["nome"]
            conteggi[nome] = conteggi.get(nome, 0) + 1
        for categoria in menu:
            for item in menu[categoria]:
                if item["nome"] in conteggi:
                    item["quantita"] = item.get("quantita", 0) + conteggi[item["nome"]]
        with open(menu_path, "w", encoding="utf-8") as f:
            json.dump(menu, f, ensure_ascii=False, indent=4)

    def load_menu_data(self):
        try:
            with open(get_menu_path(), "r") as file:
                menu_data = json.load(file)

            self.menu_items = [
                (item["nome"], f"€{item['prezzo']:.2f}", item["descrizione"])
                for item in menu_data.get("cibo", [])
            ]
            self.beverage_items = [
                (item["nome"], f"€{item['prezzo']:.2f}")
                for item in menu_data.get("bevanda", [])
            ]
        except Exception as e:
            print(f"Errore durante il caricamento di menu.json: {e}")
            self.menu_items = []
            self.beverage_items = []

    def initUI(self):
        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Top navigation bar
        top_bar = QHBoxLayout()
        main_layout.addLayout(top_bar)

        back_button = QPushButton("  ←  ")
        back_button.setStyleSheet("font-size: 25px; padding: 10px;")
        back_button.clicked.connect(self.handle_back)
        top_bar.addWidget(back_button, alignment=Qt.AlignLeft)

        # Content layout
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Menu Section
        menu_frame = QFrame()
        menu_frame.setFrameShape(QFrame.StyledPanel)
        menu_layout = QVBoxLayout()
        menu_frame.setLayout(menu_layout)

        menu_label = QLabel("Menu")
        menu_label.setFont(QFont("Arial", 18, QFont.Bold))
        menu_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(menu_label)

        self.menu_table = QTableWidget(len(self.menu_items), 2)  # <-- usa la lunghezza dei cibi
        self.menu_table.setHorizontalHeaderLabels(["Cibo", "Prezzo"])
        self.menu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.menu_table.verticalHeader().setVisible(False)
        self.menu_table.setEditTriggers(QTableWidget.NoEditTriggers)

        for row, (item, price, descript) in enumerate(self.menu_items):
            self.menu_table.setItem(row, 0, QTableWidgetItem(item))
            self.menu_table.setItem(row, 1, QTableWidgetItem(price))

        menu_layout.addWidget(self.menu_table)

        # Beverages Section
        beverages_frame = QFrame()
        beverages_frame.setFrameShape(QFrame.StyledPanel)
        beverages_layout = QVBoxLayout()
        beverages_frame.setLayout(beverages_layout)

        beverages_label = QLabel("Bevande")
        beverages_label.setFont(QFont("Arial", 18, QFont.Bold))
        beverages_label.setAlignment(Qt.AlignCenter)
        beverages_layout.addWidget(beverages_label)

        self.beverages_table = QTableWidget(len(self.beverage_items), 2)  # <-- usa la lunghezza delle bevande
        self.beverages_table.setHorizontalHeaderLabels(["Bevanda", "Prezzo"])
        self.beverages_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.beverages_table.verticalHeader().setVisible(False)
        self.beverages_table.setEditTriggers(QTableWidget.NoEditTriggers)

        for row, (item, price) in enumerate(self.beverage_items):
            self.beverages_table.setItem(row, 0, QTableWidgetItem(item))
            self.beverages_table.setItem(row, 1, QTableWidgetItem(price))

        beverages_layout.addWidget(self.beverages_table)

        # Order Section
        order_frame = QFrame()
        order_frame.setFrameShape(QFrame.StyledPanel)
        order_layout = QVBoxLayout()
        order_frame.setLayout(order_layout)

        order_label = QLabel("Ordine")
        order_label.setFont(QFont("Arial", 18, QFont.Bold))
        order_label.setAlignment(Qt.AlignCenter)
        order_layout.addWidget(order_label)

        # Total display
        total_layout = QHBoxLayout()
        total_label = QLabel("Totale:")
        total_label.setFont(QFont("Arial", 16))
        self.total_display = QLineEdit("€0")
        self.total_display.setFont(QFont("Arial", 16))
        self.total_display.setReadOnly(True)
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_display)
        order_layout.addLayout(total_layout)

        # --- INIZIO AGGIUNTA RESTO ---
        payment_layout = QHBoxLayout()
        payment_label = QLabel("Pagato:")
        payment_label.setFont(QFont("Arial", 16))
        self.paid_input = QLineEdit()
        self.paid_input.setPlaceholderText("Importo pagato")
        self.paid_input.setFixedWidth(120)
        self.paid_input.setFont(QFont("Arial", 16))
        self.change_label = QLabel("Resto: €0.00")
        self.change_label.setFont(QFont("Arial", 16))
        calc_change_btn = QPushButton("Calcola resto")
        calc_change_btn.setFont(QFont("Arial", 16))
        calc_change_btn.clicked.connect(self.calcola_resto)
        payment_layout.addWidget(payment_label)
        payment_layout.addWidget(self.paid_input)
        payment_layout.addWidget(calc_change_btn)
        payment_layout.addWidget(self.change_label)
        order_layout.addLayout(payment_layout)
        # --- FINE AGGIUNTA RESTO ---

        self.order_table = QTableWidget(0, 2)
        self.order_table.setHorizontalHeaderLabels(["Cibo", "Prezzo"])
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.order_table.verticalHeader().setVisible(False)
        self.order_table.setEditTriggers(QTableWidget.NoEditTriggers)
        order_layout.addWidget(self.order_table)

        remove_item_btn = QPushButton("Rimuovi Elemento Selezionato")
        remove_item_btn.setStyleSheet("background-color: red; color: white; font-size: 16px; padding: 10px;")
        order_layout.addWidget(remove_item_btn)

        print_receipt_btn = QPushButton("Stampa scontrini")
        print_receipt_btn.setStyleSheet("background-color: green; color: white; font-size: 16px; padding: 10px;")
        order_layout.addWidget(print_receipt_btn)

        # Add sections to content layout
        content_layout.addWidget(menu_frame, 2)
        content_layout.addWidget(beverages_frame, 2)
        content_layout.addWidget(order_frame, 2)

        # Connect buttons
        remove_item_btn.clicked.connect(self.remove_from_order)
        print_receipt_btn.clicked.connect(self.print_receipt)
        back_button.clicked.connect(self.go_back)

        # Connect table clicks
        self.menu_table.cellDoubleClicked.connect(self.show_confirm_dialog)
        self.beverages_table.cellDoubleClicked.connect(self.add_beverage_to_order)

#mi serve per ritornare la descrizione nel confirm dialog
    def get_item_description(self, item_name):
        # Controlla nella lista degli item cibo
        for nome, prezzo, descrizione in self.menu_items:
            if nome.lower() == item_name.lower():  # Usa .lower() per fare una ricerca case-insensitive
                return descrizione

    def show_confirm_dialog(self, row):
        item_name = self.menu_table.item(row, 0).text()
        item_price = self.menu_table.item(row, 1).text()
        item_descript = self.get_item_description(item_name)

        dialog = ConfirmDialog(item_name, item_price, item_descript)
        if dialog.exec_() == QDialog.Accepted:
            order_details = dialog.get_order_details()
            for _ in range(order_details['quantity']):
                row_count = self.order_table.rowCount()
                self.order_table.insertRow(row_count)
                self.order_table.setItem(row_count, 0, QTableWidgetItem(item_name))
                self.order_table.setItem(row_count, 1, QTableWidgetItem(item_price))
                self.order_notes.append(order_details['notes'])  # Salva la nota
            self.update_total()

    def show_insert_name(self):
        global Customer_Name
        dialog = Insert_Name_Order()
        if dialog.exec_() == QDialog.Accepted:
            Customer_Name = dialog.get_name()

    def add_beverage_to_order(self, row, column):
        item = self.beverages_table.item(row, 0).text()
        price = self.beverages_table.item(row, 1).text()

        row_count = self.order_table.rowCount()
        self.order_table.insertRow(row_count)
        self.order_table.setItem(row_count, 0, QTableWidgetItem(item))
        self.order_table.setItem(row_count, 1, QTableWidgetItem(price))
        self.order_notes.append("")  # Nessuna nota per le bevande

        self.update_total()

    def remove_from_order(self):
        selected_row = self.order_table.currentRow()
        if selected_row != -1:
            self.order_table.removeRow(selected_row)
            del self.order_notes[selected_row]  # Rimuovi la nota corrispondente
            self.update_total()

    def print_receipt(self):
        self.show_insert_name()

        VENDOR_ID = 0x0416 # Modifica con il tuo idVendor
        PRODUCT_ID = 0x5011  # Modifica con il tuo idProduct

        # Raccogli gli ordini
        order_items = []
        for row in range(self.order_table.rowCount()):
            item = self.order_table.item(row, 0).text()
            price = self.order_table.item(row, 1).text().replace("€", "")
            note = self.order_notes[row] if row < len(self.order_notes) else ""
            is_cibo = any(item == cibo[0] for cibo in self.menu_items)
            is_bevanda = any(item == bevanda[0] for bevanda in self.beverage_items)
            order_items.append({
                "nome": item,
                "prezzo": float(price),
                "note": note,
                "is_cibo": is_cibo,
                "is_bevanda": is_bevanda
            })

        #aggiorna le quantità nel menu
        self.aggiorna_quantita_menu(order_items)
        
        try:
            # --- Primo scontrino: Da tenere (tutto) ---
            scontrino1 = []
            scontrino1.append("Copia cliente\n")
            scontrino1.append(f"{Customer_Name}\n")
            scontrino1.append("--------------------------\n")
            total = 0.0
            for item in order_items:
                note_str = f" ({item['note']})" if item['note'] else ""
                line = f"{item['nome']}{note_str}"
                if len(line) <= 40:
                    scontrino1.append(f"{line:<35}{item['prezzo']:>8.2f} EUR\n")
                else:
                    scontrino1.append(f"{item['nome']}\n")
                    if item['note']:
                        scontrino1.append(f"{' ' * 2}{item['note']}\n")
                    scontrino1.append(f"{'':<35}{item['prezzo']:>8.2f} EUR\n")
                total += item['prezzo']
            scontrino1.append("-" * 43 + "\n")
            scontrino1.append(f"{'Totale:':<35}{total:>8.2f} EUR\n")
            scontrino1.append("-" * 43 + "\n")

            # --- Secondo scontrino: Cucina (solo cibo) ---
            scontrino2 = []
            scontrino2.append("Cucina\n")
            scontrino2.append(f"{Customer_Name}\n")
            scontrino2.append("--------------------------\n")
            total_cibo = 0.0
            for item in order_items:
                if item['is_cibo']:
                    note_str = f" ({item['note']})" if item['note'] else ""
                    line = f"{item['nome']}{note_str}"
                    if len(line) <= 35:
                        scontrino2.append(f"{line:<35}{item['prezzo']:>8.2f} EUR\n")
                    else:
                        scontrino2.append(f"{item['nome']}\n")
                        if item['note']:
                            scontrino2.append(f"{' ' * 2}{item['note']}\n")
                        scontrino2.append(f"{'':<40}{item['prezzo']:>8.2f} EUR\n")
                    total_cibo += item['prezzo']
            scontrino2.append("-" * 43 + "\n")
            scontrino2.append(f"{'Totale:':<35}{total_cibo:>8.2f} EUR\n")
            scontrino2.append("-" * 43 + "\n")

            # --- Terzo scontrino: Bar (solo bevande) ---
            scontrino3 = []
            scontrino3.append("Baar\n")
            scontrino3.append(f"{Customer_Name}\n")
            scontrino3.append("--------------------------\n")
            total_bevande = 0.0
            for item in order_items:
                if item['is_bevanda']:
                    line = item['nome']
                    scontrino3.append(f"{line:<35}{item['prezzo']:>8.2f} EUR\n")
                    total_bevande += item['prezzo']
            scontrino3.append("-" * 43 + "\n")
            scontrino3.append(f"{'Totale:':<35}{total_bevande:>8.2f} EUR\n")
            scontrino3.append("-" * 43 + "\n")
            # --- Stampa su stampante e terminale ---
            printer = Usb(VENDOR_ID, PRODUCT_ID)
            for idx, scontrino in enumerate([scontrino1, scontrino2, scontrino3]):
                # Output su terminale, separati da una riga vuota
                print("".join(scontrino))
                print("\n" + "="*35 + "\n")  # Separatore visivo
                
                # Output su stampante
                printer.set(align='center', bold=True, font='a', width=3, height=3)
                printer.text(scontrino[0])  # Titolo
                printer.set(align='center', bold=False, font='a', width=2, height=2)
                printer.text(scontrino[1])  # Nome
                printer.text(scontrino[2])  # Linea
                printer.set(align='left', bold=False, font='a', width=2, height=2)
                for line in scontrino[3:-4]:
                    printer.text(line)
                printer.text(scontrino[-4])  # Linea
                printer.set(align='right', bold=True)
                printer.text(scontrino[-3])  # Totale
                printer.text(scontrino[-2])  # Linea
                printer.set(align='center', bold=False)
                if idx == 0 and len(scontrino) > 7:
                    printer.text(scontrino[-1])  # "Grazie per la visita" solo per il primo
                printer.cut()  # Taglia la carta tra uno scontrino e l'altro
            printer.close()
    
        except Exception as e:
            print(f"Errore durante la stampa: {e}")

        # Svuota la tabella ordine e le note dopo la stampa
        self.order_table.setRowCount(0)
        self.order_notes.clear()
        self.update_total()

        print("Receipt printed.")  # Placeholder

        # Torna alla schermata home
        self.handle_back()

    def go_back(self):
        print("Go back to the previous screen.")  # Placeholder functionality

    def update_total(self):
        total = 0
        for row in range(self.order_table.rowCount()):
            price_item = self.order_table.item(row, 1)
            if price_item:
                price = price_item.text().replace("€", "")
                total += float(price)
        self.total_display.setText(f"€{total:.2f}")

    def handle_back(self):
        if self.back_callback:
            self.hide()
            self.back_callback()

    # --- INIZIO AGGIUNTA RESTO ---
    def calcola_resto(self):
        """Calcola il resto da dare al cliente."""
        totale_str = self.total_display.text().replace("€", "").replace(",", ".")
        try:
            totale = float(totale_str)
        except ValueError:
            self.change_label.setText("Resto: €0.00")
            return

        try:
            pagato = float(self.paid_input.text().replace(",", "."))
        except ValueError:
            self.change_label.setText("Resto: €0.00")
            return

        resto = pagato - totale
        if resto < 0:
            self.change_label.setText("Resto: €0.00")
        else:
            self.change_label.setText(f"Resto: €{resto:.2f}")
    # --- FINE AGGIUNTA RESTO ---

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchermataOrdine()
    window.show()
    sys.exit(app.exec_())