# Banking OOP Python

Projekt zaliczeniowy z programowania obiektowego w Pythonie. Repozytorium jest przygotowane jako osobny projekt do dalszego rozwoju, a nie jako kopia całego repo kursowego.

## Cel

- zbudowac czytelny mini-system bankowy w Pythonie,
- pokazac najwazniejsze elementy OOP wymagane na zajeciach,
- utrzymac porzadna strukture repozytorium gotowa do prezentacji.

## Struktura repo

```text
banking-oop-python/
├── README.md
├── pyproject.toml
├── src/
│   └── banking/
│       ├── __init__.py
│       ├── __main__.py
│       └── domain.py
├── tests/
│   └── test_banking.py
├── docs/
│   └── uml/
│       └── README.md
└── examples/
    └── README.md
```

## Dlaczego tak

- `src/` trzyma kod aplikacji i oddziela go od dokumentacji oraz testow.
- `src/banking/` to pakiet Python projektu.
- `__main__.py` pelni role entry pointa. W Pythonie to bardziej naturalne niz pojedynczy top-level `main.py`.
- `tests/` zawiera testy odseparowane od kodu produkcyjnego.
- `docs/` trzyma publiczne materialy do UML i prezentacji architektury.
- `examples/` jest miejscem na male moduly demonstracyjne dla tematow, ktore nie wejda naturalnie do rdzenia banku.

## Aktualny model

- `Account` obsluguje wplaty, wyplaty, walidacje kwoty i ochrone przed ujemnym saldem poczatkowym.
- `SavingsAccount` dziedziczy po `Account` i uzywa `super().__init__(balance)`.
- `CheckingAccount` dziedziczy po `Account`, przechowuje `overdraft_limit`, waliduje jego wartosc i nadpisuje `withdraw()`, aby pozwolic na zejscie ponizej zera w granicach limitu debetowego.
- `Customer` przechowuje wiele kont i pozwala pobierac je po indeksie.
- Biezace testy obejmuja przypadki pozytywne i negatywne dla `Account`, `SavingsAccount`, `CheckingAccount` i `Customer`.

## Jak uruchomic

Demo:

```bash
PYTHONPATH=src python -m banking
```

Testy:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Zakres na kolejne etapy

1. Domknac podstawowe testy `CheckingAccount` dla pozostalych walidacji wyplaty.
2. Dodac `Bank` jako warstwe agregujaca klientow i konta.
3. Rozbudowac projekt o `Transaction`, `Enum`, kontrakty i dalsze elementy OOP.
4. Uzupelnic publiczna dokumentacje i material UML do prezentacji projektu.
