# main_app.py (Finalized and Repaired)
import streamlit as st
import datetime
import pandas as pd
from streamlit_option_menu import option_menu
from model import NutritionEntry, UserWeight, UserProfile
from manajer_nutrisi import NutrisiManager
from konfigurasi import KATEGORI_MAKANAN



# Init
nutrisi_manager = NutrisiManager()
st.set_page_config(page_title=" Tugas Besar OOP Nutrition Tracker", layout="wide")

from database import load_user_profile, save_user_profile

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = load_user_profile()



with st.sidebar:
    st.title("🥗 Nutrition Tracker")

    menu = option_menu(
        menu_title="",  # Kosongin biar minimalis
        options=["Dashboard", "Add Meal", "User Profile"],
        icons=["bar-chart", "plus-circle", "person"],  # Bootstrap icons
        default_index=0,
       styles={
    "container": {"padding": "10px", "background-color": "#1e1e2f"},  # Gelap kontras
    "icon": {"color": "#f5f5f5", "font-size": "20px"},  # Ikon putih terang
    "nav-link": {
        "font-size": "16px",
        "text-align": "left",
        "color": "#dcdcdc",  # Teks default terang
        "--hover-color": "#ffb3c6",  # Warna hover soft pink
        "transition": "0.3s ease-in-out",
    },
    "nav-link-selected": {
        "background-color": "#ff4081",  # Pink cerah
        "color": "#ffffff",  # Teks putih
        "box-shadow": "2px 2px 12px rgba(255, 64, 129, 0.3)"  # Glow shadow
    }
}

    )

# User Profile
if menu == "User Profile":
    st.header("User Profile")
    with st.form("profile_form"):
        cols = st.columns(2)
        name = cols[0].text_input("Name", value=st.session_state.user_profile['name'])
        age = cols[1].number_input("Age", min_value=1, max_value=120, value=st.session_state.user_profile['age'])
        height = cols[0].number_input("Height (cm)", min_value=100, max_value=250, value=st.session_state.user_profile['height'])
        weight = cols[1].number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=st.session_state.user_profile['weight'], step=0.1)
        gender = st.selectbox("Gender", ["Male", "Female"], index=0 if st.session_state.user_profile['gender'] == "Male" else 1)
        daily_target = st.number_input("Daily Calorie Target", min_value=500, max_value=5000, value=st.session_state.user_profile['daily_target'])

        if st.form_submit_button("Save Profile"):
            st.session_state.user_profile = {
                'name': name,
                'age': age,
            'height': height,
            'gender': gender,
            'weight': weight,
            'daily_target': daily_target
            }
            save_user_profile(st.session_state.user_profile)
            st.success("Profile updated & saved!")

            today = datetime.date.today()
            weight_entry = UserWeight(weight=weight, tanggal=today)
            if nutrisi_manager.tambah_user_weight(weight_entry):
                st.success("Profile & berat badan disimpan!")
            else:
                st.warning("Profil disimpan, tapi gagal menyimpan berat badan.")

# Add Meal
elif menu == "Add Meal":
    st.header("Add New Meal")
    with st.form("meal_form", clear_on_submit=True):
        cols = st.columns(2)
        description = cols[0].text_input("Description*", placeholder="e.g., Chicken Rice")
        category = cols[1].selectbox("Category*", KATEGORI_MAKANAN)
        calories = st.number_input("Calories*", min_value=1, value=300)
        protein = st.number_input("Protein (g)", min_value=0, value=0)
        carbs = st.number_input("Carbs (g)", min_value=0, value=0)
        fat = st.number_input("Fat (g)", min_value=0, value=0)
        date = st.date_input("Date*", value=datetime.date.today())

        if st.form_submit_button("Save Meal"):
            if not description:
                st.warning("Description is required!")
            else:
                entry = NutritionEntry(deskripsi=description, jumlah=calories, kategori=category, tanggal=date)
                if nutrisi_manager.tambah_nutrition_entry(entry):
                    st.success("Meal saved successfully!")
                else:
                    st.error("Failed to save meal.")

# Dashboard
elif menu == "Dashboard":
    st.header("Nutrition Dashboard")
    today = datetime.date.today()
    target = st.session_state.user_profile['daily_target']

    # Today's Summary
    st.subheader(f"Today's Summary ({today.strftime('%d %b %Y')})")
    daily_summary = nutrisi_manager.calculate_daily_summary(today)
    daily_calories = daily_summary['total_calories'] or 0

    cols = st.columns(2)
    cols[0].metric("Calories Consumed", f"{daily_calories:.2f} kcal", f"{daily_calories - target:.2f} kcal vs target")
    cols[1].progress(min(daily_calories / target, 1.0), text=f"{daily_calories:.0f} / {target} kcal")

    # Weekly Summary
    st.subheader("Weekly Summary")
    start_date = today - datetime.timedelta(days=6)
    weekly_data = nutrisi_manager.get_weekly_nutrition(start_date, today)
    st.dataframe(weekly_data, use_container_width=True)

    # Weight Input Form
    st.subheader("Catat Berat Badan")
    with st.form("form_berat"):
        new_weight = st.number_input("Masukkan berat badan terbaru (kg)", min_value=30.0, max_value=200.0, step=0.1)
        tanggal_berat = st.date_input("Tanggal", value=datetime.date.today())
        if st.form_submit_button("Simpan Berat Badan"):
            weight_entry = UserWeight(weight=new_weight, tanggal=tanggal_berat)
            if nutrisi_manager.tambah_user_weight(weight_entry):
                st.success("Berat badan berhasil disimpan!")
                st.rerun()
            else:
                st.error("Gagal menyimpan berat badan.")

# Weight Trend
st.subheader("Weight Trend")
weight_data = nutrisi_manager.get_weight_history()
if not weight_data.empty:
    weight_data['date'] = pd.to_datetime(weight_data['date'])
    weight_data.sort_values('date', inplace=True)
    st.line_chart(weight_data.set_index('date')['weight'], use_container_width=True)
    st.caption(f"Data terakhir: {weight_data['date'].dt.strftime('%d %b %Y').iloc[-1]}")
else:
    st.warning("Belum ada data berat badan yang tercatat.")

# Reset data berat badan
with st.expander("⚠️ Reset Data Berat Badan", expanded=False):
    st.warning("Fitur ini akan menghapus semua data berat badan secara permanen.")

    konfirmasi = st.radio("Konfirmasi penghapusan:", ["Tidak", "Ya, Hapus Sekarang!"], key="reset_confirm")

    if konfirmasi == "Ya, Hapus Sekarang!":
        if st.button("🔴 KONFIRMASI: Hapus Semua Data"):
            from database import execute_query
            execute_query("DELETE FROM user_weights")
            st.success("✅ Semua data berat badan telah dihapus!")
            st.rerun()


        







