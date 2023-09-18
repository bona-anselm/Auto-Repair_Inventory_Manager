from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from autoinvento.users.forms import CreateMechanicForm, LoginForm, UpdateAccountForm, RequestForm, UpdateMechanicForm, OwnerActionForm, RequestResetForm, ResetPasswordForm
from autoinvento.users.utils import save_picture, send_reset_email
from autoinvento import db, bcrypt
#from flask_mail import Message
from sqlalchemy import func
from autoinvento.models import Mechanics, Supplier, InventoryItem, InventoryRequest
from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint('users', __name__)


@users.route('/create_mechanic', methods=['GET', 'POST'])
def create_mechanic():
    if not current_user.is_authenticated or not current_user.is_superuser:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('users.mechanic_dashboard'))
    form = CreateMechanicForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        is_superuser = form.is_superuser.data
        user = Mechanics(
            username=form.mechanic.data,
            email=form.email.data,
            password=hashed_password,
            is_superuser = is_superuser
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.mechanic.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('create_mechanic.html', title='Create Mechanic', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_superuser:
            return redirect(url_for('users.owner_dashboard'))
        else:
            return redirect(url_for('users.mechanic_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Mechanics.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if user.is_superuser:
                return redirect(next_page) if next_page else redirect(url_for('users.owner_dashboard'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('users.mechanic_dashboard'))
        else:
            flash('Login Unsuccessful, check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/owner/dashboard', methods=(['GET', 'POST']))
@login_required
def owner_dashboard():
    if not current_user.is_authenticated or not current_user.is_superuser:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('users.mechanic_dashboard'))
    total_suppliers = Supplier.query.count()
    mechanics= Mechanics.query.filter_by(is_superuser=False).count()
    total_products = InventoryItem.query.count()
    low_stock = InventoryItem.query.filter(InventoryItem.quantity <= InventoryItem.low_stock_threshold).all()
    total_low_stock = len(low_stock)
    stock_out =InventoryItem.query.filter(InventoryItem.quantity == 0).all()
    total_stock_out = len(stock_out)
    return render_template('owner_dashboard.html', title='Owner DashBoard',
                           total_suppliers=total_suppliers,
                           mechanics=mechanics,
                           total_products=total_products,
                           total_low_stock=total_low_stock,
                           total_stock_out=total_stock_out,
                          #supply_chart_data=supply_chart_data
                           )



@users.route('/mechanic/dashboard', methods=['GET', 'POST'])
@login_required
def mechanic_dashboard():
    if not current_user.is_authenticated or current_user.is_superuser:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('users.owner_dashboard'))
    total_suppliers = Supplier.query.count()
    mechanics = Mechanics.query.filter_by(is_superuser=False).count()
    total_products = InventoryItem.query.count()
    low_stock = InventoryItem.query.filter(InventoryItem.quantity <= InventoryItem.low_stock_threshold).all()
    total_low_stock = len(low_stock)
    stock_out =InventoryItem.query.filter(InventoryItem.quantity == 0).all()
    total_stock_out = len(stock_out)
    return render_template(
                            'mechanic_dashboard.html',
                            title='Mechanic Dashboard',
                            total_suppliers=total_suppliers,
                            mechanics=mechanics,
                           total_products=total_products,
                           total_low_stock=total_low_stock,
                           total_stock_out=total_stock_out
                        )


@users.route('/owner/dashboard/mechanics', methods=(['GET']))
@login_required
def mechanics():
    users = Mechanics.query.filter_by(is_superuser = False).all() 
    return render_template('mechanics.html', title='Mechanics', users=users)


@users.route('/mechanic/<int:mechanic_id>/update', methods=(['GET', 'POST']))
@login_required
def update_mechanic(mechanic_id):
    if not current_user.is_authenticated or not current_user.is_superuser:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('users.mechanic_dashboard'))
    mechanic = Mechanics.query.get_or_404(mechanic_id)
    form = UpdateMechanicForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            mechanic.image_file = picture_file
        mechanic.username = form.username.data
        mechanic.email = form.email.data
        db.session.commit()
        flash('Mechanic updated successfully!', 'success')
        return redirect(url_for('users.mechanics'))
    elif request.method == 'GET':
        form.username.data = mechanic.username
        form.email.data = mechanic.email
    image_file = url_for('static', filename='images/' + mechanic.image_file)
    return render_template('update_mechanic.html', title=f"Update {mechanic.username}", mechanic=mechanic, image_file=image_file, form=form)



@users.route('/mechanic/<int:mechanic_id>/delete', methods=['POST'])
@login_required
def delete_mechanic(mechanic_id):
    if not current_user.is_authenticated or not current_user.is_superuser:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('users.mechanic_dashboard'))
    mechanic = Mechanics.query.get_or_404(mechanic_id)
    db.session.delete(mechanic)
    db.session.commit()
    flash('Mechanic successfully deleted!', 'success')
    return redirect(url_for('users.mechanics'))



@users.route('/submit_request', methods=['GET', 'POST'])
@login_required
def submit_request():
    form = RequestForm()
    form.item_id.choices = [(item.id, item.name) for item in InventoryItem.query.all()]
    
    try:
        if form.validate_on_submit():
            quantity_requested = form.quantity_requested.data
            item_id = form.item_id.data

            # Check if quantity requested is greater than 0
            if quantity_requested <= 0:
                flash('Quantity requested must be greater than 0.', 'danger')
                return render_template('users.submit_request.html', title='Submit Request', form=form)

            # Check if quantity requested is available in InventoryItem
            item = InventoryItem.query.get(item_id)
            if item.quantity < quantity_requested:
                flash(f'Requested quantity ({quantity_requested}) exceeds available stock ({item.quantity}).', 'danger')
                return render_template('submit_request.html', title='Submit Request', form=form)

            # Create a new request using form data
            requests = InventoryRequest(
                item_id=item_id,
                quantity_requested=quantity_requested,
                mechanic_id=current_user.id,
                status='pending'
            )
            db.session.add(requests)
            db.session.commit()
            
            # Notify the owner via email
            owner_email = 'muchiskino@gmail.com' 
            #message = Message('New Request', sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[owner_email])
            #message.body = f'A new request has been submitted by {current_user.username}. Please review it.'
            #mail.send(message)

            flash('Request submitted successfully!', 'success')
            return redirect(url_for('users.submit_request'))

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('submit_request.html', title='Submit Request', form=form)


@users.route('/api/inventory-data')
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



""" MECHANIC REQUEST ROUTES """

@users.route('/view_requests', methods=['GET'])
@login_required
def view_requests():
    # Fetch requests made by the current mechanic
    mechanic_requests = (
        InventoryRequest.query
        .filter_by(mechanic_id=current_user.id)
        .join(InventoryItem)  # Join the InventoryItem table
        .add_columns(InventoryItem.name, InventoryRequest.quantity_requested, InventoryRequest.status, InventoryRequest.request_timestamp)
        .all()
    )
    return render_template('view_requests.html', title='View Requests', requests=mechanic_requests)



@users.route('/manage_requests', methods=['GET', 'POST'])
@login_required
def manage_requests():
    if not current_user.is_superuser:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.mechanic_dashboard'))
    
    # Fetch pending requests
    pending_requests = InventoryRequest.query.filter_by(status='pending').all()
    if not pending_requests:
        flash('There are currently no pending requests!', 'info')
    
    form = OwnerActionForm()

    if request.method == 'POST':
        request_id = request.form.get('request_id')
        action = request.form.get('action') 

        # Find the request by ID
        request_item = InventoryRequest.query.get(request_id)

        if request_item:
            if action == 'approve':
                # Update the request status to approved
                request_item.status = 'approved'

                # Deduct quantity from InventoryItems
                item = InventoryItem.query.get(request_item.item_id)
                item.quantity -= request_item.quantity_requested

                # Remove request from the list
                pending_requests.remove(request_item)

                db.session.commit()
                flash('Request approved successfully!', 'success')
            elif action == 'reject':
                # Update the request status to rejected
                request_item.status = 'rejected'

                # Remove request from the list
                pending_requests.remove(request_item)

                db.session.commit()
                flash('Request rejected!', 'success')
            else:
                flash('Invalid action.', 'danger')
        else:
            flash('Request not found.', 'danger')

    return render_template('manage_requests.html', title='Manage Requests', form=form, request_items=pending_requests)

@users.route('/reset_password', methods=['Get', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Mechanics.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your email', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['Get', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = Mechanics.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit() 
        flash(f'Your password is updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
