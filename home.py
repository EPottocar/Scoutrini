from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(799, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.CiboButton = QtWidgets.QPushButton(self.centralwidget)
        self.CiboButton.setGeometry(QtCore.QRect(70, 100, 241, 101))
        self.CiboButton.setObjectName("CiboButton")
        self.BevandeButton = QtWidgets.QPushButton(self.centralwidget)
        self.BevandeButton.setGeometry(QtCore.QRect(70, 220, 241, 101))
        self.BevandeButton.setObjectName("BevandeButton")
        self.AvvioSessioneButton = QtWidgets.QPushButton(self.centralwidget)
        self.AvvioSessioneButton.setGeometry(QtCore.QRect(380, 100, 241, 221))
        self.AvvioSessioneButton.setCheckable(False)
        self.AvvioSessioneButton.setObjectName("AvvioSessioneButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 799, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.CiboButton.setText(_translate("MainWindow", "Modifiche Cibo"))
        self.BevandeButton.setText(_translate("MainWindow", "Modifiche Bevande"))
        self.AvvioSessioneButton.setText(_translate("MainWindow", "Avvio Sessione"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

