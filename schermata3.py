import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame, QLineEdit
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class RestaurantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Order and Receipt App")
        self.setGeometry(100, 100, 900, 600)

        self.initUI()

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

        menu_items = [
            ("Margherita Pizza", "$10"),
            ("Pasta Carbonara", "$12"),
            ("Caesar Salad", "$8"),
            ("Grilled Salmon", "$15"),
            ("Tiramisu", "$6"),
        ]

        for row, (item, price) in enumerate(menu_items):
            self.menu_table.setItem(row, 0, QTableWidgetItem(item))
            self.menu_table.setItem(row, 1, QTableWidgetItem(price))

        menu_layout.addWidget(self.menu_table)

        add_menu_item_btn = QPushButton("Aggiungi Cibo")
        add_menu_item_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        menu_layout.addWidget(add_menu_item_btn)

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

        beverage_items = [
            ("Coca Cola", "$3"),
            ("Orange Juice", "$4"),
            ("Water", "$2"),
            ("Red Wine", "$5"),
            ("Coffee", "$3"),
        ]

        for row, (item, price) in enumerate(beverage_items):
            self.beverages_table.setItem(row, 0, QTableWidgetItem(item))
            self.beverages_table.setItem(row, 1, QTableWidgetItem(price))

        beverages_layout.addWidget(self.beverages_table)

        add_beverage_btn = QPushButton("Aggiungi Bevanda")
        add_beverage_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        beverages_layout.addWidget(add_beverage_btn)

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
        self.total_display = QLineEdit("$0")
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
        add_menu_item_btn.clicked.connect(self.add_menu_to_order)
        add_beverage_btn.clicked.connect(self.add_beverage_to_order)
        remove_item_btn.clicked.connect(self.remove_from_order)
        print_receipt_btn.clicked.connect(self.print_receipt)
        back_button.clicked.connect(self.go_back)

    def add_menu_to_order(self):
        selected_row = self.menu_table.currentRow()
        if selected_row != -1:
            item = self.menu_table.item(selected_row, 0).text()
            price = self.menu_table.item(selected_row, 1).text()

            row_count = self.order_table.rowCount()
            self.order_table.insertRow(row_count)
            self.order_table.setItem(row_count, 0, QTableWidgetItem(item))
            self.order_table.setItem(row_count, 1, QTableWidgetItem(price))

            self.update_total()

    def add_beverage_to_order(self):
        selected_row = self.beverages_table.currentRow()
        if selected_row != -1:
            item = self.beverages_table.item(selected_row, 0).text()
            price = self.beverages_table.item(selected_row, 1).text()

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
        print("Receipt printed.")  # Placeholder functionality

    def go_back(self):
        print("Go back to the previous screen.")  # Placeholder functionality

    def update_total(self):
        total = 0
        for row in range(self.order_table.rowCount()):
            price_item = self.order_table.item(row, 1)
            if price_item:
                price = price_item.text().replace("$", "")
                total += float(price)
        self.total_display.setText(f"${total:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RestaurantApp()
    window.show()
    sys.exit(app.exec_())