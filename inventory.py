import json
import os
from datetime import datetime

# فایل‌های ذخیره‌سازی
INVENTORY_FILE = "inventory.json"
TRANSACTIONS_FILE = "transactions.json"

def load_data():
    """بارگذاری اطلاعات از فایل"""
    try:
        if os.path.exists(INVENTORY_FILE):
            with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
                inventory = json.load(f)
        else:
            inventory = {}
            
        if os.path.exists(TRANSACTIONS_FILE):
            with open(TRANSACTIONS_FILE, 'r', encoding='utf-8') as f:
                transactions = json.load(f)
        else:
            transactions = []
            
    except Exception as e:
        print("خطا در بارگذاری فایل‌ها:", str(e))
        inventory = {}
        transactions = []
        
    return inventory, transactions

def save_data(inventory, transactions):
    """ذخیره اطلاعات در فایل"""
    try:
        with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(inventory, f, ensure_ascii=False, indent=2)
        with open(TRANSACTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(transactions, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("خطا در ذخیره‌سازی:", str(e))

def add_product(inventory, transactions):
    """افزودن محصول به انبار"""
    print("\n=== ورود کالا به انبار ===")
    try:
        name = input("نام محصول: ")
        quantity = int(input("تعداد: "))
        if quantity <= 0:
            print("❌ تعداد باید بیشتر از صفر باشد")
            return
            
        if name in inventory:
            inventory[name] += quantity
        else:
            inventory[name] = quantity
            
        transactions.append({
            "نوع": "ورود",
            "محصول": name,
            "تعداد": quantity,
            "تاریخ": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        save_data(inventory, transactions)
        print(f"✅ {quantity} عدد {name} به انبار اضافه شد")
        
    except ValueError:
        print("❌ لطفا عدد صحیح وارد کنید")
    except Exception as e:
        print("❌ خطا:", str(e))

def remove_product(inventory, transactions):
    """خروج محصول از انبار"""
    print("\n=== خروج کالا از انبار ===")
    try:
        name = input("نام محصول: ")
        if name not in inventory:
            print("❌ این محصول در انبار موجود نیست")
            return
            
        quantity = int(input("تعداد: "))
        if quantity <= 0:
            print("❌ تعداد باید بیشتر از صفر باشد")
            return
            
        if inventory[name] < quantity:
            print("❌ موجودی کافی نیست")
            return
            
        inventory[name] -= quantity
        if inventory[name] == 0:
            del inventory[name]
            
        transactions.append({
            "نوع": "خروج",
            "محصول": name,
            "تعداد": quantity,
            "تاریخ": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        save_data(inventory, transactions)
        print(f"✅ {quantity} عدد {name} از انبار خارج شد")
        
    except ValueError:
        print("❌ لطفا عدد صحیح وارد کنید")
    except Exception as e:
        print("❌ خطا:", str(e))

def show_inventory(inventory):
    """نمایش موجودی انبار"""
    print("\n=== موجودی انبار ===")
    if not inventory:
        print("انبار خالی است")
        return
        
    print("نام محصول | تعداد")
    print("-" * 30)
    for name, quantity in inventory.items():
        print(f"{name} | {quantity}")
    print("-" * 30)

def show_transactions(transactions):
    """نمایش تراکنش‌های اخیر"""
    print("\n=== تراکنش‌های اخیر ===")
    if not transactions:
        print("تراکنشی موجود نیست")
        return
        
    print("نوع | محصول | تعداد | تاریخ")
    print("-" * 50)
    for t in transactions[-5:]:  # نمایش 5 تراکنش آخر
        print(f"{t['نوع']} | {t['محصول']} | {t['تعداد']} | {t['تاریخ']}")
    print("-" * 50)

def main_menu():
    """منوی اصلی برنامه"""
    inventory, transactions = load_data()
    
    while True:
        print("\n=== سیستم مدیریت انبار ===")
        print("1. ورود کالا")
        print("2. خروج کالا")
        print("3. مشاهده موجودی")
        print("4. مشاهده تراکنش‌ها")
        print("5. خروج")
        
        choice = input("\nلطفا یک گزینه را انتخاب کنید: ")
        
        if choice == "1":
            add_product(inventory, transactions)
        elif choice == "2":
            remove_product(inventory, transactions)
        elif choice == "3":
            show_inventory(inventory)
        elif choice == "4":
            show_transactions(transactions)
        elif choice == "5":
            print("\nخدانگهدار! 👋")
            break
        else:
            print("❌ گزینه نامعتبر")

if __name__ == "__main__":
    main_menu()