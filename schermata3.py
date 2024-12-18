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

class ConfirmDialog(QDialog):
    def __init__(self, item_name, item_price, item_descript):
        super().__init__()
        self.setWindowTitle("Conferma")
        self.setGeometry(300, 200, 400, 300)

        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Item details
        details_layout = QHBoxLayout()
        self.item_label = QLabel(f"{item_name}")
        self.item_label.setFont(QFont("Arial", 14, QFont.Bold))
        details_layout.addWidget(self.item_label)

        self.price_label = QLabel(f"{item_price}")
        self.price_label.setFont(QFont("Arial", 14))
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
        notes_label.setFont(QFont("Arial", 12))
        layout.addWidget(notes_label)

        self.notes_field = QTextEdit()
        layout.addWidget(self.notes_field)

        # Quantity section
        quantity_layout = QHBoxLayout()
        quantity_label = QLabel("Quantità:")
        quantity_label.setFont(QFont("Arial", 12))
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

        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Notes section
        notes_label = QLabel("Inserisci Nome Ordine:")
        notes_label.setFont(QFont("Arial", 12))
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

class RestaurantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Order and Receipt App")
        self.setGeometry(100, 100, 900, 600)

        self.menu_items = []
        self.beverage_items = []

        self.load_menu_data()
        self.initUI()

    def load_menu_data(self):
        try:
            with open("menu.json", "r") as file:
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
        menu_label.setFont(QFont("Arial", 16, QFont.Bold))
        menu_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(menu_label)

        self.menu_table = QTableWidget(5, 2)
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
        beverages_label.setFont(QFont("Arial", 16, QFont.Bold))
        beverages_label.setAlignment(Qt.AlignCenter)
        beverages_layout.addWidget(beverages_label)

        self.beverages_table = QTableWidget(5, 2)
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
        order_label.setFont(QFont("Arial", 16, QFont.Bold))
        order_label.setAlignment(Qt.AlignCenter)
        order_layout.addWidget(order_label)

        # Total display
        total_layout = QHBoxLayout()
        total_label = QLabel("Totale:")
        total_label.setFont(QFont("Arial", 14))
        self.total_display = QLineEdit("€0")
        self.total_display.setFont(QFont("Arial", 14))
        self.total_display.setReadOnly(True)
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_display)
        order_layout.addLayout(total_layout)

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

        self.update_total()

    def remove_from_order(self):
        selected_row = self.order_table.currentRow()
        if selected_row != -1:
            self.order_table.removeRow(selected_row)
            self.update_total()

    def print_receipt(self):
        self.show_insert_name()

        VENDOR_ID = 0x04b8  # Modifica con il tuo idVendor
        PRODUCT_ID = 0x0851  # Modifica con il tuo idProduct

        try:
            printer = Usb(VENDOR_ID, PRODUCT_ID)

            printer.set(align='center', bold=True, font='a', width=2, height=2)
            printer.text(f"{Customer_Name}\n")
            printer.text("--------------------------\n")

            printer.set(align='left', bold=False, font='b', width=1, height=1)
            total = 0.0
            for row in range(self.order_table.rowCount()):
                item = self.order_table.item(row, 0).text()
                price = self.order_table.item(row, 1).text().replace("€", "")
                total += float(price)
                printer.text(f"{item}\t\t{price} EUR\n")

            printer.text("--------------------------\n")
            printer.set(align='right', bold=True)
            printer.text(f"Totale: {total:.2f} EUR\n")

            printer.text("--------------------------\n")
            printer.set(align='center', bold=False)
            printer.text("Grazie per la visita!\n")

            printer.cut()

        except Exception as e:
            print(f"Errore durante la stampa: {e}")

        print("Receipt printed.")  # Placeholder

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RestaurantApp()
    window.show()
    sys.exit(app.exec_())