from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required


main = Blueprint('main', __name__)


@main.route('/')
def landing_page():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template('index.html')


@main.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')