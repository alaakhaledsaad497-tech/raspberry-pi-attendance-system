import requests
import time
import lgpio


# Servo Setup

SERVO_PIN = 13
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, Sp)

GET_URL  = "https://smart-system-attendance-production-d4bd.up.railway.app/api/device/commands/pending"
POST_URL = "https://smart-system-attendance-production-d4bd.up.railway.app/api/device/command/done"

print("Gate controller started...")

while True:

    # route1 (asking for any new req)
    res = requests.get(GET_URL)
    data = res.json()

    if data["command"] == "open_gate":
        print("Opening gate!")
        lgpio.tx_servo(h, Sp, 2500)   # open 
        time.sleep(1)
        lgpio.tx_servo(h, Sp, 0)      # stopsignal avoiding pwm pulse

        # route2
        requests.post(POST_URL, json={"commandId": data["commandId"]})
        print("Gate opened ✅")

    elif data["command"] == "close_gate":
        print("Closing gate!")
        lgpio.tx_servo(h, Sp, 500)    # close
        time.sleep(1)
        lgpio.tx_servo(h, Sp, 0)      # stop signal

        
        requests.post(POST_URL, json={"commandId": data["commandId"]})
        print("Gate closed ✅")

    else:
        print("No commands...")

    time.sleep(1)  #delay