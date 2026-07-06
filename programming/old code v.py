from razrc522 import RFID
import requests

APIurl = "http://YOUR_API_URL"

reader = RFID()
print("put the card on the scanner")

while True:
    reader.wait_for_tag()

    _, _ = reader.request()  
    _, uid = reader.anticoll()  

    print("UID:", uid)

    try:
        requests.post(APIurl, json={"uid": str(uid)})
    except:
        print("there is an error")
