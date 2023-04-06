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
    class_code = db.Column(db.String(3))


class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(10), unique=True)
    absence_date = db.Column(db.DateTime)


class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(10), unique=True)
    invite_date = db.Column(db.DateTime)

# with app.app_context():
#     db.create_all()


@app.route('/')
def main():
    students = Student.query.all()
    students_list = [{"id": student.id, "code": student.code, "name": student.name,
                      "family": student.family, "class_code": student.class_code} for student in students]

    absences = Absence.query.all()
    absences_list = [{"id": absence.id, "student_code": absence.student_code,
                      "absence_date": absence.absence_date} for absence in absences]

    invites = Invite.query.all()
    invites_list = [{"id": invite.id, "student_code": invite.student_code,
                     "invite_date": invite.invite_date} for invite in invites]

    data = {"students": students_list,
            "absences": absences_list, "invites": invites_list}

    return data


if __name__ == '__main__':
    app.run(debug=True)
