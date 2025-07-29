from django.shortcuts import render, redirect
from student_documents.form import StudentDocumentForm
from .models import StudentDocument
from masterstudent.models import MasterStudent 
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import StudentDocument, DOCUMENT_TYPES
from django.contrib.auth import logout

# Create your views here.
@login_required
def upload_document(request):
    students = MasterStudent.objects.all()

    if request.method == 'POST':
        gr_no = request.POST.get('gr_no')
        doc_type = request.POST.get('document_type')
        doc_file = request.FILES.get('document')

        try:
            student = MasterStudent.objects.get(gr_no=gr_no)
        except MasterStudent.DoesNotExist:
            return render(request, 'student_documents/error.html', {'message': 'Student not found.'})

        # 🗂️ Create folder media/documents/GR_NO/
        upload_path = os.path.join('documents', gr_no)
        full_path = os.path.join(settings.MEDIA_ROOT, upload_path)
        os.makedirs(full_path, exist_ok=True)

        # 📝 Rename file to document_type.ext (eg: aadhar.pdf)
        ext = os.path.splitext(doc_file.name)[1]
        new_filename = f"{doc_type}{ext}"
        fs = FileSystemStorage(location=full_path)
        filename = fs.save(new_filename, doc_file)

        # ✅ Save to DB
        document = StudentDocument(student=student, document_type=doc_type, document_file=f'documents/{gr_no}/{new_filename}')
        document.save()

        return redirect('upload_document')  # Refresh page

    return render(request, 'student_documents/upload.html', {
    'students': students,
    'document_types': DOCUMENT_TYPES  # 👈 send to template
})

def upload_success(request):
    return render(request, 'student_documents/success.html')

def logout_user(request):
    logout(request)
    return redirect('login')