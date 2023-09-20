from flask import Blueprint, flash, redirect, url_for, render_template, request, jsonify
from flask_login import current_user, login_required
from autoinvento.suppliers.forms import AddSupplier
from autoinvento.models import Supplier, InventoryItem
from autoinvento import db
from sqlalchemy import func


supplier = Blueprint('supplier', __name__)


@supplier.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_suppliers():
    form = AddSupplier()
    if not current_user.is_authenticated or not current_user.is_superuser:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('users.mechanic_dashboard'))
    if form.validate_on_submit():
        supplier = Supplier(name=form.name.data, email=form.email.data, contact=form.contact.data)
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier successfully inserted!', 'success')
        return redirect(url_for('supplier.suppliers'))
    return render_template('add_suppliers.html', title='Add Suppliers', legend='Add Supplier', form=form)


@supplier.route('/supplier/view', methods=['GET', 'POST'])
@login_required
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', title='Suppliers', suppliers=suppliers)


@supplier.route('/suppliers/view/<int:supplier_id>', methods=['GET', 'POST'])
@login_required
def view_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    supplier_products = InventoryItem.query.filter_by(supplier_id=supplier.id).all()
    return render_template('view_supplier.html', title=supplier.name, supplier=supplier, supplier_products=supplier_products)



@supplier.route('/suppliers/<int:supplier_id>/update', methods=['GET', 'POST'])
@login_required
def update_supplier(supplier_id):
    if not current_user.is_authenticated or not current_user.is_superuser:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('users.mechanic_dashboard'))
    
    supplier = Supplier.query.get_or_404(supplier_id)
    form = AddSupplier()
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.email = form.email.data
        supplier.contact = form.contact.data
        supplier.phone_number = form.phone_number.data
        db.session.commit()
        flash('Supplier Information updated successfully!', 'success')
        return redirect(url_for('supplier.suppliers'))
    elif request.method == 'GET':
        form.name.data = supplier.name
        form.email.data = supplier.email
        form.contact.data = supplier.contact
        form.phone_number.data = supplier.phone_number
    return render_template('add_suppliers.html', title=f'Update {supplier.name}', legend='Update Supplier', supplier=supplier, form=form)


@supplier.route('/suppliers/<int:supplier_id>/delete', methods=['POST'])
@login_required
def delete_supplier(supplier_id):
    if not current_user.is_authenticated or not current_user.is_superuser:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('users.mechanic_dashboard'))
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    flash('Supplier deleted successfully!', 'success')
    return redirect(url_for('supplier.suppliers', supplier=supplier))


@supplier.route('/api/inventory-data')
@login_required
def get_inventory_supplier_data():
    # Query the database to get the quantity of items supplied by each supplier
    supplier_data = (
        Supplier.query
        .join(InventoryItem, Supplier.id == InventoryItem.supplier_id)
        .with_entities(Supplier.name, func.sum(InventoryItem.quantity).label('total_quantity'))
        .group_by(Supplier.name)
        .all()
    )

    # Convert the data to a format suitable for returning as JSON
    data_for_chart = [{'supplier': item[0], 'total_quantity': item[1]} for item in supplier_data]

    return jsonify(data_for_chart)