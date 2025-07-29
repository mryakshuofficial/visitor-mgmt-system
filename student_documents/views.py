from django.shortcuts import render, redirect
from django.contrib import messages
from student_documents.form import StudentDocumentForm
from .models import StudentDocument
from masterstudent.models import MasterStudent 
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import StudentDocument, DOCUMENT_TYPES
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password

# Create your views here.
# @login_required
def upload_document(request):
    document_uploaded = False
    error_message = None

    students = MasterStudent.objects.all()

    if request.method == 'POST':
        gr_no = request.POST.get('gr_no')
        password = request.POST.get("password", "").strip()
        doc_type = request.POST.get('document_type')
        doc_file = request.FILES.get('document')

        print("GR:", gr_no)
        print("Doc Type:", doc_type)
        print("Password:", password)
        try:
            student = MasterStudent.objects.get(gr_no=gr_no)
        except MasterStudent.DoesNotExist:
            error_message = 'Student not found.'
        else:
            # ✅ Check password
            if check_password(password,student.password):
                #  Create folder
                upload_path = os.path.join('documents', gr_no)
                full_path = os.path.join(settings.MEDIA_ROOT, upload_path)
                os.makedirs(full_path, exist_ok=True)

                # 📝 Rename file
                ext = os.path.splitext(doc_file.name)[1]
                new_filename = f"{doc_type}{ext}"
                fs = FileSystemStorage(location=full_path)
                fs.save(new_filename, doc_file)

                # ✅ Save in DB
                document = StudentDocument(
                    student=student,
                    document_type=doc_type,
                    document_file=f'documents/{gr_no}/{new_filename}'
                )
                document.save()
                document_uploaded = True
                messages.success(request, f'{doc_type} uploaded successfully for {gr_no}!')
            else:
                print("Entered password:", password)
                print("Stored hash:", student.password)
                print("Match result:", check_password(password, student.password))
                error_message = 'Invalid password.'

    return render(request, 'student_documents/upload.html', {
        'students': students,
        'document_types': DOCUMENT_TYPES,
        'document_uploaded': document_uploaded,
        'error_message': error_message,
    })


def upload_success(request):
    return render(request, 'student_documents/success.html')


def logout_user(request):
    logout(request)
    return redirect('login')



def upload_success(request):
    return render(request, 'student_documents/success.html')

def logout_user(request):
    logout(request)
    return redirect('login')