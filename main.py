import tkinter as tk
from tkinter import ttk

# -----------------------------
#   COLORS & THEME
# -----------------------------
PRIMARY_BLUE = "#1E6FFF"
LIGHT_BLUE = "#E6EEFF"
WHITE = "#FFFFFF"
DARK_TEXT = "#0A0A0A"

# -----------------------------
#   APP STATE (LOCAL VARIABLES)
# -----------------------------
balance_xrp = 0.00  # Fake balance for beta testing


# -----------------------------
#   MAIN WINDOW
# -----------------------------
root = tk.Tk()
root.title("Bankly – Fast XRP Banking")
root.geometry("900x550")
root.configure(bg=WHITE)


# -----------------------------
#   HEADER BAR
# -----------------------------
header = tk.Frame(root, bg=PRIMARY_BLUE, height=70)
header.pack(fill="x")

title = tk.Label(
    header, text="Bankly", font=("Segoe UI", 24, "bold"), fg=WHITE, bg=PRIMARY_BLUE
)
title.pack(side="left", padx=20)


# -----------------------------
#   SIDEBAR
# -----------------------------
sidebar = tk.Frame(root, bg=LIGHT_BLUE, width=180)
sidebar.pack(side="left", fill="y")

# -----------------------------
#   MAIN CONTENT AREA (SWITCHABLE)
# -----------------------------
main = tk.Frame(root, bg=WHITE)
main.pack(side="left", fill="both", expand=True, padx=20, pady=20)


# -----------------------------
#   PAGE SWITCHING SYSTEM
# -----------------------------
pages = {}


def show_page(name):
    """Hide all pages and show the selected one."""
    for page in pages.values():
        page.pack_forget()
    pages[name].pack(fill="both", expand=True)


# -----------------------------
#   DASHBOARD PAGE
# -----------------------------
dashboard = tk.Frame(main, bg=WHITE)
pages["Dashboard"] = dashboard

dash_title = tk.Label(
    dashboard,
    text="Dashboard",
    font=("Segoe UI", 20, "bold"),
    fg=PRIMARY_BLUE,
    bg=WHITE,
)
dash_title.pack(anchor="w")

# Balance card
balance_label = tk.Label(
    dashboard,
    text=f"Balance (XRP): {balance_xrp:.2f}",
    font=("Segoe UI", 18, "bold"),
    fg=PRIMARY_BLUE,
    bg=WHITE,
)
balance_label.pack(anchor="w", pady=20)


# -----------------------------
#   DEPOSIT PAGE
# -----------------------------
deposit_page = tk.Frame(main, bg=WHITE)
pages["Deposit"] = deposit_page

tk.Label(
    deposit_page,
    text="Deposit XRP",
    font=("Segoe UI", 20, "bold"),
    fg=PRIMARY_BLUE,
    bg=WHITE,
).pack(anchor="w", pady=10)

deposit_entry = tk.Entry(deposit_page, font=("Segoe UI", 14))
deposit_entry.pack(pady=10)


def deposit_action():
    global balance_xrp
    try:
        amount = float(deposit_entry.get())
        balance_xrp += amount
        balance_label.config(text=f"Balance (XRP): {balance_xrp:.2f}")
        deposit_entry.delete(0, tk.END)
    except:
        pass  # ignore invalid input for now


tk.Button(
    deposit_page,
    text="Confirm Deposit",
    font=("Segoe UI", 14, "bold"),
    bg=PRIMARY_BLUE,
    fg=WHITE,
    bd=0,
    padx=20,
    pady=10,
    command=deposit_action,
).pack(pady=10)


# -----------------------------
#   WITHDRAW PAGE
# -----------------------------
withdraw_page = tk.Frame(main, bg=WHITE)
pages["Withdraw"] = withdraw_page

tk.Label(
    withdraw_page,
    text="Withdraw XRP",
    font=("Segoe UI", 20, "bold"),
    fg=PRIMARY_BLUE,
    bg=WHITE,
).pack(anchor="w", pady=10)

withdraw_entry = tk.Entry(withdraw_page, font=("Segoe UI", 14))
withdraw_entry.pack(pady=10)


def withdraw_action():
    global balance_xrp
    try:
        amount = float(withdraw_entry.get())
        if amount <= balance_xrp:
            balance_xrp -= amount
            balance_label.config(text=f"Balance (XRP): {balance_xrp:.2f}")
        withdraw_entry.delete(0, tk.END)
    except:
        pass


tk.Button(
    withdraw_page,
    text="Confirm Withdrawal",
    font=("Segoe UI", 14, "bold"),
    bg=PRIMARY_BLUE,
    fg=WHITE,
    bd=0,
    padx=20,
    pady=10,
    command=withdraw_action,
).pack(pady=10)


# -----------------------------
#   TRANSFER PAGE (UI ONLY)
# -----------------------------
transfer_page = tk.Frame(main, bg=WHITE)
pages["Transfer"] = transfer_page

tk.Label(
    transfer_page,
    text="Send XRP (UI Only)",
    font=("Segoe UI", 20, "bold"),
    fg=PRIMARY_BLUE,
    bg=WHITE,
).pack(anchor="w", pady=10)

tk.Label(transfer_page, text="Recipient Wallet:", font=("Segoe UI", 12), bg=WHITE).pack(
    anchor="w"
)

recipient_entry = tk.Entry(transfer_page, font=("Segoe UI", 14))
recipient_entry.pack(pady=5)

tk.Label(transfer_page, text="Amount:", font=("Segoe UI", 12), bg=WHITE).pack(
    anchor="w"
)

transfer_amount_entry = tk.Entry(transfer_page, font=("Segoe UI", 14))
transfer_amount_entry.pack(pady=5)

tk.Button(
    transfer_page,
    text="Send (No Function Yet)",
    font=("Segoe UI", 14, "bold"),
    bg=PRIMARY_BLUE,
    fg=WHITE,
    bd=0,
    padx=20,
    pady=10,
).pack(pady=10)


# -----------------------------
#   SIDEBAR BUTTONS (PAGE SWITCH)
# -----------------------------
sections = ["Dashboard", "Deposit", "Withdraw", "Transfer"]

for sec in sections:
    btn = tk.Button(
        sidebar,
        text=sec,
        font=("Segoe UI", 12),
        bg=LIGHT_BLUE,
        fg=DARK_TEXT,
        bd=0,
        activebackground=PRIMARY_BLUE,
        activeforeground=WHITE,
        command=lambda s=sec: show_page(s),
    )
    btn.pack(fill="x", pady=5, padx=10)


# -----------------------------
#   DEFAULT PAGE
# -----------------------------
show_page("Dashboard")

root.mainloop()
