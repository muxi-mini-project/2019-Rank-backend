from run import db
import functools
from flask import session
import logging
from sqlalchemy import exc


def db_error_handling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except exc.SQLAlchemyError as e:
            logging.exception("%s", e)
            db.session.rollback()
            return 'DB ERROR', 500
        except exc.OperationalError as e:
            logging.exception("%s", e)
            db.session.rollback()
            return 'DB ERROR', 500
        else:
            return res

    return wrapper


@db_error_handling
def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        student = Student.query.filter_by(id=session.get('id')).first()
        if isinstance(student, Student):
            return func(*args, **kwargs)
        else:
            return 'Unauthorized', 401

    return wrapper


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.INT, primary_key=True)
    department_name = db.Column(db.VARCHAR(50))

    @staticmethod
    def members_of_dept(dept_id):
        if type(dept_id) == bytes:
            dept_id = dept_id.decode()
        members = 0
        for student in Student.query.all():
            if str(student.department_id) == str(dept_id):
                members += 1
        if members == 0:
            return 1
        else:
            return members


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.INT, primary_key=True)
    stdnum = db.Column(db.VARCHAR(16), unique=True)
    openid = db.Column(db.VARCHAR(64))
    session_key = db.Column(db.VARCHAR(64))
    department_id = db.Column(db.INT)
    username = db.Column(db.VARCHAR(50), unique=True)
    qq = db.Column(db.VARCHAR(18), unique=True)
    show_stdnum = db.Column(db.Boolean, default=0)
    show_qq = db.Column(db.Boolean, default=0)
    booknum = db.Column(db.INT, default=0)
    avatar = db.Column(db.Text)

    @staticmethod
    def get_current():
        """
        Add @login_required before you use it
        :return: Student object from session
        """
        return Student.query.get(session.get('id'))

    def is_liked(self, star_id):
        return bool(Likes.query.filter_by(star_id=star_id, visitor_id=self.id).first())

    def likes(self):
        return Likes.query.filter_by(star_id=self.id).count()


class Suggestion(db.Model):
    __tablename__ = 'suggestions'
    id = db.Column(db.INT, primary_key=True)
    user_id = db.Column(db.INT)
    time = db.Column(db.Date)
    contact = db.Column(db.VARCHAR(30))
    content = db.Column(db.Text)


class WeRun(db.Model):
    __tablename__ = 'werun'
    id = db.Column(db.INT, primary_key=True)
    user_id = db.Column(db.INT)
    time = db.Column(db.Date)
    step = db.Column(db.INT)


class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.INT, primary_key=True)
    visitor_id = db.Column(db.INT)
    star_id = db.Column(db.INT)
