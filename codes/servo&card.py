from razrc522 import RFID
import lgpio
import time
import requests

api = "https://smart-system-attendance-production-d4bd.up.railway.app/api/rfid/enter"

rd = RFID()
rd.set_antenna(True)
h = lgpio.gpiochip_open(0)
servo_pin = 13
lgpio.gpio_claim_output(h, servo_pin)

try:
    print("please put the card on the reader")
    while True:
        (error, tag_type) = rd.request()
        if not error:
            (error, uid) = rd.anticoll()
            if not error:
                s_uid = "".join([str(i) for i in uid])
                print("card detected:", s_uid)
                rd.stop_crypto()

                try:
                    response = requests.post(api, json={"cardNumber": s_uid}, timeout=5)
                    print("Response:", response.json())

                    if response.status_code == 200:
                        data = response.json()
                        if data.get("allowed", False):
                            print("Valid - Opening...")
                            lgpio.tx_pwm(h, servo_pin, 50, 7.5)
                            time.sleep(2)
                            lgpio.tx_pwm(h, servo_pin, 50, 2.5)
                            time.sleep(1)
                            lgpio.tx_pwm(h, servo_pin, 0, 0)
                            lgpio.gpio_write(h, servo_pin, 0)
                            print("Door closed.")
                        else:
                            print("Invalid Card")
                    else:
                        print("API Error:", response.status_code)

                except requests.exceptions.Timeout:
                    print("Request timed out - check internet connection")
                except requests.exceptions.ConnectionError:
                    print("Connection error - check internet connection")

                time.sleep(2)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exit")
finally:
    lgpio.tx_pwm(h, servo_pin, 0, 0)
    lgpio.gpio_write(h, servo_pin, 0)
    lgpio.gpiochip_close(h)