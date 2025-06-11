import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMainWindow
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from menu_edit import MenuEdit
from schermata_ordine import SchermataOrdine

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scoutini - Home")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("background-color: #fdf6e3;")  # beige chiaro

        self.menu_edit_window = None
        self.ordine_window = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Titolo
        title = QLabel("Benvenuto nel Gestionale Scoutrini")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #b58900; margin-bottom: 20px;")

        # Pulsante 1 - Modifica Menu
        btn_modifica_menu = QPushButton("Modifica Menu")
        btn_modifica_menu.setFont(QFont("Arial", 20))
        btn_modifica_menu.setStyleSheet(self.button_style())
        btn_modifica_menu.clicked.connect(self.go_to_modifica_menu)

        # Pulsante 2 - Crea Scontrino
        btn_crea_scontrino = QPushButton("Crea Scontrino")
        btn_crea_scontrino.setFont(QFont("Arial", 20))
        btn_crea_scontrino.setStyleSheet(self.button_style())
        btn_crea_scontrino.clicked.connect(self.go_to_crea_scontrino)

        layout.addWidget(title)
        layout.addWidget(btn_modifica_menu)
        layout.addWidget(btn_crea_scontrino)
        layout.setSpacing(20)

        self.setLayout(layout)

    def button_style(self):
        return """
        QPushButton {
            background-color: #fff;
            color: #222;
            border: 2px solid #b58900;
            border-radius: 20px;
            padding: 10px;
            font-size: 20px;
        }
        QPushButton:hover {
            background-color: #fdf6e3;
            color: #b58900;
            border: 2px solid #b58900;
        }
        """

    def show_home(self):
        self.show()
        if self.menu_edit_window:
            self.menu_edit_window.hide()
        if self.ordine_window:
            self.ordine_window.hide()

    def go_to_modifica_menu(self):
        if not self.menu_edit_window:
            self.menu_edit_window = MenuEdit(back_callback=self.show_home)
        self.menu_edit_window.show()
        self.hide()

    def go_to_crea_scontrino(self):
        if not self.ordine_window:
            self.ordine_window = SchermataOrdine(back_callback=self.show_home)
        self.ordine_window.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomeScreen()
    window.show()
    sys.exit(app.exec_())