# student_documents/forms.py
from django import forms
from .models import StudentDocument

class StudentDocumentForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = ['document_type', 'document_file']
