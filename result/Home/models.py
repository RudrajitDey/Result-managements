from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

class Latest_Result(models.Model):
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='results_pdfs/')

    def __str__(self):
        return self.title

class Course(models.Model):
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    charges = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    roll_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    contact = models.CharField(max_length=20)
    email = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    admission_date = models.DateField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return f"{self.roll_no} - {self.name}"


class Result(models.Model):
    STATUS_CHOICES = [
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    full_marks = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Fail')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate percentage automatically
        if self.full_marks > 0:
            self.percentage = (self.marks_obtained / self.full_marks) * 100
        super().save(*args, **kwargs)
        self.percentage = (self.marks_obtained / self.full_marks) * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.roll_no} - {self.course.name}"

