# How to Run the KYC Financial Exclusion Analytics System
### Step-by-Step Guide for First-Time Users

---

## What This System Does

This system has **two parts** you can run:

| Part | File | What it does |
|------|------|--------------|
| **Analysis Pipeline** | `main.py` | Generates data, trains 3 ML models, computes FERI scores, saves charts and reports |
| **Interactive Dashboard** | `app.py` | Opens a live website in your browser for exploring results and scoring individuals |

> Run `main.py` **first**, then `app.py` to explore the results visually.

---

## STEP 1 — Check That Python Is Installed

Open a terminal (Command Prompt or PowerShell on Windows, Terminal on Mac/Linux) and type:

```
python --version
```

You should see something like `Python 3.10.5`. If you see an error, download Python from:
**https://www.python.org/downloads/** (choose version 3.10 or newer)

> During installation on Windows, tick the box that says **"Add Python to PATH"**.

---

## STEP 2 — Open a Terminal in the Project Folder

**On Windows:**
1. Open File Explorer and navigate to the project folder (`group 2 project`)
2. Click on the address bar at the top
3. Type `cmd` and press Enter

**Alternative (any OS):**
```
cd "c:\Users\munya\Desktop\group 2 project"
```

All commands from this point forward must be run from inside this folder.

---

## STEP 3 — Create a Virtual Environment (Recommended — Do This Once)

A virtual environment keeps this project's packages separate from other Python projects on your computer.

```
python -m venv venv
```

This creates a folder called `venv` in the project directory.

---

## STEP 4 — Activate the Virtual Environment

**On Windows (Command Prompt):**
```
venv\Scripts\activate
```

**On Windows (PowerShell):**
```
venv\Scripts\Activate.ps1
```

**On Mac / Linux:**
```
source venv/bin/activate
```

After activation you will see `(venv)` at the start of your terminal prompt, like this:
```
(venv) C:\Users\munya\Desktop\group 2 project>
```

> To deactivate (stop using the virtual environment) later, just type: `deactivate`

---

## STEP 5 — Install All Required Packages (Do This Once)

```
pip install -r requirements.txt
```

This downloads and installs all the libraries needed (numpy, pandas, scikit-learn, xgboost, streamlit, plotly, etc.).

This may take **2–5 minutes** depending on your internet speed. You will see a stream of download messages — this is normal.

When it finishes you should see something like:
```
Successfully installed numpy-... pandas-... scikit-learn-... streamlit-...
```

---

## STEP 6 — Run the Analysis Pipeline

```
python main.py
```

**What happens:**
The script runs 9 steps automatically. You will see progress printed in the terminal:

```
============================================================
KYC Financial Exclusion Analysis - Zimbabwe
============================================================
Step 1/9: Generating synthetic dataset...
Step 2/9: Exploratory Data Analysis...
Step 3/9: Data Preprocessing...
Step 4/9: Training ML Models...
Step 5/9: Evaluating Models...
Step 6/9: Creating Visualizations...
Step 7/9: Computing FERI Scores...
Step 8/9: Analyzing High-Risk Groups...
Step 9/9: Generating Policy Recommendations...
============================================================
Analysis Complete!
============================================================
```

**Time to complete:** approximately 30–90 seconds.

**Output files saved to:**
- `data/kyc_financial_exclusion_zimbabwe.csv` — the 5,000-row dataset
- `data/kyc_with_feri.csv` — dataset enriched with FERI risk scores
- `outputs/model_comparison.csv` — accuracy, AUC, F1 for all 3 models
- `outputs/feri_summary.csv` — FERI statistics by demographic group
- `outputs/policy_recommendations.txt` — plain-text policy summary
- `outputs/figures/` — 15+ PNG charts (ROC curves, confusion matrices, FERI distribution, etc.)

---

## STEP 7 — Launch the Interactive Dashboard

```
streamlit run app.py
```

**What happens:**
- Streamlit starts a local web server
- Your default browser opens automatically at **http://localhost:8501**
- If the browser does not open, copy that URL and paste it into your browser manually

You will see in the terminal:
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

**The dashboard has 6 pages (use the sidebar to navigate):**

| Page | What You Can Do |
|------|-----------------|
| Overview Dashboard | See key statistics, exclusion rates by province, FERI distribution |
| Individual Risk Scanner | Enter a person's profile and get a real-time FERI score and ML prediction |
| Model Performance | Compare Logistic Regression, Random Forest, and XGBoost results |
| Data Explorer | Browse and filter the full 5,000-row dataset |
| FERI Analytics | Explore the Financial Exclusion Risk Index in depth |
| Policy Intelligence | View 6 evidence-based policy recommendations with a priority matrix |

**To stop the dashboard**, go back to the terminal and press `Ctrl + C`.

---

## Quick Reference — All Commands in Order

```bash
# 1. Navigate to the project folder
cd "c:\Users\munya\Desktop\group 2 project"

# 2. Create virtual environment (first time only)
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate          # Windows CMD
# venv\Scripts\Activate.ps1   # Windows PowerShell
# source venv/bin/activate     # Mac / Linux

# 4. Install packages (first time only)
pip install -r requirements.txt

# 5. Run the full analysis pipeline
python main.py

# 6. Launch the interactive dashboard
streamlit run app.py
```

---

## Troubleshooting

### "python is not recognized as an internal or external command"
Python is not installed or not on your PATH.
- Download from https://www.python.org/downloads/
- On Windows, reinstall and check "Add Python to PATH"

### "pip is not recognized"
Try using `pip3` instead of `pip`, or run:
```
python -m pip install -r requirements.txt
```

### PowerShell says "cannot be loaded because running scripts is disabled"
Run this command once in PowerShell as Administrator:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then re-run the activate command.

### "ModuleNotFoundError: No module named 'streamlit'" (or any other module)
You either skipped Step 5 or the virtual environment is not active.
- Re-activate: `venv\Scripts\activate`
- Re-install: `pip install -r requirements.txt`

### The browser does not open when running `streamlit run app.py`
Open your browser manually and go to: **http://localhost:8501**

### Port 8501 is already in use
Run on a different port:
```
streamlit run app.py --server.port 8502
```
Then open **http://localhost:8502** in your browser.

### `main.py` crashes mid-way
Make sure all packages installed without errors. Run:
```
pip install -r requirements.txt --upgrade
```

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.10 | 3.11 or 3.12 |
| RAM | 4 GB | 8 GB |
| Disk Space | 500 MB | 1 GB |
| Internet | Required (for install only) | — |
| OS | Windows 10, macOS 12, Ubuntu 20 | Any modern OS |

---

## File Map at a Glance

```
group 2 project/
│
├── main.py              <-- RUN THIS FIRST  (full analysis pipeline)
├── app.py               <-- RUN THIS SECOND (interactive dashboard)
├── requirements.txt     <-- package list (used in Step 5)
│
├── src/                 <-- source code modules (do not run directly)
│   ├── data_generator.py
│   ├── preprocessor.py
│   ├── models.py
│   ├── feri.py
│   └── visualizations.py
│
├── data/                <-- datasets (created by main.py)
├── outputs/             <-- results and charts (created by main.py)
└── venv/                <-- virtual environment (created in Step 3)
```

---

*For questions about the research content, refer to `README.md` or the project chapters in the root folder.*
