from django.shortcuts import render, get_object_or_404, redirect
from .models import MasterStudent
from marks.models import tbl_Studentmarks
from student_documents.models import StudentDocument
from django.contrib import messages
from .forms import ChangePasswordForm
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail #send mail
import random
from django.http import FileResponse, HttpResponseForbidden, Http404
import os
from django.conf import settings


def student_profile_login(request):
    if request.method == 'POST':
        gr_no = request.POST.get('gr_no')
        password = request.POST.get('password')

        # ✅ Admin shortcut
        if gr_no == 'admin' and password == 'admin':
            allrecords = MasterStudent.objects.all().order_by('-gr_no')
            return render(request, 'masterstudent/allrecord.html', {'allrecords': allrecords})

        try:
            student = MasterStudent.objects.get(gr_no=gr_no)
            # student = MasterStudent.objects.all()

            # ✅ Check hashed password
            if check_password(password, student.password):
                marks = tbl_Studentmarks.objects.filter(gr_no=gr_no)
                documents = StudentDocument.objects.filter(student=student)
                return render(request, 'masterstudent/profile.html', {
                    'student': student,
                    'marks': marks,
                    'documents': documents,
                })
            else:
                print("Entered password:", password)
                print("Stored hash:", student.password)
                print("Match result:", check_password(password, student.password))
                return render(request, 'masterstudent/login.html', {'error': 'Invalid password.'})

        except MasterStudent.DoesNotExist:
            return render(request, 'masterstudent/login.html', {'error': 'Student not found.'})

    return render(request, 'masterstudent/login.html')


def student_profile_view(request, gr_no):
    student = get_object_or_404(MasterStudent, gr_no=gr_no)
    marks = tbl_Studentmarks.objects.filter(gr_no=gr_no)
    documents = StudentDocument.objects.filter(student=student)

    return render(request, 'masterstudent/profile.html', {
        'student': student,
        'marks': marks,
        'documents': documents,
    })


def admin_search_view(request):
    qry = request.GET.get('qry')
    if qry:
        allrecords = MasterStudent.objects.filter(gr_no__icontains=qry) | MasterStudent.objects.filter(village__icontains=qry) | MasterStudent.objects.filter(name__icontains=qry)
    else:
        allrecords = MasterStudent.objects.all()
    allrecords = allrecords.order_by('-gr_no')
    return render(request, 'masterstudent/allrecord.html', {'allrecords': allrecords})


def change_password(request):
    gr_no_param = request.GET.get('gr_no')  # 👈 Get from query param

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            gr_no = form.cleaned_data['gr_no']
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            try:
                student = MasterStudent.objects.get(gr_no=gr_no)
                if check_password(old_password, student.password) or check_password('admin', student.password):
                    student.password = make_password(new_password)
                    student.save()
                    messages.success(request, 'Password changed successfully.')
                    return redirect('dashboard')  # or wherever you want
                else:
                    messages.error(request, 'Old password is incorrect.')

            except MasterStudent.DoesNotExist:
                messages.error(request, 'Student not found.')
    else:
        form = ChangePasswordForm(initial={'gr_no': gr_no_param})  # 👈 pre-fill GR No

    return render(request, 'masterstudent/change_password.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        gr_no = request.POST['gr_no']
        try:
            student = MasterStudent.objects.get(gr_no=gr_no)
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['gr_no'] = gr_no
            print(otp)
            # send OTP on email
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is: {otp}',
                'yash0808080808@gmail.com',  # From email (set in settings.py)
                [student.email],         # Student's email from DB
                fail_silently=False,
            )
            return redirect('verify_otp')
        except MasterStudent.DoesNotExist:
            messages.error(request, 'GR Number not found.')
    
    return render(request, 'masterstudent/forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST['otp']
        if str(request.session.get('otp')) == user_otp:
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP.')
    return render(request, 'masterstudent/verify_otp.html')

def reset_password(request):
    gr_no = request.session.get('gr_no')
    if request.method == 'POST':
        new_password = request.POST['new_password']
        student = MasterStudent.objects.get(gr_no=gr_no)
        student.password = make_password(new_password)
        student.save()
        messages.success(request, 'Password reset successfully.')
        return redirect('student_login')
    return render(request, 'masterstudent/reset_password.html')

def download_document(request, grno, filename):
    # Full file path: media/documents/<grno>/<filename>
    filepath = os.path.join(settings.MEDIA_ROOT, 'documents', grno, filename)

    if not os.path.exists(filepath):
        raise Http404("File not found.")

    # ✅ Security check: allow only that student to download their own file
    if request.user.username == grno:
        return FileResponse(open(filepath, 'rb'))
    else:
        return HttpResponseForbidden("Unauthorized access.")