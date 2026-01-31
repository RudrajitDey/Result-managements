from django import forms
from .models import Course, Student, Result

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter course name', 'class': 'input-box'}),
            'duration': forms.TextInput(attrs={'placeholder': 'Enter duration', 'class': 'input-box'}),
            'charges': forms.NumberInput(attrs={'placeholder': 'Enter charges', 'class': 'input-box'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description', 'class': 'input-box'}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'roll_no': forms.TextInput(attrs={'placeholder': 'Enter roll number', 'class': 'input-box'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter student name', 'class': 'input-box'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'input-box'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Enter contact number', 'class': 'input-box'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email', 'class': 'input-box'}),
            'course': forms.Select(attrs={'class': 'input-box'}),
            'gender': forms.Select(attrs={'class': 'input-box'}),
            'admission_date': forms.DateInput(attrs={'type': 'date', 'class': 'input-box'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter state', 'class': 'input-box'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter city', 'class': 'input-box'}),
            'pin_code': forms.TextInput(attrs={'placeholder': 'Enter pin code', 'class': 'input-box'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter address', 'class': 'input-box', 'rows': 3}),
        }


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'course', 'marks_obtained', 'full_marks', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'input-box'}),
            'course': forms.Select(attrs={'class': 'input-box'}),
            'marks_obtained': forms.NumberInput(attrs={'placeholder': 'Enter marks obtained', 'class': 'input-box', 'step': '0.01'}),
            'full_marks': forms.NumberInput(attrs={'placeholder': 'Enter full marks', 'class': 'input-box', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'input-box'}),
        }
