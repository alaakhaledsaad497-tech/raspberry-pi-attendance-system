'''
from razrc522 import RFID
import lgpio
import time
import requests

# back end api 
api = "https://smart-system-attendance-production-d4bd.up.railway.app/api/rfid/"

# rfid Object
rd = RFID()

# servo handling
h = lgpio.gpiochip_open(0)
sp = 13
lgpio.gpio_claim_output(h, sp)

try:
    print("please put the card on the reader")

    while True:
        rd.set_antenna(True)
        (error, tag_type) = rd.request()

        if not error:
            (error, uid) = rd.anticoll()

            if not error:
                s_uid = "".join([str(i) for i in uid])
                print("card number:", s_uid)
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
                                lgpio.tx_servo(h, sp, 2500)
                                time.sleep(3)
                                lgpio.tx_servo(h, sp, 500)
                                print("servo closed")
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

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exit")

finally:
    lgpio.gpiochip_close(h)
    
from razrc522 import RFID
import lgpio
import time
import requests

# back end api
api = "https://smart-system-attendance-production-d4bd.up.railway.app/api/rfid/"

# rfid Object
rd = RFID()

# servo handling
h = lgpio.gpiochip_open(0)
sp = 13
lgpio.gpio_claim_output(h, sp)

try:
    print("please put the card on the reader")

    while True:
        rd.set_antenna(True)
        (error, tag_type) = rd.request()

        if not error:
            (error, uid) = rd.anticoll()

            if not error:
                s_uid = "".join([str(i) for i in uid])
                print("card number:", s_uid)
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

                                # close
                                lgpio.tx_servo(h, sp, 500)
                                time.sleep(1)

                                lgpio.tx_servo(h, sp, 0)

                                print("servo closed")

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

# back end api
api = "https://smart-system-attendance-production-d4bd.up.railway.app/api/rfid/"

# rfid Object
rd = RFID()

# servo handling
h = lgpio.gpiochip_open(0)
sp = 13
lgpio.gpio_claim_output(h, sp)

try:
    print("please put the card on the reader")

    while True:
        rd.set_antenna(True)
        (error, tag_type) = rd.request()

        if not error:
            (error, uid) = rd.anticoll()

            if not error:
                s_uid = "".join([str(i) for i in uid])
                print("card number:", s_uid)
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

                                # close
                                lgpio.tx_servo(h, sp, 500)
                                time.sleep(1)

                                lgpio.tx_servo(h, sp, 0)

                                print("servo closed")

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