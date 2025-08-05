# utils/initialize_attendance_csv.py
import pandas as pd
import os
from datetime import datetime
from masterstudent.models import MasterStudent
from django.conf import settings

def initialize_attendance_csv():
    today = datetime.now()
    days = [str(day) for day in range(1, 32)]  # 1 to 31 days

    # Create column names
    columns = ['gr_no', 'fname', 'lname', 'surname'] + days
    df = pd.DataFrame(columns=columns)

    # Populate from MasterStudent table
    students = MasterStudent.objects.all()
    for s in students:
        row = {
            'gr_no': s.gr_no,
            'fname': s.fname,
            'lname': s.lname,
            'surname': s.surname
        }
        for d in days:
            row[d] = ''
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    csv_path = os.path.join(settings.BASE_DIR, 'attendance.csv')
    df.to_csv(csv_path, index=False)
    print("✅ attendance.csv initialized.")
