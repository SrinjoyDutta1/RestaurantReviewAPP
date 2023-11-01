from flaskext.mysql import MySQL
from flask import Flask
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Neel1123!'
app.config['MYSQL_DATABASE_DB'] = 'project1CS348'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)