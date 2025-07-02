# model.py
import datetime

class NutritionEntry:
    """Represents a single nutrition entry (meal)."""

    def __init__(self, deskripsi: str, jumlah: float, kategori: str,
                 tanggal: datetime.date | str, id_entry: int | None = None):
        self.id = id_entry
        self.deskripsi = str(deskripsi) if deskripsi else "No Description"

        try:
            jumlah_float = float(jumlah)
            self.jumlah = jumlah_float if jumlah_float > 0 else 0.0
            if jumlah_float <= 0:
                print(f"Warning: Amount '{jumlah}' must be positive.")
        except (ValueError, TypeError):
            self.jumlah = 0.0
            print(f"Warning: Amount '{jumlah}' is not valid.")

        self.kategori = str(kategori) if kategori else "Others"

        if isinstance(tanggal, datetime.date):
            self.tanggal = tanggal
        elif isinstance(tanggal, str):
            try:
                self.tanggal = datetime.datetime.strptime(tanggal, "%Y-%m-%d").date()
            except ValueError:
                self.tanggal = datetime.date.today()
                print(f"Warning: Date format '{tanggal}' is incorrect.")
        else:
            self.tanggal = datetime.date.today()
            print(f"Warning: Date type '{type(tanggal)}' is not valid.")

    def __repr__(self) -> str:
        return (
            f"NutritionEntry(ID:{self.id}, Date:{self.tanggal.strftime('%Y-%m-%d')}, "
            f"Amount:{self.jumlah}, Category:'{self.kategori}', Desc:'{self.deskripsi}')"
        )

    def to_dict(self) -> dict:
        return {
            "deskripsi": self.deskripsi,
            "jumlah": self.jumlah,
            "kategori": self.kategori,
            "tanggal": self.tanggal.strftime("%Y-%m-%d")
        }
class UserProfile:
    def __init__(self, name: str, age: int, height: int, 
                 gender: str, weight: float, daily_target: int):
        self.name = name
        self.age = age
        self.height = height
        self.gender = gender
        self.weight = weight
        self.daily_target = daily_target

class UserWeight:
    """Represents a user's weight entry."""

    def __init__(self, weight: float, tanggal: datetime.date | str, id_weight: int | None = None):
        self.id = id_weight
        self.weight = weight

        if isinstance(tanggal, datetime.date):
            self.tanggal = tanggal
        elif isinstance(tanggal, str):
            try:
                self.tanggal = datetime.datetime.strptime(tanggal, "%Y-%m-%d").date()
            except ValueError:
                self.tanggal = datetime.date.today()
                print(f"Warning: Date format '{tanggal}' is incorrect.")
        else:
            self.tanggal = datetime.date.today()
            print(f"Warning: Date type '{type(tanggal)}' is not valid.")

    def __repr__(self) -> str:
        return f"User Weight(ID:{self.id}, Date:{self.tanggal.strftime('%Y-%m-%d')}, Weight:{self.weight})"

    def to_dict(self) -> dict:
        return {
            "weight": self.weight,
            "tanggal": self.tanggal.strftime("%Y-%m-%d")
        }
