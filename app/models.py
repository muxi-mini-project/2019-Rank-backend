from run import db
import functools
from flask import session


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        student = None
        try:
            # maliciously edit session?
            student = Student.query.get(session.get('id'))
        finally:
            if isinstance(student, Student):
                return func(*args, **kwargs)
            else:
                return 'Unauthorized', 401

    return wrapper


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.INT, primary_key=True)
    department_name = db.Column(db.VARCHAR(50))
    member = db.Column(db.INT)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.INT, primary_key=True)
    stdnum = db.Column(db.VARCHAR(16), unique=True)
    openid = db.Column(db.VARCHAR(64))
    department_id = db.Column(db.INT)
    username = db.Column(db.VARCHAR(50), unique=True)
    qq = db.Column(db.VARCHAR(18), unique=True)
    show_stdnum = db.Column(db.Boolean, default=0)
    show_qq = db.Column(db.Boolean, default=0)
    booknum = db.Column(db.INT, default=0)
    likes = db.Column(db.INT, default=0)

    @staticmethod
    def get_current():
        """
        Add @login_required before you use it
        :return: Student object from session
        """
        return Student.query.get(session.get('id'))


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


class Likes_lib(db.Model):
    __tablename__ = 'likes_lib'
    id = db.Column(db.INT, primary_key=True)
    visitor_id = db.Column(db.INT)
    star_id = db.Column(db.INT)


class Likes_step_person(db.Model):
    __tablename__ = 'likes_step_person'
    id = db.Column(db.INT, primary_key=True)
    visitor_id = db.Column(db.INT)
    star_id = db.Column(db.INT)


class Likes_dep_daily(db.Model):
    __tablename__ = 'likes_dep_daily'
    id = db.Column(db.INT, primary_key=True)
    visitor_id = db.Column(db.INT)
    star_id = db.Column(db.INT)


class Likes_dep_weekly(db.Model):
    __tablename__ = 'likes_dep_weekly'
    id = db.Column(db.INT, primary_key=True)
    visitor_id = db.Column(db.INT)
    star_id = db.Column(db.INT)


class Likes_dep_monthly(db.Model):
    __tablename__ = 'likes_dep_monthly'
    id = db.Column(db.INT, primary_key=True)
    visitor_id = db.Column(db.INT)
    star_id = db.Column(db.INT)
