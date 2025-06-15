import pandas as pd
import folium
import datetime  # Untuk timestamp log
import time       # Hanya untuk simulasi di kelas jika diperlukan
from abc import ABC, abstractmethod

# --- Definisi Kelas (Salin dari Praktikum 3/4) ---
class Lokasi(ABC):
    def __init__(self, nama: str, latitude: float, longitude: float):
        self.nama = str(nama) if nama else "Tanpa Nama"
        try:
            self.latitude = float(latitude)
            self.longitude = float(longitude)
        except ValueError:
            self.latitude = 0.0
            self.longitude = 0.0

    def get_koordinat(self) -> tuple:
        return (self.latitude, self.longitude)

    @abstractmethod
    def get_info_popup(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}(nama='{self.nama}', lat={self.latitude:.4f}, lon={self.longitude:.4f})"

    def __str__(self) -> str:
        return f"{self.nama} [{type(self).__name__}]"

class TempatWisata(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, jenis: str, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.jenis_wisata = str(jenis) if jenis else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tidak ada deskripsi."

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>{self.jenis_wisata}</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class Kuliner(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, menu_andalan: str):
        super().__init__(nama, latitude, longitude)
        self.menu_andalan = str(menu_andalan) if menu_andalan else "Tidak diketahui"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kuliner</i><br><br>Menu Andalan: {self.menu_andalan}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class TempatIbadah(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, agama: str = "Umum", deskripsi: str = ""):
        super().__init__(nama, latitude, longitude)
        self.agama = str(agama) if agama else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tempat Ibadah"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Tempat Ibadah ({self.agama})</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

# --- Fungsi baca data dan buat objek ---
def baca_data_lokasi(nama_file: str) -> pd.DataFrame | None:
    try:
        dataframe = pd.read_csv(nama_file)
        return dataframe
    except FileNotFoundError:
        print(f"ERROR: File '{nama_file}' tidak ditemukan!")
        return None
    except Exception as e:
        print(f"ERROR saat membaca file CSV: {type(e).__name__} - {e}")
        return None

def buat_objek_lokasi_dari_df(dataframe: pd.DataFrame) -> list:
    list_objek_lokasi = []
    if dataframe is None or dataframe.empty:
        return list_objek_lokasi

    for index, row in dataframe.iterrows():
        nama = row.get('Nama', None)
        lat = row.get('Latitude', None)
        lon = row.get('Longitude', None)
        tipe = row.get('Tipe', 'Lainnya')
        deskripsi = row.get('Deskripsi', '')
        objek = None

        if nama is None or lat is None or lon is None:
            continue

        try:
            if 'Wisata' in tipe or tipe == 'Landmark':
                objek = TempatWisata(nama, lat, lon, tipe, deskripsi)
            elif tipe == 'Kuliner':
                objek = Kuliner(nama, lat, lon, deskripsi)
            elif 'Ibadah' in tipe:
                agama_info = "Umum"
                objek = TempatIbadah(nama, lat, lon, agama_info, deskripsi)

            if objek:
                list_objek_lokasi.append(objek)
        except Exception as e:
            print(f" -> GAGAL membuat objek untuk '{nama}' di baris {index}: {e}")

    return list_objek_lokasi

# --- Fungsi untuk Menulis Log ---
def tulis_log(pesan: str, file_log: str = "proses_peta.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(file_log, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {pesan}\n")
    except IOError as e:
        print(f"ERROR: Gagal menulis ke file log '{file_log}': {e}")

# --- Fungsi buat peta ---
def buat_peta_lokasi_folium(list_objek: list, file_output: str = "peta_lokasi.html"):
    nama_fungsi = "buat_peta_lokasi_folium"
    if not list_objek:
        pesan_log = f"[{nama_fungsi}] Gagal: Tidak ada data lokasi untuk dipetakan."
        print(pesan_log)
        tulis_log(pesan_log)
        return

    print(f"\n[{nama_fungsi}] Memulai pembuatan peta dari {len(list_objek)} lokasi...")
    tulis_log(f"[{nama_fungsi}] Memulai pembuatan peta '{file_output}' dengan {len(list_objek)} lokasi.")

    try:
        lat_tengah = list_objek[0].latitude
        lon_tengah = list_objek[0].longitude
    except IndexError:
        lat_tengah, lon_tengah = -6.9929, 110.4200

    peta = folium.Map(location=[lat_tengah, lon_tengah], zoom_start=12)
    jumlah_marker = 0
    lokasi_dilewati = []

    for lok in list_objek:
        koordinat = lok.get_koordinat()
        if koordinat != (0.0, 0.0):
            info_popup_html = lok.get_info_popup()
            folium.Marker(
                location=koordinat,
                popup=folium.Popup(info_popup_html, max_width=300),
                tooltip=lok.nama
            ).add_to(peta)
            jumlah_marker += 1
        else:
            lokasi_dilewati.append(lok.nama)

    if lokasi_dilewati:
        pesan_lewat = f"[{nama_fungsi}] Melewati marker untuk: {', '.join(lokasi_dilewati)} (koordinat tidak valid)."
        print(f" -> Peringatan: {pesan_lewat}")
        tulis_log(pesan_lewat)

    try:
        peta.save(file_output)
        pesan_sukses = f"[{nama_fungsi}] Peta '{file_output}' berhasil dibuat dengan {jumlah_marker} marker."
        print(f"-> {pesan_sukses}")
        tulis_log(pesan_sukses)
    except Exception as e:
        pesan_error = f"[{nama_fungsi}] ERROR saat menyimpan peta '{file_output}': {type(e).__name__} - {e}"
        print(f"-> {pesan_error}")
        tulis_log(pesan_error)

# --- Kode Utama ---
if __name__ == "__main__":
    NAMA_FILE_CSV = "lokasi_semarang.csv"
    NAMA_FILE_PETA = "peta_interaktif_semarang.html"
    FILE_LOG = "proses_peta.log"

    print("--- Memulai Praktikum 6: File Handling Tambahan (Log) ---")

    # Hapus log lama jika ada (opsional)
    # import os
    # if os.path.exists(FILE_LOG):
    #     os.remove(FILE_LOG)
    #     print(f"File log lama '{FILE_LOG}' dihapus.")

    # 1. Baca data CSV
    df_lokasi = baca_data_lokasi(NAMA_FILE_CSV)

    # 2. Buat list objek dari DataFrame
    list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)

    # 3. Buat peta (yang sekarang juga menulis log)
    buat_peta_lokasi_folium(list_semua_lokasi, NAMA_FILE_PETA)

    # 4. (Opsional) Jalankan lagi untuk melihat log bertambah
    print("\nMenjalankan pembuatan peta lagi untuk demo log append...")
    buat_peta_lokasi_folium(list_semua_lokasi, "peta_kedua.html")

    print(f"\nSilakan periksa isi file log '{FILE_LOG}' untuk melihat catatan proses.")
    print("\n--- Praktikum 6 Selesai ---")