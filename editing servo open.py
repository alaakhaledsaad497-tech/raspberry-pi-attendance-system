"""
from razrc522 import RFID
import lgpio
import time
import requests

# back end api
api = "https://smart-system-attendance-production-d4bd.up.railway.app/api/rfid/>
# rfid Object
rd = RFID()
# servo
# 1-handling
h = lgpio.gpiochip_open(0)
# 2-servo pin
sp = 13
# out put catching
lgpio.gpio_claim_output(h, sp)

try:
    print("please put 
          
          ============================================================================================

from razrc522 import RFID
import lgpio
import time
import requests

# back end api
api = "https://smart-system-attendance-production-d4bd.up.railway.app/api/rfid/>
# rfid Object
rd = RFID()
# servo
# 1-handling
h = lgpio.gpiochip_open(0)
# 2-servo pin
sp = 13
# out put catching
lgpio.gpio_claim_output(h, sp)

try:
    print("please put put the card on the reader")
    while True:
        rd.set_antenna(True)
        (error, tag_type) = rd.request()
        if not error:
            (error, uid) = rd.anticol
            if not error:
                s_uid = "".join([str(i) for i in uid])
                print("card detected:", s_uid)
                rd.stop_crypto()
                try:
                    response = requests.post(api, json={"cardNumber": s_uid}, t>
                    print("Response:", response.json())
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("allowed", False):
                            print("Valid - Opening...")
                            lgpio.tx_servo(h, sp, 2500)
                            time.sleep(3)
                            lgpio.tx_servo(h, sp, 500)
                            print("servo closed")
                        else:
                            print("Invalid")
                    else:
                        print("API Error:", response.status_code)
if not error:
                s_uid = "".join([str(i) for i in uid])
                print("card detected:", s_uid)
                rd.stop_crypto()
                try:
                    response = requests.post(api, json={"cardNumber": s_uid}, t>
                    print("Response:", response.json())
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("allowed", False):
                            print("Valid - Opening...")
                            lgpio.tx_servo(h, sp, 2500)
                            time.sleep(3)
                            lgpio.tx_servo(h, sp, 500)
                            print("servo closed")
                        else:
                            print("Invalid")
                    else:
                        print("API Error:", response.status_code)
     print("API Error:", response.status_code)
                except requests.exceptions.Timeout:
                    print("Request timed out - check internet connection")
                except requests.exceptions.ConnectionError:
                    print("Connection error - check internet connection")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exit")
finally:
    lgpio.gpiochip_close(h)
"""


