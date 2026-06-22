# Banking OOP Python

Projekt zaliczeniowy z programowania obiektowego. Napisany w całości w Pythonie. Mini system bankowy pokazujący najważniejsze elementy OOP: dziedziczenie, enkapsulację, polimorfizm, kompozycję, agregację i kontrakty. Uzupełniony o zapis/odczyt stanu do pliku JSON, obsługę wyjątków i graficzny interfejs użytkownika (tkinter).

## Wymagania

- Python 3.10 lub nowszy — **zalecana instalacja z [python.org](https://www.python.org/downloads/)**, która zawiera `tkinter` domyślnie
- Brak zewnętrznych zależności PyPI — projekt korzysta wyłącznie z biblioteki standardowej Pythona (json, abc, enum, unittest)

> **Uwaga dotycząca `tkinter`:** Moduł GUI jest oparty na `tkinter`, który wchodzi w skład oficjalnego instalatora z python.org (Windows i macOS). W przypadku innych dystrybucji może wymagać doinstalowania:
> - **macOS z Homebrew:** `brew install python-tk@3.XX` (zastąp `XX` wersją Pythona, np. `3.13`)
> - **Linux (Ubuntu/Debian):** `sudo apt install python3-tk`

## Jak uruchomić

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/Radoslaw-Stepien/banking-OOP-python
cd banking-oop-python
```

### 2. Uruchom aplikację

macOS / Linux:
```bash
PYTHONPATH=src python3 -m banking
```

Windows (cmd):
```cmd
set PYTHONPATH=src && python -m banking
```

Otworzy się okno graficzne z załadowanymi danymi demonstracyjnymi (dwóch klientów, trzy konta).

### 3. Uruchom testy

macOS / Linux:
```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Windows (cmd):
```cmd
set PYTHONPATH=src && python -m unittest discover -s tests -v
```

Oczekiwany wynik: **37 testów, wszystkie przechodzą (OK)**.

## Struktura repozytorium

```text
banking-oop-python/
├── src/banking/
│   ├── domain.py       # wszystkie klasy domenowe
│   ├── gui.py          # graficzny interfejs użytkownika (tkinter)
│   ├── __init__.py     # publiczny interfejs pakietu
│   └── __main__.py     # entry point — uruchamia GUI
├── tests/
│   └── test_banking.py # testy jednostkowe (37 testów)
├── docs/
│   ├── uml/            # diagram klas PlantUML
│   ├── decyzje-architektoniczne.md
│   └── plan-projektu.md
├── examples/           # przykłady tematów pobocznych (wielodziedziczenie, singleton, Protocol)
├── pyproject.toml      # konfiguracja pakietu
└── requirements.txt    # lista zależności (brak zewnętrznych)
```

## Model domenowy

<p align="center">
  <img src="docs/uml/banking.png" alt="Diagram klas" width="700"/>
</p>

| Klasa             | Rola                                                                       |
| ----------------- | -------------------------------------------------------------------------- |
| `Account`         | Abstrakcyjna klasa bazowa konta. Enkapsuluje saldo i historię transakcji.  |
| `SavingsAccount`  | Konto oszczędnościowe. Nalicza miesięczne odsetki (5% rocznie).            |
| `CheckingAccount` | Konto bieżące z limitem debetowym. Pobiera miesięczną opłatę.              |
| `Transaction`     | Pojedyncza operacja — typ (Enum) i kwota. Kompozycja z Account.            |
| `TransactionType` | Enum: `DEPOSIT` / `WITHDRAWAL`.                                            |
| `Customer`        | Klient przechowujący listę kont.                                           |
| `Bank`            | Agreguje klientów. Realizuje przelewy, zapis/odczyt stanu i raport sald.   |
| `BankApp`         | Główne okno GUI (tkinter). Łączy widok z modelem domenowym.                |

## Pokryte tematy OOP

- dziedziczenie i `super()` — `SavingsAccount`, `CheckingAccount` po `Account`
- enkapsulacja — prywatne pola `__balance`, `__customers`, `__transactions`
- polimorfizm — `apply_monthly_update()` działa inaczej w każdej klasie konta
- abstrakcyjna klasa bazowa (ABC) — `Account` wymusza implementację `apply_monthly_update()`
- kompozycja — `Account` zawiera listę obiektów `Transaction`
- agregacja — `Bank` zawiera listę `Customer`, `Customer` zawiera listę `Account`
- Enum — `TransactionType`
- metoda statyczna — `Account.is_valid_amount()`
- metoda chroniona — `Account._record_transaction()` dostępna dla podklas
- kolekcje `list` i `dict` — historia transakcji, lista klientów, raport sald
- obsługa wyjątków — `ValueError`, `FileNotFoundError`, `IOError`, `json.JSONDecodeError`
- serializacja — `to_dict()` w każdej klasie, zapis/odczyt JSON (`save_to_file`, `load_from_file`)
- GUI (tkinter) — `BankApp` dziedziczące po `tk.Tk`, wzorzec MVC (model = `domain.py`, widok = `gui.py`)
- wielodziedziczenie i Mixin — `examples/wielodziedziczenie.py`
- singleton (`__new__`) — `examples/singleton.py`
- `typing.Protocol` — `examples/protocol_example.py`

## Testy

macOS / Linux:
```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Windows (cmd):
```cmd
set PYTHONPATH=src && python -m unittest discover -s tests -v
```

| Klasa testów           | Co weryfikuje                                                        | Liczba testów |
| ---------------------- | -------------------------------------------------------------------- | :-----------: |
| `AccountTests`         | wpłata i wypłata — `ValueError` przy błędnych danych                 |       3       |
| `SavingsAccountTests`  | saldo początkowe, walidacja przy tworzeniu                           |       2       |
| `CheckingAccountTests` | limit debetowy, wypłata w granicach limitu, historia transakcji      |       7       |
| `CustomerTests`        | przechowywanie kont, dostęp po indeksie, walidacja danych            |       4       |
| `BankTests`            | liczenie klientów, `get_customers()`, przelew, raport sald           |       7       |
| `TransactionTests`     | historia operacji — typ i kwota transakcji                           |       2       |
| `MonthUpdateTests`     | miesięczne odsetki (`SavingsAccount`), opłata (`CheckingAccount`)    |       2       |
| `StaticMethodTests`    | walidacja kwoty — metoda statyczna `is_valid_amount`                 |       3       |
| `FileIOTests`          | zapis/odczyt JSON, historia transakcji, błędne dane wejściowe        |       7       |
| **Razem**              |                                                                      |    **37**     |
