'''                             
from razrc522 import RFID
import requests

api = ""
rd = RFID()

print("please put the card:")
while True:
    rd.set_antenna(True)
    (error, tag_type) = rd.request()
    if not error:
        (error, uid) = rd.anticoll()
        if not error:
            s_uid = "".join([str(i) for i in uid])
            response = requests.post(api, json={"cardNumber": s_uid})
            print("Response:", response.status_code, response.json())
            rd.stop_crypto()
'''

from razrc522 import RFID
import requests
import time

api = "https://smart-system-attendance-production-d4bd.up.railway.app/api/attendance/card"
rd = RFID()

print("please put the card:")
while True:
    rd.set_antenna(True)
    (error, tag_type) = rd.request()
    if not error:
        (error, uid) = rd.anticoll()
        if not error:
            s_uid = "".join([str(i) for i in uid])
            response = requests.post(api, json={"cardNumber": s_uid})
            print("Response:", response.status_code, response.json())
            rd.stop_crypto()
            time.sleep(3)