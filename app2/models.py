from django.db import models
# Create your models here.

class Class(models.Model):
    classname=models.CharField(max_length=100)
    sections=models.JSONField(default=list)
    

choices=[
    ('practical','Practical'),
    ('theory','Theory')
]
class Subject(models.Model):
    subjectcode=models.CharField(max_length=100)
    subjectname=models.CharField(max_length=100)
    type=models.CharField(max_length=50,choices=choices,default='theory')

#Name	Email	Phone	Qualification	Experience
class Instructor(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone_no=models.CharField(max_length=25)
    qualification=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)


class AssignSubject(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.CharField(max_length=50) 
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Instructor, on_delete=models.CASCADE)

class AssignClassTeacher(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.CharField(max_length=50)  # pick value from Class.sections JSON list
    teacher = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('class_name', 'section')


class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    APPROVED_CHOICES=[
        ('pending','Pending'),
        ('approved','Approved')
    ]

    student_name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    dob = models.DateField()  # dd-mm-yyyy format can be handled in frontend form
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE) 
    section = models.CharField(max_length=50)
    address = models.TextField()
    password = models.CharField(max_length=255)  # store hashed password, not plain text
    approved=models.CharField(max_length=10, choices=APPROVED_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


