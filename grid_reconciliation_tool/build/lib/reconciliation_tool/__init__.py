from flask import Flask
# from flaskext.mysql import MySQL

import os

# Initialize the Flask application
# mysql = MySQL()
app = Flask(__name__)
# config 
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
# app.config['MYSQL_DATABASE_DB'] = 'EmpData'
# app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv'])

app.secret_key = '\xe4\xfa\x1cN\xbdE\xb5\xc7\xb9\xbb"\xdc\'\xe6\xceO9\x15(\xea\xa9\xf2a\\'

# mysql.init_app(app)

import reconciliation_tool.routes