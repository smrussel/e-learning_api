from flask_marshmallow import Marshmallow

ma = Marshmallow()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class CourseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'course_title', 'course_brief')


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


class ChapterSchema(ma.Schema):
    class Meta:
        fields = ('id', 'chapter_title', 'chapter_description','video_url')


chapter_schema = ChapterSchema()
chapters_schema = ChapterSchema(many=True)
