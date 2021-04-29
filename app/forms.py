from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import email_validator

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(message="Это поле не может быть пустым"), Email(message="Неверный формат email")])
	password = PasswordField('Пароль', validators=[DataRequired(message="Это поле не может быть пустым")])
	remember_me = BooleanField('Запомнить меня')
	submit = SubmitField('Вход')

class RegistrationForm(FlaskForm):
	name = StringField('Имя', validators=[DataRequired(message="Это поле не может быть пустым")])
	surname = StringField('Фамилия', validators=[DataRequired(message="Это поле не может быть пустым")])
	email = StringField('Email', validators=[DataRequired(message="Это поле не может быть пустым"), Email(message="Неверный формат email")])
	adress = StringField('Адрес', validators=[DataRequired(message="Это поле не может быть пустым")])
	password = PasswordField('Пароль', validators=[DataRequired(message="Это поле не может быть пустым")])
	password1 = PasswordField('Повторите пароль', validators=[DataRequired(message="Это поле не может быть пустым"), EqualTo('password')])
	submit = SubmitField('Зарегистрироваться')

class EmailForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(message="Это поле не может быть пустым"), Email(message="Неверный формат email")])
	submit = SubmitField('Отправить')

class ChangePasswordForm(FlaskForm):
	password = PasswordField('Новый пароль', validators=[DataRequired(message="Это поле не может быть пустым")])
	password1 = PasswordField('Повторите новый пароль', validators=[DataRequired(message="Это поле не может быть пустым"), EqualTo('password')])
	submit = SubmitField('Изменить пароль')

class SearchForm(FlaskForm):
	search = StringField('Поиск', validators=[DataRequired(message="Это поле не может быть пустым")])
	submit = SubmitField('Найти')