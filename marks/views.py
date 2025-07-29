from django.shortcuts import render ,redirect , HttpResponse , get_object_or_404
from django.contrib.auth.decorators import login_required
from . import urls
from .models import tbl_Studentmarks
from django.db.models import Q
from django.http import JsonResponse
from masterstudent.models import MasterStudent




# Create your views here.
@login_required
def marks_index(request):
    if request.method =='POST':
        gr_no = request.POST.get('gr_no')
        name = request.POST.get('name')
        Class = request.POST.get('Class')
        marks = [int(request.POST.get(f'sub{i}')) for i in range(1, 8)]
        total = sum(marks)
        percentage = total / 7

        studentmarks = tbl_Studentmarks(
        gr_no=gr_no,
        name=name,
        student_class = Class,
        sub1=marks[0],
        sub2=marks[1],
        sub3=marks[2],
        sub4=marks[3],
        sub5=marks[4],
        sub6=marks[5],
        sub7=marks[6],
        total = total,
        percentage = percentage
        )
        studentmarks.save()
        return redirect('marks_index')
    marks = tbl_Studentmarks.objects.all().order_by('-id')

    # 👇 Class list for dropdown
    all_classes = tbl_Studentmarks.objects.values_list('student_class', flat=True).distinct()


    #start here  search by name or class
    search = request.GET.get('search')
    if search:
         marks = marks.filter(
             Q(name__icontains=search) |
            Q(student_class__icontains=search)
        )

    #start here  dropdown list by class
    selected_class = request.GET.get('filter_class')
    if selected_class:
        marks = marks.filter(student_class=selected_class)

    return render(request, 'marks/index.html', {
        'marks': marks,
        'all_classes': all_classes
    })

def marks_edit(request,id):
    fee = get_object_or_404(tbl_Studentmarks,id=id)
    if request.method == 'POST':
        fee.name = request.POST.get('name')
        fee.student_class = request.POST.get('student_class')
        fee.sub1 = int(request.POST.get('sub1'))
        fee.sub2 = int(request.POST.get('sub2'))
        fee.sub3 = int(request.POST.get('sub3'))
        fee.sub4 = int(request.POST.get('sub4'))
        fee.sub5 = int(request.POST.get('sub5'))
        fee.sub6 = int(request.POST.get('sub6'))
        fee.sub7 = int(request.POST.get('sub7'))

        fee.total = sum([fee.sub1, fee.sub2, fee.sub3, fee.sub4, fee.sub5, fee.sub6, fee.sub7])
        fee.percentage = fee.total / 7
        fee.save()
        return redirect('marks_index')
    return render(request,'marks/edit.html',{'fee':fee})

def marks_delete(request,id):
    fee = get_object_or_404(tbl_Studentmarks,id=id)
    fee.delete()
    return redirect('marks_index')

def marks_report(request,id):
    student_report = get_object_or_404(tbl_Studentmarks,id=id)
    return render(request,'marks/report.html',{'student_report':student_report})

def fetch_student(request, gr_no):
    try:
        student = MasterStudent.objects.get(gr_no=gr_no)
        data = {
            'success': True,
            'name': student.name,
            'student_class': student.student_class,
        }
    except MasterStudent.DoesNotExist:
        data = {'success': False}
    return JsonResponse(data)

def logout_user(request):
    logout(request)
    return redirect('login')  # 👈 change if your login URL name is different

