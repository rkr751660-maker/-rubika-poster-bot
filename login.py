import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)
global_data = {}

# استفاده از دامنه جایگزین به جای api.rubika.ir
BASE_URL = "https://botapi.rubika.ir/v2/" 

def send_code(phone):
    url = f"{BASE_URL}auth/sendCode"
    try:
        res = requests.post(url, json={"phone_number": phone}, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def sign_in(phone, code, phone_code_hash):
    url = f"{BASE_URL}auth/signIn"
    payload = {"phone_number": phone, "phone_code": code, "phone_code_hash": phone_code_hash}
    try:
        res = requests.post(url, json=payload, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    return '''
    <h2>مرحله ۱: دریافت کد</h2>
    <form action="/send" method="post">
        شماره (با +98): <input type="text" name="phone"><br><br>
        <input type="submit" value="ارسال کد">
    </form>
    '''

@app.route('/send', methods=['POST'])
def send():
    phone = request.form['phone']
    res = send_code(phone)
    if "error" in res: return f"خطای شبکه: {res['error']}<br><a href='/'>بازگشت</a>"
    if res.get("status") == "OK":
        global_data['phone'] = phone
        global_data['hash'] = res["data"]["phone_code_hash"]
        return '''
        <h2>مرحله ۲: وارد کردن کد</h2>
        <form action="/verify" method="post">
            کد تایید: <input type="text" name="code"><br><br>
            <input type="submit" value="ورود">
        </form>
        '''
    else:
        return f"خطای روبیکا: {res}<br><a href='/'>بازگشت</a>"

@app.route('/verify', methods=['POST'])
def verify():
    code = request.form['code']
    phone = global_data.get('phone')
    phone_code_hash = global_data.get('hash')
    if not phone or not phone_code_hash: return "خطا: ابتدا شماره را وارد کنید.<br><a href='/'>بازگشت</a>"
    
    login_res = sign_in(phone, code, phone_code_hash)
    if "error" in login_res: return f"خطای شبکه: {login_res['error']}<br><a href='/'>بازگشت</a>"
    if login_res.get("status") == "OK":
        auth_data = login_res["data"]["auth"]
        print("=== SESSION START ===")
        print(json.dumps(auth_data))
        print("=== SESSION END ===")
        return "✅ ورود موفق! حالا به تب Logs در Render بروید و Session را کپی کنید."
    else:
        return f"❌ خطای روبیکا در ورود: {login_res}<br><a href='/'>بازگشت</a>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
