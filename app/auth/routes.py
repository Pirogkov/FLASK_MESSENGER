from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user

from app.models import User
from app.auth.forms import LoginForm, RegisterationForm
from app.auth import bp
from app import db


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.chek_password(form.password.data):
            flash('неверный пользователь')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))

    return render_template('auth/login.html', title='Войти', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, ls=form.ls.data)#, room='1', )
        user.set_password(form.password.data)
        user.generate_room_code()
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем вы зарегистрировались')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Присоединиться', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

