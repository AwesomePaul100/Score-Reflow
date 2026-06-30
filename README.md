# Score-Reflow (Accessibility Edition)

Score-Reflow is a high-contrast, accessibility-focused GUI tool for managing grading workflows and interacting with LMS platforms such as Canvas (e.g., UCF Webcourses).

Link to ACM Papaer presented at GLSVLSI: https://dl.acm.org/doi/10.1145/3787109.3816049?__cf_chl_f_tk=Dfav7mAalet4U5WzNZ4faoWSW5Xi00rb2jE5o0yvDJY-1782780325-1.0.1.1-A7gyY5Vb_ydqjFewmiFROHTnoBJb09DYeGc07Ak1AX8

---

## ✨ Features

- High-contrast, accessibility-friendly UI
- Large fonts for readability
- Clean Tkinter-based interface
- LMS API integration support (Canvas-compatible)
- Lightweight and easy to run

---

## 🛠️ Technologies

- Python 3
- Tkinter
- Requests

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install requests
```

---

### 2. Configure the application

Open `Score-Reflow.py` and locate:

```python
BASE_URL = "https://webcourses.ucf.edu"  # Put your University base URL
API_TOKEN = ""  # Put your LMS access token
```

Update these values:

#### BASE_URL

Set this to your LMS domain:

```python
BASE_URL = "https://webcourses.ucf.edu"
```

#### API_TOKEN

Paste your Canvas API token:

```python
API_TOKEN = "your_token_here"
```

---

### 3. Run the program

```bash
python Score-Reflow.py
```

---

## 🔐 Security Warning

- Do NOT upload your API token to GitHub
- Treat your token like a password

---

## 👨‍💻 Author

Paul Amoruso
