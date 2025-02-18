import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from tkinter.font import Font

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")
        
        # Colors
        self.colors = {
            'primary': '#2563eb',    # Blue
            'secondary': '#f3f4f6',  # Light Gray
            'success': '#22c55e',    # Green
            'error': '#ef4444',      # Red
            'warning': '#f59e0b',    # Orange
            'text': '#1f2937',       # Dark Text
            'bg': '#ffffff'          # Background
        }
        
        # Fonts
        self.fonts = {
            'header': ('Arial', 16, 'bold'),
            'normal': ('Arial', 12),
            'small': ('Arial', 10)
        }
        
        # Load Data
        self.load_data()
        
        # Create UI
        self.setup_ui()
        
    def load_data(self):
        """Load data from files"""
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
        """Save data to files"""
        try:
            with open("inventory.json", 'w', encoding='utf-8') as f:
                json.dump(self.inventory, f, ensure_ascii=False, indent=2)
            with open("transactions.json", 'w', encoding='utf-8') as f:
                json.dump(self.transactions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")

    def setup_ui(self):
        """Setup user interface"""
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create tabs
        self.setup_inventory_tab()
        self.setup_add_tab()
        self.setup_remove_tab()
        self.setup_transactions_tab()
        
        # Custom style
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 10])
        
    def setup_inventory_tab(self):
        """Inventory tab"""
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text='Current Stock')
        
        # Inventory table
        columns = ('Product Name', 'Quantity')
        self.inventory_tree = ttk.Treeview(inventory_frame, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=150, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(inventory_frame, orient='vertical', command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.inventory_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        # Refresh button
        refresh_btn = ttk.Button(inventory_frame, text='Refresh', command=self.refresh_inventory)
        refresh_btn.pack(pady=10)
        
        # Show initial data
        self.refresh_inventory()
        
    def setup_add_tab(self):
        """Add product tab"""
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text='Add Product')
        
        # Add product form
        ttk.Label(add_frame, text='Product Name:', font=self.fonts['normal']).pack(pady=10)
        self.add_name_entry = ttk.Entry(add_frame, font=self.fonts['normal'])
        self.add_name_entry.pack(pady=5)
        
        ttk.Label(add_frame, text='Quantity:', font=self.fonts['normal']).pack(pady=10)
        self.add_quantity_entry = ttk.Entry(add_frame, font=self.fonts['normal'])
        self.add_quantity_entry.pack(pady=5)
        
        ttk.Button(add_frame, text='Add Product', command=self.add_product).pack(pady=20)
        
    def setup_remove_tab(self):
        """Remove product tab"""
        remove_frame = ttk.Frame(self.notebook)
        self.notebook.add(remove_frame, text='Remove Product')
        
        # Remove product form
        ttk.Label(remove_frame, text='Product Name:', font=self.fonts['normal']).pack(pady=10)
        self.remove_name_entry = ttk.Entry(remove_frame, font=self.fonts['normal'])
        self.remove_name_entry.pack(pady=5)
        
        ttk.Label(remove_frame, text='Quantity:', font=self.fonts['normal']).pack(pady=10)
        self.remove_quantity_entry = ttk.Entry(remove_frame, font=self.fonts['normal'])
        self.remove_quantity_entry.pack(pady=5)
        
        ttk.Button(remove_frame, text='Remove Product', command=self.remove_product).pack(pady=20)
        
    def setup_transactions_tab(self):
        """Transactions tab"""
        transactions_frame = ttk.Frame(self.notebook)
        self.notebook.add(transactions_frame, text='Transactions')
        
        # Transactions table
        columns = ('Type', 'Product', 'Quantity', 'Date')
        self.transactions_tree = ttk.Treeview(transactions_frame, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(transactions_frame, orient='vertical', command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.transactions_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        # Refresh button
        refresh_btn = ttk.Button(transactions_frame, text='Refresh', command=self.refresh_transactions)
        refresh_btn.pack(pady=10)
        
        # Show initial data
        self.refresh_transactions()
        
    def refresh_inventory(self):
        """Refresh inventory table"""
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
            
        for name, quantity in self.inventory.items():
            self.inventory_tree.insert('', 'end', values=(name, quantity))
            
    def refresh_transactions(self):
        """Refresh transactions table"""
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
            
        for t in self.transactions:
            self.transactions_tree.insert('', 0, values=(
                t['Type'],
                t['Product'],
                t['Quantity'],
                t['Date']
            ))
            
    def add_product(self):
        """Add product to inventory"""
        try:
            name = self.add_name_entry.get().strip()
            quantity = int(self.add_quantity_entry.get().strip())
            
            if not name:
                messagebox.showerror("Error", "Please enter product name")
                return
                
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than zero")
                return
                
            # Update inventory
            if name in self.inventory:
                self.inventory[name] += quantity
            else:
                self.inventory[name] = quantity
                
            # Record transaction
            self.transactions.append({
                "Type": "IN",
                "Product": name,
                "Quantity": quantity,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Save and refresh
            self.save_data()
            self.refresh_inventory()
            self.refresh_transactions()
            
            # Clear form
            self.add_name_entry.delete(0, 'end')
            self.add_quantity_entry.delete(0, 'end')
            
            messagebox.showinfo("Success", f"Added {quantity} units of {name}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for quantity")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def remove_product(self):
        """Remove product from inventory"""
        try:
            name = self.remove_name_entry.get().strip()
            quantity = int(self.remove_quantity_entry.get().strip())
            
            if not name:
                messagebox.showerror("Error", "Please enter product name")
                return
                
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than zero")
                return
                
            if name not in self.inventory:
                messagebox.showerror("Error", "Product not found in inventory")
                return
                
            if self.inventory[name] < quantity:
                messagebox.showerror("Error", "Insufficient stock")
                return
                
            # Update inventory
            self.inventory[name] -= quantity
            if self.inventory[name] == 0:
                del self.inventory[name]
                
            # Record transaction
            self.transactions.append({
                "Type": "OUT",
                "Product": name,
                "Quantity": quantity,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Save and refresh
            self.save_data()
            self.refresh_inventory()
            self.refresh_transactions()
            
            # Clear form
            self.remove_name_entry.delete(0, 'end')
            self.remove_quantity_entry.delete(0, 'end')
            
            messagebox.showinfo("Success", f"Removed {quantity} units of {name}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for quantity")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()