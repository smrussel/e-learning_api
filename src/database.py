from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    enrollments = db.relationship('Enrollment', backref="user")

    def __repr__(self) -> str:
        return '<User %r>' % self.name


class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    enrollment_date = db.Column(db.DateTime, default=datetime.now())


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(80), nullable=False)
    course_brief = db.Column(db.Text, nullable=False)
    enrollments = db.relationship('Enrollment', backref="course")
    course_chapters = db.relationship('CourseChapter', backref="course")
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Course %r>' % self.course_title


class CourseChapter(db.Model):
    __tablename__ = 'course_chapter'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    chapter_title = db.Column(db.String(80), nullable=False)
    chapter_description = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return '<course_chapter %r>' % self.chapter_title




