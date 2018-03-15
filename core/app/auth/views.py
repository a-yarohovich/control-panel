from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .. models import User
from . forms import LoginForm
from validate_email import validate_email
from logger import logger

LOG = logger.LOG


def login_int(user_or_mail, passwd, remember_me):
    if validate_email(user_or_mail):
        user = User.get_user_by_email(email=user_or_mail)
    else:
        user = User.get_user_by_name(username=user_or_mail)

    if user and user.verify_password(passwd):
        login_user(user, remember_me)
        return redirect(request.args.get('next') or url_for('main.index'))
    flash('Invalid username or password.')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_or_mail = form.username_or_email.data
        password = form.password.data
        remember_me = form.remember_me.data
        return login_int(user_or_mail, password, remember_me)
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
