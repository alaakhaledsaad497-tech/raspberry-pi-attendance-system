'''from razrc522 import RFID
import lgpio
import time
import requests
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
from time import sleep


# back end api
api = "https://smart-system-attendance-production-d4bd.up.railway.app/api/rfid/"

# rfid Object
rd = RFID()

# servo handling
h = lgpio.gpiochip_open(0)
sp = 13
lgpio.gpio_claim_output(h, sp)
# lcd handling
lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    pin_rs=26,
    pin_e=19,
    pins_data=[13, 6, 5, 11],
    cols=16,
    rows=2

try:
    lcd.clear()
    #print("please put the card on the reader")
    lcd.write_string("please put the card on the reader")
    while True:
        rd.set_antenna(True)
        (error, tag_type) = rd.request()

        if not error:
            (error, uid) = rd.anticoll()

            if not error:
                s_uid = "".join([str(i) for i in uid])
                lcd.clear()
               # print("card number:", s_uid)
                lcd.write_string("Card UID:")
                lcd.cursor_pos = (1, 0)
                lcd.write_string(s_uid)
                sleep(3)
                lcd.clear()

                rd.stop_crypto()

                try:
                    response = requests.post(
                        api,
                        json={"cardNumber": s_uid},
                        timeout=5
                    )

                    print("Status:", response.status_code)
                    print(" Response:", response.text)

                    if response.status_code == 200:
                        try:
                            data = response.json()
                            print("JSON:", data)

                            if data.get("allowed", False):
                                print("Valid - Opening...")

                                # open
                                lgpio.tx_servo(h, sp, 2500)
                                time.sleep(1)
                                lcd.write_string('opining gates')
                                time.sleep(2)


                                # close
                                lgpio.tx_servo(h, sp, 500)
                                time.sleep(1)
                               # lcd.write_string('closing gates')
                               # time.sleep(2)

                                lgpio.tx_servo(h, sp, 0)

                                #print("servo closed")
                                 lcd.write_string('closing gates')
                                time.sleep(2)

                            else:
                                print("Invalid")

                        except requests.exceptions.JSONDecodeError:
                            print("Response is not valid JSON")

                    else:
                        print("API Error:", response.status_code)

                except requests.exceptions.Timeout:
                    print("Request timed out - check internet")

                except requests.exceptions.ConnectionError:
                    print("Connection error - check internet")

                # delay علشان ميقرأش الكروت ورا بعض
                time.sleep(3)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exit")

finally:
    try:
        lgpio.tx_servo(h, sp, 0)
    except:
        pass

    lgpio.gpiochip_close(h)
    '''
from razrc522 import RFID
import lgpio
import time
import requests
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

# Back-end API
api = "https://smart-system-attendance-production-d4bd.up.railway.app/api/rfid/"

# RFID object
rd = RFID()

# Servo handling
h = lgpio.gpiochip_open(0)
sp = 13 
lgpio.gpio_claim_output(h, sp)

# LCD handling
lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    pin_rs=26,
    pin_e=19,
    pins_data=[21, 6, 5, 11],
    cols=16,
    rows=2
)

try:
    while True:
        lcd.clear()
        lcd.write_string("Please Put Card")

        rd.set_antenna(True)
        (error, tag_type) = rd.request()

        if not error:
            (error, uid) = rd.anticoll()

            if not error:
                s_uid = "".join([str(i) for i in uid])

                
                lcd.clear()
                lcd.write_string("Card UID:")
                lcd.cursor_pos = (1, 0)
                lcd.write_string(s_uid)
                time.sleep(3)
                lcd.clear()
                lcd.write_string("Please Put Card")

                rd.stop_crypto()

                try:
                    response = requests.post(
                        api,
                        json={"cardNumber": s_uid},
                        timeout=5
                    )

                    print("Status:", response.status_code)
                    print("Response:", response.text)

                    if response.status_code == 200:
                        try:
                            data = response.json()

                            if data.get("allowed", False):
                                print("Valid - Opening...")

                                
                                lgpio.tx_servo(h, sp, 2500)
                                time.sleep(1)
                                lcd.clear()
                                lcd.write_string("Opening Gates...")
                                time.sleep(2)

                               
                                lgpio.tx_servo(h, sp, 500)
                                time.sleep(1)
                                lcd.clear()
                                lcd.write_string("Closing Gates...")
                                time.sleep(2)

                                lgpio.tx_servo(h, sp, 0)

                            else:
                                print("Invalid Card")
                                lcd.clear()
                                lcd.write_string("Invalid Card...")
                                time.sleep(2)

                        except requests.exceptions.JSONDecodeError:
                            print("Response is not valid JSON")

                    else:
                        print("API Error:", response.status_code)

                except requests.exceptions.Timeout:
                    print("Request timed out - check internet")

                except requests.exceptions.ConnectionError:
                    print("Connection error - check internet")

                time.sleep(3)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exit")

finally:
    try:
        lgpio.tx_servo(h, sp, 0)
    except Exception as e:
        print("Error closing servo:", e)

    lgpio.gpiochip_close(h)
    lcd.clear()