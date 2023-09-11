from flask import Blueprint, render_template, redirect, url_for, flash
from autostock.mechanics.forms import RegistrationForm, LoginForm


mechanics = Blueprint('mechanics', __name__)


@mechanics.route('/create_mechanic', methods=['GET', 'POST'])
def create_mechanic():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Mechanic {form.mechanic.data} created successfully', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_mechanic.html', title='Create Mechanic', form=form)


@mechanics.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'bona@autostock.com' and form.password.data == 'password':
            flash('You have been logged in successfully', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful, Check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
