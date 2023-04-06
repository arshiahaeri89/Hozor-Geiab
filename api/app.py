from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DB_URI

db = SQLAlchemy(app=app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    name = db.Column(db.Text)
    family = db.Column(db.Text)
    

class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(10), unique=True)
    absence_date = db.Column(db.DateTime)

class Invite:
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(10), unique=True)
    invite_date = db.Column(db.DateTime)

@app.route('/')
def home():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)