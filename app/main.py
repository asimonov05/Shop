from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from app.forms import LoginForm, RegistrationForm, EmailForm, ChangePasswordForm, SearchForm
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Items
from flask_login import current_user, login_user
from app.email import send_confirm_email, send_change_password_email, send_buy_mail
from werkzeug.urls import url_parse
import json

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        if not user.confirm_email:
            return redirect(url_for('inform_email', name=user.name, email=user.email))
        login_user(user, remember=form.remember_me.data)
        flash('Вы вошли в аккаунт успешно!')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/category/<name>')
def category(name):
    items = Items.query.filter_by(category=name).all()
    return render_template('category.html', name_of_cat=name, items=items)

@app.route('/favicon.ico')
def favicon():
    return render_template('favicon.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u is None:
            u = User()
            u.name = form.name.data
            u.surname = form.surname.data
            u.adress = form.adress.data
            u.email = form.email.data
            u.set_password(form.password.data)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('inform_email', name=form.name.data, email=form.email.data))
        return redirect(url_for('index'))
    return render_template('registration.html', form=form)


@app.route('/cart')
@login_required
def cart():
    u = User.query.filter_by(id=current_user.id).first()
    items = []
    if u.cart is None or u.cart == '':
        return render_template('cart.html', items=items)
    id_items = u.cart.split(' ')
    for i in id_items:
        item = Items.query.filter_by(id=int(i)).first()
        if item:
            items.append(item)
    return render_template('cart.html', items=items)

@app.route('/inform_email/<name>/<email>')
def inform_email(name, email):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(email=email).first()
    if user:
        send_confirm_email(user)
    return name + ' ' + email

@app.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    user = User.verify_token(token)

    if not user:
        return redirect(url_for('index'))

    flash('Ваш аккаунт успешно подтвержден!')
    user.confirm_email=True
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/product/<id>')
def product(id):
    product = Items.query.filter_by(id=id).first()
    print(product.amount)
    return render_template('product.html', item=product)

@app.route('/user/<id>')
def user_profile(id):
    u = User.query.filter_by(id=id).first()
    return render_template('userProfile.html', user=u)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Такого аккаунта не существует!')
        else:
            send_change_password_email(user)
            flash('Вам на почту отправленны дальнейшие инструкции')
    return render_template('resetPassword.html', form=form)

@app.route('/change_password/<token>', methods=['GET', 'POST'])
def change_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль успешно изменен!')
        return redirect(url_for('login'))
    return render_template('ChangePassword.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    items = [Items()]
    items[0].name = 'search'
    if form.validate_on_submit():
        print(form.search.data)
        items = Items.query.filter((form.search.data == Items.name) | (form.search.data == Items.description)).all()
        if not items:
            items = None
    return render_template('search.html', form=form, items=items)

@app.route('/add_to_cart/<id>')
@login_required
def add_to_cart(id):
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        return redirect(url_for('product', id=id))
    if user.cart is None or user.cart == '':
        user.cart = str(id)
        db.session.commit()
        flash('Товар добавлен в карзину')
        return redirect(url_for('product', id=id))
    i = Items.query.filter_by(id=id).first()
    if i.amount == 0:
        flash('Товара нет в наличии')
        return redirect(url_for('product', id=id))
    b = True
    for item_id in user.cart.split(' '):
        if item_id == str(id):
            b = False
            break
    if b:
        user.cart = user.cart + ' ' + str(id)
        i.amount -= 1
        db.session.commit()
        flash('Товар добавлен в карзину')
    else:
        flash('Такой товар уже есть в карзине')
    return redirect(url_for('product', id=id))

@app.route('/cart_aj', methods=['POST'])
def cart_aj():
    data = json.loads(request.get_json())
    u = User.query.filter_by(id=current_user.id).first()
    if data['action'] == 'buy' and u:
        cart_i = u.cart.split(' ')
        buy_list=[]
        for i in range(len(cart_i)):
            for j in data['id']:
                if cart_i[i] == j:
                    cart_i[i] = ''
                    x = Items.query.filter_by(id=j).first()
                    if x:
                        buy_list.append(x)
        if cart_i == '':
            u.cart = None
        else:
            u.cart = ' '.join(cart_i)
        db.session.commit()
        flash('Покупка успешно совершена, подробности отправленны на почту.')
        send_buy_mail(u, buy_list)
    elif data['action'] == 'clear' and u:
        cart_i = u.cart.split(' ')
        for i in range(len(cart_i)):
            for j in data['id']:
                if cart_i[i] == j:
                    cart_i[i] = ''
        if cart_i == '':
            u.cart = None
        else:
            u.cart = ' '.join(cart_i)

        db.session.commit()

    return make_response("", 200)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

