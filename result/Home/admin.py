from django.contrib import admin
from .models import Course, User, Student, Result, Latest_Result

# Register your models here.
admin.site.register(Course)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Result)
admin.site.register(Latest_Result)
