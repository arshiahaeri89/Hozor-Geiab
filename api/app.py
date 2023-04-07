from flask import Flask, request
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
    is_excused = db.Column(db.Boolean, nullable=False, default=False)


class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(10), unique=True)
    invite_date = db.Column(db.DateTime)
    is_finished = db.Column(db.Boolean, nullable=False, default=False)


@app.route('/')
def main():
    students = Student.query.all()
    students_list = [{"id": student.id, "code": student.code, "name": student.name,
                      "family": student.family, "class_code": student.class_code} for student in students]

    absences = Absence.query.all()
    absences_list = [{"id": absence.id, "student_code": absence.student_code,
                      "absence_date": absence.absence_date, "is_excused": absence.is_excused} for absence in absences]

    invites = Invite.query.all()
    invites_list = [{"id": invite.id, "student_code": invite.student_code,
                     "invite_date": invite.invite_date, "is_finished": invite.is_finished} for invite in invites]

    data = {
        "students": students_list,
        "absences": absences_list,
        "invites": invites_list
    }

    return data


@app.route('/getdata', methods=['POST'])
def get_student_data():
    student_code = request.form.get('student_code')
    student = Student.query.filter_by(code=student_code).first()

    absences = Absence.query.filter_by(student_code=student_code).all()
    absences_list = [{"absence_date": absence.absence_date,
                      "is_excused": absence.is_excused} for absence in absences]

    invites = Invite.query.filter_by(student_code=student_code).all()
    invites_list = [{"invite_date": invite.invite_date,
                     "is_finished": invite.is_finished} for invite in invites]

    data = {
        "id": student.id,
        "code": student.code,
        "name": student.name,
        "family": student.family,
        "class_code": student.class_code,
        "absences": absences_list,
        "invites": invites_list
    }

    return data


@app.route('/addstudent', methods=['POST'])
def add_student():
    student_code = request.form.get('student-code')
    student_name = request.form.get('student-name')
    student_family = request.form.get('student-family')
    student_class_code = request.form.get('student-class-code')

    student = Student(code=student_code, name=student_name,
                      family=student_family, class_code=student_class_code)
    db.session.add(student)
    db.session.commit()

    return {"status": 'ok'}


if __name__ == '__main__':
    app.run(debug=True)
