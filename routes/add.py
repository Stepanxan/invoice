from datetime import datetime
from flask import render_template, url_for, request, flash, redirect

from app import app, db
from models.models import Product, Invoice


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template("about.html")

@app.route('/', methods=["GET", "POST"])
def add_products():
    id = request.form.get('id')
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')

    if request.method == "POST":
        if len(name) <= 5:
            flash("Назва має містити мінімум 6 символів", category='error')
            return redirect(url_for('add_products'))
        if len(quantity) <= 1:
            flash("Введіть кількість більше 1 шт )", category='error')
            return redirect(url_for('add_products'))
        if len(price) <= 1:
            flash("Введіть ціну більше 1грн)", category='error')
            return redirect(url_for('add_products'))
        else:
            product = Product(
                id=id,
                name = name,
                quantity = quantity,
                price = price
            )
            try:
                db.session.add(product)
                db.session.commit()
                flash("Пост добавлено успішно", category='success')
                return redirect("/")
            except:
                flash("Невідома помилка при добавлянні поста", category='error')
                return redirect(url_for('add_products'))

    else:
        return render_template('add_products.html')


@app.route('/invoice/expense', methods=['POST'])
def create_invoice():
    product_id = request.json['product_id']
    quantity = request.json['quantity']

    product = Product.query.get(product_id)
    if product.quantity < quantity:
        flash("Недостатня кількість товару", category='error')
        return redirect(url_for('add_products'))

    product.quantity -= quantity
    cost = 0
    invoices = Invoice.query.filter_by(product_id=product_id).order_by(Invoice.date.asc()).all()
    for invoice in invoices:
        if quantity >= invoice.quantity:
            cost += invoice.quantity * invoice.price
            quantity -= invoice.quantity
        else:
            cost += quantity * invoice.price
            break

    invoice = Invoice(date=datetime.date.today(), type='expense', product_id=product_id, quantity=quantity, price=cost)
    db.session.add(invoice)
    db.session.commit()

@app.route('/profit_report/<start_date>/<end_date>')
def profit_report(start_date, end_date):
    incomes = Invoice.query.filter(Invoice.date >= start_date, Invoice.date <= end_date).all()
    total_income = sum([income.quantity * income.price for income in incomes])
    total_profit = total_income
    return render_template('profit_report.html', total_profit=total_profit)



