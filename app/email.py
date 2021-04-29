from threading import Thread
from flask_mail import Message
from flask import render_template
from app import mail, app

def send_async_email(app, msg):
    with app.app_context():
      mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_confirm_email(user):
	token = user.get_token()
	send_email('MountainShop  Подтверждение аккаунта',
	  sender=app.config['ADMINS'][0],
	  recipients=[user.email],
	  text_body=render_template('email/confirm_email.txt',
	    user=user, token=token),
	  html_body=render_template('email/confirm_email.html',
	    user=user, token=token))

def send_change_password_email(user):
	token = user.get_token()
	send_email('MountainShop  Изменение пароля',
	  sender=app.config['ADMINS'][0],
	  recipients=[user.email],
	  text_body=render_template('email/resetPassword.txt',
	    user=user, token=token),
	  html_body=render_template('email/resetPassword.html',
	    user=user, token=token))

def send_buy_mail(user, items):
	send_email('MountainShop Покупка',
		sender=app.config['ADMINS'][0],
		recipients=[user.email],
		text_body = render_template('email/buy_mail.txt', 
			user=user, items=items),
		html_body=render_template('email/buy_mail.html', 
			user=user, items=items))
