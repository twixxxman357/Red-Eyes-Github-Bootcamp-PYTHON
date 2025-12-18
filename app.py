import tkinter as tk
from tkinter import messagebox, ttk
import random

from questions import MODULES, FINAL_TEST
from audio import play_sound

# ================= THEME =================
BG = "#020617"
CARD_BG = "#020617"
TEXT = "#f8fafc"
GHOST = "#e5e7eb"
ACCENT = "#dc2626"
SUCCESS = "#22c55e"

MODULE_ICONS = {
    "Git Basics": "📁",
    "Branching & Merging": "🌿",
    "GitHub & Remotes": "🌐",
    "Advanced Git Workflow": "⚙️",
}


class GitTutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RED EYES GITHUB BOOTCAMP")
        self.root.configure(bg=BG)
        self.root.geometry("1200x820")
        self.root.resizable(False, False)

        self.student_name = ""
        self.completed_modules = set()

        self.module_name = None
        self.questions = []
        self.index = 0
        self.score = 0
        self.answer = tk.StringVar()

        self.prompt_student_name()

    # ================= START =================
    def prompt_student_name(self):
        self.clear_screen()

        tk.Label(
            self.root,
            text="RED EYES GITHUB BOOTCAMP",
            font=("Helvetica", 36, "bold"),
            fg=ACCENT,
            bg=BG
        ).pack(pady=(120, 20))

        tk.Label(
            self.root,
            text="Enter your full name to begin",
            font=("Helvetica", 18),
            fg=TEXT,
            bg=BG
        ).pack(pady=10)

        entry = tk.Entry(
            self.root,
            font=("Helvetica", 20),
            justify="center",
            width=34
        )
        entry.pack(pady=20)
        entry.focus()

        def start():
            if not entry.get().strip():
                messagebox.showwarning("Missing Name", "Please enter your name.")
                return
            self.student_name = entry.get().strip()
            self.show_module_menu()

        tk.Button(
            self.root,
            text="START BOOTCAMP",
            font=("Helvetica", 18, "bold"),
            fg=BG,
            bg=GHOST,
            bd=0,
            padx=60,
            pady=18,
            command=start
        ).pack(pady=40)

    # ================= MODULE MENU =================
    def show_module_menu(self):
        self.clear_screen()

        tk.Label(
            self.root,
            text="SELECT A MODULE",
            font=("Helvetica", 32, "bold"),
            fg=ACCENT,
            bg=BG
        ).pack(pady=(30, 30))

        grid = tk.Frame(self.root, bg=BG)
        grid.pack(padx=40, pady=10)

        for i in range(2):
            grid.columnconfigure(i, weight=1)
            grid.rowconfigure(i, weight=1)

        for i, module in enumerate(MODULES.keys()):
            row, col = divmod(i, 2)
            completed = module in self.completed_modules
            icon = MODULE_ICONS.get(module, "📘")

            card = tk.Frame(
                grid,
                bg=CARD_BG,
                highlightbackground=GHOST,
                highlightthickness=3,
                padx=32,
                pady=30
            )
            card.grid(row=row, column=col, padx=30, pady=30, sticky="nsew")

            tk.Label(
                card,
                text=f"{icon}  {module}",
                font=("Helvetica", 26, "bold"),
                fg=TEXT,
                bg=CARD_BG,
                anchor="w"
            ).pack(fill="x")

            tk.Label(
                card,
                text="COMPLETED ✓" if completed else "25 QUESTIONS",
                font=("Helvetica", 16, "bold"),
                fg=GHOST,
                bg=CARD_BG
            ).pack(pady=(14, 26))

            tk.Button(
                card,
                text="ENTER MODULE",
                font=("Helvetica", 18, "bold"),
                fg=BG,
                bg=GHOST,
                bd=0,
                padx=52,
                pady=18,
                command=lambda m=module: self.start_module(m)
            ).pack(anchor="e")

        if len(self.completed_modules) == len(MODULES):
            final = tk.Frame(
                self.root,
                bg="#052e16",
                highlightbackground=SUCCESS,
                highlightthickness=4,
                padx=40,
                pady=30
            )
            final.pack(pady=40)

            tk.Label(
                final,
                text="🏁 FINAL EXAM (100 QUESTIONS)",
                font=("Helvetica", 28, "bold"),
                fg=TEXT,
                bg="#052e16"
            ).pack(pady=(0, 20))

            tk.Button(
                final,
                text="START FINAL EXAM",
                font=("Helvetica", 20, "bold"),
                fg=BG,
                bg=SUCCESS,
                bd=0,
                padx=70,
                pady=20,
                command=self.start_final_test
            ).pack()

    # ================= QUIZ =================
    def start_module(self, module):
        self.module_name = module
        self.questions = MODULES[module][:]
        random.shuffle(self.questions)
        self.index = 0
        self.score = 0
        self.build_quiz_ui()
        self.load_question()

    def start_final_test(self):
        self.module_name = "FINAL TEST"
        self.questions = FINAL_TEST[:]
        random.shuffle(self.questions)
        self.index = 0
        self.score = 0
        self.build_quiz_ui()
        self.load_question()

    def build_quiz_ui(self):
        self.clear_screen()

        card = tk.Frame(self.root, bg=CARD_BG)
        card.pack(padx=40, pady=40, fill="both", expand=True)

        self.status = tk.Label(
            card,
            font=("Helvetica", 16, "bold"),
            fg="#94a3b8",
            bg=CARD_BG
        )
        self.status.pack(pady=10)

        self.progress = ttk.Progressbar(card, maximum=len(self.questions), length=900)
        self.progress.pack(pady=10)

        self.question_label = tk.Label(
            card,
            wraplength=960,
            font=("Helvetica", 22, "bold"),
            fg=TEXT,
            bg=CARD_BG,
            justify="left"
        )
        self.question_label.pack(pady=30)

        self.options = []
        for _ in range(4):
            rb = tk.Radiobutton(
                card,
                variable=self.answer,
                font=("Helvetica", 18),
                fg=TEXT,
                bg=CARD_BG,
                selectcolor="#1e293b",
                anchor="w"
            )
            rb.pack(fill="x", padx=40, pady=10)
            self.options.append(rb)

        tk.Button(
            self.root,
            text="SUBMIT ANSWER",
            font=("Helvetica", 18, "bold"),
            fg=BG,
            bg=GHOST,
            bd=0,
            padx=60,
            pady=18,
            command=self.submit
        ).pack(pady=30)

    # ================= LOGIC (SCENARIO FEEDBACK) =================
    def load_question(self):
        if self.index >= len(self.questions):
            self.finish_module()
            return

        self.answer.set(None)
        q = self.questions[self.index]

        label = q.get("label", f"Q{self.index + 1}")
        self.status.config(
            text=f"{self.module_name} — {label} of {len(self.questions)} | Score: {self.score}"
        )

        self.progress["value"] = self.index
        self.question_label.config(text=q["question"])

        for btn, opt in zip(self.options, q["options"]):
            btn.config(text=opt, value=opt[0])

    def submit(self):
        q = self.questions[self.index]

        if self.answer.get() == q["answer"]:
            self.score += 1
            play_sound("assets/sounds/correct.wav")
            self.index += 1
            self.root.after(400, self.load_question)
        else:
            play_sound("assets/sounds/wrong.wav")

            explanation = (
                "❌ That choice would cause problems in a real Git/GitHub workflow.\n\n"
                f"✅ Correct Answer: {q['answer']}\n\n"
                f"🧠 Explanation:\n{q['explanation']}\n\n"
                "📌 Real-world takeaway:\n"
                "In professional teams, this decision impacts collaboration, "
                "code safety, and deployment reliability."
            )

            messagebox.showinfo("Learning Moment", explanation)
            self.index += 1
            self.load_question()

    def finish_module(self):
        self.completed_modules.add(self.module_name)
        self.show_module_menu()

    def clear_screen(self):
        for w in self.root.winfo_children():
            w.destroy()


# ================= RUN (macOS FIX) =================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    root.update_idletasks()
    root.geometry("1200x820+100+100")
    root.deiconify()
    root.lift()
    root.focus_force()
    root.attributes("-topmost", True)
    root.after(1000, lambda: root.attributes("-topmost", False))
    GitTutorApp(root)
    root.mainloop()
