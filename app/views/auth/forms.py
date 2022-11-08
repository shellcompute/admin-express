from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired as Required, DataRequired, Length, Regexp, EqualTo, ValidationError, Email, Optional

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('请输入用户名', validators=[Required(), Length(1, 64)])
    password = PasswordField('请输入密码', validators=[Required()])
    # flask_login提供快捷记住我cookie保存
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('请输入用户名', validators=[
        DataRequired(message=u'用户名不能为空'),
        Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能包含字母、数字、点或下划线')])
    email = StringField('Email', validators=[
        Optional(),
        Email()
        # Regexp('^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+)+$', 0, '请输入正确的电子邮箱地址！')
    ])
    mobile = StringField('手机号码', validators=[
        Optional(),
        Regexp('^1[35-9][0-9]{9}$', 0, '请输入正确的手机号码')
    ])
    password = PasswordField('请输入密码', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('请确认密码', validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已存在！')

    def validate(self):
        if not super().validate():
            return False
        if not self.email.data and not self.mobile.data:
            msg = 'Email和手机号码不能同时为空!'
            self.email.errors.append(msg)
            self.mobile.errors.append(msg)
            return False
        return True


class ChangePassForm(FlaskForm):
    old_pass = PasswordField('请输入旧密码', validators=[Required()])
    password = PasswordField('请输入新密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('请确认新密码', validators=[Required()])
    submit = SubmitField('确认')

    def validate_old_pass(self, field):
        pass
