from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import uuid
from sqlalchemy import desc
from .models import Item, User, Role
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
        return render_template('index.html')

@views.route("/admin")
def admin():
        return render_template('admin.html')

@views.route("/add_item", methods=["GET", "POST"])
@login_required
def add_item():
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        brand = request.form.get('brand')
        color = request.form.get('color')
        price = request.form.get('price')
        discount = request.form.get('discount')
        stock_quantity = request.form.get('stock_quantity')
        availability_status = request.form.get('availability_status')
        img = str(uuid.uuid4())
        images = request.files['images']
        images.save('website/static/images/' + img + '.jpg')
        image_filename = 'images/' + img + '.jpg'
        tag = request.form.get('tag')
        
        print(img)

        if not name:
            flash('Name cannot be empty', category='error')
        elif not description:
            flash('Description cannot be empty', category='error')
        elif not category:
            flash('Category cannot be empty', category='error')
        elif not brand:
            flash('Brand cannot be empty', category='error')
        elif not color:
            flash('Color cannot be empty', category='error')
        elif not price:
            flash('Price cannot be empty', category='error')
        elif not stock_quantity:
            flash('Stock Quantity cannot be empty', category='error')
        elif not availability_status:
            flash('Availability Status cannot be empty', category='error')
        elif not images:
            flash('At least one image is required', category='error')
        elif not tag:
            flash('Tag cannot be empty', category='error')
        else:
            new_item = Item( name=name, description=description, category=category, brand=brand, color=color, price=price, discount=discount, stock_quantity=stock_quantity, availability_status=availability_status, tag=tag, images = image_filename)
            db.session.add(new_item)
            db.session.commit()
            flash('Added new product!', category='success')
        return redirect(url_for('views.admin'))