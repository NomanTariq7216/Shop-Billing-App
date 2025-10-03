# Quick Start Guide - دکان بلنگ سسٹم

## Quick Installation

### Windows Users:
1. Double-click `run.bat` to start the application
   - If Python is not installed, download from https://www.python.org/downloads/

### Linux Users:
1. Run in terminal:
   ```bash
   ./run.sh
   ```
   OR
   ```bash
   python3 main.py
   ```

2. If tkinter is missing, install it:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # Fedora
   sudo dnf install python3-tkinter
   
   # Arch
   sudo pacman -S tk
   ```

## First Time Use

### 1. Add a Customer
- Click **"Add New Customer"** button
- Fill in: Name, Phone, Address
- Click Save

### 2. Products are Pre-loaded
The system comes with 10 sample products in Urdu:
- Rice (چاول)
- Wheat Flour (آٹا)
- Sugar (چینی)
- Cooking Oil (کھانا پکانے کا تیل)
- Tea (چائے)
- And more...

### 3. Create Your First Bill

**For Credit (Udhar):**
1. Select a customer from dropdown
2. Select product → Enter quantity → Click "Add to Cart"
3. Repeat for all items
4. Click **"Generate Bill (Credit)"**
5. Bill appears in Urdu on the right panel

**For Cash:**
1. Add products to cart (no customer needed)
2. Click **"Cash Payment"**
3. Bill generated instantly

### 4. View Reports
- Menu → Reports → **Customer Credit Report** (see who owes money)
- Menu → Reports → **Sales History** (see all transactions)

## Features at a Glance

✅ **Credit System** - Track customer debts (ادھار)  
✅ **Urdu Bills** - Beautiful Urdu formatted receipts  
✅ **Cross-Platform** - Works on Windows & Linux  
✅ **Easy to Use** - Simple interface  
✅ **No Internet Required** - Fully offline  
✅ **Automatic Database** - SQLite database created automatically  

## Sample Bill Output

```
============================================================
               دکان بلنگ سسٹم
           SHOP BILLING SYSTEM
============================================================

رسید نمبر: ۱
Receipt No: 1

تاریخ: ۲۰۲۵-۱۰-۰۳
Date: 2025-10-03

گاہک کا نام: احمد علی
Customer: Ahmad Ali

ادائیگی کی قسم: ادھار
Payment Type: CREDIT

============================================================
                   اشیاء کی فہرست
                    ITEMS LIST
============================================================

                       شے       قیمت      تعداد         کل
Item                           Price        Qty      Total
------------------------------------------------------------
                     چاول     ۱۵۰.۰۰          ۲     ۳۰۰.۰۰
Rice 1kg                      150.00          2     300.00
```

## Tips

💡 **Add Urdu Names**: When adding products, fill in the "Urdu Name" field for better-looking bills

💡 **Track Credit**: Use "Customer Credit Report" regularly to track outstanding payments

💡 **Backup**: Copy `shop_billing.db` file to backup your data

## Troubleshooting

**Problem**: Can't start application  
**Solution**: Make sure Python 3.6+ is installed

**Problem**: Urdu text looks wrong  
**Solution**: Install Urdu fonts on your system

**Problem**: "tkinter not found"  
**Solution**: Install python3-tk package (Linux) or reinstall Python with tcl/tk (Windows)

---

**Need Help?** See the full README.md file for detailed documentation.

**شکریہ - Thank You!**
