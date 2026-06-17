"""Graficzny interfejs uzytkownika systemu bankowego."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

from .domain import Bank, Customer, SavingsAccount, CheckingAccount, Account, TransactionType


class BankApp(tk.Tk):
    """Glowne okno aplikacji bankowej."""

    def __init__(self):
        super().__init__()
        self.title("System Bankowy")
        self.geometry("960x620")
        self.minsize(800, 500)

        self._bank = Bank()
        self._selected_customer: Customer | None = None
        self._selected_account: Account | None = None
        self._transfer_targets: list[tuple[str, int, int]] = []

        self._build_toolbar()
        self._build_main_area()
        self._build_status_bar()
        self._load_demo_data()
        self._refresh_tree()

    # ------------------------------------------------------------------ #
    # Budowa interfejsu                                                    #
    # ------------------------------------------------------------------ #

    def _build_toolbar(self) -> None:
        bar = ttk.Frame(self, relief="raised")
        bar.pack(side="top", fill="x", padx=2, pady=2)

        ttk.Button(bar, text="Zapisz stan", command=self._save_state).pack(side="left", padx=4, pady=3)
        ttk.Button(bar, text="Wczytaj stan", command=self._load_state).pack(side="left", padx=4, pady=3)
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=6, pady=3)
        ttk.Button(bar, text="+ Nowy klient", command=self._dialog_add_customer).pack(side="left", padx=4, pady=3)
        ttk.Button(bar, text="+ Nowe konto", command=self._dialog_add_account).pack(side="left", padx=4, pady=3)

    def _build_main_area(self) -> None:
        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=4, pady=4)

        self._build_left_panel(paned)
        self._build_right_panel(paned)

    def _build_left_panel(self, paned: ttk.PanedWindow) -> None:
        frame = ttk.LabelFrame(paned, text="Klienci i konta")
        paned.add(frame, weight=1)

        self._tree = ttk.Treeview(frame, columns=("balance", "type"), show="tree headings")
        self._tree.heading("#0", text="Nazwa")
        self._tree.heading("balance", text="Saldo (zl)")
        self._tree.heading("type", text="Typ")
        self._tree.column("#0", width=160, minwidth=120)
        self._tree.column("balance", width=100, anchor="e", minwidth=80)
        self._tree.column("type", width=120, minwidth=100)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    def _build_right_panel(self, paned: ttk.PanedWindow) -> None:
        frame = ttk.Frame(paned)
        paned.add(frame, weight=1)

        nb = ttk.Notebook(frame)
        nb.pack(fill="both", expand=True)

        nb.add(self._build_tab_operations(nb), text="Wplata / Wyplata")
        nb.add(self._build_tab_transfer(nb),   text="Przelew")
        nb.add(self._build_tab_history(nb),    text="Historia transakcji")

    def _build_tab_operations(self, parent) -> ttk.Frame:
        tab = ttk.Frame(parent, padding=12)

        ttk.Label(tab, text="Wybrane konto:").grid(row=0, column=0, sticky="w", pady=6)
        self._lbl_selected = ttk.Label(tab, text="— wybierz konto z listy po lewej", foreground="gray")
        self._lbl_selected.grid(row=0, column=1, sticky="w", pady=6)

        ttk.Label(tab, text="Kwota (zl):").grid(row=1, column=0, sticky="w", pady=6)
        self._var_amount = tk.StringVar()
        ttk.Entry(tab, textvariable=self._var_amount, width=16).grid(row=1, column=1, sticky="w", pady=6)

        btn_frame = ttk.Frame(tab)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=12)
        ttk.Button(btn_frame, text="Wplac",  width=14, command=self._deposit).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Wyplac", width=14, command=self._withdraw).pack(side="left", padx=6)

        return tab

    def _build_tab_transfer(self, parent) -> ttk.Frame:
        tab = ttk.Frame(parent, padding=12)

        ttk.Label(tab, text="Z konta:").grid(row=0, column=0, sticky="w", pady=6)
        self._lbl_transfer_from = ttk.Label(tab, text="— wybierz konto z listy po lewej", foreground="gray")
        self._lbl_transfer_from.grid(row=0, column=1, sticky="w", pady=6)

        ttk.Label(tab, text="Na konto:").grid(row=1, column=0, sticky="w", pady=6)
        self._var_transfer_target = tk.StringVar()
        self._combo_target = ttk.Combobox(tab, textvariable=self._var_transfer_target, width=34, state="readonly")
        self._combo_target.grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(tab, text="Kwota (zl):").grid(row=2, column=0, sticky="w", pady=6)
        self._var_transfer_amount = tk.StringVar()
        ttk.Entry(tab, textvariable=self._var_transfer_amount, width=16).grid(row=2, column=1, sticky="w", pady=6)

        ttk.Button(tab, text="Wykonaj przelew", command=self._transfer).grid(row=3, column=0, columnspan=2, pady=12)

        return tab

    def _build_tab_history(self, parent) -> ttk.Frame:
        tab = ttk.Frame(parent, padding=12)

        self._history_box = tk.Listbox(tab, font=("Courier", 10), height=16)
        vsb = ttk.Scrollbar(tab, orient="vertical", command=self._history_box.yview)
        self._history_box.configure(yscrollcommand=vsb.set)
        self._history_box.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        return tab

    def _build_status_bar(self) -> None:
        self._var_status = tk.StringVar(value="Gotowy.")
        ttk.Label(self, textvariable=self._var_status, relief="sunken", anchor="w").pack(
            side="bottom", fill="x", padx=2, pady=1
        )

    # ------------------------------------------------------------------ #
    # Dane demonstracyjne                                                  #
    # ------------------------------------------------------------------ #

    def _load_demo_data(self) -> None:
        jan = Customer("Jan", "Kowalski")
        jan.add_account(SavingsAccount(1000.0))
        jan.add_account(CheckingAccount(500.0, 200.0))

        anna = Customer("Anna", "Nowak")
        anna.add_account(SavingsAccount(2000.0))

        self._bank.add_customer(jan)
        self._bank.add_customer(anna)

    # ------------------------------------------------------------------ #
    # Odswiez widoki                                                       #
    # ------------------------------------------------------------------ #

    def _refresh_tree(self) -> None:
        self._tree.delete(*self._tree.get_children())
        for ci, customer in enumerate(self._bank.get_customers()):
            name = f"{customer.get_first_name()} {customer.get_last_name()}"
            node = self._tree.insert("", "end", iid=f"c{ci}", text=name,
                                     values=("", "Klient"), open=True)
            for ai, account in enumerate(customer.get_accounts()):
                atype = self._account_type_label(account)
                self._tree.insert(node, "end", iid=f"c{ci}a{ai}",
                                  text=f"Konto {ai + 1}",
                                  values=(f"{account.get_balance():.2f}", atype))
        self._refresh_transfer_targets()

    def _refresh_transfer_targets(self) -> None:
        targets = []
        for ci, customer in enumerate(self._bank.get_customers()):
            for ai, account in enumerate(customer.get_accounts()):
                label = (
                    f"{customer.get_first_name()} {customer.get_last_name()} "
                    f"— Konto {ai + 1} ({account.get_balance():.2f} zl)"
                )
                targets.append((label, ci, ai))
        self._transfer_targets = targets
        self._combo_target["values"] = [t[0] for t in targets]

    def _refresh_history(self) -> None:
        self._history_box.delete(0, tk.END)
        if self._selected_account is None:
            return
        transactions = self._selected_account.get_transactions()
        if not transactions:
            self._history_box.insert(tk.END, "Brak transakcji dla tego konta.")
            return
        for t in transactions:
            prefix = "WPLATA  +" if t.get_type() == TransactionType.DEPOSIT else "WYPLATA -"
            self._history_box.insert(tk.END, f"  {prefix}  {t.get_amount():.2f} zl")

    def _update_account_label(self) -> None:
        if self._selected_account and self._selected_customer:
            text = self._describe_selected()
            self._lbl_selected.config(text=text, foreground="black")
            self._lbl_transfer_from.config(text=text, foreground="black")

    def _describe_selected(self) -> str:
        atype = self._account_type_label(self._selected_account)
        name = f"{self._selected_customer.get_first_name()} {self._selected_customer.get_last_name()}"
        return f"{name} — {atype}  ({self._selected_account.get_balance():.2f} zl)"

    @staticmethod
    def _account_type_label(account: Account) -> str:
        return "Oszczednosciowe" if isinstance(account, SavingsAccount) else "Biezace"

    # ------------------------------------------------------------------ #
    # Zdarzenie: wybor w drzewie                                           #
    # ------------------------------------------------------------------ #

    def _on_tree_select(self, _event) -> None:
        sel = self._tree.selection()
        if not sel:
            return
        iid = sel[0]
        if "a" not in iid:
            self._selected_customer = None
            self._selected_account = None
            self._lbl_selected.config(text="— wybierz konto z listy po lewej", foreground="gray")
            self._lbl_transfer_from.config(text="— wybierz konto z listy po lewej", foreground="gray")
            return

        ci, ai = self._parse_iid(iid)
        self._selected_customer = self._bank.get_customer(ci)
        self._selected_account = self._selected_customer.get_account(ai)

        self._update_account_label()
        self._refresh_history()
        self._var_status.set(f"Wybrano: {self._describe_selected()}")

    @staticmethod
    def _parse_iid(iid: str) -> tuple[int, int]:
        parts = iid.split("a")
        return int(parts[0][1:]), int(parts[1])

    # ------------------------------------------------------------------ #
    # Operacje bankowe                                                     #
    # ------------------------------------------------------------------ #

    def _require_account(self) -> bool:
        if self._selected_account is None:
            messagebox.showwarning("Brak wyboru", "Najpierw wybierz konto z listy po lewej.")
            return False
        return True

    def _parse_amount(self, var: tk.StringVar) -> float | None:
        try:
            return float(var.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Niepoprawna kwota", "Podaj liczbe, np. 100 lub 50.50")
            return None

    def _deposit(self) -> None:
        if not self._require_account():
            return
        amount = self._parse_amount(self._var_amount)
        if amount is None:
            return
        try:
            self._selected_account.deposit(amount)
            self._var_amount.set("")
            self._refresh_tree()
            self._refresh_history()
            self._update_account_label()
            self._var_status.set(
                f"Wplacono {amount:.2f} zl.  Nowe saldo: {self._selected_account.get_balance():.2f} zl"
            )
        except ValueError as e:
            messagebox.showerror("Blad wplaty", str(e))

    def _withdraw(self) -> None:
        if not self._require_account():
            return
        amount = self._parse_amount(self._var_amount)
        if amount is None:
            return
        try:
            self._selected_account.withdraw(amount)
            self._var_amount.set("")
            self._refresh_tree()
            self._refresh_history()
            self._update_account_label()
            self._var_status.set(
                f"Wyplacono {amount:.2f} zl.  Nowe saldo: {self._selected_account.get_balance():.2f} zl"
            )
        except ValueError as e:
            messagebox.showerror("Blad wyplaty", str(e))

    def _transfer(self) -> None:
        if not self._require_account():
            return
        idx = self._combo_target.current()
        if idx < 0:
            messagebox.showwarning("Brak wyboru", "Wybierz konto docelowe z listy.")
            return
        amount = self._parse_amount(self._var_transfer_amount)
        if amount is None:
            return

        _, ci, ai = self._transfer_targets[idx]
        target = self._bank.get_customer(ci).get_account(ai)

        if target is self._selected_account:
            messagebox.showwarning("Blad", "Konto zrodlowe i docelowe musza byc rozne.")
            return
        try:
            self._bank.transfer(self._selected_account, target, amount)
            self._var_transfer_amount.set("")
            self._refresh_tree()
            self._refresh_history()
            self._update_account_label()
            self._var_status.set(f"Przelano {amount:.2f} zl.")
        except ValueError as e:
            messagebox.showerror("Blad przelewu", str(e))

    # ------------------------------------------------------------------ #
    # Dodawanie klientow i kont                                            #
    # ------------------------------------------------------------------ #

    def _dialog_add_customer(self) -> None:
        first = simpledialog.askstring("Nowy klient", "Imie:", parent=self)
        if not first:
            return
        last = simpledialog.askstring("Nowy klient", "Nazwisko:", parent=self)
        if not last:
            return
        try:
            self._bank.add_customer(Customer(first.strip(), last.strip()))
            self._refresh_tree()
            self._var_status.set(f"Dodano klienta: {first.strip()} {last.strip()}")
        except ValueError as e:
            messagebox.showerror("Blad", str(e))

    def _dialog_add_account(self) -> None:
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Brak wyboru", "Wybierz klienta z listy, dla ktorego chcesz dodac konto.")
            return
        iid = sel[0]
        ci = self._parse_iid(iid)[0] if "a" in iid else int(iid[1:])
        customer = self._bank.get_customer(ci)
        if customer is None:
            return

        atype = simpledialog.askstring(
            "Typ konta",
            "Podaj typ:\n  1 = Oszczednosciowe\n  2 = Biezace",
            parent=self,
        )
        if atype not in ("1", "2"):
            return

        bal_str = simpledialog.askstring("Saldo poczatkowe", "Saldo poczatkowe (zl):", parent=self)
        try:
            balance = float(bal_str.replace(",", "."))
        except (ValueError, AttributeError):
            messagebox.showerror("Blad", "Niepoprawna kwota salda.")
            return

        try:
            if atype == "1":
                account: Account = SavingsAccount(balance)
            else:
                ov_str = simpledialog.askstring("Limit debetowy", "Limit debetowy (zl):", parent=self)
                try:
                    overdraft = float(ov_str.replace(",", "."))
                except (ValueError, AttributeError):
                    messagebox.showerror("Blad", "Niepoprawna kwota limitu.")
                    return
                account = CheckingAccount(balance, overdraft)

            customer.add_account(account)
            self._refresh_tree()
            name = f"{customer.get_first_name()} {customer.get_last_name()}"
            self._var_status.set(f"Dodano konto dla: {name}")
        except ValueError as e:
            messagebox.showerror("Blad", str(e))

    # ------------------------------------------------------------------ #
    # Zapis i odczyt pliku                                                 #
    # ------------------------------------------------------------------ #

    def _save_state(self) -> None:
        filepath = filedialog.asksaveasfilename(
            title="Zapisz stan banku",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Wszystkie pliki", "*.*")],
            initialfile="bank_state.json",
        )
        if not filepath:
            return
        try:
            self._bank.save_to_file(filepath)
            self._var_status.set(f"Stan zapisany: {filepath}")
        except IOError as e:
            messagebox.showerror("Blad zapisu", str(e))

    def _load_state(self) -> None:
        filepath = filedialog.askopenfilename(
            title="Wczytaj stan banku",
            filetypes=[("JSON", "*.json"), ("Wszystkie pliki", "*.*")],
        )
        if not filepath:
            return
        try:
            self._bank.load_from_file(filepath)
            self._selected_customer = None
            self._selected_account = None
            self._lbl_selected.config(text="— wybierz konto z listy po lewej", foreground="gray")
            self._lbl_transfer_from.config(text="— wybierz konto z listy po lewej", foreground="gray")
            self._history_box.delete(0, tk.END)
            self._refresh_tree()
            self._var_status.set(f"Stan wczytany: {filepath}")
        except FileNotFoundError as e:
            messagebox.showerror("Plik nie istnieje", str(e))
        except ValueError as e:
            messagebox.showerror("Blad danych w pliku", str(e))
        except IOError as e:
            messagebox.showerror("Blad odczytu", str(e))
