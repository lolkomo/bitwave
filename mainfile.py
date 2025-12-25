import json
import time
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# --- Ensure data file exists and initialize with admin structure if missing ---
admin = {
    "loans": [],
    "reports": [],
    "bannedusers": [],
    "feedbacks": []
}

if not os.path.exists("userdatas2.json"):
    with open("userdatas2.json", "w") as f:
        json.dump({}, f)

# --- CLASS DEFINITION (Moved up so it can be called) ---
class mainmenu(ctk.CTk):
    def __init__(self, userdata):
        super().__init__()
        self.title("BitWave Banking")
        self.geometry("1900x975")
        self.minsize(900, 600)
        self.maxsize(1918, 1033)
        ctk.set_appearance_mode("dark")

        # Modern color palette
        self.colors = {
            "primary": "#5a2e7e",
            "secondary": "#340a58",
            "accent": "#723bd8",
            "card_bg": "#26093e",
            "success": "#2fa572",
            "danger": "#d32f2f",
            "warning": "#ed6c02",
            "text_primary": "#DABFF6",
            "text_secondary": "#b0b0b0",
            "hover": "#c96ce6",
        }

        # Extract user data with defaults
        user = userdata.get("username", "User")
        password = userdata.get("password", "")
        balance = userdata.get("balance", 0)
        creditscore = userdata.get("creditscore", 750)
        telephone = userdata.get("teleno", "N/A")
        loans = userdata.get("loans", [])
        emeratesid = userdata.get("emerateid", "N/A")
        account_number = userdata.get("accountno", "N/A")
        creditcard = userdata.get("creditcard", "N/A")
        status = userdata.get("status", "Active")

        # ============== MAIN CONTAINER ==============
        self.frame_options = ctk.CTkFrame(self, fg_color=self.colors["secondary"], corner_radius=0)
        self.frame_options.pack(fill="both", expand=True)

        # ============== MODERN HEADER BAR ==============
        header_frame = ctk.CTkFrame(self.frame_options, height=100, fg_color=self.colors["primary"], corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        welcome_label = ctk.CTkLabel(
            header_frame,
            text=f"👋 Welcome back, {user}",
            text_color=self.colors["text_primary"],
            font=('Bauhaus 93', 36)
        )
        welcome_label.pack(side="left", padx=40, pady=30)

        import datetime
        current_time = datetime.datetime.now().strftime("%B %d, %Y | %I:%M %p")
        time_label = ctk.CTkLabel(
            header_frame,
            text=f"🕐 {current_time}",
            text_color=self.colors["text_secondary"],
            font=('Cooper Black', 16)
        )
        time_label.pack(side="right", padx=40)

        # ============== MODERN TAB VIEW ==============
        self.tabs1 = ctk.CTkTabview(
            self.frame_options,
            fg_color=self.colors["secondary"],
            segmented_button_fg_color=self.colors["card_bg"],
            segmented_button_selected_color=self.colors["primary"],
            segmented_button_selected_hover_color=self.colors["accent"],
            text_color=self.colors["text_primary"],
            corner_radius=15
        )
        self.tabs1.pack(pady=15, padx=15, fill="both", expand=True)

        self.tabs1.add("🏠 Dashboard")
        self.tabs1.add("💸 Transfers & Payments")
        self.tabs1.add("📜 Transaction History")
        self.tabs1.add("🏡 Loans and credit")
        self.tabs1.add("👤 Profile & Settings")
        self.tabs1.add("🏧 ATM")
        self.tabs1.add("🛠 Support & Help")

        # ============== DASHBOARD TAB ==============
        dashboard_tab = self.tabs1.tab("🏠 Dashboard")
        dashboard_scroll = ctk.CTkScrollableFrame(dashboard_tab, fg_color="transparent")
        dashboard_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Hidden label for username reference
        self.dashtext = ctk.CTkLabel(dashboard_scroll, text=f"Welcome to BitWave Banking Dashboard {user}", font=('Arial', 1))
        self.dashtext.pack_forget()

        # Row 1: Balance and Credit Card
        row1_frame = ctk.CTkFrame(dashboard_scroll, fg_color="transparent")
        row1_frame.pack(fill="x", pady=(0, 20))
        row1_frame.grid_columnconfigure(0, weight=1)
        row1_frame.grid_columnconfigure(1, weight=1)

        # BALANCE CARD
        balance_card = ctk.CTkFrame(row1_frame, fg_color=self.colors["card_bg"], corner_radius=20, border_width=2, border_color=self.colors["accent"])
        balance_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(balance_card, text="💰 Current Balance", text_color=self.colors["text_secondary"], font=("Cooper Black", 22)).pack(pady=(30, 10))

        self.balance_label = ctk.CTkLabel(balance_card, text=f"{balance:,.2f} AED", font=("Bauhaus 93", 56), text_color=self.colors["text_primary"])
        self.balance_label.pack(pady=(10, 30))

        action_frame = ctk.CTkFrame(balance_card, fg_color="transparent")
        action_frame.pack(pady=(0, 20))

        ctk.CTkButton(action_frame, text="➕ Deposit", fg_color=self.colors["success"], hover_color="#258f5f", corner_radius=12, height=45, width=140, font=("Cooper Black", 16), command=lambda: self.tabs1.set("🏧 ATM")).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="➖ Withdraw", fg_color=self.colors["warning"], hover_color="#c55a02", corner_radius=12, height=45, width=140, font=("Cooper Black", 16), command=lambda: self.tabs1.set("🏧 ATM")).pack(side="left", padx=5)

        # CREDIT CARD CARD
        cc_card = ctk.CTkFrame(row1_frame, fg_color=self.colors["card_bg"], corner_radius=20, border_width=2, border_color=self.colors["accent"])
        cc_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(cc_card, text="💳 Credit Card", text_color=self.colors["text_secondary"], font=("Cooper Black", 22)).pack(pady=(30, 10))

        formatted_cc = f"{creditcard[:4]} {creditcard[4:8]} {creditcard[8:12]} {creditcard[12:]}" if len(str(creditcard)) == 16 else creditcard
        self.ccno = ctk.CTkLabel(cc_card, text=formatted_cc, text_color=self.colors["text_primary"], font=("Courier New", 38, "bold"))
        self.ccno.pack(pady=(10, 40))

        ctk.CTkLabel(cc_card, text="VISA DEBIT", text_color=self.colors["text_secondary"], font=("Cooper Black", 16)).pack(pady=(0, 20))

        # Row 2: Credit Score and Account Number
        row2_frame = ctk.CTkFrame(dashboard_scroll, fg_color="transparent")
        row2_frame.pack(fill="x", pady=(0, 20))
        row2_frame.grid_columnconfigure(0, weight=1)
        row2_frame.grid_columnconfigure(1, weight=1)

        # CREDIT SCORE CARD
        cs_card = ctk.CTkFrame(row2_frame, fg_color=self.colors["card_bg"], corner_radius=20, border_width=2, border_color=self.colors["success"] if creditscore >= 700 else self.colors["warning"])
        cs_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(cs_card, text="📊 Credit Score", text_color=self.colors["text_secondary"], font=("Cooper Black", 22)).pack(pady=(30, 10))

        self.csno = ctk.CTkLabel(cs_card, text=str(creditscore), text_color=self.colors["success"] if creditscore >= 700 else self.colors["warning"], font=("Bauhaus 93", 72))
        self.csno.pack(pady=(0, 10))

        status_text = "Excellent" if creditscore >= 750 else "Good" if creditscore >= 700 else "Fair"
        ctk.CTkLabel(cs_card, text=f"● {status_text}", text_color=self.colors["success"] if creditscore >= 700 else self.colors["warning"], font=("Cooper Black", 18)).pack(pady=(0, 30))

        # ACCOUNT NUMBER CARD
        acc_card = ctk.CTkFrame(row2_frame, fg_color=self.colors["card_bg"], corner_radius=20, border_width=2, border_color=self.colors["accent"])
        acc_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(acc_card, text="🏦 Account Number", text_color=self.colors["text_secondary"], font=("Cooper Black", 22)).pack(pady=(30, 10))

        self.acno = ctk.CTkLabel(acc_card, text=account_number, text_color=self.colors["text_primary"], font=("Courier New", 42, "bold"))
        self.acno.pack(pady=(10, 20))

        ctk.CTkLabel(acc_card, text=f"Status: {status}", text_color=self.colors["success"] if status.lower() == "active" else self.colors["warning"], font=("Cooper Black", 16)).pack(pady=(0, 30))

        # Row 3: Quick Stats
        stats_frame = ctk.CTkFrame(dashboard_scroll, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)

        active_loans = len(loans) if isinstance(loans, list) else 0
        quick_stats = [
            ("📱 Phone", telephone, self.colors["primary"]),
            ("🆔 Emirates ID", emeratesid[-4:] if len(str(emeratesid)) > 4 else emeratesid, self.colors["primary"]),
            ("💼 Active Loans", str(active_loans), self.colors["warning"])
        ]

        for i, (label, value, color) in enumerate(quick_stats):
            stat_card = ctk.CTkFrame(stats_frame, fg_color=self.colors["card_bg"], corner_radius=15, height=120)
            stat_card.grid(row=0, column=i, sticky="nsew", padx=7)
            stat_card.grid_propagate(False)
            ctk.CTkLabel(stat_card, text=label, text_color=self.colors["text_secondary"], font=("Cooper Black", 16)).pack(pady=(25, 5))
            ctk.CTkLabel(stat_card, text=value, text_color=color, font=("Bauhaus 93", 28)).pack(pady=(5, 25))

        # ============== TRANSFERS TAB ==============
        transfer_scroll = ctk.CTkScrollableFrame(self.tabs1.tab("💸 Transfers & Payments"), fg_color="transparent")
        transfer_scroll.pack(fill="both", expand=True, padx=20, pady=20)

        self.maketransctionframe = ctk.CTkFrame(transfer_scroll, fg_color=self.colors["card_bg"], corner_radius=20, border_width=2, border_color=self.colors["accent"])
        self.maketransctionframe.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.maketransctionframe, text="💸 Make a Transfer", text_color=self.colors["text_primary"], font=("Bauhaus 93", 48)).pack(pady=(30, 20))

        # Amount field
        amount_label = ctk.CTkLabel(self.maketransctionframe, text="Amount (AED)", text_color=self.colors["text_secondary"], font=("Cooper Black", 18))
        amount_label.pack(pady=(20, 5), padx=40, anchor="w")
        self.maketransctionframe.amount = ctk.CTkEntry(self.maketransctionframe, placeholder_text="Enter amount", text_color=self.colors["text_primary"], font=("Cooper Black", 28), width=800, height=60, corner_radius=15)
        self.maketransctionframe.amount.pack(pady=(0, 20), padx=40)

        # Recipient field
        to_label = ctk.CTkLabel(self.maketransctionframe, text="Recipient Username", text_color=self.colors["text_secondary"], font=("Cooper Black", 18))
        to_label.pack(pady=(20, 5), padx=40, anchor="w")
        self.maketransctionframe.to = ctk.CTkEntry(self.maketransctionframe, placeholder_text="Enter recipient username", text_color=self.colors["text_primary"], font=("Cooper Black", 28), width=800, height=60, corner_radius=15)
        self.maketransctionframe.to.pack(pady=(0, 20), padx=40)

        # Type selector
        type_label = ctk.CTkLabel(self.maketransctionframe, text="Transaction Type", text_color=self.colors["text_secondary"], font=("Cooper Black", 18))
        type_label.pack(pady=(20, 5), padx=40, anchor="w")
        self.maketransctionframe.type = ctk.CTkOptionMenu(self.maketransctionframe, values=["Transfer", "Payment"], text_color=self.colors["text_primary"], font=("Cooper Black", 24), width=800, height=60, corner_radius=15, fg_color=self.colors["primary"], button_color=self.colors["accent"], button_hover_color=self.colors["hover"])
        self.maketransctionframe.type.pack(pady=(0, 30), padx=40)

        # Submit button
        self.maketransctionframe.submit = ctk.CTkButton(self.maketransctionframe, text="🚀 Submit Transfer", text_color="white", font=("Cooper Black", 32), width=800, height=70, corner_radius=15, fg_color=self.colors["success"], hover_color="#258f5f", command=self.make_transaction)
        self.maketransctionframe.submit.pack(pady=(10, 40), padx=40)

        # ============== TRANSACTION HISTORY TAB ==============
        history_scroll = ctk.CTkScrollableFrame(self.tabs1.tab("📜 Transaction History"), fg_color="transparent")
        history_scroll.pack(fill="both", expand=True, padx=20, pady=20)

        # Transactions section
        self.transactions = ctk.CTkFrame(history_scroll, fg_color=self.colors["card_bg"], corner_radius=20, border_width=2, border_color=self.colors["accent"])
        self.transactions.pack(fill="both", expand=True, pady=(0, 20))

        ctk.CTkLabel(self.transactions, text="💳 Transaction History", text_color=self.colors["text_primary"], font=("Bauhaus 93", 40)).pack(pady=(20, 10), padx=20)

        # Style for treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", background=self.colors["secondary"], foreground=self.colors["text_primary"], fieldbackground=self.colors["secondary"], rowheight=35, font=("Segoe UI", 11))
        style.configure("Custom.Treeview.Heading", background=self.colors["primary"], foreground=self.colors["text_primary"], font=("Cooper Black", 13))
        style.map('Custom.Treeview', background=[('selected', self.colors["accent"])])

        self.transactions.tree = ttk.Treeview(self.transactions, columns=("Date", "Amount", "Type"), show="headings", style="Custom.Treeview", height=8)
        self.transactions.tree.heading("Date", text="Date")
        self.transactions.tree.heading("Amount", text="Amount")
        self.transactions.tree.heading("Type", text="Type")
        self.transactions.tree.column("Date", width=300)
        self.transactions.tree.column("Amount", width=200)
        self.transactions.tree.column("Type", width=200)
        self.transactions.tree.pack(pady=20, padx=20, fill="both", expand=True)

        # Loans section
        self.loansframe = ctk.CTkFrame(history_scroll, fg_color=self.colors["card_bg"], corner_radius=20, border_width=2, border_color=self.colors["warning"])
        self.loansframe.pack(fill="both", expand=True)

        ctk.CTkLabel(self.loansframe, text="🏡 Loans History", text_color=self.colors["text_primary"], font=("Bauhaus 93", 40)).pack(pady=(20, 10), padx=20)

        self.loansframe.tree = ttk.Treeview(self.loansframe, columns=("Date", "Amount", "Type"), show="headings", style="Custom.Treeview", height=8)
        self.loansframe.tree.heading("Date", text="Date")
        self.loansframe.tree.heading("Amount", text="Amount")
        self.loansframe.tree.heading("Type", text="Type")
        self.loansframe.tree.column("Date", width=300)
        self.loansframe.tree.column("Amount", width=200)
        self.loansframe.tree.column("Type", width=200)
        self.loansframe.tree.pack(pady=20, padx=20, fill="both", expand=True)

        # ============== LOANS TAB ==============
        loans_scroll = ctk.CTkScrollableFrame(self.tabs1.tab("🏡 Loans and credit"), fg_color="transparent")
        loans_scroll.pack(fill="both", expand=True, padx=20, pady=20)

        self.applyforloanframe = ctk.CTkFrame(loans_scroll, fg_color=self.colors["card_bg"], corner_radius=20, border_width=2, border_color=self.colors["warning"])
        self.applyforloanframe.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.applyforloanframe, text="🏡 Apply for a Loan", text_color=self.colors["text_primary"], font=("Bauhaus 93", 48)).pack(pady=(30, 20))

        # Loan amount
        loan_amt_label = ctk.CTkLabel(self.applyforloanframe, text="Loan Amount (AED)", text_color=self.colors["text_secondary"], font=("Cooper Black", 18))
        loan_amt_label.pack(pady=(20, 5), padx=40, anchor="w")
        self.applyforloanframe.amount = ctk.CTkEntry(self.applyforloanframe, placeholder_text="Enter loan amount", text_color=self.colors["text_primary"], font=("Cooper Black", 28), width=800, height=60, corner_radius=15)
        self.applyforloanframe.amount.pack(pady=(0, 20), padx=40)

        # Loan type
        loan_type_label = ctk.CTkLabel(self.applyforloanframe, text="Loan Type", text_color=self.colors["text_secondary"], font=("Cooper Black", 18))
        loan_type_label.pack(pady=(20, 5), padx=40, anchor="w")
        self.applyforloanframe.type = ctk.CTkOptionMenu(self.applyforloanframe, values=["Personal Loan", "Home Loan", "Car Loan"], text_color=self.colors["text_primary"], font=("Cooper Black", 24), width=800, height=60, corner_radius=15, fg_color=self.colors["primary"], button_color=self.colors["accent"], button_hover_color=self.colors["hover"])
        self.applyforloanframe.type.pack(pady=(0, 20), padx=40)

        # Duration
        duration_label = ctk.CTkLabel(self.applyforloanframe, text="Duration (months)", text_color=self.colors["text_secondary"], font=("Cooper Black", 18))
        duration_label.pack(pady=(20, 5), padx=40, anchor="w")
        self.applyforloanframe.duration = ctk.CTkEntry(self.applyforloanframe, placeholder_text="Enter duration in months", text_color=self.colors["text_primary"], font=("Cooper Black", 28), width=800, height=60, corner_radius=15)
        self.applyforloanframe.duration.pack(pady=(0, 30), padx=40)

        # Buttons
        btn_frame = ctk.CTkFrame(self.applyforloanframe, fg_color="transparent")
        btn_frame.pack(pady=(10, 40))

        self.applyforloanframe.submit = ctk.CTkButton(btn_frame, text="✓ Submit Application", text_color="white", font=("Cooper Black", 28), width=380, height=65, corner_radius=15, fg_color=self.colors["success"], hover_color="#258f5f", command=self.loan_application)
        self.applyforloanframe.submit.pack(side="left", padx=10)

        self.applyforloanframe.cancel = ctk.CTkButton(btn_frame, text="✗ Cancel", text_color="white", font=("Cooper Black", 28), width=380, height=65, corner_radius=15, fg_color=self.colors["danger"], hover_color="#9a2424")
        self.applyforloanframe.cancel.pack(side="left", padx=10)

        # ============== PROFILE TAB ==============
        profile_scroll = ctk.CTkScrollableFrame(self.tabs1.tab("👤 Profile & Settings"), fg_color="transparent")
        profile_scroll.pack(fill="both", expand=True, padx=20, pady=20)

        self.profileframe = ctk.CTkFrame(profile_scroll, fg_color=self.colors["card_bg"], corner_radius=20, border_width=2, border_color=self.colors["accent"])
        self.profileframe.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.profileframe, text="👤 Profile & Settings", text_color=self.colors["text_primary"], font=("Bauhaus 93", 48)).pack(pady=(30, 30))

        # Profile info in grid
        info_frame = ctk.CTkFrame(self.profileframe, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=40, pady=20)

        profile_data = [
            ("👤 Username:", user),
            ("🆔 Emirates ID:", emeratesid),
            ("📱 Telephone:", telephone),
            ("🏦 Account Number:", account_number),
            ("💳 Credit Card:", creditcard),
            ("💰 Balance:", f"{balance} AED"),
            ("📊 Credit Score:", str(creditscore)),
            ("✓ Status:", status)
        ]

        for label, value in profile_data:
            row = ctk.CTkFrame(info_frame, fg_color=self.colors["secondary"], corner_radius=10, height=60)
            row.pack(fill="x", pady=10)
            row.grid_propagate(False)

            ctk.CTkLabel(row, text=label, text_color=self.colors["text_secondary"], font=("Cooper Black", 20), anchor="w").pack(side="left", padx=20)
            ctk.CTkLabel(row, text=value, text_color=self.colors["text_primary"], font=("Courier New", 20, "bold"), anchor="e").pack(side="right", padx=20)

        # Action buttons
        btn_container = ctk.CTkFrame(self.profileframe, fg_color="transparent")
        btn_container.pack(pady=30)

        self.profileframe.change_password = ctk.CTkButton(btn_container, text="🔒 Change Password", text_color="white", font=("Cooper Black", 24), width=380, height=60, corner_radius=15, fg_color=self.colors["warning"], hover_color="#c55a02", command=self.change_password_window)
        self.profileframe.change_password.pack(side="left", padx=10)

        self.profileframe.deleteuser = ctk.CTkButton(btn_container, text="🗑 Delete Account", text_color="white", font=("Cooper Black", 24), width=380, height=60, corner_radius=15, fg_color=self.colors["danger"], hover_color="#9a2424")
        self.profileframe.deleteuser.pack(side="left", padx=10)

        # ============== ATM TAB ==============
        atm_scroll = ctk.CTkScrollableFrame(self.tabs1.tab("🏧 ATM"), fg_color="transparent")
        atm_scroll.pack(fill="both", expand=True, padx=20, pady=20)

        self.atmframe = ctk.CTkFrame(atm_scroll, fg_color=self.colors["card_bg"], corner_radius=20, border_width=2, border_color=self.colors["accent"])
        self.atmframe.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.atmframe, text="🏧 ATM Services", text_color=self.colors["text_primary"], font=("Bauhaus 93", 48)).pack(pady=(30, 20))

        # Current balance display
        balance_display = ctk.CTkFrame(self.atmframe, fg_color=self.colors["secondary"], corner_radius=15, height=100)
        balance_display.pack(fill="x", padx=40, pady=20)
        balance_display.pack_propagate(False)

        ctk.CTkLabel(balance_display, text="Current Balance:", text_color=self.colors["text_secondary"], font=("Cooper Black", 24)).pack(side="left", padx=30)
        self.atmframe.balance = ctk.CTkLabel(balance_display, text=f"{balance:,.2f} AED", text_color=self.colors["success"], font=("Bauhaus 93", 36))
        self.atmframe.balance.pack(side="right", padx=30)

        # Withdraw section
        withdraw_label = ctk.CTkLabel(self.atmframe, text="💸 Withdraw Amount", text_color=self.colors["text_secondary"], font=("Cooper Black", 18))
        withdraw_label.pack(pady=(30, 5), padx=40, anchor="w")
        self.atmframe.withdraw_amount = ctk.CTkEntry(self.atmframe, placeholder_text="Enter amount to withdraw", text_color=self.colors["text_primary"], font=("Cooper Black", 28), width=800, height=60, corner_radius=15)
        self.atmframe.withdraw_amount.pack(pady=(0, 20), padx=40)

        # Deposit section
        deposit_label = ctk.CTkLabel(self.atmframe, text="💰 Deposit Amount", text_color=self.colors["text_secondary"], font=("Cooper Black", 18))
        deposit_label.pack(pady=(20, 5), padx=40, anchor="w")
        self.atmframe.deposit_amount = ctk.CTkEntry(self.atmframe, placeholder_text="Enter amount to deposit", text_color=self.colors["text_primary"], font=("Cooper Black", 28), width=800, height=60, corner_radius=15)
        self.atmframe.deposit_amount.pack(pady=(0, 30), padx=40)

        # Action buttons
        atm_btn_frame = ctk.CTkFrame(self.atmframe, fg_color="transparent")
        atm_btn_frame.pack(pady=(10, 40))

        ctk.CTkButton(atm_btn_frame, text="📤 Withdraw", text_color="white", font=("Cooper Black", 28), width=380, height=65, corner_radius=15, fg_color=self.colors["warning"], hover_color="#c55a02", command=self.atm_transactions).pack(side="left", padx=10)
        ctk.CTkButton(atm_btn_frame, text="📥 Deposit", text_color="white", font=("Cooper Black", 28), width=380, height=65, corner_radius=15, fg_color=self.colors["success"], hover_color="#258f5f", command=self.atm_transactions).pack(side="left", padx=10)

        # ============== SUPPORT TAB ==============
        support_scroll = ctk.CTkScrollableFrame(self.tabs1.tab("🛠 Support & Help"), fg_color="transparent")
        support_scroll.pack(fill="both", expand=True, padx=20, pady=20)

        self.support_feedbackframe = ctk.CTkFrame(support_scroll, fg_color=self.colors["card_bg"], corner_radius=20, border_width=2, border_color=self.colors["accent"])
        self.support_feedbackframe.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.support_feedbackframe, text="🛠 Support & Feedback", text_color=self.colors["text_primary"], font=("Bauhaus 93", 48)).pack(pady=(30, 20))

        feedback_label = ctk.CTkLabel(self.support_feedbackframe, text="Share your feedback or report an issue:", text_color=self.colors["text_secondary"], font=("Cooper Black", 18))
        feedback_label.pack(pady=(20, 10), padx=40, anchor="w")

        self.support_feedbackframe.feedback_textbox = ctk.CTkTextbox(self.support_feedbackframe, text_color=self.colors["text_primary"], font=("Cooper Black", 18), width=800, height=400, corner_radius=15)
        self.support_feedbackframe.feedback_textbox.insert("1.0", "Enter your feedback here...")
        self.support_feedbackframe.feedback_textbox.pack(pady=(0, 30), padx=40)

        # Support buttons
        support_btn_frame = ctk.CTkFrame(self.support_feedbackframe, fg_color="transparent")
        support_btn_frame.pack(pady=(10, 20))

        self.support_feedbackframe.submit = ctk.CTkButton(support_btn_frame, text="📤 Submit Feedback", text_color="white", font=("Cooper Black", 26), width=380, height=60, corner_radius=15, fg_color=self.colors["success"], hover_color="#258f5f", command=self.support_feedback_submit)
        self.support_feedbackframe.submit.pack(side="left", padx=10)

        self.support_feedbackframe.cancel = ctk.CTkButton(support_btn_frame, text="✗ Clear", text_color="white", font=("Cooper Black", 26), width=180, height=60, corner_radius=15, fg_color=self.colors["danger"], hover_color="#9a2424", command=lambda: self.support_feedbackframe.feedback_textbox.delete("1.0", "end"))
        self.support_feedbackframe.cancel.pack(side="left", padx=10)

        self.support_feedbackframe.abtdev = ctk.CTkButton(self.support_feedbackframe, text="ℹ️ About Developer", text_color="white", font=("Cooper Black", 26), width=600, height=60, corner_radius=15, fg_color=self.colors["primary"], hover_color=self.colors["accent"], command=self.show_about_developer)
        self.support_feedbackframe.abtdev.pack(pady=(20, 40))

    def make_transaction(self):
        """Handle money transfers between users"""
        amount_str = self.maketransctionframe.amount.get()
        recipient = self.maketransctionframe.to.get()
        trans_type = self.maketransctionframe.type.get()

        if not amount_str or not recipient:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered!")
            return

        try:
            current_balance = float(self.balance_label.cget("text").split()[0].replace(",", ""))
        except Exception:
            current_balance = 0.0

        if amount > current_balance:
            messagebox.showerror("Error", "Insufficient balance!")
            return

        with open("userdatas2.json", "r") as f:
            userdatas2 = json.load(f)

        sender_username = self.dashtext.cget("text").split()[-1]

        if recipient not in userdatas2:
            messagebox.showerror("Error", "Recipient user not found!")
            return

        new_balance = current_balance - amount
        recipient_balance = userdatas2[recipient].get("balance", 0) + amount

        userdatas2[sender_username]["balance"] = new_balance
        userdatas2[recipient]["balance"] = recipient_balance

        transaction_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        userdatas2.setdefault(sender_username, {}).setdefault("transfers", []).append({
            "date": transaction_date,
            "amount": f"-{amount}",
            "type": f"{trans_type} to {recipient}"
        })

        userdatas2.setdefault(recipient, {}).setdefault("transfers", []).append({
            "date": transaction_date,
            "amount": f"+{amount}",
            "type": f"{trans_type} from {sender_username}"
        })

        with open("userdatas2.json", "w") as f:
            json.dump(userdatas2, f)

        self.balance_label.configure(text=f"{new_balance:,.2f} AED")

        self.maketransctionframe.amount.delete(0, 'end')
        self.maketransctionframe.to.delete(0, 'end')

        messagebox.showinfo("Success", f"Successfully transferred {amount} AED to {recipient}!")

    def loan_application(self):
        """Submit loan application"""
        loanamount = self.applyforloanframe.amount.get()
        loanduration = self.applyforloanframe.duration.get()
        loantype = self.applyforloanframe.type.get()
        loandate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if not loanamount or not loanduration:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        try:
            float(loanamount)
            int(loanduration)
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Check amount and duration.")
            return

        with open("userdatas2.json", "r") as f:
            userdatas2 = json.load(f)

        sender_username = self.dashtext.cget("text").split()[-1]
        userdatas2.setdefault(sender_username, {}).setdefault("loans", []).append({
            "date": loandate,
            "amount": loanamount,
            "type": loantype,
            "duration": loanduration,
            "status": "Pending"
        })

        with open("userdatas2.json", "w") as f:
            json.dump(userdatas2, f)

        self.applyforloanframe.amount.delete(0, 'end')
        self.applyforloanframe.duration.delete(0, 'end')

        messagebox.showinfo("Success", "Loan application submitted successfully!")

    def atm_transactions(self):
        """Handle ATM withdraw and deposit"""
        withdraw_amount = self.atmframe.withdraw_amount.get()
        deposit_amount = self.atmframe.deposit_amount.get()

        try:
            current_balance = float(self.balance_label.cget("text").split()[0].replace(",", ""))
        except Exception:
            current_balance = 0.0

        new_balance = current_balance

        if withdraw_amount:
            try:
                withdraw_val = float(withdraw_amount)
                if withdraw_val <= 0:
                    messagebox.showerror("Error", "Withdraw amount must be greater than 0!")
                    return
                if withdraw_val > current_balance:
                    messagebox.showerror("Error", "Insufficient balance for withdrawal.")
                    return
                new_balance = current_balance - withdraw_val
                self.balance_label.configure(text=f"{new_balance:,.2f} AED")
                self.atmframe.balance.configure(text=f"{new_balance:,.2f} AED")
                messagebox.showinfo("Success", f"Withdrawal of {withdraw_val} AED completed successfully!")
                self.atmframe.withdraw_amount.delete(0, 'end')
            except ValueError:
                messagebox.showerror("Error", "Invalid withdraw amount!")
                return

        if deposit_amount:
            try:
                deposit_val = float(deposit_amount)
                if deposit_val <= 0:
                    messagebox.showerror("Error", "Deposit amount must be greater than 0!")
                    return
                new_balance = new_balance + deposit_val
                self.balance_label.configure(text=f"{new_balance:,.2f} AED")
                self.atmframe.balance.configure(text=f"{new_balance:,.2f} AED")
                messagebox.showinfo("Success", f"Deposit of {deposit_val} AED completed successfully!")
                self.atmframe.deposit_amount.delete(0, 'end')
            except ValueError:
                messagebox.showerror("Error", "Invalid deposit amount!")
                return

        with open("userdatas2.json", "r") as f:
            userdatas2 = json.load(f)

        sender_username = self.dashtext.cget("text").split()[-1]
        userdatas2.setdefault(sender_username, {})["balance"] = new_balance

        with open("userdatas2.json", "w") as f:
            json.dump(userdatas2, f)

    def transaction_history_load(self):
        """Load transaction history"""
        with open("userdatas2.json", "r") as f:
            userdatas2 = json.load(f)
        transactions = userdatas2[self.dashtext.cget("text").split()[-1]].get("transfers", [])
        for transaction in transactions:
            self.transactions.tree.insert("", "end", values=(transaction["date"], transaction["amount"], transaction["type"]))

    def loan_history_load(self):
        """Load loan history"""
        with open("userdatas2.json", "r") as f:
            userdatas2 = json.load(f)
        loans = userdatas2[self.dashtext.cget("text").split()[-1]].get("loans", [])
        for loan in loans:
            self.loansframe.tree.insert("", "end", values=(loan["date"], loan["amount"], loan["type"]))

    def support_feedback_submit(self):
        """Submit support feedback"""
        feedback_text = self.support_feedbackframe.feedback_textbox.get("1.0", "end-1c")
        feedback_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if not feedback_text or feedback_text.strip() == "Enter your feedback here...":
            messagebox.showerror("Error", "Please enter your feedback!")
            return

        with open("userdatas2.json", "r") as f:
            userdatas2 = json.load(f)
        sender_username = self.dashtext.cget("text").split()[-1]
        userdatas2.setdefault(sender_username, {}).setdefault("feedbacks", []).append({
            "date": feedback_date,
            "feedback": feedback_text
        })
        with open("userdatas2.json", "w") as f:
            json.dump(userdatas2, f)

        self.support_feedbackframe.feedback_textbox.delete("1.0", "end")
        messagebox.showinfo("Success", "Feedback submitted successfully!")

    def change_password_window(self):
        """Open password change window"""
        password_win = ctk.CTkToplevel(self)
        password_win.title("Change Password")
        password_win.geometry("600x500")
        password_win.resizable(False, False)
        password_win.grab_set()

        title_label = ctk.CTkLabel(password_win, text="🔒 Change Password", text_color="#DABFF6", font=("Bauhaus 93", 40))
        title_label.pack(pady=30)

        current_pass_label = ctk.CTkLabel(password_win, text="Current Password:", text_color="#DABFF6", font=("Cooper Black", 18))
        current_pass_label.pack(pady=(20, 5))
        current_pass_entry = ctk.CTkEntry(password_win, width=400, height=50, font=("Cooper Black", 16), show="*", corner_radius=12)
        current_pass_entry.pack(pady=5)

        new_pass_label = ctk.CTkLabel(password_win, text="New Password:", text_color="#DABFF6", font=("Cooper Black", 18))
        new_pass_label.pack(pady=(20, 5))
        new_pass_entry = ctk.CTkEntry(password_win, width=400, height=50, font=("Cooper Black", 16), show="*", corner_radius=12)
        new_pass_entry.pack(pady=5)

        confirm_pass_label = ctk.CTkLabel(password_win, text="Confirm New Password:", text_color="#DABFF6", font=("Cooper Black", 18))
        confirm_pass_label.pack(pady=(20, 5))
        confirm_pass_entry = ctk.CTkEntry(password_win, width=400, height=50, font=("Cooper Black", 16), show="*", corner_radius=12)
        confirm_pass_entry.pack(pady=5)

        def submit_password_change():
            current_password = current_pass_entry.get()
            new_password = new_pass_entry.get()
            confirm_password = confirm_pass_entry.get()

            if not current_password or not new_password or not confirm_password:
                messagebox.showerror("Error", "All fields are required!")
                return

            username = self.dashtext.cget("text").split()[-1]

            with open("userdatas2.json", "r") as f:
                userdatas2 = json.load(f)

            if userdatas2[username]['password'] != current_password:
                messagebox.showerror("Error", "Current password is incorrect!")
                return

            if new_password != confirm_password:
                messagebox.showerror("Error", "New passwords do not match!")
                return

            if len(new_password) < 8:
                messagebox.showerror("Error", "Password must be at least 8 characters long!")
                return

            userdatas2[username]['password'] = new_password

            with open("userdatas2.json", "w") as f:
                json.dump(userdatas2, f)

            messagebox.showinfo("Success", "Password changed successfully!")
            password_win.destroy()

        submit_btn = ctk.CTkButton(password_win, text="Change Password", text_color="white", font=("Cooper Black", 22), width=400, height=55, corner_radius=12, fg_color="#2fa572", hover_color="#258f5f", command=submit_password_change)
        submit_btn.pack(pady=30)

    def show_about_developer(self):
        """Display developer information"""
        about_text = (
            "BitWave Banking System\n\n"
            "Developed by: Nihan & Alvin\n"
            "Class: 11 CS Project\n"
            "Year: 2025\n\n"
            "This application showcases core banking features such as\n"
            "dashboards, transactions, loans, ATM utilities, and support."
        )
        messagebox.showinfo("About Developer", about_text)



# --- HELPER FUNCTION (Replaces 'from ex import...') ---
def open_user_window(data):
    app = mainmenu(data)
    app.mainloop()

# FIRST SUBMIT (rename, do not overwrite)
def submit_empty_check():
    if userentry.get() == '' or passentry.get() == '':
        messagebox.showwarning('Empty fields', 'Please enter both username and password')
        return

# LOGIN FUNCTION
def submit():
    with open('userdatas2.json', 'r') as f:
        userdatas2 = json.load(f)

    user = userentry.get()
    password = passentry.get()
    
    if user=="admin" and password == "admin123":
        login.destroy()
        app = AdminApp()
        app.mainloop()
    elif user in userdatas2:
        # Check if account is banned first
        if userdatas2[user].get("status") == "banned":
            messagebox.showerror('Login failed', 'Your account has been banned, please contact support for more information')
        elif userdatas2[user]['password'] == password:
            messagebox.showinfo('Login success', 'You have successfully logged in')
            login.destroy()
            open_user_window(userdatas2[user])
        else:
            messagebox.showerror('Login failed', 'Incorrect password')
    else:
        messagebox.showinfo('User not found', 'The user you have entered is not found, to fix this just signup')





# SIGNUP FUNCTION
def signup():
    user_win = ctk.CTkToplevel()
    user_win.title("user data")
    user_win.geometry('1350x750')
    user_win.resizable(False, False)

    def data_collection():
        username_ = usernamec.get()
        password_ = passwordc.get()
        emirateid_ = emirateid.get()
        creditcard_ = creditcard.get()
        teleno_ = teleno.get()
        accountno_ = accountno.get()
        plan_ = plan.get()

        balance = 0
        transfers = []

        with open('userdatas2.json', 'r') as f:
            usersdata = json.load(f)

        # Extract lists
        users = [data["username"] for data in usersdata.values()] if usersdata else []

        userdata = {
            "username": username_,
            "password": password_,
            "emerateid": emirateid_,
            "creditcard": creditcard_,
            "teleno": teleno_,
            "accountno": accountno_,
            "plan": plan_,
            "balance": balance,
            "transfers": transfers
        }

        # VALIDATION (unchanged)
        if username_ == '' or password_ == '' or emirateid_ == '' or creditcard_ == '' or teleno_ == '' or accountno_ == '' or plan_ == '':
            messagebox.showwarning('incomplete data', 'please fill all the fields')
            return

        if username_ in users:
            messagebox.showwarning('duplicate username', 'this username is already taken')
            return
        if emirateid_ != '' and len(emirateid_) != 15:
            messagebox.showwarning('invalid emirate id', 'emirate id must be 15 characters long')
        elif creditcard_ != '' and len(creditcard_) != 16:
            messagebox.showwarning('invalid credit card number', 'credit card number must be 16 digits long')
        elif teleno_ != '' and len(teleno_) != 10:
            messagebox.showwarning('invalid telephone number', 'telephone number must be 10 digits long')
        elif accountno_ != '' and len(accountno_) != 12:
            messagebox.showwarning('invalid account number', 'account number must be 12 digits long')
        elif password_ != '' and len(password_) != 8:
            messagebox.showwarning('weak password', 'password must be at least 8 characters long')
        elif creditcard_ != '' and not creditcard_.isdigit():
            messagebox.showwarning('invalid credit card number', 'credit card number must contain only digits')
        elif teleno_ != '' and not teleno_.isdigit():
            messagebox.showwarning('invalid telephone number', 'telephone number must contain only digits')
        elif accountno_ != '' and not accountno_.isdigit():
            messagebox.showwarning('invalid account number', 'account number must contain only digits')
        elif creditcard_ in (userdata["creditcard"] for userdata in usersdata.values()):
            messagebox.showwarning('credit card exists', 'the credit card number you have entered already exists, please check again')
        elif teleno_ in (userdata["teleno"] for userdata in usersdata.values()):
            messagebox.showwarning('telephone number exists', 'the telephone number you have entered already exists, please check again')
        elif accountno_ in (userdata["accountno"] for userdata in usersdata.values()):
            messagebox.showwarning('account number exists', 'the account number you have entered already exists, please check again')
        elif emirateid_ in (userdata["emerateid"] for userdata in usersdata.values()):
            messagebox.showwarning('emirate id exists', 'the emirate id you have entered already exists, please check again, if you are sure it\'s correct please contact support')

        # Save user
        usersdata[username_] = userdata

        with open('userdatas2.json', 'w') as f:
            json.dump(usersdata, f)

        messagebox.showinfo("Success", "Account created successfully!")
        user_win.destroy()



    # Safe image loading
    try:
        bgimage2 = ctk.CTkImage(light_image=Image.open('bgimage2.png'),
                                dark_image=Image.open('bgimage2.png'), size=(1350, 750))
        bg2 = ctk.CTkLabel(user_win, image=bgimage2, text="")
        bg2.pack()
    except Exception:
        bg2 = ctk.CTkLabel(user_win, text="Background Image Missing", fg_color="#340a58")
        bg2.pack(fill="both", expand=True)

    usernamec = ctk.CTkEntry(user_win, width=360, height=45, corner_radius=20, bg_color='#340a58',
                             font=('Gabriola', 23), fg_color='#723bd8')
    usernamec.place(x=330, y=130)
    passwordc = ctk.CTkEntry(user_win, width=360, height=30, corner_radius=20, bg_color='#340a58',
                             font=('Gabriola', 23), fg_color='#723bd8')
    passwordc.place(x=330, y=219)
    emirateid = ctk.CTkEntry(user_win, width=360, height=30, corner_radius=20, bg_color='#340a58',
                             font=('Gabriola', 23), fg_color='#723bd8')
    emirateid.place(x=330, y=310)
    creditcard = ctk.CTkEntry(user_win, width=360, height=45, corner_radius=20, bg_color='#340a58',
                              font=('Gabriola', 23), fg_color='#723bd8')
    creditcard.place(x=360, y=660)
    teleno = ctk.CTkEntry(user_win, width=360, height=45, corner_radius=20, bg_color='#340a58',
                          font=('Gabriola', 23), fg_color='#723bd8')
    teleno.place(x=330, y=490)
    accountno = ctk.CTkEntry(user_win, width=360, height=45, corner_radius=20, bg_color='#340a58',
                             font=('Gabriola', 23), fg_color='#723bd8')
    accountno.place(x=330, y=400)
    plan = ctk.CTkOptionMenu(user_win, values=["Lite – Simple and fast",
                                               "Pro – Enhanced tools",
                                               "Elite – Exclusive financial insights",
                                               "Infinity – No limits, full access",
                                               "Omni – All-in-one premium experience"],
                             width=360, height=30, corner_radius=20, bg_color='#5a2e7e',
                             font=('Gabriola', 23), fg_color='#723bd8', hover=True)
    plan.place(x=330, y=580)
    saveb = ctk.CTkButton(user_win, width=610, height=45, corner_radius=20, bg_color='#340a58',
                          text='save', fg_color='#5a2e7e', hover_color='#c96ce6',
                          font=('Gabriola', 30), command=data_collection)
    saveb.place(x=730, y=650)
    agree = ctk.CTkCheckBox(user_win, text='i agree to the terms and conditions', font=('Gabriola', 35),
                            bg_color='#5a2e7e', hover_color='#723bd8')
    agree.place(x=740, y=560)
    user_win.mainloop()



# --- LOGIN UI ---
login = ctk.CTk()
login.title("Login")
login.geometry("1272x677")
login.resizable(False, False)

try:
    icon = tk.PhotoImage(file='logo.png')
    login.iconphoto(True, icon)
    bgimage = tk.PhotoImage(file='bg2.png')
    bg = ctk.CTkLabel(login, image=bgimage, text=" ")
    bg.pack()
except Exception:
    # Fallback if images are missing
    bg = ctk.CTkLabel(login, text="Background Image Missing", font=('Arial', 20))
    bg.pack(pady=50)

logintext = ctk.CTkLabel(login, text='login', font=('Gabriola', 48,), bg_color='#7c5ecf')
logintext.place(x=900, y=62)
userentry = ctk.CTkEntry(login, width=360, height=45, corner_radius=20, bg_color='#745dcd',
                         font=('Gabriola', 23))
userentry.place(x=861, y=174)
passentry = ctk.CTkEntry(login, width=360, height=45, corner_radius=20, bg_color='#745dcd',
                         font=('Gabriola', 23), show="*")
passentry.place(x=858, y=288)
submitb = ctk.CTkButton(login, width=493, height=60, corner_radius=20, bg_color='#9362d6',
                        text='submit', fg_color='#014aad', hover_color='#c96ce6',
                        font=('Gabriola', 38), command=submit)
submitb.place(x=692, y=561)

signupb = ctk.CTkButton(login, width=493, height=60, corner_radius=20, bg_color='#9362d6',
                        text='signup', fg_color='#014aad', hover_color='#c96ce6',
                        font=('Gabriola', 38), command=signup)
signupb.place(x=692, y=467)
with open("userdatas2.json", "r") as f:
    usersdatas = json.load(f)
#admin app
class AdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BitWave Banking - Admin Panel")
        self.geometry("1900x975")
        
        # Modern color scheme matching your banking theme
        self.colors = {
            "primary": "#5a2e7e",
            "secondary": "#340a58",
            "accent": "#723bd8",
            "success": "#2fa572",
            "danger": "#d32f2f",
            "warning": "#ed6c02",
            "bg_dark": "#1a1a1a",
            "bg_card": "#26093e",
            "text_primary": "#DABFF6",
            "text_secondary": "#b0b0b0",
            "hover": "#c96ce6"
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_container = ctk.CTkFrame(self, fg_color=self.colors["bg_dark"])
        main_container.pack(fill="both", expand=True)
        
        # Header with gradient effect
        header = ctk.CTkFrame(main_container, fg_color=self.colors["primary"], height=90, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        header_title = ctk.CTkLabel(
            header, 
            text="🏦 BitWave Admin Dashboard", 
            font=("Bauhaus 93", 38),
            text_color=self.colors["text_primary"]
        )
        header_title.pack(side="left", padx=40, pady=25)
        
        # Current time
        import datetime
        current_time = datetime.datetime.now().strftime("%B %d, %Y - %I:%M %p")
        time_label = ctk.CTkLabel(
            header,
            text=f"🕐 {current_time}",
            font=("Cooper Black", 16),
            text_color=self.colors["text_secondary"]
        )
        time_label.pack(side="right", padx=40)
        
        # Tabview
        self.tabs = ctk.CTkTabview(
            main_container,
            fg_color=self.colors["bg_dark"],
            segmented_button_fg_color=self.colors["secondary"],
            segmented_button_selected_color=self.colors["primary"],
            segmented_button_selected_hover_color=self.colors["accent"],
            text_color=self.colors["text_primary"]
        )
        self.tabs.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Add tabs with icons
        self.tabs.add("👥 Users")
        self.tabs.add("💳 Transactions")
        self.tabs.add("📋 Logs")
        self.tabs.add("📊 Reports")
        self.tabs.add("🚫 Management")
        self.tabs.add("💬 Feedback")
        
        # Setup each tab
        self.setup_users_tab()
        self.setup_transactions_tab()
        self.setup_logs_tab()
        self.setup_reports_tab()
        self.setup_banning_tab()
        self.setup_feedback_tab()
    
    def setup_users_tab(self):
        """Enhanced users tab"""
        tab = self.tabs.tab("👥 Users")
        
        # Header card
        header_card = ctk.CTkFrame(tab, fg_color=self.colors["bg_card"], corner_radius=15, height=80)
        header_card.pack(fill="x", padx=20, pady=20)
        header_card.pack_propagate(False)
        
        ctk.CTkLabel(
            header_card,
            text="User Database Management",
            font=("Cooper Black", 26),
            text_color=self.colors["text_primary"]
        ).pack(side="left", padx=25)
        
        ctk.CTkButton(
            header_card,
            text="🔄 Refresh",
            command=self.refresh_users,
            fg_color=self.colors["accent"],
            hover_color=self.colors["hover"],
            corner_radius=10,
            width=140,
            height=45,
            font=("Cooper Black", 16)
        ).pack(side="right", padx=25)
        
        # Table card
        table_card = ctk.CTkFrame(tab, fg_color=self.colors["bg_card"], corner_radius=15)
        table_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Configure ttk style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
            background=self.colors["secondary"],
            foreground=self.colors["text_primary"],
            fieldbackground=self.colors["secondary"],
            rowheight=35,
            font=("Segoe UI", 11)
        )
        style.configure("Custom.Treeview.Heading",
            background=self.colors["primary"],
            foreground=self.colors["text_primary"],
            font=("Cooper Black", 13)
        )
        style.map('Custom.Treeview', 
            background=[('selected', self.colors["accent"])],
            foreground=[('selected', '#ffffff')]
        )
        
        # Tree container
        tree_container = ctk.CTkFrame(table_card, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        self.tree = ttk.Treeview(
            tree_container,
            columns=("Username", "Phone", "Emirates ID", "Account No", "Balance", "Status", "Plan"),
            show="headings",
            height=18,
            style="Custom.Treeview"
        )
        
        # Column configuration
        columns = {
            "Username": 150,
            "Phone": 130,
            "Emirates ID": 140,
            "Account No": 140,
            "Balance": 130,
            "Status": 110,
            "Plan": 250
        }
        
        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        self.load_users()
    
    def setup_transactions_tab(self):
        """Enhanced transactions tab"""
        tab = self.tabs.tab("💳 Transactions")
        
        # Header
        header_card = ctk.CTkFrame(tab, fg_color=self.colors["bg_card"], corner_radius=15, height=80)
        header_card.pack(fill="x", padx=20, pady=20)
        header_card.pack_propagate(False)
        
        ctk.CTkLabel(
            header_card,
            text="Transaction History Viewer",
            font=("Cooper Black", 26),
            text_color=self.colors["text_primary"]
        ).pack(side="left", padx=25)
        
        ctk.CTkButton(
            header_card,
            text="🔄 Refresh",
            command=self.load_transactions,
            fg_color=self.colors["accent"],
            hover_color=self.colors["hover"],
            corner_radius=10,
            width=140,
            height=45,
            font=("Cooper Black", 16)
        ).pack(side="right", padx=25)
        
        # Table card
        table_card = ctk.CTkFrame(tab, fg_color=self.colors["bg_card"], corner_radius=15)
        table_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        tree_container = ctk.CTkFrame(table_card, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        self.transactionstree = ttk.Treeview(
            tree_container,
            columns=("Username", "Phone", "Date", "Amount", "Type", "To/From"),
            show="headings",
            height=18,
            style="Custom.Treeview"
        )
        
        columns = {
            "Username": 160,
            "Phone": 140,
            "Date": 200,
            "Amount": 130,
            "Type": 120,
            "To/From": 160
        }
        
        for col, width in columns.items():
            self.transactionstree.heading(col, text=col)
            self.transactionstree.column(col, width=width, anchor="center")
        
        y_scroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.transactionstree.yview)
        x_scroll = ttk.Scrollbar(tree_container, orient="horizontal", command=self.transactionstree.xview)
        self.transactionstree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        self.transactionstree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        self.load_transactions()
    
    def setup_logs_tab(self):
        """Enhanced logs tab"""
        tab = self.tabs.tab("📋 Logs")
        
        header_card = ctk.CTkFrame(tab, fg_color=self.colors["bg_card"], corner_radius=15, height=80)
        header_card.pack(fill="x", padx=20, pady=20)
        header_card.pack_propagate(False)
        
        ctk.CTkLabel(
            header_card,
            text="System Activity Logs",
            font=("Cooper Black", 26),
            text_color=self.colors["text_primary"]
        ).pack(side="left", padx=25)
        
        table_card = ctk.CTkFrame(tab, fg_color=self.colors["bg_card"], corner_radius=15)
        table_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        tree_container = ctk.CTkFrame(table_card, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        self.logstree = ttk.Treeview(
            tree_container,
            columns=("Username", "Phone", "Emirates ID", "Timestamp", "Action", "Details"),
            show="headings",
            height=18,
            style="Custom.Treeview"
        )
        
        columns = {
            "Username": 140,
            "Phone": 130,
            "Emirates ID": 140,
            "Timestamp": 190,
            "Action": 120,
            "Details": 350
        }
        
        for col, width in columns.items():
            self.logstree.heading(col, text=col)
            self.logstree.column(col, width=width, anchor="w" if col == "Details" else "center")
        
        y_scroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.logstree.yview)
        x_scroll = ttk.Scrollbar(tree_container, orient="horizontal", command=self.logstree.xview)
        self.logstree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        self.logstree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
    
    def setup_reports_tab(self):
        """Dashboard-style reports tab"""
        tab = self.tabs.tab("📊 Reports")
        
        # Header
        header_card = ctk.CTkFrame(tab, fg_color=self.colors["bg_card"], corner_radius=15, height=80)
        header_card.pack(fill="x", padx=20, pady=20)
        header_card.pack_propagate(False)
        
        ctk.CTkLabel(
            header_card,
            text="System Analytics & Reports",
            font=("Cooper Black", 26),
            text_color=self.colors["text_primary"]
        ).pack(side="left", padx=25)
        
        ctk.CTkButton(
            header_card,
            text="🔄 Refresh",
            command=self.refresh_reports,
            fg_color=self.colors["accent"],
            hover_color=self.colors["hover"],
            corner_radius=10,
            width=140,
            height=45,
            font=("Cooper Black", 16)
        ).pack(side="right", padx=25)
        
        # Scrollable content area
        self.reportsframe = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        self.reportsframe.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Load data
        with open("userdatas2.json", "r") as f:
            usersdatas_report = json.load(f)
        
        total_users = len(usersdatas_report)
        banned_users = len([u for u in usersdatas_report.values() if u.get("status", "active") == "banned"])
        total_money = sum(float(u.get("balance", 0)) for u in usersdatas_report.values())
        
        total_loans = 0
        total_loan_amount = 0
        for user in usersdatas_report.values():
            user_loans = user.get("loans", [])
            if isinstance(user_loans, list):
                total_loans += len(user_loans)
                for loan in user_loans:
                    if isinstance(loan, dict):
                        total_loan_amount += float(loan.get("amount", 0))
        
        total_transactions = sum(len(u.get("transfers", [])) for u in usersdatas_report.values())
        active_users = total_users - banned_users
        
        # Create metric cards
        metrics = [
            ("👥 Total Users", str(total_users), self.colors["primary"], "users"),
            ("✅ Active Users", str(active_users), self.colors["success"], "active"),
            ("🚫 Banned Users", str(banned_users), self.colors["danger"], "banned"),
            ("💰 System Balance", f"{total_money:,.2f} AED", self.colors["accent"], "balance"),
            ("📊 Total Loans", f"{total_loans} Loans", self.colors["warning"], "loans"),
            ("💵 Loan Amount", f"{total_loan_amount:,.2f} AED", self.colors["warning"], "loan_amt"),
            ("💳 Transactions", str(total_transactions), self.colors["primary"], "trans")
        ]
        
        # Store references for refresh
        self.report_widgets = {}
        
        for i, (title, value, color, key) in enumerate(metrics):
            card = ctk.CTkFrame(
                self.reportsframe, 
                fg_color=self.colors["bg_card"], 
                corner_radius=15,
                height=160
            )
            card.grid(row=i//2, column=i%2, padx=15, pady=15, sticky="ew")
            card.grid_propagate(False)
            
            # Icon/Title
            ctk.CTkLabel(
                card,
                text=title,
                font=("Cooper Black", 20),
                text_color=self.colors["text_secondary"]
            ).pack(pady=(30, 10))
            
            # Value
            value_label = ctk.CTkLabel(
                card,
                text=value,
                font=("Bauhaus 93", 34),
                text_color=color
            )
            value_label.pack(pady=(0, 30))
            
            self.report_widgets[key] = value_label
        
        self.reportsframe.grid_columnconfigure(0, weight=1)
        self.reportsframe.grid_columnconfigure(1, weight=1)
    
    def setup_banning_tab(self):
        """User management tab"""
        tab = self.tabs.tab("🚫 Management")
        
        header_card = ctk.CTkFrame(tab, fg_color=self.colors["bg_card"], corner_radius=15, height=80)
        header_card.pack(fill="x", padx=20, pady=20)
        header_card.pack_propagate(False)
        
        ctk.CTkLabel(
            header_card,
            text="User Status Management",
            font=("Cooper Black", 26),
            text_color=self.colors["text_primary"]
        ).pack(side="left", padx=25)
        
        ctk.CTkButton(
            header_card,
            text="🔄 Refresh",
            command=self.refresh_banning_frame,
            fg_color=self.colors["accent"],
            hover_color=self.colors["hover"],
            corner_radius=10,
            width=140,
            height=45,
            font=("Cooper Black", 16)
        ).pack(side="right", padx=25)
        
        self.banningframe = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        self.banningframe.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.refresh_banning_frame()
    
    def setup_feedback_tab(self):
        """Feedback display tab"""
        tab = self.tabs.tab("💬 Feedback")
        
        header_card = ctk.CTkFrame(tab, fg_color=self.colors["bg_card"], corner_radius=15, height=80)
        header_card.pack(fill="x", padx=20, pady=20)
        header_card.pack_propagate(False)
        
        ctk.CTkLabel(
            header_card,
            text="User Feedback & Support",
            font=("Cooper Black", 26),
            text_color=self.colors["text_primary"]
        ).pack(side="left", padx=25)
        
        feedback_card = ctk.CTkFrame(tab, fg_color=self.colors["bg_card"], corner_radius=15)
        feedback_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.feedback_text = ctk.CTkTextbox(
            feedback_card,
            font=("Consolas", 13),
            wrap="word",
            fg_color=self.colors["secondary"]
        )
        self.feedback_text.pack(fill="both", expand=True, padx=25, pady=25)
        
        self.load_feedback()
    
    # Data loading methods
    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        with open("userdatas2.json", "r") as f:
            usersdatas_load = json.load(f)
        
        for username, user in usersdatas_load.items():
            status = user.get("status", "active")
            tags = ("banned",) if status == "banned" else ("active",)
            
            self.tree.insert("", tk.END, values=(
                user.get("username", username),
                user.get("teleno", "N/A"),
                user.get("emerateid", "N/A"),
                user.get("accountno", "N/A"),
                f"{user.get('balance', 0):.2f}",
                status.upper(),
                user.get("plan", "N/A")
            ), tags=tags)
        
        self.tree.tag_configure("banned", foreground="#ff6b6b")
        self.tree.tag_configure("active", foreground="#51cf66")
    
    def load_transactions(self):
        for item in self.transactionstree.get_children():
            self.transactionstree.delete(item)
        
        with open("userdatas2.json", "r") as f:
            usersdatas_trans = json.load(f)
        
        for username, user in usersdatas_trans.items():
            transfers = user.get("transfers", [])
            phone = user.get("teleno", "N/A")
            for transfer in transfers:
                if isinstance(transfer, dict):
                    self.transactionstree.insert("", tk.END, values=(
                        username,
                        phone,
                        transfer.get("date", "N/A"),
                        transfer.get("amount", 0),
                        transfer.get("type", "N/A"),
                        transfer.get("to", transfer.get("from", "N/A"))
                    ))
    
    def load_feedback(self):
        self.feedback_text.delete("1.0", tk.END)
        
        with open("userdatas2.json", "r") as f:
            usersdatas = json.load(f)
        
        feedback_count = 0
        for username, user in usersdatas.items():
            if "feedbacks" in user and user["feedbacks"]:
                for fb in user["feedbacks"]:
                    feedback_count += 1
                    self.feedback_text.insert(tk.END, f"{'═' * 80}\n", "divider")
                    self.feedback_text.insert(tk.END, f"📩 From: {username}\n", "username")
                    self.feedback_text.insert(tk.END, f"🕐 Date: {fb.get('date', 'N/A')}\n", "date")
                    self.feedback_text.insert(tk.END, f"Message: {fb.get('feedback', 'No message')}\n\n", "feedback")
        
        if feedback_count == 0:
            self.feedback_text.insert(tk.END, "No feedback received yet.", "empty")
        
        # Remove font parameter - CTkTextbox doesn't allow it in tag_config
        self.feedback_text.tag_config("username", foreground="#c96ce6")
        self.feedback_text.tag_config("date", foreground="#9fb4ff")
        self.feedback_text.tag_config("feedback", foreground="#e0e0e0")
        self.feedback_text.tag_config("divider", foreground="#5a2e7e")
        self.feedback_text.tag_config("empty", foreground="#b0b0b0")

    def refresh_users(self):
        self.load_users()
        messagebox.showinfo("Success", "User list refreshed successfully!")
    
    def refresh_banning_frame(self):
        for widget in self.banningframe.winfo_children():
            widget.destroy()
        
        with open("userdatas2.json", "r") as f:
            usersdatas = json.load(f)
        
        for username, user in usersdatas.items():
            user_card = ctk.CTkFrame(
                self.banningframe,
                fg_color=self.colors["bg_card"],
                corner_radius=12,
                height=90
            )
            user_card.pack(fill="x", padx=10, pady=10)
            user_card.pack_propagate(False)
            
            # User info section
            info_frame = ctk.CTkFrame(user_card, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=25, pady=20)
            
            status = user.get("status", "active")
            status_color = self.colors["danger"] if status == "banned" else self.colors["success"]
            status_icon = "🔴" if status == "banned" else "🟢"
            
            ctk.CTkLabel(
                info_frame,
                text=f"👤 {user.get('username', username)}",
                font=("Cooper Black", 18),
                text_color=self.colors["text_primary"]
            ).pack(side="left", padx=(0, 30))
            
            ctk.CTkLabel(
                info_frame,
                text=f"{status_icon} {status.upper()}",
                font=("Cooper Black", 16),
                text_color=status_color
            ).pack(side="left")
            
            # Action button
            if status == "banned":
                btn = ctk.CTkButton(
                    user_card,
                    text="✓ Unban User",
                    command=lambda u=username: self.unban_user(u),
                    fg_color=self.colors["success"],
                    hover_color="#2d8f5f",
                    width=150,
                    height=50,
                    corner_radius=10,
                    font=("Cooper Black", 16)
                )
            else:
                btn = ctk.CTkButton(
                    user_card,
                    text="✕ Ban User",
                    command=lambda u=username: self.ban_user(u),
                    fg_color=self.colors["danger"],
                    hover_color="#b02525",
                    width=150,
                    height=50,
                    corner_radius=10,
                    font=("Cooper Black", 16)
                )
            
            btn.pack(side="right", padx=25, pady=20)
    
    def ban_user(self, username):
        with open("userdatas2.json", "r") as f:
            usersdatas = json.load(f)
        
        if username not in usersdatas:
            messagebox.showerror("Error", f"User {username} not found.")
            return
        
        usersdatas[username]['status'] = 'banned'
        
        with open("userdatas2.json", "w") as f:
            json.dump(usersdatas, f)
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        phone = usersdatas[username].get('teleno', 'N/A')
        emirates_id = usersdatas[username].get('emerateid', 'N/A')
        self.logstree.insert("", 0, values=(username, phone, emirates_id, timestamp, "BAN", f"User {username} was banned by admin"))
        
        messagebox.showinfo("User Banned", f"User {username} has been banned successfully.")
        self.refresh_banning_frame()
    
    def unban_user(self, username):
        with open("userdatas2.json", "r") as f:
            usersdatas = json.load(f)
        
        if username not in usersdatas:
            messagebox.showerror("Error", f"User {username} not found.")
            return
        
        usersdatas[username]['status'] = 'active'
        
        with open("userdatas2.json", "w") as f:
            json.dump(usersdatas, f)
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        phone = usersdatas[username].get('teleno', 'N/A')
        emirates_id = usersdatas[username].get('emerateid', 'N/A')
        self.logstree.insert("", 0, values=(username, phone, emirates_id, timestamp, "UNBAN", f"User {username} was unbanned by admin"))
        
        messagebox.showinfo("User Unbanned", f"User {username} has been unbanned successfully.")
        self.refresh_banning_frame()
    
    def refresh_reports(self):
        with open("userdatas2.json", "r") as f:
            usersdatas_report = json.load(f)
        
        total_users = len(usersdatas_report)
        banned_users = len([u for u in usersdatas_report.values() if u.get("status", "active") == "banned"])
        active_users = total_users - banned_users
        total_money = sum(float(u.get("balance", 0)) for u in usersdatas_report.values())
        
        total_loans = 0
        total_loan_amount = 0
        for user in usersdatas_report.values():
            user_loans = user.get("loans", [])
            if isinstance(user_loans, list):
                total_loans += len(user_loans)
                for loan in user_loans:
                    if isinstance(loan, dict):
                        total_loan_amount += float(loan.get("amount", 0))
        
        total_transactions = sum(len(u.get("transfers", [])) for u in usersdatas_report.values())
        

        # Update widgets
        self.report_widgets["users"].configure(text=str(total_users))
        self.report_widgets["active"].configure(text=str(active_users))
        self.report_widgets["banned"].configure(text=str(banned_users))
        self.report_widgets["balance"].configure(text=f"{total_money:,.2f} AED")
        self.report_widgets["loans"].configure(text=f"{total_loans} Loans")
        self.report_widgets["loan_amt"].configure(text=f"{total_loan_amount:,.2f} AED")
        self.report_widgets["trans"].configure(text=str(total_transactions))
        
        messagebox.showinfo("Success", "Reports refreshed successfully!")
    
    def logs(self):
        pass

login.mainloop()


#and thats it our sweat and tears went into this project i hope you like it
