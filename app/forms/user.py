# coding=utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length

from app.common.constants import UserRole


class UserForm(Form):
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 20, 'input username')])
    password = PasswordField(u'密码', validators=[Optional()])
    reset_password = BooleanField(u'重置密码', default=False)
    role_admin = BooleanField(u'系统管理员', default=False)
    submit = SubmitField('Submit')

    def init_with_user(self, user):
        if user:
            self.username.data = user.username
            self.password.data = ''
            self.reset_password.data = False
            self.role_admin.data = (user.role == UserRole.ROLE_ADMIN)

