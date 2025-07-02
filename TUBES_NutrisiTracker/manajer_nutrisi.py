# manajer_nutrisi.py

import datetime
import pandas as pd
from model import NutritionEntry, UserWeight
import database  # Import our database module

class NutrisiManager:
    """Manage the business logic for nutrition entries and user weights."""
    
    def __init__(self):
        if not database.setup_database_initial():  # Ensure DB setup
            print("[NutrisiManager] CRITICAL: Initial database setup FAILED!")

    def tambah_nutrition_entry(self, entry: NutritionEntry) -> bool:
        """Add a new nutrition entry to the database."""
        if not isinstance(entry, NutritionEntry) or entry.jumlah <= 0:
            return False

        sql = "INSERT INTO nutrition_entries (deskripsi, jumlah, kategori, tanggal) VALUES (?, ?, ?, ?)"
        params = (
            entry.deskripsi,
            entry.jumlah,
            entry.kategori,
            entry.tanggal.strftime("%Y-%m-%d")
        )
        last_id = database.execute_query(sql, params)
        if last_id is not None:
            entry.id = last_id
            return True
        return False

    def tambah_user_weight(self, weight: UserWeight) -> bool:
        """Add a new user weight entry to the database."""
        if not isinstance(weight, UserWeight) or weight.weight <= 0:
            return False

        sql = "INSERT INTO user_weights (weight, tanggal) VALUES (?, ?)"
        params = (weight.weight, weight.tanggal.strftime("%Y-%m-%d"))
        last_id = database.execute_query(sql, params)
        if last_id is not None:
            weight.id = last_id
            return True
        return False

    def get_weekly_nutrition(self, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
        """Get weekly nutrition data as DataFrame."""
        query = """
        SELECT tanggal, SUM(jumlah) as calories
        FROM nutrition_entries
        WHERE tanggal BETWEEN ? AND ?
        GROUP BY tanggal
        ORDER BY tanggal
        """
        return database.get_dataframe(query, (start_date, end_date))

    def get_weight_history(self) -> pd.DataFrame:
        """Get weight history as DataFrame"""
        return database.get_dataframe("""
        SELECT 
            tanggal as date, 
            weight 
        FROM user_weights 
        ORDER BY tanggal
        """)

    def get_all_nutrition_entries(self) -> list[NutritionEntry]:
        """Fetch all nutrition entries from the database."""
        sql = "SELECT id, deskripsi, jumlah, kategori, tanggal FROM nutrition_entries ORDER BY tanggal DESC, id DESC"
        rows = database.fetch_query(sql, fetch_all=True)
        entries_list = []
        if rows:
            for row in rows:
                entries_list.append(NutritionEntry(
                    id_entry=row['id'],
                    deskripsi=row['deskripsi'],
                    jumlah=row['jumlah'],
                    kategori=row['kategori'],
                    tanggal=row['tanggal']
                ))
        return entries_list

    def get_all_user_weights(self) -> list[UserWeight]:
        """Fetch all user weight entries from the database."""
        sql = "SELECT id, weight, tanggal FROM user_weights ORDER BY tanggal DESC, id DESC"
        rows = database.fetch_query(sql, fetch_all=True)
        weights_list = []
        if rows:
            for row in rows:
                weights_list.append(UserWeight(
                    id_weight=row['id'],
                    weight=row['weight'],
                    tanggal=row['tanggal']
                ))
        return weights_list

    def calculate_daily_summary(self, date: datetime.date) -> dict:
        """Calculate daily summary of nutrition entries."""
        sql = "SELECT SUM(jumlah) FROM nutrition_entries WHERE tanggal = ?"
        params = (date.strftime("%Y-%m-%d"),)
        result = database.fetch_query(sql, params=params, fetch_all=False)
        total_calories = result[0] if result and result[0] is not None else 0.0
        return {"total_calories": total_calories}

    def calculate_weekly_summary(self, start_date: datetime.date) -> dict:
        """Calculate weekly summary of nutrition entries."""
        end_date = start_date + datetime.timedelta(days=6)
        sql = "SELECT SUM(jumlah) FROM nutrition_entries WHERE tanggal BETWEEN ? AND ?"
        params = (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        result = database.fetch_query(sql, params=params, fetch_all=False)
        total_calories = result[0] if result and result[0] is not None else 0.0
        return {"total_calories": total_calories}

    def calculate_monthly_summary(self, month: int, year: int) -> dict:
        """Calculate monthly summary of nutrition entries."""
        sql = """
        SELECT SUM(jumlah) FROM nutrition_entries 
        WHERE strftime('%m', tanggal) = ? AND strftime('%Y', tanggal) = ?
        """
        params = (f"{month:02}", str(year))
        result = database.fetch_query(sql, params=params, fetch_all=False)
        total_calories = result[0] if result and result[0] is not None else 0.0
        return {"total_calories": total_calories}
    import pandas as pd
import datetime

class NutritionData:

    def get_weekly_nutrition(self, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
        """Get weekly nutrition data as DataFrame"""
        
        # SQL query to get weekly nutrition data
        query = """
        SELECT tanggal, SUM(jumlah) as calories
        FROM nutrition_entries
        WHERE tanggal BETWEEN ? AND ?
        GROUP BY tanggal
        ORDER BY tanggal
        """
        
        # Execute the query and return DataFrame
        return database.get_dataframe(query, (start_date, end_date))



