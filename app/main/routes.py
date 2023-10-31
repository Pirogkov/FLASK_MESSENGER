from app.main import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')