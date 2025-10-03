from __future__ import annotations

import os
from datetime import datetime
from decimal import Decimal

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


# -----------------------------------------------------------------------------
# App & Database setup
# -----------------------------------------------------------------------------

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "billing.sqlite3")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

URDU_DIGITS_MAP = {
    "0": "۰",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "۴",
    "5": "۵",
    "6": "۶",
    "7": "۷",
    "8": "۸",
    "9": "۹",
}


def to_urdu_digits(value: object) -> str:
    text = str(value)
    return "".join(URDU_DIGITS_MAP.get(ch, ch) for ch in text)


app.jinja_env.filters["urdu"] = to_urdu_digits


def parse_decimal(value: str) -> Decimal:
    try:
        return Decimal(value)
    except Exception:
        return Decimal("0")


# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    opening_balance = db.Column(db.Numeric(12, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    invoices = db.relationship("Invoice", back_populates="customer", lazy="dynamic")
    payments = db.relationship("Payment", back_populates="customer", lazy="dynamic")

    def balance(self) -> Decimal:
        total_invoices = (
            db.session.query(db.func.coalesce(db.func.sum(Invoice.total_amount), 0))
            .filter(Invoice.customer_id == self.id, Invoice.is_credit.is_(True))
            .scalar()
        )
        total_payments = (
            db.session.query(db.func.coalesce(db.func.sum(Payment.amount), 0))
            .filter(Payment.customer_id == self.id)
            .scalar()
        )
        return Decimal(self.opening_balance or 0) + Decimal(total_invoices or 0) - Decimal(total_payments or 0)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_credit = db.Column(db.Boolean, default=False)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)

    customer = db.relationship("Customer", back_populates="invoices")
    items = db.relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoice.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    quantity = db.Column(db.Numeric(12, 2), nullable=False, default=1)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    line_total = db.Column(db.Numeric(12, 2), nullable=False, default=0)

    invoice = db.relationship("Invoice", back_populates="items")
    product = db.relationship("Product")


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    method = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.String(255), nullable=True)

    customer = db.relationship("Customer", back_populates="payments")


with app.app_context():
    db.create_all()


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------


@app.get("/")
def dashboard():
    customer_count = Customer.query.count()
    product_count = Product.query.count()
    invoice_count = Invoice.query.count()
    total_receivables = Decimal(
        db.session.query(db.func.coalesce(db.func.sum(Invoice.total_amount), 0))
        .filter(Invoice.is_credit.is_(True))
        .scalar()
    )
    total_payments = Decimal(
        db.session.query(db.func.coalesce(db.func.sum(Payment.amount), 0)).scalar()
    )
    outstanding = total_receivables - total_payments
    recent_invoices = Invoice.query.order_by(Invoice.created_at.desc()).limit(10).all()
    return render_template(
        "dashboard.html",
        customer_count=customer_count,
        product_count=product_count,
        invoice_count=invoice_count,
        outstanding=outstanding,
        recent_invoices=recent_invoices,
    )


# Customers
@app.get("/customers")
def customers_list():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return render_template("customers.html", customers=customers)


@app.post("/customers")
def customers_create():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone")
    address = request.form.get("address")
    opening_balance = parse_decimal(request.form.get("opening_balance", "0"))
    if not name:
        flash("Name is required", "error")
        return redirect(url_for("customers_list"))
    customer = Customer(name=name, phone=phone, address=address, opening_balance=opening_balance)
    db.session.add(customer)
    db.session.commit()
    flash("Customer added", "success")
    return redirect(url_for("customers_list"))


@app.post("/customers/<int:customer_id>/delete")
def customers_delete(customer_id: int):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash("Customer deleted", "success")
    return redirect(url_for("customers_list"))


# Products
@app.get("/products")
def products_list():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("products.html", products=products)


@app.post("/products")
def products_create():
    name = request.form.get("name", "").strip()
    unit_price = parse_decimal(request.form.get("unit_price", "0"))
    if not name:
        flash("Product name is required", "error")
        return redirect(url_for("products_list"))
    product = Product(name=name, unit_price=unit_price)
    db.session.add(product)
    db.session.commit()
    flash("Product added", "success")
    return redirect(url_for("products_list"))


@app.post("/products/<int:product_id>/delete")
def products_delete(product_id: int):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted", "success")
    return redirect(url_for("products_list"))


# Payments
@app.get("/payments")
def payments_list():
    customers = Customer.query.order_by(Customer.name.asc()).all()
    payments = Payment.query.order_by(Payment.created_at.desc()).limit(100).all()
    return render_template("payments.html", customers=customers, payments=payments)


@app.post("/payments")
def payments_create():
    customer_id = int(request.form.get("customer_id"))
    amount = parse_decimal(request.form.get("amount", "0"))
    method = request.form.get("method")
    notes = request.form.get("notes")
    payment = Payment(customer_id=customer_id, amount=amount, method=method, notes=notes)
    db.session.add(payment)
    db.session.commit()
    flash("Payment recorded", "success")
    return redirect(url_for("payments_list"))


@app.get("/customers/<int:customer_id>/statement")
def customer_statement(customer_id: int):
    customer = Customer.query.get_or_404(customer_id)
    invoices = (
        Invoice.query.filter_by(customer_id=customer.id, is_credit=True)
        .order_by(Invoice.created_at.asc())
        .all()
    )
    payments = (
        Payment.query.filter_by(customer_id=customer.id)
        .order_by(Payment.created_at.asc())
        .all()
    )
    balance = customer.balance()
    return render_template(
        "statement.html", customer=customer, invoices=invoices, payments=payments, balance=balance
    )


# Invoices
@app.get("/invoices/new")
def invoice_new():
    customers = Customer.query.order_by(Customer.name.asc()).all()
    products = Product.query.order_by(Product.name.asc()).all()
    return render_template("invoice_new.html", customers=customers, products=products)


@app.post("/invoices")
def invoice_create():
    customer_id_raw = request.form.get("customer_id")
    is_credit = request.form.get("is_credit") == "on"

    customer_id = int(customer_id_raw) if customer_id_raw else None

    # Collect items
    descriptions = request.form.getlist("description")
    product_ids = request.form.getlist("product_id")
    quantities = request.form.getlist("quantity")
    unit_prices = request.form.getlist("unit_price")

    items: list[InvoiceItem] = []
    total = Decimal("0")
    for idx in range(len(descriptions)):
        desc = (descriptions[idx] or "").strip()
        pid_raw = (product_ids[idx] or "").strip()
        qty = parse_decimal(quantities[idx]) if idx < len(quantities) else Decimal("0")
        price = parse_decimal(unit_prices[idx]) if idx < len(unit_prices) else Decimal("0")
        if not desc and not pid_raw:
            continue
        line_total = qty * price
        total += line_total
        pid = int(pid_raw) if pid_raw else None
        items.append(
            InvoiceItem(product_id=pid, description=desc, quantity=qty, unit_price=price, line_total=line_total)
        )

    invoice = Invoice(customer_id=customer_id, is_credit=is_credit, total_amount=total)
    db.session.add(invoice)
    db.session.flush()  # get invoice id
    for it in items:
        it.invoice_id = invoice.id
        db.session.add(it)
    db.session.commit()

    flash("Invoice created", "success")
    return redirect(url_for("invoice_view_urdu", invoice_id=invoice.id))


@app.get("/invoices/<int:invoice_id>/print")
def invoice_view_urdu(invoice_id: int):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template("invoice_view_urdu.html", invoice=invoice)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

