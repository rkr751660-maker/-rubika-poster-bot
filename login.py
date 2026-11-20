import requests
import json
import time

def send_code(phone):
    url = "https://api.rubika.ir/v2/auth/sendCode"
    return requests.post(url, json={"phone_number": phone}).json()

def sign_in(phone, code, phone_code_hash):
    url = "https://api.rubika.ir/v2/auth/signIn"
    payload = {"phone_number": phone, "phone_code": code, "phone_code_hash": phone_code_hash}
    return requests.post(url, json=payload).json()

print("=== LOGIN SCRIPT STARTED ===")
# شماره خود را با کد کشور اینجا بنویسید (مثلاً +989121234567)
PHONE = "+989919466845" 

print(f"Sending code to {PHONE}...")
res = send_code(PHONE)
print("Response:", res)

if res.get("status") == "OK":
    phone_code_hash = res["data"]["phone_code_hash"]
    # چون سرور منتظر می‌ماند، ۶۰ ثانیه صبر می‌کند تا شما کد را در لاگ‌ها ببینید
    time.sleep(10) 
    # کدی که به روبیکا می‌آید را اینجا بنویسید
    CODE = "12345" 
    
    login_res = sign_in(PHONE, CODE, phone_code_hash)
    print("Login Response:", login_res)
    
    if login_res.get("status") == "OK":
        with open("session.txt", "w") as f:
            json.dump(login_res["data"]["auth"], f)
        print("✅ SESSION FILE CREATED SUCCESSFULLY!")
