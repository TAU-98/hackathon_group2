# Teammate Setup Instructions

Welcome to the MADM Experiment Project! Follow these steps to set up and run the experiment on your computer.

---

## 1. Prerequisites
- **Python 3.8 or newer** (Python 3.12 recommended)
- **pip** (comes with Python)
- **git** (for cloning the repository)

> **No special extensions or IDEs are required.**

---

## 2. Clone the Repository
Open a terminal (Command Prompt, PowerShell, or Terminal) and run:
```bash
git clone https://github.com/TAU-98/hackathon_group2.git
cd hackathon_group2
```

---

## 3. Set Up a Virtual Environment (Recommended)
This keeps dependencies isolated from your system Python.

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

---

## 4. Install Dependencies
Install all required Python packages:
```bash
pip install -r requirements.txt
```
This will install:
- `pygame` (for the experiment GUI)
- `numpy`
- `pytest` (for running tests)

---

## 5. Run the Experiment
You can run either experiment from the command line:
```bash
python -m src.experiment.madm_skewde
# or
python -m src.experiment.main_experiment
```
A window will open with the experiment interface. Follow the on-screen instructions.

---

## 6. (Optional) Run Tests
To verify everything works:
```bash
pytest tests/
```

---

## 7. Troubleshooting
- **ModuleNotFoundError:** Make sure you activated the virtual environment and installed dependencies.
- **pygame errors:** Ensure you have the latest version of Python and pip. Try reinstalling pygame: `pip install --upgrade pygame`.
- **Still stuck?** Ask in the team chat or open an issue on GitHub.

---

## 8. No MATLAB or Special Hardware Needed
- The experiment is fully in Python.
- Eye-tracking is mocked (no hardware required).

---

## 9. Need Help?
- Check the `README.md` for more details.
- Ask your teammates or project maintainer.

Good luck and have fun! 