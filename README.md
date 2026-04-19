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
│   ├── repo-structure.md
│   ├── notes/
│   │   └── README.md
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
- `docs/` trzyma opis architektury, UML i notatki do zaliczenia.
- `examples/` jest miejscem na male moduly demonstracyjne dla tematow, ktore nie wejda naturalnie do rdzenia banku.

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

1. Uporzadkowac obecny model `Account` i `Customer`.
2. Dodac `SavingsAccount` i `CheckingAccount` z uzyciem dziedziczenia i `super()`.
3. Dodac testy dla podstawowych przypadkow biznesowych.
4. Rozbudowac projekt o `Bank`, `Transaction`, `Enum`, kontrakty i UML.
