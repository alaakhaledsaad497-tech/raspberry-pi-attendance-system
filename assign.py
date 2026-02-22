                             
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


