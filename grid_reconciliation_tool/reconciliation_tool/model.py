from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float
import config  
 
# DB class 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URI
db = SQLAlchemy(app)
 
# # DB classess 
# class Player(db.Model):
#     __tablename__ = 'player'
 
#     playerid = db.Column('playerid', Integer, primary_key=True)
#     username = db.Column('username', String(30), unique=True)
#     email = db.Column('email', String(50), unique=True)
#     password = db.Column('password', String(100), unique=Fal4se)
#     avatarid = db.Column('avatarid', Integer,default=1)
#     language = db.Column('language', Integer,default=1)
#     regdate = db.Column('regdate', Date)
#     activation_key = db.Column('activation_key', String(60))
#     active = db.Column('active', Integer, default=0)
 
#     def __init__(self, username=None, email=None,password=None):
#         self.username = username
#         self.email = email
#         self.password = password 
 
#     def __repr__(self):
#         return '<Player %s %s>' % (self.username, self.email)