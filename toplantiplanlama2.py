import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk  # Pillow kütüphanesinden gerekli modüller
import json

class ToplantiUygulamasiYeni:
    def __init__(self, master):
        self.master = master
        self.master.title("Yeni Toplanti Uygulamasi")

        # Pencere boyutunu ayarla
        window_width = 800
        window_height = 410
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Arkaplan resmi ekle
        image = Image.open("toplanti.png")
        image = image.resize((window_width, window_height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(image)
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Toplanti olusturma kismi
        self.label_toplanti_kodu = tk.Label(master, text="Toplanti Kodu:", font=("Helvetica", 10, "bold"))
        self.label_isim = tk.Label(master, text="Isim:", font=("Helvetica", 10, "bold"))
        self.label_tarih = tk.Label(master, text="Toplanti Tarihi:", font=("Helvetica", 10, "bold"))
        self.label_aciklama = tk.Label(master, text="Aciklama:", font=("Helvetica", 10, "bold"))

        self.entry_toplanti_kodu = tk.Entry(master)
        self.entry_isim = tk.Entry(master)
        self.entry_tarih = DateEntry(master, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entry_aciklama = tk.Entry(master)

        self.button_toplanti_olustur = tk.Button(master, text="Toplantiyi Olustur", command=self.toplantiyi_olustur, bg="blue", fg="white")

        # Toplantiya katilma kismi
        self.label_katilma_kodu = tk.Label(master, text="Toplanti Kodu:", font=("Helvetica", 10, "bold"))
        self.label_katilma_isim = tk.Label(master, text="Isim:", font=("Helvetica", 10, "bold"))
        self.label_katilma_tarih = tk.Label(master, text="Uygun Tarih:", font=("Helvetica", 10, "bold"))

        self.entry_katilma_kodu = tk.Entry(master)
        self.entry_katilma_isim = tk.Entry(master)
        self.entry_katilma_tarih = DateEntry(master, width=12, background='darkblue', foreground='white', borderwidth=2)

        self.button_toplantiya_katil = tk.Button(master, text="Toplantiya Katil", command=self.toplantiya_katil, bg="blue", fg="white")

        # Listbox kismi
        self.listbox_label = tk.Label(master, text="Toplanti Listesi:", font=("Helvetica", 12, "bold"), underline=True)
        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE, activestyle=tk.NONE, font=("Helvetica", 10), height=10)
        self.listbox.bind("<Double-1>", self.show_full_details_listbox)

        # Layout
        self.label_toplanti_kodu.grid(row=0, column=0, padx=10, pady=10)
        self.label_isim.grid(row=1, column=0, padx=10, pady=10)
        self.label_tarih.grid(row=2, column=0, padx=10, pady=10)
        self.label_aciklama.grid(row=3, column=0, padx=10, pady=10)

        self.entry_toplanti_kodu.grid(row=0, column=1, padx=10, pady=10)
        self.entry_isim.grid(row=1, column=1, padx=10, pady=10)
        self.entry_tarih.grid(row=2, column=1, padx=10, pady=10)
        self.entry_aciklama.grid(row=3, column=1, padx=10, pady=10)

        self.button_toplanti_olustur.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

        self.label_katilma_kodu.grid(row=5, column=0, padx=10, pady=10)
        self.label_katilma_isim.grid(row=6, column=0, padx=10, pady=10)
        self.label_katilma_tarih.grid(row=7, column=0, padx=10, pady=10)

        self.entry_katilma_kodu.grid(row=5, column=1, padx=10, pady=10)
        self.entry_katilma_isim.grid(row=6, column=1, padx=10, pady=10)
        self.entry_katilma_tarih.grid(row=7, column=1, padx=10, pady=10)

        self.button_toplantiya_katil.grid(row=8, column=0, columnspan=2, pady=10, sticky="nsew")

        self.listbox_label.grid(row=0, column=2, padx=10, pady=10, columnspan=2, sticky="w")

        # Genişleme için configure işlemleri
        self.master.rowconfigure(1, weight=1)  # 1. satır (Listbox'ın olduğu satır)
        self.master.columnconfigure(2, weight=1)  # 2. sütun (Listbox'ın olduğu sütun)

        self.listbox.grid(row=1, column=2, padx=10, pady=10, columnspan=2, rowspan=8, sticky="nsew")

        # JSON dosyası için dosya adı
        self.json_filename = "toplanti_verileri.json"

        # Başlangıçta varolan verileri yükle
        self.load_data()

    def toplantiyi_olustur(self):
        toplanti_kodu = self.entry_toplanti_kodu.get()
        isim = self.entry_isim.get()
        tarih = self.entry_tarih.get_date()
        aciklama = self.entry_aciklama.get()

        if toplanti_kodu and isim and tarih and aciklama:
            messagebox.showinfo("Toplanti Oluşturuldu", f"Toplanti Kodu: {toplanti_kodu}\nIsim: {isim}\nTarih: {tarih}\nAciklama: {aciklama}")
            self.listbox.insert(tk.END, f"Toplanti Kodu: {toplanti_kodu}, Isim: {isim}, Tarih: {tarih}, Aciklama: {aciklama}")
            # Verileri JSON dosyasına kaydet
            self.save_data()
        else:
            messagebox.showerror("Hata", "Lütfen tüm bilgileri doldurun!")

    def toplantiya_katil(self):
        toplanti_kodu = self.entry_katilma_kodu.get()
        isim = self.entry_katilma_isim.get()
        uygun_tarih = self.entry_katilma_tarih.get_date()

        found = False
        for i in range(self.listbox.size()):
            existing_toplanti_kodu = self.listbox.get(i).split(", ")[0].split(": ")[1]
            if toplanti_kodu == existing_toplanti_kodu:
                found = True
                break

        if found:
            messagebox.showinfo("Toplantiya Katilma", f"Toplanti Kodu: {toplanti_kodu}, Isim: {isim}, Uygun Tarih: {uygun_tarih}")
            self.listbox.insert(tk.END, f"Toplanti Kodu: {toplanti_kodu}, Katilan: {isim}, Uygun Tarih: {uygun_tarih}")
            # Verileri JSON dosyasına kaydet
            self.save_data()
        else:
            messagebox.showerror("Hata", "Boyle bir toplanti bulunmamaktadir!")

    def show_full_details_listbox(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_item = self.listbox.get(selected_index)
            messagebox.showinfo("Toplanti Detaylari", selected_item)

    def load_data(self):
        try:
            with open(self.json_filename, "r") as file:
                data = json.load(file)
                for values in data:
                    self.listbox.insert(tk.END, ", ".join(values))
        except FileNotFoundError:
            pass  # İlk çalıştırma, dosya henüz oluşturulmamış olabilir

    def save_data(self):
        # Listbox'taki tüm verileri al
        all_data = [self.listbox.get(i) for i in range(self.listbox.size())]

        # Verileri JSON dosyasına kaydet
        with open(self.json_filename, "w") as file:
            json.dump([data.split(", ") for data in all_data], file)

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = ToplantiUygulamasiYeni(root)
    root.mainloop()