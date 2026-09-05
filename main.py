import tkinter as tk
from tkinter import messagebox, ttk

PRIMARY_BLUE = "#246BFD"
DEEP_BLUE = "#1748B5"
PALE_BLUE = "#EEF4FF"
BACKGROUND = "#F7F9FC"
WHITE = "#FFFFFF"
DARK_TEXT = "#172033"
MUTED_TEXT = "#6D7890"
BORDER = "#DCE4F2"

balance_xrp = 0.00

root = tk.Tk()
root.title("Bankly - Fast XRP Banking")
root.geometry("1024x650")
root.minsize(760, 500)
root.configure(bg=BACKGROUND)

styles = ttk.Style(root)
styles.theme_use("clam")
styles.configure("TEntry", padding=(12, 10), fieldbackground=WHITE, bordercolor=BORDER)
styles.configure("Page.TFrame", background=WHITE)
styles.configure("Card.TFrame", background=WHITE)
styles.configure(
    "Body.TLabel", background=WHITE, foreground=MUTED_TEXT, font=("Segoe UI", 11)
)
styles.configure(
    "Title.TLabel",
    background=WHITE,
    foreground=DARK_TEXT,
    font=("Segoe UI", 24, "bold"),
)
styles.configure(
    "CardTitle.TLabel",
    background=WHITE,
    foreground=DARK_TEXT,
    font=("Segoe UI", 14, "bold"),
)


class RoundedButton(tk.Canvas):
    """A scalable rounded button that keeps its own hover state."""

    def __init__(self, parent, text, command, width=180, height=44, **kwargs):
        super().__init__(
            parent,
            width=width,
            height=height,
            highlightthickness=0,
            bd=0,
            bg=WHITE,
            **kwargs,
        )
        self.command = command
        self.text = text
        self.fill = PRIMARY_BLUE
        self.hover_fill = DEEP_BLUE
        self.bind("<Configure>", lambda _event: self.draw(self.fill))
        self.bind("<Enter>", lambda _event: self.draw(self.hover_fill))
        self.bind("<Leave>", lambda _event: self.draw(self.fill))
        self.bind("<Button-1>", lambda _event: self.command())
        self.draw(self.fill)

    def draw(self, fill):
        self.delete("all")
        width = max(self.winfo_width(), int(self.cget("width")))
        height = max(self.winfo_height(), int(self.cget("height")))
        radius = min(14, height // 2)
        self.create_round_rect(2, 2, width - 2, height - 2, radius, fill)
        self.create_text(
            width / 2,
            height / 2,
            text=self.text,
            fill=WHITE,
            font=("Segoe UI", 10, "bold"),
        )

    def create_round_rect(self, x1, y1, x2, y2, radius, fill):
        diameter = radius * 2
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=fill, outline=fill)
        self.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=fill, outline=fill)
        self.create_arc(
            x1,
            y1,
            x1 + diameter,
            y1 + diameter,
            start=90,
            extent=90,
            fill=fill,
            outline=fill,
        )
        self.create_arc(
            x2 - diameter,
            y1,
            x2,
            y1 + diameter,
            start=0,
            extent=90,
            fill=fill,
            outline=fill,
        )
        self.create_arc(
            x2 - diameter,
            y2 - diameter,
            x2,
            y2,
            start=270,
            extent=90,
            fill=fill,
            outline=fill,
        )
        self.create_arc(
            x1,
            y2 - diameter,
            x1 + diameter,
            y2,
            start=180,
            extent=90,
            fill=fill,
            outline=fill,
        )


class RoundedFrame(tk.Canvas):
    """A resizable rounded surface that hosts regular Tk widgets."""

    def __init__(self, parent, fill, radius=20, margin=8, **kwargs):
        super().__init__(parent, bg=BACKGROUND, highlightthickness=0, bd=0, **kwargs)
        self.fill = fill
        self.radius = radius
        self.margin = margin
        self.content = tk.Frame(self, bg=fill)
        self.window_id = self.create_window(
            margin, margin, window=self.content, anchor="nw"
        )
        self.bind("<Configure>", self._resize)

    def _resize(self, event):
        width = max(1, event.width - self.margin * 2)
        height = max(1, event.height - self.margin * 2)
        self.itemconfigure(self.window_id, width=width, height=height)
        self.delete("surface")
        self.create_round_rect(
            1,
            1,
            event.width - 1,
            event.height - 1,
            min(self.radius, event.height // 2, event.width // 2),
            self.fill,
        )
        self.tag_lower("surface")

    def create_round_rect(self, x1, y1, x2, y2, radius, fill):
        diameter = radius * 2
        self.create_rectangle(
            x1 + radius, y1, x2 - radius, y2, fill=fill, outline=fill, tags="surface"
        )
        self.create_rectangle(
            x1, y1 + radius, x2, y2 - radius, fill=fill, outline=fill, tags="surface"
        )
        for box, start in (
            ((x1, y1, x1 + diameter, y1 + diameter), 90),
            ((x2 - diameter, y1, x2, y1 + diameter), 0),
            ((x2 - diameter, y2 - diameter, x2, y2), 270),
            ((x1, y2 - diameter, x1 + diameter, y2), 180),
        ):
            self.create_arc(
                *box, start=start, extent=90, fill=fill, outline=fill, tags="surface"
            )


header_surface = RoundedFrame(root, WHITE, radius=18, margin=4, height=76)
header_surface.grid(row=0, column=0, columnspan=2, sticky="ew", padx=12, pady=12)
header = header_surface.content
header.grid_propagate(False)
header.grid_propagate(False)
tk.Label(
    header, text="Bankly", font=("Segoe UI", 25, "bold"), fg=PRIMARY_BLUE, bg=WHITE
).pack(side="left", padx=28)
tk.Label(
    header,
    text="Your XRP wallet, made simple",
    font=("Segoe UI", 10),
    fg=MUTED_TEXT,
    bg=WHITE,
).pack(side="left", padx=4)

sidebar_surface = RoundedFrame(root, PALE_BLUE, radius=18, margin=4, width=210)
sidebar_surface.grid(row=1, column=0, sticky="nsew", padx=(12, 8), pady=(0, 12))
sidebar = sidebar_surface.content
sidebar.grid_propagate(False)
tk.Label(
    sidebar, text="WORKSPACE", font=("Segoe UI", 9, "bold"), fg=MUTED_TEXT, bg=PALE_BLUE
).pack(anchor="w", padx=22, pady=(28, 14))

main_surface = RoundedFrame(root, WHITE, radius=20, margin=1)
main_surface.grid(row=1, column=1, sticky="nsew", padx=(0, 12), pady=(0, 12))
main = ttk.Frame(main_surface.content, style="Page.TFrame", padding=(32, 28))
main.pack(fill="both", expand=True)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

pages = {}
nav_buttons = {}


def show_page(name):
    for page in pages.values():
        page.grid_remove()
    pages[name].grid(row=0, column=0, sticky="nsew")
    for section, button in nav_buttons.items():
        button.configure(
            bg=PRIMARY_BLUE if section == name else PALE_BLUE,
            fg=WHITE if section == name else DARK_TEXT,
        )


main.grid_rowconfigure(0, weight=1)
main.grid_columnconfigure(0, weight=1)

dashboard = ttk.Frame(main, style="Page.TFrame")
pages["Dashboard"] = dashboard
dashboard.grid_columnconfigure(0, weight=1)
ttk.Label(dashboard, text="Dashboard", style="Title.TLabel").grid(sticky="w")
ttk.Label(
    dashboard, text="A quick view of your wallet activity.", style="Body.TLabel"
).grid(row=1, sticky="w", pady=(4, 24))

balance_surface = RoundedFrame(dashboard, PRIMARY_BLUE, radius=18, margin=26)
balance_surface.grid(row=2, sticky="ew")
balance_card = balance_surface.content
balance_card.grid_columnconfigure(0, weight=1)
tk.Label(
    balance_card,
    text="TOTAL BALANCE",
    font=("Segoe UI", 9, "bold"),
    fg="#CFE0FF",
    bg=PRIMARY_BLUE,
).grid(row=0, column=0, sticky="w")
balance_label = tk.Label(
    balance_card,
    text=f"{balance_xrp:.2f} XRP",
    font=("Segoe UI", 30, "bold"),
    fg=WHITE,
    bg=PRIMARY_BLUE,
)
balance_label.grid(row=1, column=0, sticky="w", pady=(8, 0))
tk.Label(
    balance_card,
    text="Available to use",
    font=("Segoe UI", 10),
    fg="#CFE0FF",
    bg=PRIMARY_BLUE,
).grid(row=2, column=0, sticky="w", pady=(4, 0))


def make_form_page(name, title, description, action_text, action):
    page = ttk.Frame(main, style="Page.TFrame")
    pages[name] = page
    page.grid_columnconfigure(0, weight=1)
    ttk.Label(page, text=title, style="Title.TLabel").grid(sticky="w")
    ttk.Label(page, text=description, style="Body.TLabel").grid(
        row=1, sticky="w", pady=(4, 24)
    )
    card_surface = RoundedFrame(page, WHITE, radius=16, margin=26)
    card_surface.grid(row=2, sticky="ew")
    card = card_surface.content
    card.grid_columnconfigure(0, weight=1)
    ttk.Label(card, text="Amount (XRP)", style="CardTitle.TLabel").grid(sticky="w")
    entry = ttk.Entry(card, font=("Segoe UI", 12))
    entry.grid(row=1, sticky="ew", pady=(12, 18))
    RoundedButton(card, action_text, action, width=190).grid(row=2, sticky="w")
    return entry


def refresh_balance():
    balance_label.config(text=f"{balance_xrp:.2f} XRP")


def deposit_action():
    global balance_xrp
    try:
        amount = float(deposit_entry.get())
        if amount <= 0:
            raise ValueError
        balance_xrp += amount
        refresh_balance()
        deposit_entry.delete(0, tk.END)
        show_page("Dashboard")
    except ValueError:
        messagebox.showerror("Invalid amount", "Enter a positive XRP amount.")


def withdraw_action():
    global balance_xrp
    try:
        amount = float(withdraw_entry.get())
        if amount <= 0 or amount > balance_xrp:
            raise ValueError
        balance_xrp -= amount
        refresh_balance()
        withdraw_entry.delete(0, tk.END)
        show_page("Dashboard")
    except ValueError:
        messagebox.showerror(
            "Invalid amount", "Enter an amount within your available balance."
        )


deposit_entry = make_form_page(
    "Deposit",
    "Deposit XRP",
    "Add XRP to your Bankly balance.",
    "Confirm deposit",
    deposit_action,
)
withdraw_entry = make_form_page(
    "Withdraw",
    "Withdraw XRP",
    "Move XRP out of your Bankly balance.",
    "Confirm withdrawal",
    withdraw_action,
)

transfer_page = ttk.Frame(main, style="Page.TFrame")
pages["Transfer"] = transfer_page
transfer_page.grid_columnconfigure(0, weight=1)
ttk.Label(transfer_page, text="Send XRP", style="Title.TLabel").grid(sticky="w")
ttk.Label(
    transfer_page, text="Transfer XRP to another wallet.", style="Body.TLabel"
).grid(row=1, sticky="w", pady=(4, 24))
transfer_surface = RoundedFrame(transfer_page, WHITE, radius=16, margin=26)
transfer_surface.grid(row=2, sticky="ew")
transfer_card = transfer_surface.content
transfer_card.grid_columnconfigure(0, weight=1)
ttk.Label(transfer_card, text="Recipient wallet", style="CardTitle.TLabel").grid(
    sticky="w"
)
recipient_entry = ttk.Entry(transfer_card, font=("Segoe UI", 12))
recipient_entry.grid(row=1, sticky="ew", pady=(12, 18))
ttk.Label(transfer_card, text="Amount (XRP)", style="CardTitle.TLabel").grid(
    row=2, sticky="w"
)
transfer_amount_entry = ttk.Entry(transfer_card, font=("Segoe UI", 12))
transfer_amount_entry.grid(row=3, sticky="ew", pady=(12, 18))
RoundedButton(
    transfer_card,
    "Send XRP",
    lambda: messagebox.showinfo(
        "Coming soon", "Transfers will be available in a future release."
    ),
    width=150,
).grid(row=4, sticky="w")

for section in ("Dashboard", "Deposit", "Withdraw", "Transfer"):
    button = tk.Button(
        sidebar,
        text=section,
        font=("Segoe UI", 11, "bold"),
        anchor="w",
        padx=16,
        pady=10,
        bg=PALE_BLUE,
        fg=DARK_TEXT,
        activebackground=PRIMARY_BLUE,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda name=section: show_page(name),
    )
    button.pack(fill="x", padx=12, pady=3)
    nav_buttons[section] = button

show_page("Dashboard")
root.mainloop()
