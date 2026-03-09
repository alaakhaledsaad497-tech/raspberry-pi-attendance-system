# library

 """from razrc522 import RFID
import time
import requests
import face_recognition
import numpy as np
import os
from picamera2 import Picamera2

# object
rd = RFID()

# api
api = ""  # ← رابط الـ backend بتاعك

# ── تحميل صور الموظفين ──
# اعملي فولدر اسمه employees وحطي فيه صور الموظفين
# اسم الصورة = رقم الموظف
# مثال: employees/EMP001.jpg

known_faces = []
known_ids   = []

for filename in os.listdir("employees"):
    if not filename.endswith((".jpg", ".jpeg", ".png")):
        continue
    emp_id    = filename.rsplit(".", 1)[0]
    image     = face_recognition.load_image_file(os.path.join("employees", filename))
    encodings = face_recognition.face_encodings(image)
    if encodings:
        known_faces.append(encodings[0])
        known_ids.append(emp_id)
        print(f"Loaded: {emp_id}")

# ── تشغيل الكاميرا ──
cam = Picamera2()
cam.configure(cam.create_still_configuration())
cam.start()

# code logic
try:
    print("please put the card on the reader:")
    while True:
        rd.set_antenna(True)
        (error, tag_type) = rd.request()
        if not error:
            (error, uid) = rd.anticoll()
            if not error:
                s_uid = "".join([str(i) for i in uid])

                # ── الخطوة 1: تحقق من الكارت في الداتابيز ──
                response = requests.post(api, json={"cardNumber": s_uid})

                if response.status_code == 404:
                    print("Card not found")
                    rd.stop_crypto()
                    time.sleep(0.5)
                    continue

                if response.status_code != 200:
                    print("Server error")
                    rd.stop_crypto()
                    time.sleep(0.5)
                    continue

                # ── الخطوة 2: تحقق من الوجه ──
                print("Card found - verifying face...")

                # السطر ده لو الـ backend بيرجع employeeId في الـ response
                employee_id = response.json().get("employeeId")

                # لو الـ backend مش بيرجع employeeId، امسحي السطر فوق
                # وشيلي الـ # من السطر ده:
                # employee_id = s_uid

                time.sleep(0.3)
                photo = cam.capture_array()  # Picamera2 بترجع RGB مباشرة

                face_locations = face_recognition.face_locations(photo)
                face_encodings = face_recognition.face_encodings(photo, face_locations)

                if not face_encodings:
                    print("No face detected - please look at the camera")
                    rd.stop_crypto()
                    time.sleep(0.5)
                    continue

                distances     = face_recognition.face_distance(known_faces, face_encodings[0])
                best_idx      = int(np.argmin(distances))
                best_distance = distances[best_idx]
                detected_id   = known_ids[best_idx] if best_distance < 0.5 else None

                if detected_id == employee_id:
                    print("Employee marked as attended")
                else:
                    print("Face does not match - attendance not recorded")

                rd.stop_crypto()
            else:
                print("please re put the card")
        else:
            print("please contact the IT")
        time.sleep(0.5)

except KeyboardInterrupt:
    cam.stop()
    cam.close()
    print("Exit")
    """
from razrc522 import RFID
from picamera2 import Picamera2
import face_recognition
import requests
import numpy as np
import os
import time

# ========================
# إعدادات
# ========================
API_URL = "PUT_YOUR_API_HERE"
TOLERANCE = 0.5

# ========================
# تحميل صور الموظفين
# ========================
known_faces = []
known_ids = []

if os.path.exists("employees"):
    for file in os.listdir("employees"):
        if file.endswith((".jpg", ".png", ".jpeg")):
            emp_id = file.split(".")[0]
            img = face_recognition.load_image_file(f"employees/{file}")
            enc = face_recognition.face_encodings(img)

            if enc:
                known_faces.append(enc[0])
                known_ids.append(emp_id)
                print(f"Loaded {emp_id}")

# ========================
# تشغيل الأجهزة
# ========================
rd = RFID()
cam = Picamera2()
cam.configure(cam.create_still_configuration())
cam.start()

print("System Ready - Put your card")

# ========================
# اللوب الرئيسي
# ========================
try:
    while True:
        rd.set_antenna(True)
        error, _ = rd.request()

        if error:
            time.sleep(0.3)
            continue

        error, uid = rd.anticoll()
        if error:
            print("Card read error")
            continue

        card_number = "".join(map(str, uid))

        # تحقق من الكارت
        res = requests.post(API_URL, json={"cardNumber": card_number})

        if res.status_code != 200:
            print("Card not valid")
            continue

        employee_id = res.json().get("employeeId")

        # التقاط صورة
        print("Verifying face...")
        frame = cam.capture_array()

        encodings = face_recognition.face_encodings(frame)
        if not encodings:
            print("No face detected")
            continue

        # مقارنة الوجه
        distances = face_recognition.face_distance(known_faces, encodings[0])
        best_match = np.argmin(distances)

        if distances[best_match] < TOLERANCE and known_ids[best_match] == employee_id:
            print("Attendance Recorded ✅")
        else:
            print("Face mismatch ❌")

        time.sleep(1)

except KeyboardInterrupt:
    cam.stop()
    cam.close()
    print("System Closed")