from src.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.database import User, Course, Enrollment
from src.schemas import courses_schema, chapters_schema
from flasgger import swag_from

students = Blueprint("students", __name__, url_prefix="/api/v1/students")


@students.get('/<int:user_id>/courses')
@jwt_required()
@swag_from('./docs/students/enrolled_courses.yaml')
def enrolled_course(user_id):
    if not User.query.filter_by(id=user_id).first():
        return jsonify({
            'error': "User id is invalid."
        }), HTTP_400_BAD_REQUEST
    user = User.query.get(user_id)
    enrolments = user.enrollments
    courses = []
    for enrolment in enrolments:
        course = Course.query.get(enrolment.course_id)
        courses.append(course)

    courses_opt = courses_schema.dump(courses)
    return jsonify({
        'message': "All enrolled courses",
        "courses": courses_opt,
        "user_id": user_id
    }), HTTP_200_OK


@students.get('/<int:user_id>/courses/<int:course_id>')
@jwt_required()
@swag_from('./docs/students/enrolled_course_chapters.yaml')
def get_course_chapters(user_id, course_id):
    if not User.query.filter_by(id=user_id).first():
        return jsonify({
            'error': "User id is invalid."
        }), HTTP_400_BAD_REQUEST

    if not Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first():
        return jsonify({
            'error': "You are not enrolled in this course."
        }), HTTP_400_BAD_REQUEST

    course = Course.query.get(course_id)

    chapters = course.course_chapters

    chapters_opt = chapters_schema.dump(chapters)
    return jsonify({
        "user_id": user_id,
        "course": course.course_title,
        "chapters": chapters_opt
    }), HTTP_200_OK
