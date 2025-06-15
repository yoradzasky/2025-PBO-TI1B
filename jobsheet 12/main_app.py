# Jalankan jika belum ada folium dan pandas
# !pip install folium pandas

import pandas as pd
import folium
from abc import ABC, abstractmethod

from peta_log import tulis_log

# --- Definisi Kelas ---
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
  
class Kantor(Lokasi):
    def __init__(self, nama, latitude, longitude, deskripsi=""):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = deskripsi or "Instansi Pemerintahan"
    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kantor Pemerintahan</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class Museum(Lokasi):
    def __init__(self, nama, latitude, longitude, deskripsi=""):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = deskripsi or "Museum"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Museum</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class TamanKota(Lokasi):
    def __init__(self, nama, latitude, longitude, deskripsi=""):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = deskripsi or "Taman Publik"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Taman Kota</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"


# --- Fungsi Baca Data ---
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

# --- Fungsi Buat Objek Lokasi ---
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
                objek = TempatIbadah(nama, lat, lon, 'Umum', deskripsi)
            elif 'Kantor' in tipe:
                objek = Kantor(nama, lat, lon, deskripsi)
            elif 'Museum' in tipe:
                objek = Museum(nama, lat, lon, deskripsi)
            elif 'Taman' in tipe:
                objek = TamanKota(nama, lat, lon, deskripsi)

            if objek:
                list_objek_lokasi.append(objek)
        except Exception as e:
            print(f" -> GAGAL membuat objek untuk '{nama}' di baris {index}: {e}")

    return list_objek_lokasi

# --- Fungsi Buat Peta ---
def buat_peta_lokasi_folium(list_objek: list, file_output: str = "peta_lokasi.html"):
    """
    Membuat peta Folium dengan konfigurasi dari file, menambahkan marker per tipe lokasi, dan menyimpan ke HTML.
    """
    nama_fungsi = "buat_peta_lokasi_folium"

    if not list_objek:
        pesan_log = f"[{nama_fungsi}] Gagal: Tidak ada data lokasi untuk dipetakan."
        print(pesan_log)
        tulis_log(pesan_log)
        return

    # Default konfigurasi
    lat_tengah, lon_tengah, zoom = -6.9929, 110.4200, 12

    # Membaca konfigurasi dari config_peta.txt
    try:
        with open("config_peta.txt", "r", encoding="utf-8") as f:
            baris = [line.strip() for line in f.readlines()]
            lat_tengah = float(baris[0])
            lon_tengah = float(baris[1])
            zoom = int(baris[2])
    except (FileNotFoundError, ValueError, IndexError) as e:
        print(f"[{nama_fungsi}] Gagal membaca config. Gunakan nilai default.")
        tulis_log(f"[{nama_fungsi}] Gagal membaca konfigurasi peta: {type(e).__name__} - {e}")

    print(f"\n[{nama_fungsi}] Memulai pembuatan peta dari {len(list_objek)} lokasi...")
    tulis_log(f"[{nama_fungsi}] Memulai pembuatan peta '{file_output}' dengan {len(list_objek)} lokasi.")

    peta = folium.Map(location=[lat_tengah, lon_tengah], zoom_start=zoom)

    jumlah_marker = 0
    lokasi_dilewati = []

    for lok in list_objek:
        koordinat = lok.get_koordinat()
        if koordinat != (0.0, 0.0):
            info_popup_html = lok.get_info_popup()
            
            # Kustomisasi ikon
            if isinstance(lok, TempatWisata):
                ikon = folium.Icon(color="blue", icon="info-sign")
            elif isinstance(lok, Kuliner):
                ikon = folium.Icon(color="red", icon="cutlery")
            elif isinstance(lok, Kantor):
                ikon = folium.Icon(color="gray", icon="briefcase")
            elif isinstance(lok, Museum):
                ikon = folium.Icon(color="purple", icon="book")
            elif isinstance(lok, TamanKota):
                ikon = folium.Icon(color="green", icon="leaf")
            elif isinstance(lok, TempatIbadah):
                ikon = folium.Icon(color="darkpurple", icon="star")

            folium.Marker(
                location=koordinat,
                popup=folium.Popup(info_popup_html, max_width=300),
                tooltip=lok.nama,
                icon=ikon
            ).add_to(peta)

            jumlah_marker += 1
        else:
            lokasi_dilewati.append(lok.nama)

    if lokasi_dilewati:
        pesan_lewat = f"[{nama_fungsi}] Melewati marker untuk: {', '.join(lokasi_dilewati)} (koordinat tidak valid)."
        print(f" -> Peringatan: {pesan_lewat}")
        tulis_log(pesan_lewat)

    # Simpan peta
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

    print("--- Memulai Praktikum 5: Visualisasi Peta dengan Folium ---")

    # 1. Baca data CSV
    df_lokasi = baca_data_lokasi(NAMA_FILE_CSV)

    # 2. Buat list objek dari DataFrame
    list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)

    # 3. Buat peta dari list objek
    buat_peta_lokasi_folium(list_semua_lokasi, NAMA_FILE_PETA)
  
    print(f"\nSilakan buka file '{NAMA_FILE_PETA}' di browser Anda untuk melihat hasilnya.")
    print("\n--- Praktikum 5 Selesai ---")