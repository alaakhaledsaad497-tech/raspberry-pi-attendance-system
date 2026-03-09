import requests

qr_code = input("Scan QR: ")

url = ""

data = {
    "qr_code": qr_code.strip()
}

response = requests.post(url, json=data)

print("Status:", response.status_code)
print("Response:", response.json())