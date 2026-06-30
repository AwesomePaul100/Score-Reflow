# Score-Reflow (Accessibility Edition)

Score-Reflow is a high-contrast, accessibility-focused GUI tool for managing grading workflows and interacting with LMS platforms such as Canvas (e.g., UCF Webcourses).

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
