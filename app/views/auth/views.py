from datetime import datetime
from flask import flash, render_template, redirect, url_for, request, session
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from app import db, login_manager
from .forms import LoginForm, RegistrationForm, ChangePassForm
from app.models import User
from config import ROOT_URL, USER_AUDIT_ENABLED


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.verify_password(form.password.data):
                if USER_AUDIT_ENABLED:  # current_app.config.get('USER_AUDIT_ENABLED'):
                    if user.activated == '1':
                        if not user.is_locked:
                            user.last_login = datetime.now()
                            db.session.commit()
                            login_user(user, form.remember_me.data)
                            session.permanent = True
                            return redirect(request.args.get('next') or ROOT_URL)
                        else:
                            flash('用户账号已锁定，请联系管理员！', 'danger')
                    else:
                        flash('用户注册信息审核中！', 'warning')
                else:
                    user.last_login = datetime.now()
                    db.session.commit()
                    login_user(user, form.remember_me.data)
                    session.permanent = True
                    return redirect(request.args.get('next') or ROOT_URL)
            else:
                flash('用户名或密码错误！', 'danger')
        else:
            flash('用户名或密码错误!', 'danger')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # flash('您已登出系统！', 'warning')
    # return redirect(url_for('auth.login'))
    return redirect(ROOT_URL)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        print("new register request!")
        user = User(username=form.username.data,
                    password=form.password.data,
                    email=form.email.data,
                    mobile=form.mobile.data)
        user.activated = 'A'
        db.session.add(user)
        db.session.commit()
        flash('注册申请已提交！', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/change_pass', methods=['GET', 'POST'])
@login_required
def change_pass():
    form = ChangePassForm()
    if form.validate_on_submit():
        user_id = current_user.get_id()
        user = User.query.filter_by(id=user_id).first()
        user.password = form.password.data
        user.pwd_set_time = datetime.now()
        db.session.commit()
        logout_user()
        flash('密码修改成功！请重新登录', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/change_pass.html', form=form)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))
