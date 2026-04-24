# Decyzje projektowe

## 1. Account jako abstrakcyjna klasa bazowa (ABC)

`Account` nie może być tworzone bezpośrednio — wymaga użycia `SavingsAccount` albo `CheckingAccount`.

Zdecydowano, że `Account` dziedziczy po `ABC` i deklaruje `apply_monthly_update()` jako `@abstractmethod`.

- każdy typ konta ma inną logikę miesięcznej aktualizacji (odsetki vs opłata),
- ABC wymusza, że każda nowa klasa konta musi tę metodę zaimplementować,
- bez ABC Python nie zgłosiłby błędu przy braku implementacji — błąd wyszedłby dopiero w czasie wykonania.

## 2. Polimorfizm zamiast isinstance

Zły wzorzec (który nie został użyty):

```python
if isinstance(account, SavingsAccount):
    account.deposit(account.get_balance() * 0.05 / 12)
elif isinstance(account, CheckingAccount):
    account._change_balance(-5.0)
```

Dobry wzorzec (który został wykorzystany):

```python
account.apply_monthly_update()
```

Dzięki polimorfizmowi kod wywołujący nie musi wiedzieć, z jakim typem konta ma do czynienia. Python sam wybiera odpowiednią implementację metody.

## 3. Kompozycja: Account zawiera Transaction

`Account` nie dziedziczy po `Transaction` i nie przekazuje odpowiedzialności za zapis historii na zewnątrz.

Zamiast tego każde konto przechowuje prywatną listę `__transactions` i samo zarządza jej zawartością.

To jest kompozycja: `Account` jest właścicielem listy `Transaction`. Gdy konto przestaje istnieć, jego historia też znika razem z nim.

`get_transactions()` zwraca kopię listy, a nie oryginał — zewnętrzny kod nie może modyfikować historii bezpośrednio.

## 4. Agregacja: Bank i Customer

`Bank` przechowuje listę `Customer`, a `Customer` przechowuje listę `Account`.

To jest agregacja: obiekty istnieją niezależnie. Można stworzyć `Customer` bez `Bank`, a `Account` bez `Customer`. `Bank` tylko nimi zarządza.

Rozróżnienie między kompozycją a agregacją:

- `Account` _zawiera_ `Transaction` — bez konta transakcje nie mają sensu (kompozycja),
- `Bank` _zarządza_ `Customer` — klient może istnieć bez banku (agregacja).

## 5. Enkapsulacja przez podwójne podkreślenie

Wszystkie pola wewnętrzne są prywatne (`__balance`, `__customers`, `__transactions`).

Dostęp z zewnątrz możliwy jest tylko przez metody publiczne (`get_balance()`, `get_transactions()`).

Wyjątkiem jest `_change_balance()` z pojedynczym podkreśleniem — to metoda chroniona, dostępna dla klas pochodnych (`CheckingAccount` używa jej w `withdraw()`), ale nie dla zewnętrznego kodu.

## 6. Enum dla typów transakcji

Zamiast używać napisów `"deposit"` / `"withdrawal"` bezpośrednio w kodzie, zdefiniowano `TransactionType` jako `Enum`.

Zalety:

- Python nie pozwoli użyć wartości spoza zbioru,
- IDE i narzędzia do analizy kodu widzą wszystkie możliwe wartości,
- refaktoryzacja nazwy jest bezpieczna — zmiana w jednym miejscu.

## 7. Metoda statyczna is_valid_amount

Sprawdzenie `amount > 0` pojawia się w `deposit()` i `withdraw()`. Zamiast powtarzać ten warunek, wyodrębniono go jako metodę statyczną `Account.is_valid_amount(amount)`.

Metoda statyczna, bo:

- nie zależy od stanu żadnego konkretnego konta,
- jest logicznie związana z klasą `Account`,
- może być wywołana bez tworzenia obiektu: `Account.is_valid_amount(50.0)`.

## 8. Transfer w Bank, nie w Account

Przelew dotyczy dwóch kont jednocześnie. `Account` opisuje jedno konto i jego operacje — nie jest przewidziany do obsługi relacji między kontami.

`Bank` jest odpowiednim miejscem na operacje łączące wiele obiektów. Metoda `transfer()` najpierw próbuje wypłaty z konta źródłowego, a dopiero po sukcesie wpłaca na docelowe. Dzięki temu pieniądze nie mogą „pojawić się z powietrza" przy nieudanym przelewie.
