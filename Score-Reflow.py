import tkinter as tk
from tkinter import messagebox
import requests
import threading
import time

# ── High-Contrast Accessible Palette ──────────────────────────────────────────
BG          = "#FFFFFF"   # Pure white background
PANEL       = "#F0f2f5"   # Light grey for separation
PANEL2      = "#FFFFFF"   # Input field bg
ACCENT      = "#0056b3"   # High-contrast "Action Blue"
ACCENT2     = "#003d7a"   # Darker blue for hover
SUCCESS     = "#008000"   # Standard green
WARNING     = "#856404"   # Dark gold for visibility on white
ERROR       = "#b22222"   # Firebrick red
INFO        = "#000000"   # Default black text
TEXT        = "#000000"   # Primary text
TEXT_DIM    = "#404040"   # Secondary text (Dark enough for contrast)
BORDER      = "#000000"   # Bold borders
RADIUS      = 8

# ── Canvas API stub ──────────────────────────────────────────────────────────
BASE_URL = "https://webcourses.ucf.edu" #Put your University base URL
API_TOKEN = "<Put your LMS access token>"#Put your LMS access token, such as ll58~...

class RoundedEntry(tk.Frame):
    """Accessible Entry: High contrast and large text."""
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(parent, bg=BORDER, padx=2, pady=2) # Thicker border
        self.placeholder = placeholder
        self._var = tk.StringVar()
        self.entry = tk.Entry(
            self, textvariable=self._var,
            bg=PANEL2, fg=TEXT, insertbackground=ACCENT,
            relief="flat", font=("Arial", 18), # Larger, cleaner font
            bd=10, highlightthickness=0,
        )
        self.entry.pack(fill="x")
        if placeholder:
            self._show_placeholder()
        self.entry.bind("<FocusIn>",  self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._restore_placeholder)

    def _show_placeholder(self):
        if not self._var.get():
            self.entry.config(fg=TEXT_DIM)
            self._var.set(self.placeholder)

    def _clear_placeholder(self, _=None):
        if self._var.get() == self.placeholder:
            self._var.set("")
            self.entry.config(fg=TEXT)

    def _restore_placeholder(self, _=None):
        if not self._var.get():
            self._show_placeholder()

    def get(self):
        v = self._var.get()
        return "" if v == self.placeholder else v

    def set(self, value):
        self._var.set(value)
        self.entry.config(fg=TEXT)


class GradeFlowApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Score-Reflow | Accessibility Edition")
        self.root.configure(bg=BG)
        self.root.geometry("900x850") # Slightly wider for larger fonts
        self.root.resizable(True, True)
        self._build_ui()

    def _build_ui(self):
        # ── Header ──────────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg=PANEL, pady=25)
        header.pack(fill="x")

        tk.Label(header, text="Score-Reflow", font=("Arial", 48, "bold"),
                 bg=PANEL, fg=ACCENT).pack()
        tk.Label(header, text="Canvas LMS Grade Aggregator",
                 font=("Arial", 16, "bold"), bg=PANEL, fg=TEXT).pack()

        sep = tk.Frame(self.root, bg=BORDER, height=3)
        sep.pack(fill="x")

        # ── Main body ────────────────────────────────────────────────────────
        body = tk.Frame(self.root, bg=BG, padx=30, pady=20)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)

        fields = [
            ("Course ID",                 "e.g. 648291",          "course"),
            ("Source Assignment IDs",     "e.g. 98431, 98445",    "sources"),
            ("Target Assignment ID",      "e.g. 99102",           "target"),
            ("Curve Points",              "0",                     "curve"),
            ("Max Points (optional)",    "e.g. 100",             "maxpts"),
        ]
        self.entries = {}
        for row, (lbl, ph, key) in enumerate(fields):
            tk.Label(body, text=lbl, font=("Arial", 18, "bold"),
                     bg=BG, fg=TEXT, anchor="w"
                     ).grid(row=row, column=0, sticky="w",
                            padx=(0, 20), pady=12) # More vertical spacing
            e = RoundedEntry(body, placeholder=ph)
            e.grid(row=row, column=1, sticky="ew", pady=12)
            self.entries[key] = e

        self.entries["curve"].set("0")

        # ── Log panel ────────────────────────────────────────────────────────
        log_label = tk.Frame(body, bg=BG)
        log_label.grid(row=len(fields), column=0, columnspan=2,
                       sticky="w", pady=(25, 5))
        tk.Label(log_label, text="ACTIVITY LOG", font=("Arial", 14, "bold"),
                 bg=BG, fg=TEXT).pack(side="left")

        log_frame = tk.Frame(body, bg=BORDER, padx=2, pady=2)
        log_frame.grid(row=len(fields)+1, column=0, columnspan=2,
                       sticky="nsew", pady=(0, 20))
        body.rowconfigure(len(fields)+1, weight=1)

        self.log_text = tk.Text(
            log_frame, bg=PANEL, fg=TEXT,
            font=("Arial", 14), relief="flat",
            bd=10, wrap="word", state="disabled"
        )
        self.log_text.pack(fill="both", expand=True)

        # High-contrast tags
        self.log_text.tag_config("ok",   foreground=SUCCESS, font=("Arial", 14, "bold"))
        self.log_text.tag_config("warn", foreground=WARNING, font=("Arial", 14, "bold"))
        self.log_text.tag_config("err",  foreground=ERROR,   font=("Arial", 14, "bold"))
        self.log_text.tag_config("info", foreground=INFO)

        # ── Button row ───────────────────────────────────────────────────────
        btn_row = tk.Frame(body, bg=BG)
        btn_row.grid(row=len(fields)+2, column=0, columnspan=2, pady=(10, 10))

        self.run_btn = tk.Button(
            btn_row, text="RUN Score-Reflow",
            font=("Arial", 18, "bold"),
            bg=ACCENT, fg="black", activebackground=ACCENT2,
            activeforeground="black", relief="raised", # Raised looks more like a button
            padx=50, pady=20, cursor="hand2",
            command=self._start_grading,
        )
        self.run_btn.pack(side="left", padx=(0, 20))

        tk.Button(
            btn_row, text="CLEAR LOG",
            font=("Arial", 14, "bold"),
            bg="#e0e0e0", fg="black", activebackground="#bdbdbd",
            relief="raised", padx=25, pady=20, cursor="hand2",
            command=self._clear_log,
        ).pack(side="left")

        # ── Status bar ───────────────────────────────────────────────────────
        self.statusbar = tk.Label(
            self.root, text="System Ready", font=("Arial", 14, "bold"),
            bg=PANEL, fg=TEXT, anchor="w", padx=15, pady=10,
        )
        self.statusbar.pack(fill="x", side="bottom")

    # [Logic remains the same as your original script]
    def _log(self, msg: str, tag: str = "info"):
        self.log_text.config(state="normal")
        prefix = {"ok": "[OK] ", "warn": "[SKIP] ", "err": "[FAIL] ", "info": "[INFO] "}.get(tag, "")
        self.log_text.insert("end", prefix + msg + "\n", tag)
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.root.update_idletasks()

    def _clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    def _set_status(self, msg: str, color: str = TEXT):
        self.statusbar.config(text=msg, fg=color)

    def _headers(self):
        return {"Authorization": f"Bearer {API_TOKEN}"}

    def _get_all_pages(self, url: str) -> list:
        results = []
        while url:
            r = requests.get(url, headers=self._headers(), timeout=15)
            r.raise_for_status()
            results.extend(r.json())
            url = r.links.get("next", {}).get("url")
        return results

    def _get_students(self, course_id: int) -> list:
        url = (f"{BASE_URL}/api/v1/courses/{course_id}/enrollments"
               f"?type[]=StudentEnrollment&per_page=100")
        return self._get_all_pages(url)

    def _get_assignments(self, course_id: int) -> list:
        url = f"{BASE_URL}/api/v1/courses/{course_id}/assignments?per_page=100"
        return self._get_all_pages(url)

    def _resolve_ids(self, course_id: int, source_ids: list) -> dict:
        assignments = self._get_assignments(course_id)
        mapping = {}
        for sid in source_ids:
            match = [a for a in assignments if a.get("id") == sid or a.get("quiz_id") == sid]
            if match:
                mapping[sid] = match[0]["id"]
            else:
                self._log(f"Unresolvable ID {sid}", "warn")
        return mapping

    def _get_score(self, course_id: int, assignment_id: int, user_id: int):
        url = (f"{BASE_URL}/api/v1/courses/{course_id}"
               f"/assignments/{assignment_id}/submissions/{user_id}")
        r = requests.get(url, headers=self._headers(), timeout=15)
        if r.status_code == 404: return None
        r.raise_for_status()
        return r.json().get("score") or 0

    def _post_grade(self, course_id: int, assignment_id: int, user_id: int, grade: float):
        url = (f"{BASE_URL}/api/v1/courses/{course_id}"
               f"/assignments/{assignment_id}/submissions/{user_id}")
        payload = {"submission": {"posted_grade": grade}}
        r = requests.put(url, headers=self._headers(), json=payload, timeout=15)
        r.raise_for_status()

    def _run_grading_thread(self):
        self.run_btn.config(state="disabled", text="PROCESSING...")
        self._set_status("Grading in progress...", ACCENT)
        try:
            course_id = int(self.entries["course"].get())
            sources = [int(s.strip()) for s in self.entries["sources"].get().split(",") if s.strip().isdigit()]
            target_id = int(self.entries["target"].get())
            curve = float(self.entries["curve"].get() or 0)
            
            self._log(f"Starting Course {course_id}...", "info")
            students = self._get_students(course_id)
            id_map = self._resolve_ids(course_id, sources)
            
            for student in students:
                uid = student.get("user_id")
                if not uid: continue
                total = 0.0
                for aid in id_map.values():
                    s = self._get_score(course_id, aid, uid)
                    if s is not None: total += s
                
                final = total + curve
                self._post_grade(course_id, target_id, uid, final)
                self._log(f"User {uid}: Posted {final}", "ok")

            self._set_status("Grading Complete", SUCCESS)
            messagebox.showinfo("Success", "All grades have been processed.")
        except Exception as e:
            self._log(f"Error: {e}", "err")
            messagebox.showerror("Error", str(e))
        finally:
            self.run_btn.config(state="normal", text="RUN GRADING")

    def _start_grading(self):
        self._clear_log()
        threading.Thread(target=self._run_grading_thread, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeFlowApp(root)
    root.mainloop()
