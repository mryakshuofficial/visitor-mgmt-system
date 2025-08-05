# face_attendance/views.py

import cv2
import os
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
from datetime import datetime
from masterstudent.models import MasterStudent 
from types import SimpleNamespace

# Haarcascade for face detection
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# -------------------- Helper Functions --------------------

def extract_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return None
    for (x, y, w, h) in faces:
        return img[y:y + h, x:x + w]
    return None


def train_model():
    data_path = os.path.join(settings.BASE_DIR, 'images')
    training_data, labels = [], []
    label_map = {}
    current_label = 0

    if not os.path.exists(data_path):
        return False, {}

    for folder in os.listdir(data_path):
        folder_path = os.path.join(data_path, folder)
        if not os.path.isdir(folder_path):
            continue
        for image_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, image_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            training_data.append(img)
            labels.append(current_label)
        label_map[current_label] = folder
        current_label += 1

    if len(training_data) == 0:
        return False, {}

    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(training_data, np.array(labels))
    model.save(os.path.join(settings.BASE_DIR, 'trained_model.yml'))

    return True, label_map


# -------------------- Views --------------------

def capture_face(request):
    if request.method == 'POST':
        gr_no = request.POST.get('gr_no')
        name = request.POST.get('name')

        if not gr_no or not name:
            return HttpResponse("❌ GR Number and Name are required.")

        folder_name = f"{gr_no}_{name.replace(' ', '_')}"
        save_path = os.path.join(settings.BASE_DIR, 'images', folder_name)
        os.makedirs(save_path, exist_ok=True)

        cap = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            face = extract_face(frame)
            if face is not None:
                count += 1
                face = cv2.resize(face, (200, 200))
                gray_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                file_path = os.path.join(save_path, f"{count}.jpg")
                cv2.imwrite(file_path, gray_face)
                cv2.putText(gray_face, f"{count}/50", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.imshow("Face Capture", gray_face)
            else:
                cv2.imshow("Face Capture", frame)

            if cv2.waitKey(1) & 0xFF == ord('q') or count >= 50:
                break

        cap.release()
        cv2.destroyAllWindows()

        trained, _ = train_model()
        if trained:
            return HttpResponse(f"✅ {count} images captured & model trained! Folder: {folder_name}")
        else:
            return HttpResponse("⚠️ Images saved but model training failed.")

    return render(request, 'face_attendance/capture.html')


from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import time

# global temp variable
TEMP_RECOGNIZED = {}

def recognize_face(request):
    global TEMP_RECOGNIZED
    model_path = os.path.join(settings.BASE_DIR, 'trained_model.yml')
    if not os.path.exists(model_path):
        return HttpResponse("❌ Please train the model first.")

    model = cv2.face.LBPHFaceRecognizer_create()
    model.read(model_path)

    data_path = os.path.join(settings.BASE_DIR, 'images')
    label_map = {i: folder for i, folder in enumerate(os.listdir(data_path))}

    cap = cv2.VideoCapture(0)

    detected = None
    hold_time = 2.5  # seconds
    start_hold = None
    last_label = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        face = extract_face(frame)
        if face is not None:
            face = cv2.resize(face, (200, 200))
            gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            label, confidence = model.predict(gray)

            if confidence < 60:
                person = label_map.get(label, 'Unknown')
                parts = person.split('_')
                gr_no = parts[0]
                fname = parts[1] if len(parts) > 1 else ''
                lname = parts[2] if len(parts) > 2 else ''
                surname = parts[3] if len(parts) > 3 else ''

                # Display green recognized text
                text = f"✅ Recognized: {fname} {lname} ({gr_no})"
                cv2.putText(frame, text, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                if label == last_label:
                    if start_hold and (time.time() - start_hold) >= hold_time:
                        # Face held for 2.5 seconds
                        detected = {
                            'gr_no': gr_no,
                            'fname': fname,
                            'lname': lname,
                            'surname': surname
                        }
                        cap.release()
                        cv2.destroyAllWindows()
                        TEMP_RECOGNIZED = detected
                        return redirect('confirm_attendance')
                else:
                    start_hold = time.time()
                    last_label = label
            else:
                cv2.putText(frame, "❌ Unknown Face", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                start_hold = None
                last_label = None
        else:
            cv2.putText(frame, "No Face Detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            start_hold = None
            last_label = None

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return HttpResponse("❌ No face recognized.")


def mark_attendance_csv(gr_no, fname, lname, surname):
    csv_path = os.path.join(settings.BASE_DIR, 'attendance.csv')
    today_day = str(datetime.now().day)

    # Create new CSV if not exists
    if not os.path.exists(csv_path):
        cols = ['gr_no', 'fname', 'lname', 'surname'] + [str(i) for i in range(1, 32)]
        df = pd.DataFrame(columns=cols)
        df.to_csv(csv_path, index=False)

    df = pd.read_csv(csv_path)

    if gr_no in df['gr_no'].values:
        df.loc[df['gr_no'] == gr_no, today_day] = 'P'
    else:
        new_row = {
            'gr_no': gr_no,
            'fname': fname,
            'lname': lname,
            'surname': surname
        }
        for i in range(1, 32):
            new_row[str(i)] = 'A'
        new_row[today_day] = 'P'
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_csv(csv_path, index=False)
    
@csrf_exempt
def confirm_attendance(request):
    global TEMP_RECOGNIZED
    student_dict = TEMP_RECOGNIZED
    student = SimpleNamespace(**student_dict)  # convert dict to object-like

    if request.method == 'POST':
        answer = request.POST.get('confirm')
        if answer == 'yes':
            mark_attendance_csv(student.gr_no, student.fname, student.lname, student.surname)
            return render(request, 'face_attendance/recognize.html', {'student': student, 'status': 'present'})
        else:
            return HttpResponse("❌ Attendance not confirmed.")

    return render(request, 'face_attendance/confirm.html', {'student': student})

