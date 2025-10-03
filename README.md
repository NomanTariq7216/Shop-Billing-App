## Billing App (Urdu invoices, Credit system)

Cross-platform Flask app for small shops. Generates Urdu-only printable invoices, supports credit (udhār) with customer statements. Runs on Linux and Windows.

### Features
- Customers, Products, Payments
- Invoices: Cash or Credit
- Urdu invoice view with RTL layout and Urdu numerals
- Customer statement and dashboard

### Requirements
- Python 3.10+

### Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run (development)
```bash
python app.py
```
Open http://localhost:5000

### Notes
- Urdu font: The invoice uses system Urdu Nastaliq fonts if available. For best results, install "Noto Nastaliq Urdu" or "Jameel Noori Nastaleeq" on your system.
- Database: SQLite file `billing.sqlite3` is created in the project directory.
- Printing: Use the browser print dialog from the Urdu invoice view.

