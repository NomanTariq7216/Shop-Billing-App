#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
دکان بلنگ سسٹم - Shop Billing System
Credit-based billing system with Urdu language support
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import sqlite3
from database import Database
from bill_generator import BillGenerator

class ShopBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("دکان بلنگ سسٹم - Shop Billing System")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Initialize database
        self.db = Database()
        self.bill_gen = BillGenerator()
        
        # Variables
        self.cart = []
        self.selected_customer = None
        
        # Setup UI
        self.setup_ui()
        self.load_products()
        self.load_customers()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left Panel - Customer and Product Management
        left_frame = ttk.LabelFrame(main_frame, text="Customer & Products", padding="10")
        left_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Customer Selection
        ttk.Label(left_frame, text="Select Customer:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.customer_combo = ttk.Combobox(left_frame, width=30, state='readonly')
        self.customer_combo.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.customer_combo.bind('<<ComboboxSelected>>', self.on_customer_select)
        
        ttk.Button(left_frame, text="Add New Customer", command=self.add_customer_dialog).grid(
            row=2, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Customer Info Display
        self.customer_info = tk.Text(left_frame, height=4, width=35, state='disabled')
        self.customer_info.grid(row=3, column=0, columnspan=2, pady=5)
        
        ttk.Separator(left_frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Product Management
        ttk.Label(left_frame, text="Product Management:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Button(left_frame, text="Add Product", command=self.add_product_dialog).grid(
            row=6, column=0, pady=5, sticky=(tk.W, tk.E), padx=(0, 2))
        ttk.Button(left_frame, text="View Products", command=self.view_products).grid(
            row=6, column=1, pady=5, sticky=(tk.W, tk.E), padx=(2, 0))
        
        ttk.Separator(left_frame, orient='horizontal').grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Add to Cart Section
        ttk.Label(left_frame, text="Add Item to Cart:").grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(left_frame, text="Product:").grid(row=9, column=0, sticky=tk.W)
        self.product_combo = ttk.Combobox(left_frame, width=30, state='readonly')
        self.product_combo.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(left_frame, text="Quantity:").grid(row=11, column=0, sticky=tk.W)
        self.quantity_var = tk.StringVar(value="1")
        ttk.Entry(left_frame, textvariable=self.quantity_var, width=15).grid(row=12, column=0, sticky=tk.W, pady=5)
        
        ttk.Button(left_frame, text="Add to Cart", command=self.add_to_cart).grid(
            row=13, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Right Panel - Cart and Billing
        right_frame = ttk.LabelFrame(main_frame, text="Current Bill", padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        # Cart Tree
        cart_scroll = ttk.Scrollbar(right_frame)
        cart_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.cart_tree = ttk.Treeview(right_frame, columns=('Product', 'Price', 'Qty', 'Total'), 
                                       show='headings', yscrollcommand=cart_scroll.set)
        cart_scroll.config(command=self.cart_tree.yview)
        
        self.cart_tree.heading('Product', text='Product')
        self.cart_tree.heading('Price', text='Price')
        self.cart_tree.heading('Qty', text='Quantity')
        self.cart_tree.heading('Total', text='Total')
        
        self.cart_tree.column('Product', width=250)
        self.cart_tree.column('Price', width=100)
        self.cart_tree.column('Qty', width=80)
        self.cart_tree.column('Total', width=100)
        
        self.cart_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cart Controls
        cart_controls = ttk.Frame(right_frame)
        cart_controls.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(cart_controls, text="Remove Selected", command=self.remove_from_cart).pack(side=tk.LEFT, padx=5)
        ttk.Button(cart_controls, text="Clear Cart", command=self.clear_cart).pack(side=tk.LEFT, padx=5)
        
        # Total Display
        total_frame = ttk.Frame(right_frame)
        total_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        ttk.Label(total_frame, text="Total Amount:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        self.total_label = ttk.Label(total_frame, text="Rs. 0.00", font=('Arial', 14, 'bold'), foreground='blue')
        self.total_label.pack(side=tk.LEFT, padx=5)
        
        # Action Buttons
        action_frame = ttk.Frame(right_frame)
        action_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(action_frame, text="Generate Bill (Credit)", command=self.generate_credit_bill, 
                   style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Cash Payment", command=self.cash_payment).pack(side=tk.LEFT, padx=5)
        
        # Bottom Panel - Bill Preview
        bottom_frame = ttk.LabelFrame(main_frame, text="Bill Preview (Urdu)", padding="10")
        bottom_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.rowconfigure(0, weight=1)
        
        self.bill_preview = scrolledtext.ScrolledText(bottom_frame, height=15, width=60, 
                                                      font=('Arial', 10), wrap=tk.WORD)
        self.bill_preview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Menu Bar
        self.create_menu()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Bill", command=self.new_bill)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Reports Menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Customer Credit Report", command=self.show_credit_report)
        reports_menu.add_command(label="Sales History", command=self.show_sales_history)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def load_customers(self):
        customers = self.db.get_all_customers()
        customer_list = [f"{c['id']} - {c['name']}" for c in customers]
        self.customer_combo['values'] = customer_list
        
    def load_products(self):
        products = self.db.get_all_products()
        product_list = [f"{p['id']} - {p['name']} (Rs. {p['price']})" for p in products]
        self.product_combo['values'] = product_list
        
    def on_customer_select(self, event):
        selection = self.customer_combo.get()
        if selection:
            customer_id = int(selection.split(' - ')[0])
            customer = self.db.get_customer(customer_id)
            self.selected_customer = customer
            
            self.customer_info.config(state='normal')
            self.customer_info.delete('1.0', tk.END)
            self.customer_info.insert('1.0', 
                f"Name: {customer['name']}\n"
                f"Phone: {customer['phone']}\n"
                f"Current Credit: Rs. {customer['credit_balance']:.2f}\n"
                f"Address: {customer.get('address', 'N/A')}")
            self.customer_info.config(state='disabled')
            
    def add_customer_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Customer")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Customer Name:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Phone Number:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        phone_entry = ttk.Entry(dialog, width=30)
        phone_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Address:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        address_entry = ttk.Entry(dialog, width=30)
        address_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def save_customer():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_entry.get().strip()
            
            if not name or not phone:
                messagebox.showerror("Error", "Name and Phone are required!")
                return
                
            self.db.add_customer(name, phone, address)
            messagebox.showinfo("Success", "Customer added successfully!")
            self.load_customers()
            dialog.destroy()
            
        ttk.Button(dialog, text="Save", command=save_customer).grid(row=3, column=0, columnspan=2, pady=20)
        
    def add_product_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Product Name:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Price (Rs.):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        price_entry = ttk.Entry(dialog, width=30)
        price_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Urdu Name (Optional):").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        urdu_entry = ttk.Entry(dialog, width=30)
        urdu_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def save_product():
            name = name_entry.get().strip()
            urdu_name = urdu_entry.get().strip()
            try:
                price = float(price_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Invalid price!")
                return
                
            if not name or price <= 0:
                messagebox.showerror("Error", "Valid name and price are required!")
                return
                
            self.db.add_product(name, price, urdu_name)
            messagebox.showinfo("Success", "Product added successfully!")
            self.load_products()
            dialog.destroy()
            
        ttk.Button(dialog, text="Save", command=save_product).grid(row=3, column=0, columnspan=2, pady=20)
        
    def view_products(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Product List")
        dialog.geometry("600x400")
        
        tree_scroll = ttk.Scrollbar(dialog)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(dialog, columns=('ID', 'Name', 'Urdu Name', 'Price'), 
                           show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Product Name')
        tree.heading('Urdu Name', text='Urdu Name')
        tree.heading('Price', text='Price')
        
        tree.column('ID', width=50)
        tree.column('Name', width=200)
        tree.column('Urdu Name', width=200)
        tree.column('Price', width=100)
        
        products = self.db.get_all_products()
        for p in products:
            tree.insert('', 'end', values=(p['id'], p['name'], p['urdu_name'] or 'N/A', f"Rs. {p['price']}"))
            
        tree.pack(fill=tk.BOTH, expand=True)
        
    def add_to_cart(self):
        if not self.product_combo.get():
            messagebox.showwarning("Warning", "Please select a product!")
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity!")
            return
            
        product_id = int(self.product_combo.get().split(' - ')[0])
        product = self.db.get_product(product_id)
        
        total = product['price'] * quantity
        
        self.cart.append({
            'product_id': product_id,
            'name': product['name'],
            'urdu_name': product['urdu_name'],
            'price': product['price'],
            'quantity': quantity,
            'total': total
        })
        
        self.update_cart_display()
        
    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if selected:
            index = self.cart_tree.index(selected[0])
            self.cart.pop(index)
            self.update_cart_display()
            
    def clear_cart(self):
        self.cart = []
        self.update_cart_display()
        
    def update_cart_display(self):
        # Clear tree
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
            
        # Add items
        total_amount = 0
        for item in self.cart:
            self.cart_tree.insert('', 'end', values=(
                item['name'],
                f"Rs. {item['price']:.2f}",
                item['quantity'],
                f"Rs. {item['total']:.2f}"
            ))
            total_amount += item['total']
            
        self.total_label.config(text=f"Rs. {total_amount:.2f}")
        
    def generate_credit_bill(self):
        if not self.selected_customer:
            messagebox.showwarning("Warning", "Please select a customer!")
            return
            
        if not self.cart:
            messagebox.showwarning("Warning", "Cart is empty!")
            return
            
        # Calculate total
        total_amount = sum(item['total'] for item in self.cart)
        
        # Create transaction
        transaction_id = self.db.create_transaction(
            self.selected_customer['id'],
            total_amount,
            'credit'
        )
        
        # Add transaction items
        for item in self.cart:
            self.db.add_transaction_item(
                transaction_id,
                item['product_id'],
                item['quantity'],
                item['price']
            )
        
        # Update customer credit
        self.db.update_customer_credit(self.selected_customer['id'], total_amount)
        
        # Generate Urdu bill
        bill_text = self.bill_gen.generate_bill(
            transaction_id,
            self.selected_customer,
            self.cart,
            total_amount,
            'credit'
        )
        
        # Display bill
        self.bill_preview.delete('1.0', tk.END)
        self.bill_preview.insert('1.0', bill_text)
        
        messagebox.showinfo("Success", f"Bill generated! Transaction ID: {transaction_id}\nAmount added to credit: Rs. {total_amount:.2f}")
        
        # Reset
        self.new_bill()
        self.load_customers()
        
    def cash_payment(self):
        if not self.cart:
            messagebox.showwarning("Warning", "Cart is empty!")
            return
            
        # Calculate total
        total_amount = sum(item['total'] for item in self.cart)
        
        # Create transaction (cash - no customer required)
        transaction_id = self.db.create_transaction(
            None,  # No customer for cash
            total_amount,
            'cash'
        )
        
        # Add transaction items
        for item in self.cart:
            self.db.add_transaction_item(
                transaction_id,
                item['product_id'],
                item['quantity'],
                item['price']
            )
        
        # Generate Urdu bill
        bill_text = self.bill_gen.generate_bill(
            transaction_id,
            {'name': 'نقد گاہک', 'phone': '', 'address': ''},  # Cash customer
            self.cart,
            total_amount,
            'cash'
        )
        
        # Display bill
        self.bill_preview.delete('1.0', tk.END)
        self.bill_preview.insert('1.0', bill_text)
        
        messagebox.showinfo("Success", f"Cash bill generated! Transaction ID: {transaction_id}")
        
        # Reset
        self.new_bill()
        
    def new_bill(self):
        self.cart = []
        self.selected_customer = None
        self.customer_combo.set('')
        self.customer_info.config(state='normal')
        self.customer_info.delete('1.0', tk.END)
        self.customer_info.config(state='disabled')
        self.update_cart_display()
        self.bill_preview.delete('1.0', tk.END)
        
    def show_credit_report(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Customer Credit Report")
        dialog.geometry("700x500")
        
        tree_scroll = ttk.Scrollbar(dialog)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(dialog, columns=('ID', 'Name', 'Phone', 'Credit'), 
                           show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Customer Name')
        tree.heading('Phone', text='Phone')
        tree.heading('Credit', text='Credit Balance')
        
        tree.column('ID', width=50)
        tree.column('Name', width=200)
        tree.column('Phone', width=150)
        tree.column('Credit', width=150)
        
        customers = self.db.get_all_customers()
        total_credit = 0
        for c in customers:
            if c['credit_balance'] > 0:
                tree.insert('', 'end', values=(c['id'], c['name'], c['phone'], f"Rs. {c['credit_balance']:.2f}"))
                total_credit += c['credit_balance']
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        total_label = ttk.Label(dialog, text=f"Total Outstanding Credit: Rs. {total_credit:.2f}", 
                               font=('Arial', 12, 'bold'))
        total_label.pack(pady=10)
        
    def show_sales_history(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Sales History")
        dialog.geometry("800x500")
        
        tree_scroll = ttk.Scrollbar(dialog)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(dialog, columns=('ID', 'Date', 'Customer', 'Amount', 'Type'), 
                           show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        
        tree.heading('ID', text='Trans. ID')
        tree.heading('Date', text='Date/Time')
        tree.heading('Customer', text='Customer')
        tree.heading('Amount', text='Amount')
        tree.heading('Type', text='Payment Type')
        
        tree.column('ID', width=80)
        tree.column('Date', width=180)
        tree.column('Customer', width=200)
        tree.column('Amount', width=120)
        tree.column('Type', width=100)
        
        transactions = self.db.get_all_transactions()
        for t in transactions:
            customer_name = 'Cash Customer' if t['customer_id'] is None else self.db.get_customer(t['customer_id'])['name']
            tree.insert('', 'end', values=(
                t['id'],
                t['transaction_date'],
                customer_name,
                f"Rs. {t['total_amount']:.2f}",
                t['payment_type'].upper()
            ))
            
        tree.pack(fill=tk.BOTH, expand=True)
        
    def show_about(self):
        messagebox.showinfo("About", 
            "Shop Billing System v1.0\n\n"
            "Credit-based billing with Urdu support\n"
            "Compatible with Linux and Windows\n\n"
            "© 2025")

def main():
    root = tk.Tk()
    app = ShopBillingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
