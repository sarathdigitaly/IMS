from django.urls import path
from .views import AssignClassTeacherDetailView, AssignClassTeacherView, ClassView,ClassDetailView, StudentApproveView, StudentDetailView, StudentListView,SubjectDetailView,SubjectView,InstructorView,InstructorDetailView,AssignSubjectView,AssignSubjectDetailView

urlpatterns = [
    path("class/", ClassView.as_view(), name="class-create"),
    path("class/<int:pk>/", ClassDetailView.as_view(), name="class-detail"),
    path("subject/", SubjectView.as_view(), name="subject-create"),
    path("subject/<int:pk>/", SubjectDetailView.as_view(), name="subject-detail"),
    path("instructor/", InstructorView.as_view(), name="subject-create"),
    path("instructor/<int:pk>/", InstructorDetailView.as_view(), name="subject-detail"),
    path("assignsubject/", AssignSubjectView.as_view(), name="subject-create"),
    path("assignsubject/<int:pk>/", AssignSubjectDetailView.as_view(), name="subject-detail"),
    path("assignclassteacher/", AssignClassTeacherView.as_view(), name="subject-create"),
    path("assignclassteacher/<int:pk>/", AssignClassTeacherDetailView.as_view(), name="subject-detail"),
    path('students/', StudentListView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('students/<int:pk>/approve/', StudentApproveView.as_view(), name='student-approve'),


]
