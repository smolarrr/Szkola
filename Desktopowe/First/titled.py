from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 150)
        self.Form = QtWidgets.QWidget(parent=MainWindow)
        self.Form.setObjectName("Form")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 531, 131))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout.setContentsMargins(50, 0, 50, 0)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnFile = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.btnFile.setObjectName("btnFile")
        self.horizontalLayout.addWidget(self.btnFile)
        self.entryName = QtWidgets.QLineEdit(parent=self.horizontalLayoutWidget)
        self.entryName.setObjectName("entryName")
        self.horizontalLayout.addWidget(self.entryName)
        self.btnSet = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.btnSet.setObjectName("btnSet")
        self.horizontalLayout.addWidget(self.btnSet)
        self.horizontalLayout.setStretch(0, 50)
        self.horizontalLayout.setStretch(1, 50)
        self.horizontalLayout.setStretch(2, 50)
        MainWindow.setCentralWidget(self.Form)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnFile.setText(_translate("MainWindow", "Przeglądaj"))
        self.btnSet.setText(_translate("MainWindow", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
