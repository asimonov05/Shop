import datetime
from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer,
                         primary_key=True, autoincrement=True)
  surname = db.Column(db.String, nullable=False)
  name = db.Column(db.String, nullable=False)
  adress = db.Column(db.String, nullable=False)
  email = db.Column(db.String,index=True, unique=False, nullable=False)
  confirm_email = db.Column(db.Boolean, default=False)
  password_hash = db.Column(db.String, nullable=False)
  created_date = db.Column(db.DateTime,
                                   default=datetime.datetime.now)
  cart = db.Column(db.String, default=None, nullable=True)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def get_token(self, expires_in=600):
    return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
      app.config['SECRET_KEY'], algorithm='HS256')

  @staticmethod
  def verify_token(token):
    try:
      id = jwt.decode(token, app.config['SECRET_KEY'],
        algorithms=['HS256'])['reset_password']
    except:
      return
    return User.query.get(id)



class Items(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer,
                           primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    img1 = db.Column(db.String, nullable=False)
    img2 = db.Column(db.String, nullable=False)
    img3 = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime,
                                     default=datetime.datetime.now)
    amount = db.Column(db.Integer, default=0)
    coast = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)

db.create_all()
db.session.commit()