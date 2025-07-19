from django.shortcuts import render, get_object_or_404
from masterstudent import urls
from django.shortcuts import render
from .models import MasterStudent  # adjust your import if needed
from marks.models import tbl_Studentmarks  # import from your marks app

# Create your views here.
def student_profile_login(request):
    if request.method == 'POST':
        gr_no = request.POST.get('gr_no')
        password = request.POST.get('password')

        if password != 'admin':
            print("hello",password)
            return render(request, 'masterstudent/login.html', {'error': 'Invalid password.'})
        else:
            try:
                # student = MasterStudent.objects.get(gr_no=gr_no)
                student = MasterStudent.objects.get(gr_no=gr_no)
                marks = tbl_Studentmarks.objects.filter(gr_no=gr_no)
                # return render(request,'masterstudent/profile.html')
                return render(request, 'masterstudent/profile.html', {'student': student, 'marks': marks})
            except MasterStudent.DoesNotExist:
                return render(request, 'masterstudent/login.html', {'error': 'Student not found.'})

    return render(request, 'masterstudent/login.html')

def student_profile_view(request, gr_no):
    student = get_object_or_404(StudentMaster, gr_no=gr_no)
    
    # Yahi sabse important line hai: sirf usi GR No ke marks fetch karo
    marks = tbl_Studentmarks.objects.filter(gr_no=gr_no)

    return render(request, 'student_profile_view.html', {
        'student': student,
        'marks': marks
    })