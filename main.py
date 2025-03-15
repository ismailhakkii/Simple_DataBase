import os
import json
import tkinter as tk
from tkinter import ttk, messagebox


class SimpleDB:
    """JSON tabanlı basit veritabanı sınıfı."""

    def __init__(self, db_file='database.json'):
        self.db_file = db_file
        if not os.path.exists(db_file):
            with open(db_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _read_db(self):
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_db(self, data):
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_record(self, record):
        if not isinstance(record, dict):
            raise ValueError("Record must be a dictionary")
        data = self._read_db()
        record['id'] = 1 if not data else data[-1]['id'] + 1
        data.append(record)
        self._write_db(data)
        return record['id']

    def get_all_records(self):
        return self._read_db()

    def get_record_by_id(self, record_id):
        data = self._read_db()
        for record in data:
            if record['id'] == record_id:
                return record
        return None

    def search_records(self, key, value):
        data = self._read_db()
        return [record for record in data if str(record.get(key, '')).lower() == str(value).lower()]

    def update_record(self, record_id, updated_data):
        data = self._read_db()
        for i, record in enumerate(data):
            if record['id'] == record_id:
                updated_data['id'] = record_id
                data[i] = updated_data
                self._write_db(data)
                return True
        return False

    def delete_record(self, record_id):
        data = self._read_db()
        for i, record in enumerate(data):
            if record['id'] == record_id:
                del data[i]
                self._write_db(data)
                return True
        return False


class DatabaseApp:
    """Tkinter tabanlı veritabanı yönetim arayüzü."""

    def __init__(self, root):
        self.root = root
        self.root.title("Simple Database Management")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.db = SimpleDB()
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Ana alanlar: sol panel (işlemler) ve sağ panel (tablo)
        self.left_frame = tk.Frame(self.root, bg="#f0f0f0", width=200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.right_frame = tk.Frame(self.root, bg="#ffffff")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # İşlem butonları
        btn_style = {"width": 20, "padx": 5, "pady": 5}
        tk.Button(self.left_frame, text="Add Record", command=self.add_record, bg="#4CAF50", fg="white",
                  **btn_style).pack(pady=5)
        tk.Button(self.left_frame, text="Edit Record", command=self.edit_record, bg="#2196F3", fg="white",
                  **btn_style).pack(pady=5)
        tk.Button(self.left_frame, text="Delete Record", command=self.delete_record, bg="#F44336", fg="white",
                  **btn_style).pack(pady=5)
        tk.Button(self.left_frame, text="Refresh", command=self.load_data, bg="#9E9E9E", fg="white", **btn_style).pack(
            pady=5)

        # Arama bölümü
        search_frame = tk.LabelFrame(self.left_frame, text="Search", bg="#f0f0f0")
        search_frame.pack(pady=10, fill=tk.X)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(padx=5, pady=5, fill=tk.X)
        tk.Button(search_frame, text="Search by Name", command=self.search_by_name, bg="#FF9800", fg="white").pack(
            pady=5)

        # Tablo (Treeview)
        columns = ("id", "name", "email")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID", command=lambda: self.sort_treeview("id", False))
        self.tree.heading("name", text="Name", command=lambda: self.sort_treeview("name", False))
        self.tree.heading("email", text="Email", command=lambda: self.sort_treeview("email", False))
        self.tree.column("id", width=50)
        self.tree.column("name", width=200)
        self.tree.column("email", width=250)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Çift tıklama ile düzenleme
        self.tree.bind("<Double-1>", lambda event: self.edit_record())

        # Durum çubuğu
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                              bg="#e0e0e0")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_data(self):
        """Veritabanındaki tüm kayıtları tabloya yükler."""
        self.tree.delete(*self.tree.get_children())
        records = self.db.get_all_records()
        for record in records:
            self.tree.insert("", tk.END, values=(record.get("id", ""), record.get("name", ""), record.get("email", "")))
        self.status_var.set(f"{len(records)} record(s) loaded")

    def add_record(self):
        """Yeni kayıt eklemek için dialog penceresi açar."""
        add_win = tk.Toplevel(self.root)
        add_win.title("Add New Record")
        add_win.geometry("300x200")
        add_win.resizable(False, False)
        add_win.grab_set()

        tk.Label(add_win, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Label(add_win, text="Email:").grid(row=1, column=0, padx=10, pady=10, sticky="e")

        name_var = tk.StringVar()
        email_var = tk.StringVar()
        name_entry = tk.Entry(add_win, textvariable=name_var)
        email_entry = tk.Entry(add_win, textvariable=email_var)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        email_entry.grid(row=1, column=1, padx=10, pady=10)
        name_entry.focus()

        def save():
            name = name_var.get().strip()
            email = email_var.get().strip()
            if not name or not email:
                messagebox.showerror("Error", "Name and Email are required!")
                return
            try:
                self.db.add_record({"name": name, "email": email})
                add_win.destroy()
                self.load_data()
                self.status_var.set("Record added successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(add_win, text="Save", command=save, bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=2,
                                                                                     pady=20)

    def edit_record(self):
        """Seçili kaydı düzenlemek için dialog penceresi açar."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to edit")
            return
        record_id = int(self.tree.item(selected[0])['values'][0])
        record = self.db.get_record_by_id(record_id)
        if not record:
            messagebox.showerror("Error", "Record not found")
            return

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Record")
        edit_win.geometry("300x200")
        edit_win.resizable(False, False)
        edit_win.grab_set()

        tk.Label(edit_win, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Label(edit_win, text="Email:").grid(row=1, column=0, padx=10, pady=10, sticky="e")

        name_var = tk.StringVar(value=record.get("name", ""))
        email_var = tk.StringVar(value=record.get("email", ""))
        name_entry = tk.Entry(edit_win, textvariable=name_var)
        email_entry = tk.Entry(edit_win, textvariable=email_var)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        email_entry.grid(row=1, column=1, padx=10, pady=10)

        def update():
            name = name_var.get().strip()
            email = email_var.get().strip()
            if not name or not email:
                messagebox.showerror("Error", "Name and Email are required!")
                return
            if self.db.update_record(record_id, {"name": name, "email": email}):
                edit_win.destroy()
                self.load_data()
                self.status_var.set("Record updated successfully")
            else:
                messagebox.showerror("Error", "Failed to update record")

        tk.Button(edit_win, text="Update", command=update, bg="#2196F3", fg="white").grid(row=2, column=0, columnspan=2,
                                                                                          pady=20)

    def delete_record(self):
        """Seçili kaydı siler."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        record_id = int(self.tree.item(selected[0])['values'][0])
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            if self.db.delete_record(record_id):
                self.load_data()
                self.status_var.set("Record deleted successfully")
            else:
                messagebox.showerror("Error", "Failed to delete record")

    def search_by_name(self):
        """Name alanına göre arama yapar."""
        term = self.search_entry.get().strip()
        if not term:
            self.load_data()
            return
        results = self.db.search_records("name", term)
        self.tree.delete(*self.tree.get_children())
        for record in results:
            self.tree.insert("", tk.END, values=(record.get("id", ""), record.get("name", ""), record.get("email", "")))
        self.status_var.set(f"{len(results)} record(s) found")

    def sort_treeview(self, col, reverse):
        """Treeview sütununa tıklanınca kayıtları sıralar."""
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        # Aynı sütuna sonraki tıklamada ters sıralama yapabilmek için yeniden ayarla
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
