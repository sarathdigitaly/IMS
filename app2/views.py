from django.shortcuts import render
from .serializers import SubjectSerializer,InstructorSerializer,ClassSerializer,AssignSubjectSerializer,AssignClassTeacherSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Class,Subject,Instructor,AssignSubject,AssignClassTeacher
from rest_framework.permissions import AllowAny

class ClassView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Class created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassDetailView(APIView):
    def get(self, request, pk):
        try:
            class_obj = Class.objects.get(id=pk)
        except Class.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClassSerializer(class_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)



class SubjectView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Subject created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class SubjectDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            subject = Subject.objects.get(id=pk)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubjectSerializer(subject)
        return Response(serializer.data)



class InstructorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InstructorSerializer(data=request.data)
        if serializer.is_valid():
            instructor = serializer.save()  # Serializer handles subjects_ids

            return Response({
                "status": True,
                "message": "Instructor created successfully",
                "data": InstructorSerializer(instructor).data
            }, status=status.HTTP_201_CREATED)

        return Response({"status": False, "errors": serializer.errors}, status=400)

    def get(self, request):
        instructors = Instructor.objects.all()
        serializer = InstructorSerializer(instructors, many=True)
        return Response({
            "status": True,
            "count": len(serializer.data),
            "data": serializer.data
        }, status=200)


class InstructorDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            instructor = Instructor.objects.get(id=pk)
        except Instructor.DoesNotExist:
            return Response({"status": False, "error": "Instructor not found"}, status=404)

        serializer = InstructorSerializer(instructor)
        return Response({"status": True, "data": serializer.data}, status=200)




class AssignSubjectView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AssignSubjectSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response({
                "message": "Subject assigned successfully",
                "data": AssignSubjectSerializer(obj).data   # ✅ return enriched data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request):
        assignments = AssignSubject.objects.all()
        serializer = AssignSubjectSerializer(assignments, many=True)

        # Convert outer list into dict keyed by ID or something meaningful
        data = {str(item['id']): item for item in serializer.data}

        return Response({
            "status": True,
            "count": len(serializer.data),
            "data": data
        }, status=200)


class AssignSubjectDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            assignment = AssignSubject.objects.get(id=pk)
        except AssignSubject.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AssignSubjectSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import AssignClassTeacher, Class, Instructor
from .serializers import AssignClassTeacherSerializer

class AssignClassTeacherView(APIView):
    permission_classes = [AllowAny]

    # GET all assignments
    def get(self, request):
        assignments = AssignClassTeacher.objects.all()
        serializer = AssignClassTeacherSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # CREATE or UPDATE assignment
    def post(self, request):
        class_id = request.data.get("class_name")
        section = request.data.get("section")
        teacher_id = request.data.get("teacher")

        if not all([class_id, section, teacher_id]):
            return Response({"error": "class_name, section, and teacher are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if assignment already exists
        if AssignClassTeacher.objects.filter(class_name_id=class_id, section=section).exists():
            return Response({"error": "This assignment already exists"}, status=status.HTTP_400_BAD_REQUEST)

        assignment = AssignClassTeacher.objects.create(
            class_name_id=class_id,
            section=section,
            teacher_id=teacher_id
        )

        return Response({
            "message": "Assignment created successfully",
            "data": {
                "class_id": assignment.class_name.id,
                "class_name": assignment.class_name.classname,
                "section": assignment.section,
                "teacher_id": assignment.teacher.id,
                "teacher_name": assignment.teacher.name
            }
        }, status=status.HTTP_201_CREATED)


class AssignClassTeacherDetailView(APIView):
    permission_classes = [AllowAny]

    # GET assignment by ID
    def get(self, request, pk):
        try:
            assignment = AssignClassTeacher.objects.get(pk=pk)
        except AssignClassTeacher.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "class_id": assignment.class_name.id,
            "class_name": assignment.class_name.classname,
            "section": assignment.section,
            "teacher_id": assignment.teacher.id,
            "teacher_name": assignment.teacher.name
        }, status=status.HTTP_200_OK)



from .models import Student
from .serializers import StudentSerializer

# 1. Register student & Get all students
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer

class StudentListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response({
            "message": "Students retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def post(self, request):
        try:
            if email := request.data.get('email'):
                if Student.objects.filter(email=email).exists():
                    return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if password := request.data.get('password'):
            if len(password) < 6:
                return Response({"error": "Password must be at least 6 characters long"}, status=status.HTTP_400_BAD_REQUEST)     
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # approved will automatically be 'pending'
            return Response({
                "message": "Student registered successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. Get student by ID
class StudentDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 3. Approve student (change 'pending' to 'approved')
class StudentApproveView(APIView):
    permission_classes = [AllowAny]
    def patch(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        if student.approved == 'approved':
            return Response({"message": "Student already approved"}, status=status.HTTP_200_OK)

        student.approved = 'approved'
        student.save()
        serializer = StudentSerializer(student)
        return Response({
            "message": "Student approved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
