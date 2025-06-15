# --- Fungsi baca data (Salin dari Praktikum 2) ---
def baca_data_lokasi(nama_file: str) -> pd.DataFrame | None:
    # print(f"Mencoba membaca file CSV: {nama_file}")  # Kurangi verbosity
    try:
        dataframe = pd.read_csv(nama_file)
        return dataframe
    except FileNotFoundError:
        print(f"ERROR: File '{nama_file}' tidak ditemukan!")
        return None
    except Exception as e:
        print(f"ERROR saat membaca file CSV: {type(e).__name__} - {e}")
        return None

# --- Fungsi Inti Praktikum Ini ---
def buat_objek_lokasi_dari_df(dataframe: pd.DataFrame) -> list:
    """
    Mengiterasi DataFrame Pandas dan membuat list berisi objek-objek
    Lokasi (atau turunannya) berdasarkan data di setiap baris.

    Args:
        dataframe (pd.DataFrame): DataFrame yang berisi data lokasi
        dengan kolom 'Nama', 'Latitude', 'Longitude', 'Tipe', 'Deskripsi'.

    Returns:
        list: List berisi instance objek Lokasi atau turunannya.
    """
    list_objek_lokasi = []

    if dataframe is None or dataframe.empty:
        print("DataFrame kosong atau None, tidak ada objek dibuat.")
        return list_objek_lokasi

    print("\nMembuat objek dari DataFrame...")
    for index, row in dataframe.iterrows():
        nama = row.get('Nama', None)
        lat = row.get('Latitude', None)
        lon = row.get('Longitude', None)
        tipe = row.get('Tipe', 'Lainnya')
        deskripsi = row.get('Deskripsi', '')

        objek = None
        if nama is None or lat is None or lon is None:
            print(f"  -> Melewati baris {index}: Data Nama/Latitude/Longitude tidak lengkap.")
            continue

        try:
            if 'Wisata' in tipe or tipe == 'Landmark':
                objek = TempatWisata(nama, lat, lon, tipe, deskripsi)
            elif tipe == 'Kuliner':
                objek = Kuliner(nama, lat, lon, deskripsi)
            elif 'Ibadah' in tipe:
                agama_info = "Umum"
                if "Islam" in tipe:
                    agama_info = "Islam"
                elif "Kristen" in tipe:
                    agama_info = "Kristen"
                elif "Klenteng" in tipe:
                    agama_info = "Tridharma"
                objek = TempatIbadah(nama, lat, lon, agama_info, deskripsi)
            else:
                print(f" -> Peringatan: Tipe '{tipe}' untuk '{nama}' tidak dikenali. Tidak membuat objek spesifik.")

            if objek:
                list_objek_lokasi.append(objek)
                # print(f" -> Objek {type(objek).__name__} untuk '{nama}' dibuat.")
        except Exception as e:
            print(f" -> GAGAL membuat objek untuk '{nama}' di baris {index}: {e}")

    print(f"Total {len(list_objek_lokasi)} objek lokasi berhasil dibuat dari {len(dataframe)} baris data.")
    return list_objek_lokasi

# --- Kode Utama ---
if __name__ == "__main__":
    NAMA_FILE_CSV = "lokasi_semarang.csv"

    print("--- Memulai Praktikum 4: Membuat Objek dari Data Pandas ---")

    # 1. Baca data CSV
    df_lokasi = baca_data_lokasi(NAMA_FILE_CSV)

    # 2. Buat list objek dari DataFrame
    list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)

    # 3. Tampilkan hasil (representasi objek)
    print("\n--- Daftar Objek Lokasi yang Berhasil Dibuat ---")
    if list_semua_lokasi:
        for idx, lok in enumerate(list_semua_lokasi):
            print(f"{idx + 1}. {repr(lok)}")
    else:
        print("Tidak ada objek lokasi yang dibuat.")

    print("\n--- Praktikum 4 Selesai ---")
