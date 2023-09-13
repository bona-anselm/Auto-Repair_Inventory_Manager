from flask import Blueprint, render_template, redirect, url_for, flash, request
from autostock.mechanics.forms import CreateMechanicForm, LoginForm, UpdateAccountForm, RequestForm
from autostock.mechanics.utils import save_picture
from autostock import create_app, db, bcrypt
from autostock.models import Mechanics, Supplier, InventoryItem, InventoryRequest
from flask_login import login_user, current_user, logout_user, login_required


mechanics = Blueprint('mechanics', __name__)


@mechanics.route('/create_mechanic', methods=['GET', 'POST'])
def create_mechanic():
    #if not current_user.is_authenticated or not current_user.is_superuser:
        #flash('You are not authorized to access this page.', 'danger')
        #return redirect(url_for('mechanics.mechanic_dashboard'))
    form = CreateMechanicForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        is_superuser = form.is_superuser.data
        user = Mechanics(
            mechanic=form.mechanic.data,
            email=form.email.data,
            password=hashed_password,
            is_superuser = is_superuser
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.mechanic.data}!', 'success')
        return redirect(url_for('mechanics.login'))
    return render_template('create_mechanic.html', title='Create Mechanic', form=form)


@mechanics.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_superuser:
            return redirect(url_for('mechanics.owner_dashboard'))
        else:
            return redirect(url_for('mechanics.mechanic_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Mechanics.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if user.is_superuser:
                return redirect(next_page) if next_page else redirect(url_for('mechanics.owner_dashboard'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('mechanics.mechanic_dashboard'))
        else:
            flash('Login Unsuccessful, check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@mechanics.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('mechanics.login'))


@mechanics.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('mechanics.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@mechanics.route('/owner/dashboard', methods=(['GET', 'POST']))
@login_required
def owner_dashboard():
    if not current_user.is_authenticated or not current_user.is_superuser:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('mechanics.mechanic_dashboard'))
    total_suppliers = Supplier.query.count()
    mechanics = Mechanics.query.filter_by(is_superuser=False).count()
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




@mechanics.route('/submit_request', methods=['GET', 'POST'])
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
                return render_template('submit_request.html', title='Submit Request', form=form)

            # Check if quantity requested is available in InventoryItem
            item = InventoryItem.query.get(item_id)
            if item.quantity < quantity_requested:
                flash(f'Requested quantity ({quantity_requested}) exceeds available stock ({item.quantity}).', 'danger')
                return render_template('submit_request.html', title='Submit Request', form=form)

            # Create a new request using form data
            requests = InventoryRequest(
                item_id=item_id,
                quantity_requested=quantity_requested,
                user_id=current_user.id,
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
            return redirect(url_for('mechanics.submit_request'))

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('submit_request.html', title='Submit Request', form=form)