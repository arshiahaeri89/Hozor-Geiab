from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import config
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DB_URI

db = SQLAlchemy(app=app)


class Student(db.Model):
    """
        This Model is using for save each student data.
    """
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    name = db.Column(db.Text)
    family = db.Column(db.Text)
    class_code = db.Column(db.String(3))


class Absence(db.Model):
    """
        This Model is using for save abseces for students.
    """
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(10))
    absence_date = db.Column(db.DateTime)
    is_excused = db.Column(db.Boolean, nullable=False, default=False)


class Invite(db.Model):
    """
        This Model is using for save parent invites for students.
    """
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(10))
    invite_date = db.Column(db.DateTime)
    is_finished = db.Column(db.Boolean, nullable=False, default=False)


class Admin(db.Model):
    """
        Admin Users data for authentication
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)


@app.route('/')
def main():
    """
        This Function returns All Data in the database (students, absences, invites)
    """
    try:
        students = Student.query.all()
        students_list = [{"id": student.id, "code": student.code, "name": student.name,
                          "family": student.family, "class_code": student.class_code}
                         for student in students]

        absences = Absence.query.all()
        absences_list = [{"id": absence.id, "student_code": absence.student_code,
                          "absence_date": absence.absence_date, "is_excused": absence.is_excused}
                         for absence in absences]

        invites = Invite.query.all()
        invites_list = [{"id": invite.id, "student_code": invite.student_code,
                         "invite_date": invite.invite_date, "is_finished": invite.is_finished}
                        for invite in invites]

        data = {
            "students": students_list,
            "absences": absences_list,
            "invites": invites_list
        }

    except Exception as err:
        data = {
            "status": "error",
            "exception": str(err)
        }

    return data


@app.route('/getdata', methods=['POST'])
def get_student_data():
    """
        This Function gets National Code of student from POST and returns All Student 
            data, absences, and invites
    """
    try:
        student_code = request.form.get('student-code')
        student = Student.query.filter_by(code=student_code).first()

        absences = Absence.query.filter_by(student_code=student_code).all()
        absences_list = [{"absence_id": absence.id, "absence_date": absence.absence_date,
                          "is_excused": absence.is_excused} for absence in absences]

        invites = Invite.query.filter_by(student_code=student_code).all()
        invites_list = [{"invite_id": invite.id, "invite_date": invite.invite_date,
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

    except Exception as err:
        data = {
            "status": "error",
            "exception": str(err)
        }

    return data


@app.route('/addstudent', methods=['POST'])
def add_student():
    """
        This Function adds a Student and gets the data from POST
    """
    try:
        student_code = request.form.get('student-code')
        student_name = request.form.get('student-name')
        student_family = request.form.get('student-family')
        student_class_code = request.form.get('student-class-code')

        student = Student(code=student_code, name=student_name,
                          family=student_family, class_code=student_class_code)
        db.session.add(student)
        db.session.commit()

        data = {
            "status": 'ok'
        }

    except Exception as err:
        data = {
            "status": "error",
            "exception": str(err)
        }

    return data


@app.route('/addabsence', methods=['POST'])
def add_absence():
    """
        This Function adds an Absence for a student and gets the data from POST
    """
    try:
        student_code = request.form.get('student-code')
        absence_date = request.form.get('absence-date')

        absence_datetime = datetime.datetime.strptime(
            absence_date, config.DATETIME_FORMAT)

        absence = Absence(student_code=student_code,
                          absence_date=absence_datetime)
        db.session.add(absence)
        db.session.commit()

        data = {
            "status": 'ok'
        }

    except Exception as err:
        data = {
            "status": "error",
            "exception": str(err)
        }

    return data


@app.route('/addinvite', methods=['POST'])
def add_invite():
    """
        This Function adds a Invite for a student and gets the data from POST
    """
    try:
        student_code = request.form.get('student-code')
        invite_date = request.form.get('invite-date')

        invite_datetime = datetime.datetime.strptime(
            invite_date, config.DATETIME_FORMAT)

        invite = Invite(student_code=student_code,
                        invite_date=invite_datetime)
        db.session.add(invite)
        db.session.commit()

        data = {
            "status": 'ok'
        }
    except Exception as err:
        data = {
            "status": "error",
            "exception": str(err)
        }

    return data


@app.route('/excuseabsence', methods=['POST'])
def excuse_absence():
    """
        This function gets a Absence id from POST and excuse the absence with that id
    """
    try:
        absence_id = int(request.form.get('absence-id'))
        absence = Absence.query.get(absence_id)
        absence.is_excused = True
        db.session.commit()

        data = {
            "status": 'ok'
        }

    except Exception as err:
        data = {
            "status": "error",
            "exception": str(err)
        }

    return data


@app.route('/finishinvite', methods=['POST'])
def finish_invite():
    """
        This Function gets a invite id and sets the status to finished
    """
    try:
        invite_id = int(request.form.get('invite-id'))
        invite = Invite.query.get(invite_id)
        invite.is_finished = True
        db.session.commit()

        data = {
            "status": 'ok'
        }

    except Exception as err:
        data = {
            "status": "error",
            "exception": str(err)
        }

    return data


@app.route('/login')
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(
            username=username, password=password).first()

        data = {
            "status": "ok",
            "exists": bool(admin)
        }
    except Exception as err:
        data = {
            "status": "error",
            "exception": str(err)
        }

    return data


if __name__ == '__main__':
    app.run(debug=True)
