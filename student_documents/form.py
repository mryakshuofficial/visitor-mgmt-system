# student_documents/forms.py
from django import forms
from .models import StudentDocument

class StudentDocumentForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = ['document_type', 'document_file']

    def clean_document_file(self):
        file = self.cleaned_data.get('document_file')

        # ✅ Check extension
        allowed_extensions = ['jpg', 'jpeg', 'png', 'pdf']
        extension = file.name.split('.')[-1].lower()
        if extension not in allowed_extensions:
            raise forms.ValidationError("Only JPG, JPEG, PNG, and PDF files are allowed.")

        # ✅ Check file size (max 2 MB)
        max_file_size = 2 * 1024 * 1024  # 2 MB
        if file.size > max_file_size:
            raise forms.ValidationError("File size must be under 2 MB.")

        return file