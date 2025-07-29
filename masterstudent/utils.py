import pandas as pd
from .models import MasterStudent
from django.contrib.auth.hashers import make_password

def load_students_from_excel(file_path='masterstudent.xlsx'):
    df = pd.read_excel(file_path)

    for index, row in df.iterrows():
        gr_no = row.get('gr_no')

        if not MasterStudent.objects.filter(gr_no=gr_no).exists():
            full_name = f"{row.get('fname') or ''} {row.get('lname') or ''} {row.get('surname') or ''}".strip()

            MasterStudent.objects.create(
                gr_no = gr_no,
                student_class = row.get('student_class'),
                fname = row.get('fname'),
                lname = row.get('lname'),
                surname = row.get('surname'),
                name = full_name,  # 👈 fixed here
                village = row.get('village'),
                mobile = str(row.get('mobile')),
                aadhar = str(row.get('aadhar')),
                email = row.get('email'),
                gender = row.get('gender'),
                dob = row.get('DOB'),
                photo_path = row.get('Photo Path'),
                password = make_password('admin'),
            )