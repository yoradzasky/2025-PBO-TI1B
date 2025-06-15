class Buku:
    def __init__(self, judul, penulis, tahun, jml_halaman):
        self.judul = judul
        self.penulis = penulis
        self.tahun = tahun
        self.jml_halaman = max(0, jml_halaman)  # Pastikan non-negatif

    def __str__(self):
        # Versi singkat untuk kejelasan perbandingan
        return f"'{self.judul}' ({self.tahun})"

    def __repr__(self):
        return (f"Buku(judul='{self.judul}', penulis='{self.penulis}', "
                f"tahun={self.tahun}, jml_halaman={self.jml_halaman})")

    def __len__(self):
        return self.jml_halaman

    # --- Implementasi Perbandingan ---
    # __eq__: Dipanggil saat menggunakan operator ==
    def __eq__(self, other):
        """Membandingkan kesamaan dua objek Buku berdasarkan judul dan penulis."""
        print(f"-> Memanggil __eq__: Membandingkan '{self.judul}' == '{getattr(other, 'judul', '?')}'")
        if isinstance(other, Buku):
            return (self.judul == other.judul) and (self.penulis == other.penulis)
        return NotImplemented

    # __lt__: Dipanggil saat menggunakan operator <
    def __lt__(self, other):
        """Membandingkan objek Buku berdasarkan tahun terbit (lebih kecil dari)."""
        print(f"-> Memanggil __lt__: Membandingkan '{self.judul}' ({self.tahun}) < "
              f"'{getattr(other, 'judul', '?')}' ({getattr(other, 'tahun', '?')})")
        if isinstance(other, Buku):
            return self.tahun < other.tahun
        return NotImplemented


# --- Kode Utama ---
if __name__ == "__main__":
    buku_A = Buku("Sejarah Jawa Kuno", "Prof. X", 1995, 450)
    buku_B = Buku("Teknologi AI", "Dr. Y", 2022, 300)
    buku_C = Buku("Sejarah Jawa Kuno", "Prof. X", 1995, 500)  # Sama judul & penulis dgn A
    buku_D = Buku("Pengantar Python", "Prof. X", 2018, 400)

    print("\n--- Perbandingan Kesamaan (==) ---")
    print(f"'{buku_A.judul}' == '{buku_B.judul}' ? {buku_A == buku_B}")  # False
    print(f"'{buku_A.judul}' == '{buku_C.judul}' ? {buku_A == buku_C}")  # True
    print(f"'{buku_A.judul}' == 'Teks' ? {buku_A == 'Teks'}")            # False

    print("\n--- Perbandingan Kurang Dari (<) ---")
    print(f"{buku_A} < {buku_B} ? {buku_A < buku_B}")  # True
    print(f"{buku_B} < {buku_A} ? {buku_B < buku_A}")  # False
    print(f"{buku_A} < {buku_C} ? {buku_A < buku_C}")  # False
    print(f"{buku_A} < {buku_D} ? {buku_A < buku_D}")  # True

    print("\n--- Perbandingan Lain (Otomatis dari __lt__ dan __eq__) ---")
    print(f"{buku_B} > {buku_A} ? {buku_B > buku_A}")  # True
    print(f"{buku_A} != {buku_B} ? {buku_A != buku_B}")  # True

    print("\n--- Perbandingan dengan Tipe Lain ---")
    try:
        hasil_error = buku_A < 5
        print(f"Hasil buku_A < 5: {hasil_error}")
    except TypeError as e:
        print(f"Error saat membandingkan buku_A < 5: {e}")
