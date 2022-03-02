from src.constants.http_status_codes import HTTP_200_OK
from flask import Blueprint, jsonify
from src.database import Course
from src.schemas import courses_schema
from flasgger import swag_from

course = Blueprint("courses", __name__, url_prefix="/api/v1/courses")


@course.get('/')
@swag_from('./docs/courses/courses.yaml')
def get_all_courses():
    all_courses = Course.query.all()
    results = courses_schema.dump(all_courses)
    return jsonify({
        'courses':  results
    }), HTTP_200_OK
