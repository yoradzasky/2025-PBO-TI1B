# konfigurasi.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'nutrition_tracker.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

KATEGORI_MAKANAN = [
    "Carbohydrates", "Proteins", "Fats", "Vegetables", "Fruits", "Beverages", "Supplements", "Others"
]

NUTRIENT_KEYS = ['calories', 'carbs', 'protein', 'fat']

