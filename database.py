#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database module for Shop Billing System
Handles SQLite database operations
"""

import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name='shop_billing.db'):
        self.db_name = db_name
        self.conn = None
        self.create_tables()
        
    def get_connection(self):
        """Get database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row
        return self.conn
        
    def create_tables(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT,
                credit_balance REAL DEFAULT 0.0,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                urdu_name TEXT,
                price REAL NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                total_amount REAL NOT NULL,
                payment_type TEXT NOT NULL,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # Transaction items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaction_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (transaction_id) REFERENCES transactions (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Credit payments table (for tracking credit payments)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credit_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        conn.commit()
        
        # Add some sample data if tables are empty
        self.add_sample_data()
        
    def add_sample_data(self):
        """Add sample data if database is empty"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if products exist
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] == 0:
            sample_products = [
                ('Rice 1kg', 'چاول 1 کلو', 150.0),
                ('Wheat Flour 1kg', 'آٹا 1 کلو', 80.0),
                ('Sugar 1kg', 'چینی 1 کلو', 120.0),
                ('Cooking Oil 1L', 'کھانا پکانے کا تیل 1 لیٹر', 450.0),
                ('Tea 500g', 'چائے 500 گرام', 200.0),
                ('Salt 1kg', 'نمک 1 کلو', 40.0),
                ('Milk 1L', 'دودھ 1 لیٹر', 180.0),
                ('Eggs (dozen)', 'انڈے (درجن)', 250.0),
                ('Bread', 'روٹی', 60.0),
                ('Biscuits', 'بسکٹ', 100.0),
            ]
            
            for name, urdu_name, price in sample_products:
                cursor.execute('INSERT INTO products (name, urdu_name, price) VALUES (?, ?, ?)',
                             (name, urdu_name, price))
            
            conn.commit()
    
    def add_customer(self, name, phone, address=''):
        """Add a new customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)',
                      (name, phone, address))
        conn.commit()
        return cursor.lastrowid
        
    def get_customer(self, customer_id):
        """Get customer by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
        
    def get_all_customers(self):
        """Get all customers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]
        
    def update_customer_credit(self, customer_id, amount):
        """Update customer credit balance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE customers SET credit_balance = credit_balance + ? WHERE id = ?',
                      (amount, customer_id))
        conn.commit()
        
    def add_product(self, name, price, urdu_name=''):
        """Add a new product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, urdu_name, price) VALUES (?, ?, ?)',
                      (name, urdu_name, price))
        conn.commit()
        return cursor.lastrowid
        
    def get_product(self, product_id):
        """Get product by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
        
    def get_all_products(self):
        """Get all products"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]
        
    def create_transaction(self, customer_id, total_amount, payment_type):
        """Create a new transaction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (customer_id, total_amount, payment_type, transaction_date)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, total_amount, payment_type, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        return cursor.lastrowid
        
    def add_transaction_item(self, transaction_id, product_id, quantity, unit_price):
        """Add item to transaction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        total_price = quantity * unit_price
        cursor.execute('''
            INSERT INTO transaction_items (transaction_id, product_id, quantity, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (transaction_id, product_id, quantity, unit_price, total_price))
        conn.commit()
        
    def get_transaction(self, transaction_id):
        """Get transaction by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
        
    def get_all_transactions(self):
        """Get all transactions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions ORDER BY transaction_date DESC LIMIT 100')
        return [dict(row) for row in cursor.fetchall()]
        
    def get_transaction_items(self, transaction_id):
        """Get all items for a transaction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ti.*, p.name, p.urdu_name
            FROM transaction_items ti
            JOIN products p ON ti.product_id = p.id
            WHERE ti.transaction_id = ?
        ''', (transaction_id,))
        return [dict(row) for row in cursor.fetchall()]
        
    def add_credit_payment(self, customer_id, amount, notes=''):
        """Record a credit payment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO credit_payments (customer_id, amount, notes)
            VALUES (?, ?, ?)
        ''', (customer_id, amount, notes))
        
        # Update customer credit balance
        cursor.execute('UPDATE customers SET credit_balance = credit_balance - ? WHERE id = ?',
                      (amount, customer_id))
        conn.commit()
        return cursor.lastrowid
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
