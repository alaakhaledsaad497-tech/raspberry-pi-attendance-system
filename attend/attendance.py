#library
from razrc522 import RFID
import time
import requests
# object
rd = RFID()
#api
api = ""

'''
When the employee scans the card, the API checks whether the card is in the database or not.
There are two scenarios:
First: If the card is in the database, the employee will be marked as attended.
Second: If the card is not in the database, a message will appear on the LCD.
'''

#code logic
try:
 print("please put the card on the reader:")
 while True:
  rd.set_antenna(True)
  (error,tag_type)=rd.request()
  if not error:
   (error,uid)=rd.anticoll()
   if not error:
    s_uid="".join([str(i)for i in uid])
    response=requests.post(api,json={"cardNumber":s_uid})
    if response.status_code==200:
     print("Employee marked as attended")
    elif response.status_code==404:
     print("Card not found")
    else:
     print("Server error")
    rd.stop_crypto()
   else:
    print("please re put the card")
  else:
   print("please contact the IT")
  time.sleep(0.5)
except KeyboardInterrupt:
 print("Exit")