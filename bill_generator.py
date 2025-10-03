#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bill Generator module for Shop Billing System
Generates bills in Urdu language
"""

from datetime import datetime

class BillGenerator:
    def __init__(self):
        # Urdu number mapping
        self.urdu_numbers = {
            '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
            '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
        }
        
    def to_urdu_number(self, number):
        """Convert English number to Urdu digits"""
        str_num = str(number)
        urdu_num = ''
        for char in str_num:
            urdu_num += self.urdu_numbers.get(char, char)
        return urdu_num
        
    def generate_bill(self, transaction_id, customer, cart_items, total_amount, payment_type):
        """Generate bill in Urdu"""
        
        current_time = datetime.now()
        date_str = current_time.strftime('%Y-%m-%d')
        time_str = current_time.strftime('%H:%M:%S')
        
        # Convert to Urdu numbers
        urdu_trans_id = self.to_urdu_number(transaction_id)
        urdu_date = self.to_urdu_number(date_str)
        urdu_time = self.to_urdu_number(time_str)
        
        # Bill header
        bill = "=" * 60 + "\n"
        bill += "               دکان بلنگ سسٹم\n"
        bill += "           SHOP BILLING SYSTEM\n"
        bill += "=" * 60 + "\n\n"
        
        # Transaction details
        bill += f"رسید نمبر: {urdu_trans_id}\n"
        bill += f"Receipt No: {transaction_id}\n\n"
        
        bill += f"تاریخ: {urdu_date}\n"
        bill += f"Date: {date_str}\n\n"
        
        bill += f"وقت: {urdu_time}\n"
        bill += f"Time: {time_str}\n\n"
        
        bill += "-" * 60 + "\n"
        
        # Customer details
        bill += f"گاہک کا نام: {customer['name']}\n"
        bill += f"Customer: {customer['name']}\n\n"
        
        if customer.get('phone'):
            urdu_phone = self.to_urdu_number(customer['phone'])
            bill += f"فون: {urdu_phone}\n"
            bill += f"Phone: {customer['phone']}\n\n"
        
        # Payment type
        if payment_type == 'credit':
            bill += "ادائیگی کی قسم: ادھار\n"
            bill += "Payment Type: CREDIT\n\n"
        else:
            bill += "ادائیگی کی قسم: نقد\n"
            bill += "Payment Type: CASH\n\n"
        
        bill += "=" * 60 + "\n"
        bill += "                   اشیاء کی فہرست\n"
        bill += "                    ITEMS LIST\n"
        bill += "=" * 60 + "\n\n"
        
        # Table header
        bill += f"{'شے':>25} {'قیمت':>10} {'تعداد':>10} {'کل':>10}\n"
        bill += f"{'Item':<25} {'Price':>10} {'Qty':>10} {'Total':>10}\n"
        bill += "-" * 60 + "\n"
        
        # Items
        for item in cart_items:
            # Use Urdu name if available, otherwise use English name
            item_name = item.get('urdu_name', '') or item['name']
            
            urdu_price = self.to_urdu_number(f"{item['price']:.2f}")
            urdu_qty = self.to_urdu_number(item['quantity'])
            urdu_total = self.to_urdu_number(f"{item['total']:.2f}")
            
            # Urdu line
            bill += f"{item_name:>25} {urdu_price:>10} {urdu_qty:>10} {urdu_total:>10}\n"
            # English line
            bill += f"{item['name']:<25} {item['price']:>10.2f} {item['quantity']:>10} {item['total']:>10.2f}\n"
            bill += "\n"
        
        bill += "=" * 60 + "\n"
        
        # Total
        urdu_total = self.to_urdu_number(f"{total_amount:.2f}")
        bill += f"\n{'کل رقم:':>30} روپے {urdu_total}\n"
        bill += f"{'TOTAL AMOUNT:':>30} Rs. {total_amount:.2f}\n\n"
        
        bill += "=" * 60 + "\n"
        
        # Footer message
        if payment_type == 'credit':
            bill += "\n                  یہ رقم آپ کے ادھار میں شامل کر دی گئی ہے\n"
            bill += "              This amount has been added to your credit\n\n"
        else:
            bill += "\n                        شکریہ! دوبارہ تشریف لائیں\n"
            bill += "                    Thank you! Please visit again\n\n"
        
        bill += "=" * 60 + "\n"
        
        return bill
