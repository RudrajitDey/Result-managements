from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.contrib import auth
from django.conf import settings
from .models import Course, Student, Result, Latest_Result
from .forms import CourseForm, StudentForm, ResultForm


User = get_user_model()
# Create your views here.


def homepage(request):    
    return render(request, 'homepage.html')

def dashboard(request):
    context = {
        "total_students": Student.objects.count(),
        "total_courses": Course.objects.count(),
        "total_results": Result.objects.count(),
        "latest_result": Latest_Result.objects.order_by('-id').first(),
        "results": Latest_Result.objects.all(),
    }
    return render(request, 'dashboard.html', context)

def user_dashboard(request):
    context = {
        "total_students": Student.objects.count(),
        "total_courses": Course.objects.count(),
        "total_results": Result.objects.count(),
        "latest_result": Latest_Result.objects.order_by('-id').first(),
        "results": Latest_Result.objects.all(),
    }
    return render(request, 'user_dashboard.html', context)


def download_result(request, id):
    result = get_object_or_404(Latest_Result, id=id)
    response = FileResponse(result.pdf.open('rb'), as_attachment=True, filename=result.pdf.name)
    return response


    
def course(request):
    # Delegate to the full manage_course view so the template
    # receives the `form` and `courses` context it expects.
    return manage_course(request)


# course management view

def manage_course(request):
    courses = Course.objects.all()
    form = CourseForm()
    selected_id = None

    # If the user clicked an Edit link, prepare the form for that instance
    if request.method == 'GET' and request.GET.get('edit'):
        cid = request.GET.get('edit')
        course = get_object_or_404(Course, id=cid)
        form = CourseForm(instance=course)
        selected_id = course.id

    # --- Save / Update ---
    if request.method == "POST":
        if 'save' in request.POST:
            form = CourseForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_course')

        if 'update' in request.POST:
            cid = request.POST.get('course_id')
            course = get_object_or_404(Course, id=cid)
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
                return redirect('manage_course')

        if 'delete' in request.POST:
            cid = request.POST.get('course_id')
            Course.objects.filter(id=cid).delete()
            return redirect('manage_course')

        if 'clear' in request.POST:
            return redirect('manage_course')

    # --- Search ---
    query = request.GET.get("search")
    if query:
        courses = Course.objects.filter(name__icontains=query)

    context = {
        "courses": courses,
        "form": form,
        "selected_id": selected_id
    }
    return render(request, "course.html", context)

def student(request):
    # Delegate to the full manage_student view
    return manage_student(request)


# student management view

def manage_student(request):
    students = Student.objects.all()
    form = StudentForm()
    selected_id = None

    # If the user clicked an Edit link, prepare the form for that instance
    if request.method == 'GET' and request.GET.get('edit'):
        sid = request.GET.get('edit')
        student = get_object_or_404(Student, id=sid)
        form = StudentForm(instance=student)
        selected_id = student.id

    # --- Save / Update ---
    if request.method == "POST":
        if 'save' in request.POST:
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_student')

        if 'update' in request.POST:
            sid = request.POST.get('student_id')
            student = get_object_or_404(Student, id=sid)
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                return redirect('manage_student')

        if 'delete' in request.POST:
            sid = request.POST.get('student_id')
            Student.objects.filter(id=sid).delete()
            return redirect('manage_student')

        if 'clear' in request.POST:
            return redirect('manage_student')

    # --- Search ---
    query = request.GET.get("search")
    if query:
        students = Student.objects.filter(roll_no__icontains=query) | Student.objects.filter(name__icontains=query)

    context = {
        "students": students,
        "form": form,
        "selected_id": selected_id
    }
    return render(request, "student.html", context)


def manage_result(request):
    results = Result.objects.all().select_related('student', 'course')
    form = ResultForm()
    selected_id = None
    student_name = ""
    course_name = ""

    # If the user clicked an Edit link, prepare the form for that instance
    if request.method == 'GET' and request.GET.get('edit'):
        rid = request.GET.get('edit')
        result = get_object_or_404(Result, id=rid)
        form = ResultForm(instance=result)
        selected_id = result.id
        student_name = result.student.name
        course_name = result.course.name

    # --- Save / Update ---
    if request.method == "POST":
        if 'save' in request.POST:
            form = ResultForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_result')

        if 'update' in request.POST:
            rid = request.POST.get('result_id')
            result = get_object_or_404(Result, id=rid)
            form = ResultForm(request.POST, instance=result)
            if form.is_valid():
                form.save()
                return redirect('manage_result')

        if 'delete' in request.POST:
            rid = request.POST.get('result_id')
            Result.objects.filter(id=rid).delete()
            return redirect('manage_result')

        if 'clear' in request.POST:
            return redirect('manage_result')

    # --- Search ---
    query = request.GET.get("search")
    if query:
        results = Result.objects.filter(
            student__roll_no__icontains=query
        ) | Result.objects.filter(
            student__name__icontains=query
        ) | Result.objects.filter(
            course__name__icontains=query
        )

    context = {
        "results": results,
        "form": form,
        "selected_id": selected_id,
        "student_name": student_name,
        "course_name": course_name
    }
    return render(request, "add_result.html", context)

def view_result(request):
    results = []

    # --- Search by Roll No ---
    query = request.GET.get("search")
    if query:
        results = Result.objects.filter(
            student__roll_no__icontains=query
        ).select_related('student', 'course')

    context = {
        "results": results,
    }
    return render(request, "view_result.html", context)

# **************User Register*****************


def user_register(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')
        secretkey = request.POST.get('secretkey')
        
#****************EMPTY FIELD CHECK*****************
        if not all([fullname, email, password, password2, role, secretkey]):
            messages.info(request, 'All fields are required')
            return redirect('register')
#****************PASSWORD CHECK*******************
        if password != password2:
            messages.info(request, 'Password do not match')
            return redirect('register')
#***************Email Check********************
        if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exist')
                return redirect('register')
        
#**************Secret Key Validation*****************

#*************************For user
        if role == 'user' and secretkey != settings.USER_SECRET_KEY:
            messages.info(request, 'Invalid User Secret Key')
            return redirect('register')
#*************************For Admin        
        if role == 'admin' and secretkey != settings.ADMIN_SECRET_KEY:
            messages.info(request, 'Invalid Admin Secret Key')
            return redirect('register')
        
#***********************CREATE USER**************

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role=role,
            first_name=fullname
        )
        user.save()

        messages.success(request, 'Account Created Successfully')
        return redirect('login')
        
    else:
        return render(request, 'register.html')

#**************User Login*****************

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        email = (email or '').strip().lower()
        user = auth.authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if getattr(user, 'role', None) == 'admin':
                return redirect('dashboard')
            if getattr(user, 'role', None) == 'user':
                return redirect('user_dashboard')
            return redirect('dashboard')

        messages.info(request, 'Invalid Credentials')
        return redirect('login')

    return render(request, 'login.html') 


def user_logout(request):
    django_logout(request)
    return redirect('login')



