"""Entry point projektu — uruchamia graficzny interfejs uzytkownika."""

from .gui import BankApp


def main() -> None:
    app = BankApp()
    app.mainloop()


if __name__ == "__main__":
    main()
