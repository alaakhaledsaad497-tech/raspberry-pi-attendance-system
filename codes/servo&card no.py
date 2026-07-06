"""from razrc522 import RFID
import lgpio
import time
import requests

api = ""
rd = RFID()
h = lgpio.gpiochip_open(0)
servo_pin = 18
lgpio.gpio_claim_output(h, servo_pin)
try:
    print("please put the card on the reader")
    while True:
        rd.set_antenna(True)
        rd.wait_for_tag()
        (_, tag_type) = rd.request()
        (_, uid) = rd.anticoll()
        s_uid = "".join([str(i) for i in uid])
        print("card detected:", s_uid)

        response = requests.post(api, json={"cardNumber": s_uid})

        if response.status_code == 200:
            data = response.json()
            if data.get("valid", False):
                print(" Valid - Opening...")
                lgpio.tx_servo(h, servo_pin, 2500) 
                time.sleep(3)
                lgpio.tx_servo(h, servo_pin, 500)   
                print("Invalid Card")
        else:
            print("there is an error:", response.status_code)

        time.sleep(2)

except KeyboardInterrupt:
    print("Exit")
finally:
    lgpio.gpiochip_close(h)








    ====================
"""""
from razrc522 import RFID
import lgpio
import time
import requests

api = ""
rd = RFID()
h = lgpio.gpiochip_open(0)
servo_pin = 18
lgpio.gpio_claim_output(h, servo_pin)

try:
    print("please put the card on the reader")
    while True:
        rd.set_antenna(True)
        rd.wait_for_tag()
        (_, tag_type) = rd.request()
        (_, uid) = rd.anticoll()
        s_uid = "".join([str(i) for i in uid])
        print("card detected:", s_uid)
        
        rd.stop_crypto()  # ✅ زيادة

        try:  # ✅ زيادة
            response = requests.post(api, json={"cardNumber": s_uid}, timeout=5)  # ✅ زيادة

            if response.status_code == 200:
                data = response.json()
                if data.get("valid", False):
                    print("✅ Valid - Opening...")
                    lgpio.tx_servo(h, servo_pin, 2500)
                    time.sleep(3)
                    lgpio.tx_servo(h, servo_pin, 500)
                else:
                    print("Invalid Card")
            else:
                print("there is an error:", response.status_code)

        except requests.exceptions.Timeout:  
            print("Request timed out")
        except requests.exceptions.ConnectionError:  

        time.sleep(2)

except KeyboardInterrupt:
    print("Exit")
finally:
    lgpio.gpiochip_close(h)