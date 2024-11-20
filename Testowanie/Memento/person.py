from datetime import date
from copy import deepcopy

class Person:
    def __init__(self, imie, nazwisko, dataUrodzenia, miejsceUrodzenia, email, telefon):
        self.imie = imie
        self.nazwisko = nazwisko
        self.dataUrodzenia = dataUrodzenia
        self.miejsceUrodzenia = miejsceUrodzenia
        self.email = email
        self.telefon = telefon

    def create_backup(self):
        return PersonBackup(deepcopy(self))

    def restore_backup(self, backup):
        self.__dict__.update(backup.get_state().__dict__)

    def __str__(self):
        return (f"Imię: {self.imie}, Nazwisko: {self.nazwisko}, "
                f"Data urodzenia: {self.dataUrodzenia}, Miejsce urodzenia: {self.miejsceUrodzenia}, "
                f"Email: {self.email}, Telefon: {self.telefon}")
        
class PersonBackup:
    def __init__(self, person_state):
        self._state = person_state

    def get_state(self):
        return self._state

class Caretaker:
    def __init__(self):
        self._backups = []

    def save(self, backup):
        self._backups.append(backup)

    def restore(self, index):
        if 0 <= index < len(self._backups):
            return self._backups[index]
        else:
            print("Invalid backup index.")
            return None

    def list_backups(self):
        for i, backup in enumerate(self._backups):
            print(f"Backup {i}: {backup.get_state()}")

if __name__ == "__main__":
    person = Person(
        imie="John",
        nazwisko="Cena",
        dataUrodzenia=date(1990, 5, 15),
        miejsceUrodzenia="Warszawa",
        email="john.cena@example.com",
        telefon=123456789
    )

    print("Stan początkowy:")
    print(person)
    print()

    caretaker = Caretaker()

    caretaker.save(person.create_backup())

    person.email = "meowmeow@example.com"
    person.telefon = 987654321

    print("Po zmianach:")
    print(person)
    print()

    caretaker.save(person.create_backup())

    person.imie = "Krzysztof"
    person.nazwisko = "Kononowicz"

    print("Po kolejnych zmianach:")
    print(person)
    print()

    backup = caretaker.restore(0)
    if backup:
        person.restore_backup(backup)

    print("Po przywróceniu pierwszej kopii zapasowej:")
    print(person)
