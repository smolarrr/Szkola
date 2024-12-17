import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QFileIconProvider
)
from PyQt6.QtCore import Qt, QFileInfo

class ClipClapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clip-Clap")
        self.resize(1000, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.buttons_layout = QHBoxLayout()
        self.catalogue_button = QPushButton("Przeglądaj Katalog")
        self.save_button = QPushButton("Zapisz TXT")
        self.buttons_layout.addWidget(self.catalogue_button)
        self.buttons_layout.addWidget(self.save_button)

        self.file_table = QTableWidget()
        self.file_table.setColumnCount(4)
        self.file_table.setHorizontalHeaderLabels(["Ikona", "Plik", "Ścieżka", "Akcje"])
        self.file_table.setColumnWidth(0, 50)
        self.file_table.setColumnWidth(1, 200)
        self.file_table.setColumnWidth(2, 400)
        self.file_table.setColumnWidth(3, 300)
        self.file_table.setAcceptDrops(True)

        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addWidget(self.file_table)

        self.status_bar = self.statusBar()
        self.updateStatusBar("Aplikacja gotowa!")

        self.catalogue_button.clicked.connect(self.browseCatalogue)
        self.save_button.clicked.connect(self.saveToTxt)
        
        self.file_icon_provider = QFileIconProvider()

        self.file_paths = []

    def browseCatalogue(self):
        directory = QFileDialog.getExistingDirectory(self, "Wybierz katalog")
        if directory:
            self.loadFilesFromDirectory(directory)
            self.updateStatusBar(f"Wczytano pliki z katalogu: {directory}")

    def loadFilesFromDirectory(self, directory):
        if os.path.isdir(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    self.addFileToTable(file_path)
        else:
            QMessageBox.warning(self, "Błąd", "Nieprawidłowy katalog.")
            self.updateStatusBar("Błąd: Nieprawidłowy katalog.")

    def addFileToTable(self, file_path):
        if file_path in self.file_paths:
            return

        self.file_paths.append(file_path)
        row_position = self.file_table.rowCount()
        self.file_table.insertRow(row_position)

        icon_item = QTableWidgetItem()
        #icon_item.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_FileIcon))
        icon_item.setIcon(self.file_icon_provider.icon(QFileInfo(file_path)))
        icon_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.file_table.setItem(row_position, 0, icon_item)

        file_name_item = QTableWidgetItem(os.path.basename(file_path))
        file_name_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.file_table.setItem(row_position, 1, file_name_item)

        file_path_item = QTableWidgetItem(file_path)
        file_path_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.file_table.setItem(row_position, 2, file_path_item)

        action_widget = self.createActionWidget(file_path)
        self.file_table.setCellWidget(row_position, 3, action_widget)

        self.updateStatusBar(f"Dodano plik: {file_path}")

    def createActionWidget(self, file_path):
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 0, 0, 0)

        copy_button = QPushButton("Użyj/Kopiuj")
        copy_button.setProperty("file_path", file_path)
        copy_button.clicked.connect(self.handleCopyClick)
        action_layout.addWidget(copy_button)

        open_button = QPushButton("Otwórz katalog")
        open_button.setProperty("file_path", file_path)
        open_button.clicked.connect(self.handleOpenClick)
        action_layout.addWidget(open_button)

        delete_button = QPushButton("Usuń")
        delete_button.setProperty("file_path", file_path)
        delete_button.clicked.connect(self.handleDeleteClick)
        action_layout.addWidget(delete_button)

        return action_widget

    def handleCopyClick(self):
        sender_button = self.sender()
        if sender_button:
            file_path = sender_button.property("file_path")
            self.copyToClipboard(file_path)

    def handleOpenClick(self):
        sender_button = self.sender()
        if sender_button:
            file_path = sender_button.property("file_path")
            self.openDirectory(file_path)

    def handleDeleteClick(self):
        sender_button = self.sender()
        if sender_button:
            file_path = sender_button.property("file_path")
            row = self.findFileRow(file_path)
            if row is not None:
                self.removeFile(row, file_path)

    def findFileRow(self, file_path):
        for row in range(self.file_table.rowCount()):
            item = self.file_table.item(row, 2)
            if item and item.text() == file_path:
                return row
        return None

    def copyToClipboard(self, file_path):
        QApplication.clipboard().setText(file_path)
        self.updateStatusBar(f"Skopiowano ścieżkę: {file_path}")

    def openDirectory(self, file_path):
        directory = os.path.dirname(file_path)
        if os.path.exists(directory):
            if sys.platform == "win32":
                os.startfile(directory)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", directory])
            else:
                subprocess.Popen(["xdg-open", directory])
            self.updateStatusBar(f"Otworzono katalog: {directory}")
        else:
            QMessageBox.warning(self, "Błąd", "Katalog nie istnieje!")
            self.updateStatusBar("Błąd: katalog nie istnieje!")

    def removeFile(self, row, file_path):
        if file_path in self.file_paths:
            self.file_paths.remove(file_path)
        self.file_table.removeRow(row)
        self.updateStatusBar(f"Usunięto plik: {file_path}")

        if not self.file_paths:
            self.updateStatusBar("Lista plików jest pusta.")

    def saveToTxt(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Zapisz plik", "", "Pliki tekstowe (*.txt)")
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                for path in self.file_paths:
                    file.write(f"{path}\n")
            QMessageBox.information(self, "Zapisano", f"Lista plików zapisana do: {file_name}")
            self.updateStatusBar(f"Zapisano listę plików do: {file_name}")

    def updateStatusBar(self, message):
        self.status_bar.showMessage(message)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                self.addFileToTable(file_path)
            elif os.path.isdir(file_path):
                self.loadFilesFromDirectory(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClipClapApp()
    window.show()
    sys.exit(app.exec())
