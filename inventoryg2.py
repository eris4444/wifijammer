import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import threading
import time
import pandas as pd

class AutoHideMessage:
    def __init__(self, x, y, message, parent, duration=3):
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)
        
        # Style the message window
        self.window.configure(bg='#2563eb')
        padding = 20
        
        # Create message label
        self.label = tk.Label(
            self.window,
            text=message,
            font=('Arial', 12),
            bg='#2563eb',
            fg='white',
            padx=padding,
            pady=padding
        )
        self.label.pack()
        
        # Position the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        self.window.geometry(f"+{x-width//2}+{y}")
        
        # Add rounded corners and shadow effect
        self.window.lift()
        self.window.attributes('-topmost', True)
        
        # Start auto-hide timer
        self.window.after(duration * 1000, self.hide)
        
        # Fade in effect
        self.window.attributes('-alpha', 0)
        self.fade_in()
        
    def fade_in(self):
        alpha = self.window.attributes('-alpha')
        if alpha < 1:
            alpha += 0.1
            self.window.attributes('-alpha', alpha)
            self.window.after(20, self.fade_in)
            
    def fade_out(self):
        alpha = self.window.attributes('-alpha')
        if alpha > 0:
            alpha -= 0.1
            self.window.attributes('-alpha', alpha)
            self.window.after(20, self.fade_out)
        else:
            self.window.destroy()
            
    def hide(self):
        self.fade_out()

class QuantityDialog:
    def __init__(self, parent, title, initial_value=0, callback=None):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.callback = callback
        
        # Set dialog style
        self.dialog.configure(bg='white')
        self.dialog.geometry('300x200')
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create widgets
        style = ttk.Style()
        style.configure('Dialog.TLabel', font=('Arial', 12))
        style.configure('Dialog.TButton', font=('Arial', 11))
        
        # Quantity adjustment frame
        adjust_frame = ttk.Frame(self.dialog)
        adjust_frame.pack(pady=20)
        
        # Decrease button
        self.dec_btn = ttk.Button(adjust_frame, text='-', command=self.decrease, style='Dialog.TButton')
        self.dec_btn.pack(side='left', padx=5)
        
        # Quantity entry
        self.quantity = tk.StringVar(value=str(initial_value))
        self.entry = ttk.Entry(adjust_frame, textvariable=self.quantity, width=8, font=('Arial', 12))
        self.entry.pack(side='left', padx=10)
        
        # Increase button
        self.inc_btn = ttk.Button(adjust_frame, text='+', command=self.increase, style='Dialog.TButton')
        self.inc_btn.pack(side='left', padx=5)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=20)
        
        # OK and Cancel buttons
        ttk.Button(btn_frame, text='OK', command=self.ok_clicked, style='Dialog.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Cancel', command=self.cancel_clicked, style='Dialog.TButton').pack(side='left', padx=5)
        
    def decrease(self):
        try:
            current = int(self.quantity.get())
            if current > 0:
                self.quantity.set(str(current - 1))
        except ValueError:
            self.quantity.set('0')
            
    def increase(self):
        try:
            current = int(self.quantity.get())
            self.quantity.set(str(current + 1))
        except ValueError:
            self.quantity.set('0')
            
    def ok_clicked(self):
        try:
            quantity = int(self.quantity.get())
            if self.callback:
                self.callback(quantity)
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid number')
            
    def cancel_clicked(self):
        self.dialog.destroy()

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1000x700")
        
        # Set theme colors
        self.colors = {
            'primary': '#2563eb',    # Blue
            'secondary': '#f3f4f6',  # Light Gray
            'success': '#22c55e',    # Green
            'error': '#ef4444',      # Red
            'warning': '#f59e0b',    # Orange
            'text': '#1f2937',       # Dark Text
            'bg': '#ffffff'          # Background
        }
        
        # Configure styles
        self.setup_styles()
        
        # Load Data
        self.load_data()
        
        # Create UI
        self.setup_ui()
        
    def setup_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        
        # Configure main theme
        style.configure('.',
            font=('Arial', 12),
            background=self.colors['bg']
        )
        
        # Notebook style
        style.configure('TNotebook',
            background=self.colors['bg'],
            tabmargins=[2, 5, 2, 0]
        )
        
        style.configure('TNotebook.Tab',
            padding=[20, 10],
            font=('Arial', 11)
        )
        
        # Treeview style
        style.configure('Treeview',
            background=self.colors['secondary'],
            fieldbackground=self.colors['bg'],
            rowheight=30
        )
        
        style.configure('Treeview.Heading',
            font=('Arial', 11, 'bold'),
            padding=5
        )
        
        # Button style
        style.configure('TButton',
            padding=10,
            font=('Arial', 11)
        )
        
    def show_message(self, message):
        """Show auto-hiding message"""
        # Get the root window position and dimensions
        x = self.root.winfo_x() + self.root.winfo_width()//2
        y = self.root.winfo_y() + 50
        AutoHideMessage(x, y, message, self.root)
        
    def setup_ui(self):
        """Setup user interface"""
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(expand=True, fill='both')
        
        # Create tabs
        self.setup_inventory_tab()
        self.setup_add_tab()
        self.setup_transactions_tab()
        
    def setup_inventory_tab(self):
        """Inventory tab with enhanced interaction and export"""
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text='Current Stock')
        
        # Top frame for search and export
        top_frame = ttk.Frame(inventory_frame)
        top_frame.pack(fill='x', padx=5, pady=5)
        
        # Search frame (left side)
        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side='left', fill='x', expand=True)
        
        ttk.Label(search_frame, text='Search:').pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_inventory)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side='left', padx=5)
        
        # Export button (right side)
        export_btn = ttk.Button(
            top_frame,
            text='Export to Excel',
            command=lambda: self.export_to_excel('inventory'),
            style='TButton'
        )
        export_btn.pack(side='right', padx=5)
        
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
        
        # Bind right-click menu
        self.inventory_tree.bind('<Button-3>', self.show_item_menu)
        self.inventory_tree.bind('<Double-1>', self.edit_item)
        
        # Create right-click menu
        self.item_menu = tk.Menu(self.root, tearoff=0)
        self.item_menu.add_command(label='Edit Quantity', command=self.edit_selected_item)
        self.item_menu.add_command(label='Remove Item', command=self.remove_selected_item)
        
        # Show initial data
        self.refresh_inventory()
        

    def filter_inventory(self, *args):
        """Filter inventory items based on search"""
        search_term = self.search_var.get().lower()
        self.refresh_inventory(search_term)
        
    def show_item_menu(self, event):
        """Show right-click menu for inventory items"""
        item = self.inventory_tree.identify_row(event.y)
        if item:
            self.inventory_tree.selection_set(item)
            self.item_menu.post(event.x_root, event.y_root)
            
    def edit_item(self, event):
        """Handle double-click on inventory item"""
        item = self.inventory_tree.selection()[0]
        self.edit_item_quantity(item)
        
    def edit_selected_item(self):
        """Edit quantity of selected item"""
        selected = self.inventory_tree.selection()
        if selected:
            self.edit_item_quantity(selected[0])
            
    def edit_item_quantity(self, item):
        """Show dialog to edit item quantity"""
        name = self.inventory_tree.item(item)['values'][0]
        current_quantity = self.inventory[name]
        
        def update_quantity(new_quantity):
            if new_quantity >= 0:
                self.inventory[name] = new_quantity
                if new_quantity == 0:
                    del self.inventory[name]
                
                self.transactions.append({
                    "Type": "UPDATE",
                    "Product": name,
                    "Quantity": new_quantity,
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                self.save_data()
                self.refresh_inventory()
                self.refresh_transactions()
                self.show_message(f"Updated quantity of {name} to {new_quantity}")
            else:
                messagebox.showerror("Error", "Quantity cannot be negative")
        
        QuantityDialog(self.root, f"Edit Quantity: {name}", current_quantity, update_quantity)
        
    def remove_selected_item(self):
        """Remove selected item from inventory"""
        selected = self.inventory_tree.selection()
        if selected:
            item = selected[0]
            name = self.inventory_tree.item(item)['values'][0]
            
            if messagebox.askyesno("Confirm", f"Remove {name} from inventory?"):
                quantity = self.inventory[name]
                del self.inventory[name]
                
                self.transactions.append({
                    "Type": "REMOVE",
                    "Product": name,
                    "Quantity": quantity,
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                self.save_data()
                self.refresh_inventory()
                self.refresh_transactions()
                self.show_message(f"Removed {name} from inventory")

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

    def setup_add_tab(self):
        """Add product tab"""
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text='Add Product')
        
        # Add product form
        ttk.Label(add_frame, text='Product Name:', style='TLabel').pack(pady=10)
        self.add_name_entry = ttk.Entry(add_frame, style='TEntry')
        self.add_name_entry.pack(pady=5)
        
        ttk.Label(add_frame, text='Quantity:', style='TLabel').pack(pady=10)
        self.add_quantity_entry = ttk.Entry(add_frame, style='TEntry')
        self.add_quantity_entry.pack(pady=5)
        
        ttk.Button(add_frame, text='Add Product', command=self.add_product, style='TButton').pack(pady=20)
        
    def setup_remove_tab(self):
        """Remove product tab"""
        remove_frame = ttk.Frame(self.notebook)
        self.notebook.add(remove_frame, text='Remove Product')
        
        # Remove product form
        ttk.Label(remove_frame, text='Product Name:', style='TLabel').pack(pady=10)
        self.remove_name_entry = ttk.Entry(remove_frame, style='TEntry')
        self.remove_name_entry.pack(pady=5)
        
        ttk.Label(remove_frame, text='Quantity:', style='TLabel').pack(pady=10)
        self.remove_quantity_entry = ttk.Entry(remove_frame, style='TEntry')
        self.remove_quantity_entry.pack(pady=5)
        
        ttk.Button(remove_frame, text='Remove Product', command=self.remove_product, style='TButton').pack(pady=20)
        
    def setup_transactions_tab(self):
        """Transactions tab with export functionality"""
        transactions_frame = ttk.Frame(self.notebook)
        self.notebook.add(transactions_frame, text='Transactions')
        
        # Add export button at top
        export_frame = ttk.Frame(transactions_frame)
        export_frame.pack(fill='x', padx=5, pady=5)
        
        export_btn = ttk.Button(
            export_frame,
            text='Export to Excel',
            command=lambda: self.export_to_excel('transactions'),
            style='TButton'
        )
        export_btn.pack(side='right', padx=5)
        
        # Transactions table
        columns = ('Type', 'Product', 'Quantity', 'Date')
        self.transactions_tree = ttk.Treeview(transactions_frame, columns=columns, show='headings', style='Treeview')
        
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
        refresh_btn = ttk.Button(transactions_frame, text='Refresh', command=self.refresh_transactions, style='TButton')
        refresh_btn.pack(pady=10)
        
        # Show initial data
        self.refresh_transactions()
        
    def refresh_inventory(self, search_term=""):
        """Refresh inventory table"""
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
            
        for name, quantity in self.inventory.items():
            if search_term in name.lower():
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
            
            # Show auto-hiding message instead of messagebox
            self.show_message(f"Added {quantity} units of {name}")
            
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
            
            self.show_message(f"Removed {quantity} units of {name}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for quantity")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_to_excel(self, export_type):
        """Export data to Excel file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if export_type == 'inventory':
                # Create DataFrame for inventory
                data = []
                for name, quantity in self.inventory.items():
                    data.append({
                        'Product Name': name,
                        'Quantity': quantity
                    })
                df = pd.DataFrame(data)
                filename = f'inventory_export_{timestamp}.xlsx'
                
                # Create Excel writer with styling
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Inventory')
                    
                    # Get the workbook and the worksheet
                    workbook = writer.book
                    worksheet = writer.sheets['Inventory']
                    
                    # Add header styling
                    header_format = {
                        'font': {'bold': True, 'color': 'FFFFFF'},
                        'fill': {'fgColor': '2563EB'},
                        'border': {'style': 'thin'},
                        'alignment': {'horizontal': 'center'}
                    }
                    
                    # Apply header formatting
                    for col in range(len(df.columns)):
                        cell = worksheet.cell(row=1, column=col+1)
                        cell.font = workbook.create_font(bold=True, color='FFFFFF')
                        cell.fill = workbook.create_patternfill(
                            start_color='2563EB',
                            end_color='2563EB',
                            fill_type='solid'
                        )
                        cell.border = workbook.create_border(style='thin')
                        cell.alignment = workbook.create_alignment(horizontal='center')
                    
                    # Adjust column widths
                    for column in worksheet.columns:
                        max_length = 0
                        column = [cell for cell in column]
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = (max_length + 2)
                        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
                
            else:  # transactions export
                # Create DataFrame for transactions
                df = pd.DataFrame(self.transactions)
                filename = f'transactions_export_{timestamp}.xlsx'
                
                # Create Excel writer with styling
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Transactions')
                    
                    # Get the workbook and the worksheet
                    workbook = writer.book
                    worksheet = writer.sheets['Transactions']
                    
                    # Add header styling
                    for col in range(len(df.columns)):
                        cell = worksheet.cell(row=1, column=col+1)
                        cell.font = workbook.create_font(bold=True, color='FFFFFF')
                        cell.fill = workbook.create_patternfill(
                            start_color='2563EB',
                            end_color='2563EB',
                            fill_type='solid'
                        )
                        cell.border = workbook.create_border(style='thin')
                        cell.alignment = workbook.create_alignment(horizontal='center')
                    
                    # Adjust column widths
                    for column in worksheet.columns:
                        max_length = 0
                        column = [cell for cell in column]
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = (max_length + 2)
                        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            
            # Show success message
            self.show_message(f"Successfully exported to {filename}")
            
            # Open the containing folder
            os.startfile(os.path.dirname(os.path.abspath(filename)))
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting to Excel: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()