import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

def send_code(phone):
    url = "https://api.rubika.ir/v2/auth/sendCode"
    return requests.post(url, json={"phone_number": phone}).json()

def sign_in(phone, code, phone_code_hash):
    url = "https://api.rubika.ir/v2/auth/signIn"
    payload = {"phone_number": phone, "phone_code": code, "phone_code_hash": phone_code_hash}
    return requests.post(url, json=payload).json()

@app.route('/')
def home():
    return '''
    <h2>ورود به اکانت روبیکا</h2>
    <form action="/login" method="post">
        شماره (با +98): <input type="text" name="phone"><br><br>
        کد تایید: <input type="text" name="code"><br><br>
        <input type="submit" value="ورود">
    </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    phone = request.form['phone']
    code = request.form['code']
    
    # ارسال کد (اگر قبلا ارسال نشده باشد)
    # برای سادگی، فرض می‌کنیم کد قبلا ارسال شده و phone_code_hash را از جای دیگری می‌آوریم.
    # اما در اینجا ما دوباره کد را ارسال می‌کنیم تا phone_code_hash را بگیریم.
    # این کار باعث می‌شود کد جدیدی برای شما ارسال شود. باید سریع کد را وارد کنید.
    
    res = send_code(phone)
    if res.get("status") != "OK":
        return f"خطا در ارسال کد: {res}"
    
    phone_code_hash = res["data"]["phone_code_hash"]
    
    # حالا با کدی که کاربر وارد کرده، وارد می‌شویم
    login_res = sign_in(phone, code, phone_code_hash)
    
    if login_res.get("status") == "OK":
        auth_data = login_res["data"]["auth"]
        # چاپ session در لاگ‌ها برای کپی کردن
        print("=== SESSION START ===")
        print(json.dumps(auth_data, indent=2))
        print("=== SESSION END ===")
        return "✅ ورود موفق! فایل session.txt در لاگ‌ها چاپ شد. آن را کپی کنید."
    else:
        return f"❌ خطا در ورود: {login_res}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
