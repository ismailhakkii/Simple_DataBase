import tkinter as tk
from tkinter import messagebox

# Veritabanı dosya işlemleri
def ekle(id, isim, yas):
    # ID'nin benzersizliğini kontrol et
    if id_var_mi(id):
        messagebox.showerror("Hata", "Bu ID zaten mevcut!")
        return
    # Veriyi dosyaya ekle
    with open("veriler.txt", "a") as dosya:
        dosya.write(f"{id},{isim},{yas}\n")
    messagebox.showinfo("Başarılı", "Kayıt eklendi.")
    # Giriş alanlarını temizle
    id_entry.delete(0, tk.END)
    isim_entry.delete(0, tk.END)
    yas_entry.delete(0, tk.END)

def sil(id):
    if not id_var_mi(id):
        messagebox.showerror("Hata", "Bu ID bulunamadı!")
        return
    with open("veriler.txt", "r") as dosya:
        satirlar = dosya.readlines()
    with open("veriler.txt", "w") as dosya:
        for satir in satirlar:
            if not satir.startswith(id + ","):
                dosya.write(satir)
    messagebox.showinfo("Başarılı", "Kayıt silindi.")
    sil_id_entry.delete(0, tk.END)

def ara(kosul_alani, kosul_degeri):
    with open("veriler.txt", "r") as dosya:
        satirlar = dosya.readlines()
    alanlar = ["id", "isim", "yas"]
    kosul_indeksi = alanlar.index(kosul_alani)
    sonuclar = []
    for satir in satirlar:
        degerler = satir.strip().split(",")
        if degerler[kosul_indeksi] == kosul_degeri:
            sonuclar.append(satir.strip())
    return sonuclar

def id_var_mi(id):
    try:
        with open("veriler.txt", "r") as dosya:
            for satir in dosya:
                if satir.startswith(id + ","):
                    return True
        return False
    except FileNotFoundError:
        return False

def tum_verileri_goster():
    try:
        with open("veriler.txt", "r") as dosya:
            veriler = dosya.readlines()
        return veriler
    except FileNotFoundError:
        return ["Veri bulunamadı."]

# Tkinter arayüzü
root = tk.Tk()
root.title("Basit Veritabanı Yönetimi")
root.geometry("600x400")
root.configure(bg="white")

# Veri Ekleme Bölümü
tk.Label(root, text="ID:", bg="white").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="İsim:", bg="white").grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Yaş:", bg="white").grid(row=2, column=0, padx=5, pady=5)

id_entry = tk.Entry(root)
isim_entry = tk.Entry(root)
yas_entry = tk.Entry(root)
id_entry.grid(row=0, column=1, padx=5, pady=5)
isim_entry.grid(row=1, column=1, padx=5, pady=5)
yas_entry.grid(row=2, column=1, padx=5, pady=5)

def ekle_buton():
    id = id_entry.get()
    isim = isim_entry.get()
    yas = yas_entry.get()
    if not id or not isim or not yas:
        messagebox.showerror("Hata", "Tüm alanları doldurun!")
        return
    if not yas.isdigit():
        messagebox.showerror("Hata", "Yaş bir sayı olmalı!")
        return
    ekle(id, isim, yas)

tk.Button(root, text="Ekle", command=ekle_buton).grid(row=3, column=1, pady=10)

# Veri Silme Bölümü
tk.Label(root, text="Silinecek ID:", bg="white").grid(row=4, column=0, padx=5, pady=5)
sil_id_entry = tk.Entry(root)
sil_id_entry.grid(row=4, column=1, padx=5, pady=5)

def sil_buton():
    id = sil_id_entry.get()
    if not id:
        messagebox.showerror("Hata", "ID girin!")
        return
    sil(id)

tk.Button(root, text="Sil", command=sil_buton).grid(row=5, column=1, pady=10)

# Veri Arama Bölümü
tk.Label(root, text="Arama Kriteri (örn: yas:25):", bg="white").grid(row=6, column=0, padx=5, pady=5)
ara_entry = tk.Entry(root)
ara_entry.grid(row=6, column=1, padx=5, pady=5)

def ara_buton():
    kriter = ara_entry.get()
    if ":" not in kriter:
        messagebox.showerror("Hata", "Kriteri 'alan:değer' formatında girin!")
        return
    alan, deger = kriter.split(":")
    if alan not in ["id", "isim", "yas"]:
        messagebox.showerror("Hata", "Geçerli alanlar: id, isim, yas")
        return
    sonuclar = ara(alan, deger)
    sonuc_text.delete(1.0, tk.END)
    if sonuclar:
        for sonuc in sonuclar:
            sonuc_text.insert(tk.END, sonuc + "\n")
    else:
        sonuc_text.insert(tk.END, "Sonuç bulunamadı.\n")

tk.Button(root, text="Ara", command=ara_buton).grid(row=7, column=1, pady=10)

# Tüm Verileri Göster
def tumunu_goster_buton():
    veriler = tum_verileri_goster()
    sonuc_text.delete(1.0, tk.END)
    for veri in veriler:
        sonuc_text.insert(tk.END, veri)

tk.Button(root, text="Tüm Verileri Göster", command=tumunu_goster_buton).grid(row=8, column=1, pady=10)

# Sonuç Alanı
sonuc_text = tk.Text(root, height=10, width=50)
sonuc_text.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Ana döngüyü başlat
root.mainloop()