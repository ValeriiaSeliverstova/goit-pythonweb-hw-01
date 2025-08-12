from dataclasses import dataclass
from abc import ABC, abstractmethod
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# 1:Щоб виконати принцип єдиної відповідальності (SRP), створіть клас Book, який відповідатиме за зберігання інформації про книгу.
@dataclass
class Book:
    title: str
    author: str
    year: int


# 4: Щоб виконати принцип розділення інтерфейсів (ISP), використовуйте інтерфейс LibraryInterface для чіткої специфікації методів, які необхідні для роботи з бібліотекою library.
class LibraryInterface(ABC):
    @abstractmethod
    def add_book(self, title: str, author: str, year: int) -> None:
        pass

    @abstractmethod
    def remove_book(self, title: str) -> None:
        pass

    @abstractmethod
    def show_books(self) -> None:
        pass


# 3:Щоб виконати принцип підстанови Лісков (LSP), переконайтеся, що будь-який клас, який наслідує інтерфейс LibraryInterface, може замінити клас Library без порушення роботи програми.


class LibraryManager:
    def __init__(
        self, library: LibraryInterface
    ) -> (
        None
    ):  # 5: : LibraryManager приймає library: LibraryInterface у конструкторі — залежить від абстракції
        self.library = library

    def add_book(self, title: str, author: str, year: int) -> None:
        self.library.add_book(title, author, year)

    def remove_book(self, title: str) -> None:
        self.library.remove_book(title)

    def show_books(self) -> None:
        self.library.show_books()


class Library(LibraryInterface):
    def __init__(self) -> None:
        self.books: list[Book] = []

    def add_book(self, title: str, author: str, year: int) -> None:
        book = Book(title, author, year)
        self.books.append(book)
        logging.info("Book '%s' by %s (%d) has been added", title, author, year)

    def remove_book(self, title: str) -> None:
        for book in self.books:
            if book.title == title:
                self.books.remove(book)
                break
        else:
            logging.info("Book '%s' not found in the library", title)
            return

    def show_books(self) -> None:
        for book in self.books:
            logging.info(
                "Title: %s, Author: %s, Year: %d", book.title, book.author, book.year
            )


# 2:Щоб забезпечити принцип відкритості/закритості (OCP), зробіть так, щоб клас Library міг бути розширений для нової функціональності без зміни його коду.
# Розширяю функціонал - додаю збереження списку книг у файл.


class FileLibrary(Library):
    def __init__(self, filename: str) -> None:
        super().__init__()
        self.filename: Path = Path(filename)
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        if not self.filename.exists():
            self.filename.touch()
            logging.info("File '%s' created", self.filename)
        self.load_books()

    def add_book(self, title: str, author: str, year: int) -> None:
        super().add_book(title, author, year)
        self.save_books()

    def remove_book(self, title: str) -> None:
        before = len(self.books)
        super().remove_book(title)
        if len(self.books) != before:
            self.save_books()

    def load_books(self) -> None:
        try:
            with self.filename.open("r", encoding="utf-8", newline="") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        title, author, year_str = [p.strip() for p in line.split(",")]
                        self.books.append(Book(title, author, int(year_str)))
                    except Exception:
                        logging.info("Skip bad line: %r", line)
        except OSError as e:
            logging.error("Cannot read '%s': %s", self.filename, e)

    def save_books(self) -> None:
        try:
            with self.filename.open("w", encoding="utf-8", newline="") as f:
                for b in self.books:
                    f.write(f"{b.title},{b.author},{b.year}\n")
            logging.info("Saved %d book(s) to '%s'", len(self.books), self.filename)
        except OSError as e:
            logging.error("Cannot write '%s': %s", self.filename, e)


def main() -> None:
    library = FileLibrary("books.txt")
    manager = LibraryManager(library)

    while True:
        command = input("Enter command (add, remove, show, exit): ").strip().lower()

        match command:
            case "add":
                title = input("Enter book title: ").strip()
                author = input("Enter book author: ").strip()
                year = input("Enter book year: ").strip()
                try:
                    year = int(year)
                except ValueError:
                    logging.error("Year must be an integer")
                    continue
                manager.add_book(title, author, year)
            case "remove":
                title = input("Enter book title to remove: ").strip()
                manager.remove_book(title)
            case "show":
                manager.show_books()
            case "exit":
                break
            case _:
                logging.info("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
