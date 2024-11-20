import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from titled import Ui_MainWindow

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btnFile.clicked.connect(self.clear_text)
        self.btnSet.clicked.connect(self.close_app)

        self.show()

    def close_app(self):
        QApplication.quit()

    def clear_text(self):
        self.entryName.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())