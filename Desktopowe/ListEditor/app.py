from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidgetItem
from meow import Ui_MainWindow  # Import wygenerowanego interfejsu

class ListEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Na starcie ukrywamy panel pomocy
        self.ui.dockWidget.setVisible(False)

        # Dodaj możliwości wyboru do formularza 'Klasa'
        self.ui.klasaComboBox.addItems(["4tp", "5tp", "5tr", "3rs"])

        # Podłączenie funkcji do przycisków
        self.ui.openBtn.clicked.connect(self.openFile)
        self.ui.saveBtn.clicked.connect(self.saveFile)
        self.ui.duplicateBtn.clicked.connect(self.duplicateEntry)
        self.ui.deleteButton.clicked.connect(self.removeEntry)
        self.ui.menuButton.clicked.connect(self.toggleDock)

        # Nowy przycisk do zapisania formularza jako wpis
        self.ui.tabWidget.setTabText(0, "Edytor")
        self.ui.tabWidget.setTabText(1, "Pomoc")
        self.ui.saveFormBtn = self.createSaveFormButton()
        self.ui.formLayout.setWidget(6, self.ui.formLayout.ItemRole.FieldRole, self.ui.saveFormBtn)

        # Inicjalizacja innych zmiennych
        self.current_file = None  # Przechowuje ścieżkę aktualnie otwartego pliku

    def createSaveFormButton(self):
        """Tworzy przycisk do zapisywania formularza do listy."""
        from PyQt6.QtWidgets import QPushButton
        button = QPushButton("Dodaj formularz jako wpis")
        button.clicked.connect(self.addFormToList)
        return button

    def addFormToList(self):
        """Dodaje dane z formularza jako nowy wpis w QListWidget i czyści formularz."""
        klasa = self.ui.klasaComboBox.currentText()
        nazwisko = self.ui.nazwiskoLineEdit.text()
        imie = self.ui.imiLineEdit.text()
        grupa = "g1" if self.ui.radioButton.isChecked() else "g2"
        stanowisko = self.ui.stanowiskoSpinBox.value()
        uwagi = self.ui.uwagiLineEdit.text()

        if not nazwisko or not imie:
            QMessageBox.warning(self, "Błąd", "Nazwisko i Imię są wymagane!")
            return

        # Tworzymy sformatowany wpis
        entry = f"Klasa: {klasa}, Nazwisko: {nazwisko}, Imię: {imie}, Grupa: {grupa}, Stanowisko: {stanowisko}, Uwagi: {uwagi}"
        self.ui.leftBar.addItem(entry)
        self.ui.statusBar.showMessage("Dodano wpis do listy.")

        # Czyszczenie formularza po dodaniu wpisu
        self.clearForm()

    def clearForm(self):
        """Czyści pola formularza."""
        self.ui.klasaComboBox.setCurrentIndex(0)  # Resetuje wybór klasy
        self.ui.nazwiskoLineEdit.clear()         # Czyści pole nazwiska
        self.ui.imiLineEdit.clear()              # Czyści pole imienia
        self.ui.radioButton.setChecked(False)    # Odznacza grupę g1
        self.ui.radioButton_2.setChecked(False)  # Odznacza grupę g2
        self.ui.stanowiskoSpinBox.setValue(1)    # Resetuje wartość pola stanowiska
        self.ui.uwagiLineEdit.clear()            # Czyści pole uwag


    def openFile(self):
        """Otwiera plik i ładuje jego zawartość do ListWidget, parsując format."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Otwórz Plik", "", "Pliki tekstowe (*.txt);;Wszystkie pliki (*)")
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    self.ui.leftBar.clear()
                    for line in file:
                        if line.strip():
                            self.ui.leftBar.addItem(line.strip())
                self.current_file = file_name
                self.ui.statusBar.showMessage(f"Otworzono plik: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się otworzyć pliku: {e}")

    def saveFile(self):
        """Zapisuje zawartość ListWidget do pliku w sformatowany sposób."""
        file_name, _ = QFileDialog.getSaveFileName(self, "Zapisz Plik", "", "Pliki tekstowe (*.txt);;Wszystkie pliki (*)")
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    for i in range(self.ui.leftBar.count()):
                        file.write(self.ui.leftBar.item(i).text() + '\n')
                self.ui.statusBar.showMessage(f"Zapisano plik: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się zapisać pliku: {e}")

    def duplicateEntry(self):
        """Duplikuje aktualnie wybrany wpis na liście."""
        current_item = self.ui.leftBar.currentItem()
        if current_item:
            self.ui.leftBar.addItem(current_item.text())
            self.ui.statusBar.showMessage("Wpis zduplikowany.")
        else:
            self.ui.statusBar.showMessage("Nie wybrano żadnego wpisu.")

    def removeEntry(self):
        """Usuwa aktualnie wybrany wpis na liście."""
        current_row = self.ui.leftBar.currentRow()
        if current_row >= 0:
            self.ui.leftBar.takeItem(current_row)
            self.ui.statusBar.showMessage("Wpis usunięty.")
        else:
            self.ui.statusBar.showMessage("Nie wybrano żadnego wpisu do usunięcia.")

    def toggleDock(self):
        """Przełącza widoczność DockWidget."""
        is_visible = self.ui.dockWidget.isVisible()
        self.ui.dockWidget.setVisible(not is_visible)
        self.ui.statusBar.showMessage("Panel pomocy " + ("ukryty" if is_visible else "pokazany."))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ListEditorApp()
    window.show()
    sys.exit(app.exec())
