from django.db import models
from masterstudent.models import MasterStudent  # Adjust path if needed

DOCUMENT_TYPES = [
    ('aadhar', 'Aadhar Card'),
    ('photo', 'Passport Size Photo'),
    ('ration_card', 'Ration Card'),
    ('marksheet_9', '9th Marksheet'),
    ('marksheet_10', '10th Marksheet'),
    ('marksheet_11', '11th Marksheet'),
    ('marksheet_12', '12th Marksheet'),
    ('lc_10', '10th Leaving Certificate'),
    ('lc_12', '12th Leaving Certificate'),
    ('caste', 'Caste Certificate'),
    ('non-creamyLayer', 'Non-Creamy Layer Certificate'),
]
def upload_to_path(instance, filename):
    return f'documents/{instance.gr_no}/{instance.document_type}.pdf'
class StudentDocument(models.Model):
    student = models.ForeignKey(MasterStudent, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.gr_no} - {self.document_type}"
