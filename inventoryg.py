import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from tkinter.font import Font

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("سیستم مدیریت انبار")
        self.root.geometry("800x600")
        
        # تنظیم رنگ‌ها
        self.colors = {
            'primary': '#2563eb',    # آبی
            'secondary': '#f3f4f6',  # خاکستری روشن
            'success': '#22c55e',    # سبز
            'error': '#ef4444',      # قرمز
            'warning': '#f59e0b',    # نارنجی
            'text': '#1f2937',       # متن تیره
            'bg': '#ffffff'          # پس‌زمینه
        }
        
        # تنظیم فونت‌ها
        self.fonts = {
            'header': ('Arial', 16, 'bold'),
            'normal': ('Arial', 12),
            'small': ('Arial', 10)
        }
        
        # بارگذاری داده‌ها
        self.load_data()
        
        # ایجاد رابط کاربری
        self.setup_ui()
        
    def load_data(self):
        """بارگذاری اطلاعات از فایل"""
        try:
            if os.path.exists("inventory.json"):
                with open("inventory.json", 'r', encoding='utf-8') as f:
                    self.inventory = json.load(f)
            else:
                self.inventory = {}
                
            if os.path.exists("transactions.json"):
                with open("transactions.json", 'r', encoding='utf-8') as f:
                    self.transactions = json.load(f)
            else:
                self.transactions = []
        except:
            self.inventory = {}
            self.transactions = []
            
    def save_data(self):
        """ذخیره اطلاعات در فایل"""
        try:
            with open("inventory.json", 'w', encoding='utf-8') as f:
                json.dump(self.inventory, f, ensure_ascii=False, indent=2)
            with open("transactions.json", 'w', encoding='utf-8') as f:
                json.dump(self.transactions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در ذخیره‌سازی: {str(e)}")

    def setup_ui(self):
        """راه‌اندازی رابط کاربری"""
        # ایجاد نوت‌بوک (تب‌ها)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # ایجاد تب‌ها
        self.setup_inventory_tab()
        self.setup_add_tab()
        self.setup_remove_tab()
        self.setup_transactions_tab()
        
        # سفارشی‌سازی استایل
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 10])
        
    def setup_inventory_tab(self):
        """تب موجودی انبار"""
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text='موجودی انبار')
        
        # جدول موجودی
        columns = ('نام کالا', 'تعداد')
        self.inventory_tree = ttk.Treeview(inventory_frame, columns=columns, show='headings')
        
        # تنظیم عنوان ستون‌ها
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=150, anchor='center')
        
        # اسکرول‌بار
        scrollbar = ttk.Scrollbar(inventory_frame, orient='vertical', command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        
        # چیدمان
        self.inventory_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        # دکمه بروزرسانی
        refresh_btn = ttk.Button(inventory_frame, text='بروزرسانی', command=self.refresh_inventory)
        refresh_btn.pack(pady=10)
        
        # نمایش اطلاعات اولیه
        self.refresh_inventory()
        
    def setup_add_tab(self):
        """تب افزودن کالا"""
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text='ورود کالا')
        
        # فرم ورود کالا
        ttk.Label(add_frame, text='نام کالا:', font=self.fonts['normal']).pack(pady=10)
        self.add_name_entry = ttk.Entry(add_frame, font=self.fonts['normal'])
        self.add_name_entry.pack(pady=5)
        
        ttk.Label(add_frame, text='تعداد:', font=self.fonts['normal']).pack(pady=10)
        self.add_quantity_entry = ttk.Entry(add_frame, font=self.fonts['normal'])
        self.add_quantity_entry.pack(pady=5)
        
        ttk.Button(add_frame, text='افزودن کالا', command=self.add_product).pack(pady=20)
        
    def setup_remove_tab(self):
        """تب خروج کالا"""
        remove_frame = ttk.Frame(self.notebook)
        self.notebook.add(remove_frame, text='خروج کالا')
        
        # فرم خروج کالا
        ttk.Label(remove_frame, text='نام کالا:', font=self.fonts['normal']).pack(pady=10)
        self.remove_name_entry = ttk.Entry(remove_frame, font=self.fonts['normal'])
        self.remove_name_entry.pack(pady=5)
        
        ttk.Label(remove_frame, text='تعداد:', font=self.fonts['normal']).pack(pady=10)
        self.remove_quantity_entry = ttk.Entry(remove_frame, font=self.fonts['normal'])
        self.remove_quantity_entry.pack(pady=5)
        
        ttk.Button(remove_frame, text='خروج کالا', command=self.remove_product).pack(pady=20)
        
    def setup_transactions_tab(self):
        """تب تراکنش‌ها"""
        transactions_frame = ttk.Frame(self.notebook)
        self.notebook.add(transactions_frame, text='تراکنش‌ها')
        
        # جدول تراکنش‌ها
        columns = ('نوع', 'نام کالا', 'تعداد', 'تاریخ')
        self.transactions_tree = ttk.Treeview(transactions_frame, columns=columns, show='headings')
        
        # تنظیم عنوان ستون‌ها
        for col in columns:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, width=100, anchor='center')
        
        # اسکرول‌بار
        scrollbar = ttk.Scrollbar(transactions_frame, orient='vertical', command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        
        # چیدمان
        self.transactions_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        # دکمه بروزرسانی
        refresh_btn = ttk.Button(transactions_frame, text='بروزرسانی', command=self.refresh_transactions)
        refresh_btn.pack(pady=10)
        
        # نمایش اطلاعات اولیه
        self.refresh_transactions()
        
    def refresh_inventory(self):
        """بروزرسانی جدول موجودی"""
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
            
        for name, quantity in self.inventory.items():
            self.inventory_tree.insert('', 'end', values=(name, quantity))
            
    def refresh_transactions(self):
        """بروزرسانی جدول تراکنش‌ها"""
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
            
        for t in self.transactions:
            self.transactions_tree.insert('', 0, values=(t['نوع'], t['محصول'], t['تعداد'], t['تاریخ']))
            
    def add_product(self):
        """افزودن کالا به انبار"""
        try:
            name = self.add_name_entry.get().strip()
            quantity = int(self.add_quantity_entry.get().strip())
            
            if not name:
                messagebox.showerror("خطا", "لطفا نام کالا را وارد کنید")
                return
                
            if quantity <= 0:
                messagebox.showerror("خطا", "تعداد باید بیشتر از صفر باشد")
                return
                
            # بروزرسانی موجودی
            if name in self.inventory:
                self.inventory[name] += quantity
            else:
                self.inventory[name] = quantity
                
            # ثبت تراکنش
            self.transactions.append({
                "نوع": "ورود",
                "محصول": name,
                "تعداد": quantity,
                "تاریخ": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # ذخیره و بروزرسانی
            self.save_data()
            self.refresh_inventory()
            self.refresh_transactions()
            
            # پاک کردن فرم
            self.add_name_entry.delete(0, 'end')
            self.add_quantity_entry.delete(0, 'end')
            
            messagebox.showinfo("موفق", f"{quantity} عدد {name} به انبار اضافه شد")
            
        except ValueError:
            messagebox.showerror("خطا", "لطفا تعداد را به صورت عدد صحیح وارد کنید")
        except Exception as e:
            messagebox.showerror("خطا", str(e))
            
    def remove_product(self):
        """خروج کالا از انبار"""
        try:
            name = self.remove_name_entry.get().strip()
            quantity = int(self.remove_quantity_entry.get().strip())
            
            if not name:
                messagebox.showerror("خطا", "لطفا نام کالا را وارد کنید")
                return
                
            if quantity <= 0:
                messagebox.showerror("خطا", "تعداد باید بیشتر از صفر باشد")
                return
                
            if name not in self.inventory:
                messagebox.showerror("خطا", "این کالا در انبار موجود نیست")
                return
                
            if self.inventory[name] < quantity:
                messagebox.showerror("خطا", "موجودی کافی نیست")
                return
                
            # بروزرسانی موجودی
            self.inventory[name] -= quantity
            if self.inventory[name] == 0:
                del self.inventory[name]
                
            # ثبت تراکنش
            self.transactions.append({
                "نوع": "خروج",
                "محصول": name,
                "تعداد": quantity,
                "تاریخ": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # ذخیره و بروزرسانی
            self.save_data()
            self.refresh_inventory()
            self.refresh_transactions()
            
            # پاک کردن فرم
            self.remove_name_entry.delete(0, 'end')
            self.remove_quantity_entry.delete(0, 'end')
            
            messagebox.showinfo("موفق", f"{quantity} عدد {name} از انبار خارج شد")
            
        except ValueError:
            messagebox.showerror("خطا", "لطفا تعداد را به صورت عدد صحیح وارد کنید")
        except Exception as e:
            messagebox.showerror("خطا", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()