# دکان بلنگ سسٹم - Shop Billing System

A comprehensive billing system for shops with credit management and Urdu language support. This application runs on both Linux and Windows.

## Features

- **Credit System**: Track customer credit/outstanding balances
- **Urdu Language Support**: Bills are displayed in Urdu with English translations
- **Customer Management**: Add and manage customer information
- **Product Management**: Maintain product inventory with prices
- **Dual Payment Modes**: 
  - Credit billing (adds to customer's credit balance)
  - Cash billing (immediate payment)
- **Reports**: 
  - Customer credit report
  - Sales history
- **Cross-Platform**: Works on Linux and Windows
- **User-Friendly GUI**: Simple and intuitive interface

## System Requirements

- Python 3.6 or higher
- tkinter (usually comes pre-installed with Python)
- SQLite3 (comes pre-installed with Python)

## Installation

### Windows

1. Download and install Python from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation
   - tkinter is included by default

2. Download the application files

3. Run the application:
   ```bash
   python main.py
   ```

### Linux

1. Install Python and tkinter:

   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-tk
   ```

   **Fedora:**
   ```bash
   sudo dnf install python3 python3-tkinter
   ```

   **Arch Linux:**
   ```bash
   sudo pacman -S python tk
   ```

2. Download the application files

3. Make the script executable (optional):
   ```bash
   chmod +x main.py
   ```

4. Run the application:
   ```bash
   python3 main.py
   # or if made executable:
   ./main.py
   ```

## Usage

### Starting the Application

Run the main application:
```bash
python main.py
```

### Adding Customers

1. Click "Add New Customer" button
2. Enter customer name, phone number, and address
3. Click "Save"

### Adding Products

1. Click "Add Product" button
2. Enter product name, price, and optionally Urdu name
3. Click "Save"

The system comes pre-loaded with sample products in Urdu.

### Creating a Bill

#### Credit Bill:
1. Select a customer from the dropdown
2. Select products and add them to cart
3. Click "Generate Bill (Credit)"
4. The bill will be displayed in Urdu and the amount will be added to customer's credit

#### Cash Bill:
1. Add products to cart (no need to select customer)
2. Click "Cash Payment"
3. The bill will be generated for a cash customer

### Viewing Reports

- **Customer Credit Report**: Menu → Reports → Customer Credit Report
- **Sales History**: Menu → Reports → Sales History

## File Structure

```
shop-billing-system/
│
├── main.py              # Main application with GUI
├── database.py          # Database operations (SQLite)
├── bill_generator.py    # Urdu bill generation
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── shop_billing.db     # SQLite database (created automatically)
```

## Database Schema

The application uses SQLite with the following tables:

- **customers**: Customer information and credit balances
- **products**: Product inventory with Urdu names
- **transactions**: Sales transactions
- **transaction_items**: Individual items in each transaction
- **credit_payments**: Credit payment records

## Urdu Language Support

The application displays bills in Urdu with:
- Urdu numbers (۰۱۲۳۴۵۶۷۸۹)
- Urdu product names
- Urdu headers and labels
- English translations for clarity

## Features in Detail

### Credit Management
- Track outstanding balances for each customer
- View total credit across all customers
- Add credit to customer accounts with each credit sale

### Reporting
- View all customers with outstanding credit
- View complete sales history
- Filter and analyze transactions

## Troubleshooting

### Windows

**Issue**: "tkinter module not found"
- Solution: Reinstall Python and ensure "tcl/tk and IDLE" is selected during installation

### Linux

**Issue**: "No module named '_tkinter'"
- Solution: Install tkinter package for your distribution (see Installation section)

**Issue**: Urdu text not displaying correctly
- Solution: Ensure you have Urdu fonts installed on your system
  ```bash
  # Ubuntu/Debian
  sudo apt-get install fonts-noto-nastaliq-urdu
  ```

## Support

For issues or questions, please ensure:
1. Python 3.6+ is installed
2. tkinter is properly installed
3. You have write permissions in the application directory (for SQLite database)

## License

Free to use for personal and commercial purposes.

## Version

Version 1.0 - October 2025

---

**شکریہ - Thank you for using Shop Billing System!**
