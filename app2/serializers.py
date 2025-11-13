from rest_framework import serializers
from .models import AssignClassTeacher, AssignSubject, Class,Subject,Instructor
from django.contrib.auth.hashers import make_password
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"



class InstructorSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    subjects_ids = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        write_only=True,
        many=True,
        required=False
    )

    class Meta:
        model = Instructor
        fields = [
            'id',
            'name',
            'email',
            'phone_no',
            'qualification',
            'experience',
            'subjects',      # Response
            'subjects_ids'   # Input only
        ]

    def create(self, validated_data):
        subjects = validated_data.pop("subjects_ids", [])
        instructor = Instructor.objects.create(**validated_data)
        instructor.subjects.set(subjects)
        return instructor



from rest_framework import serializers
from .models import AssignSubject

class AssignSubjectSerializer(serializers.ModelSerializer):

    class_data = serializers.SerializerMethodField()
    subject_data = serializers.SerializerMethodField()
    teacher_data = serializers.SerializerMethodField()

    class Meta:
        model = AssignSubject
        fields = [
            "id",
            "class_name",   # FK input
            "section",
            "subject",      # FK input
            "teacher",      # FK input
            "class_data",
            "subject_data",
            "teacher_data"
        ]

    def get_class_data(self, obj):
        return {
            "id": obj.class_name.id,
            "name": obj.class_name.classname,
            "section": obj.section
        }

    def get_subject_data(self, obj):
        return {
            "id": obj.subject.id,
            "name": obj.subject.subjectname,
            "code": obj.subject.subjectcode
        }

    def get_teacher_data(self, obj):
        return {
            "id": obj.teacher.id,
            "name": obj.teacher.name  # fixed from 'fullname' to 'name'
        }


# from rest_framework import serializers
# from .models import AssignClassTeacher

# class AssignClassTeacherSerializer(serializers.ModelSerializer):
#     class_data = serializers.SerializerMethodField()
#     teacher_data = serializers.SerializerMethodField()

#     class Meta:
#         model = AssignClassTeacher
#         fields = ['id', 'class_name', 'section', 'teacher', 'class_data', 'teacher_data']  # corrected 'class_name'

#     def get_class_data(self, obj):
#         return {
#             "id": obj.class_name.id,
#             "name": obj.class_name.classname  # your model field is 'classname'
#         }

#     def get_teacher_data(self, obj):
#         return {
#             "id": obj.teacher.id,
#             "name": obj.teacher.name
#         }

from rest_framework import serializers
from .models import AssignClassTeacher

class AssignClassTeacherSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(source='class_name.id', read_only=True)
    class_name = serializers.CharField(source='class_name.classname', read_only=True)
    teacher_id = serializers.IntegerField(source='teacher.id', read_only=True)
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)

    class Meta:
        model = AssignClassTeacher
        fields = ['class_id', 'class_name', 'section', 'teacher_id', 'teacher_name', 'id']




from rest_framework import serializers
from .models import Student, Class
from django.contrib.auth.hashers import make_password

class StudentSerializer(serializers.ModelSerializer):
    student_class_name = serializers.SerializerMethodField()  # <-- add this field

    class Meta:
        model = Student
        fields = [
            "id",
            "student_name",
            "father_name",
            "dob",
            "gender",
            "phone",
            "email",
            "student_class",       # FK input
            "student_class_name",  # name in response
            "section",
            "address",
            "password",
            "approved",
            "created_at",
        ]
        read_only_fields = ['approved', 'created_at']
    def validate(self, attrs):
        """✅ Ensure that the selected section exists in the chosen class."""
        class_obj = attrs.get("student_class")
        section = attrs.get("section")

        if class_obj and section:
            if section not in class_obj.sections:
                raise serializers.ValidationError({"section": "Invalid section for this class."})

        return attrs
    def create(self, validated_data):
        # Hash the password
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        # Set approved to pending
        validated_data['approved'] = 'pending'
        return super().create(validated_data)

    def get_student_class_name(self, obj):
        return obj.student_class.classname  # return the class name instead of just id
