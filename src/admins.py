from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_409_CONFLICT,HTTP_400_BAD_REQUEST
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.database import User, db, Course, CourseChapter, Enrollment
from src.schemas import users_schema, course_schema, user_schema
from src.admin_decorator import admin_required
from flasgger import swag_from

admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


@admin.post('/courses')
@jwt_required()
@admin_required
@swag_from('./docs/admin/create-course.yaml')
def create_course():
    course_title = request.json.get('course_title', '')
    course_brief = request.json.get('course_brief', '')
    course = Course(course_title=course_title, course_brief=course_brief)
    db.session.add(course)
    db.session.commit()

    return course_schema.jsonify(course), HTTP_201_CREATED


@admin.post('/courses/<int:course_id>/chapters')
@jwt_required()
@admin_required
@swag_from('./docs/admin/create-chapter.yaml')
def create_course_chapter(course_id):
    chapter_title = request.json.get('title', '')
    chapter_description = request.json.get('description', '')
    video_url = request.json.get('video_url', '')
    if not Course.query.filter_by(id=course_id).first():
        return jsonify({
            'error': "Course id is invalid."
        }), HTTP_400_BAD_REQUEST
    course = Course.query.get(course_id)
    chapter = CourseChapter(course_id=course_id,
                            chapter_title=chapter_title,
                            chapter_description=chapter_description,
                            video_url=video_url)
    db.session.add(chapter)
    db.session.commit()
    course_opt = course_schema.dump(course)
    return jsonify({
        'message': "Chapter created",
        'chapter': {
            "course": course_opt,
            'chapter_title': chapter_title,
            "course_description": chapter_description
        }

    }), HTTP_201_CREATED


@admin.get('/students')
@jwt_required()
@admin_required
@swag_from('./docs/admin/students.yaml')
def get_all_students():
    students = User.query.filter_by(is_admin=False)
    results = users_schema.dump(students)
    return jsonify({
            'students': results
    }), HTTP_200_OK


@admin.post('/assign')
@jwt_required()
@admin_required
@swag_from('./docs/admin/assign.yaml')
def assign_course():
    user_id = request.json.get('user_id', '')
    course_id = request.json.get('course_id', '')
    if Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first():
        return jsonify({
            'error': "Course already assigned to this student"
        }), HTTP_409_CONFLICT
    if not User.query.filter_by(id=user_id).first():
        return jsonify({
            'error': "User id is invalid."
        }), HTTP_400_BAD_REQUEST
    if not Course.query.filter_by(id=course_id).first():
        return jsonify({
            'error': "Course id is invalid."
        }), HTTP_400_BAD_REQUEST

    course = Course.query.get(course_id)
    user = User.query.get(user_id)
    assign = Enrollment(user_id=user_id, course_id=course_id)
    db.session.add(assign)
    db.session.commit()

    user_opt = user_schema.dump(user)
    course_opt = course_schema.dump(course)
    return jsonify({
        'message': "Course Assigned successfully",
        "course": course_opt,
        "user": user_opt
    }), HTTP_201_CREATED


