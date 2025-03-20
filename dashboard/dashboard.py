import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import matplotlib.patches as mpatches
sns.set(style='dark')
import os

# Load Data
# Dapatkan path absolut dari folder tempat dashboard.py berada
base_path = os.path.dirname(__file__)
# Gabungkan dengan nama file
main_data_path = os.path.join(base_path, "..", "dashboard", "main_data.csv")
# Baca file CSV
air_quality = pd.read_csv(main_data_path)

# Sidebar Menu
st.sidebar.title("Dashboard Kualitas Udara di Kota Changping dan Dingling")
menu = st.sidebar.radio(
    "Pilih Halaman",
    ["Data", "Visualisasi polutan", "Kualitas Udara", "Polutan Tertinggi"]
)

# Halaman Data 
if menu == "Data":
    st.title("Data Air Quality Kota Changping Dan Dingling")

    # Membuat filter tahun 
    tahun_tersedia = sorted(air_quality["year"].unique()) 
    tahun_dipilih = st.selectbox("Pilih Tahun:", tahun_tersedia, index=len(tahun_tersedia)-1)
    state_tersedia = sorted(air_quality["station"].unique()) 
    state_dipilih = st.selectbox("Pilih station:", state_tersedia, index=len(state_tersedia)-1) 

    # Filter dataset berdasarkan tahun dan station yang dipilih
    data_filtered = air_quality[
        (air_quality["year"] == tahun_dipilih) &
        (air_quality["station"] == state_dipilih)
    ]    
    
    # Menampilkan jumlah data yang difilter
    st.write(f"Menampilkan data untuk tahun **{tahun_dipilih}**. Jumlah data: **{len(data_filtered)}**. Pada station: **{state_dipilih}**")

    # Menampilkan data dengan ukuran tabel yang bisa di-scroll
    st.dataframe(data_filtered)

    # Menampilkan statistik jumlah data yang difilter
    st.write(f"Menampilkan statistik data untuk tahun **{tahun_dipilih}**. Jumlah data: **{len(data_filtered)}**. Pada station: **{state_dipilih}**")
    st.write(data_filtered.describe())

# Halaman Filter Visualisasi Polutan Data
elif menu == "Visualisasi polutan":
    st.title("Visualisasi Polutan")

    # Dictionary untuk konversi angka bulan ke nama bulan
    bulan_dict = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }

    # Membuat filter data
    tahun_dipilih = st.selectbox("Pilih tahun: ", sorted(air_quality["year"].unique()))
    month_dipilih = st.selectbox("Pilih bulan: ", sorted(air_quality["month"].unique()))
    station_dipilih = st.selectbox("Pilih station: ", sorted(air_quality["station"].unique()))
    polutan_options = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "wd", "WSPM"]
    polutan_dipilih = st.selectbox("Pilih polutan: ", polutan_options)

    # Konversi angka bulan ke nama bulan
    nama_bulan = bulan_dict.get(month_dipilih, month_dipilih)

    # Filter Data berdasarkan tahun, bulan dan station yang dipilih
    data_filtered = air_quality[
        (air_quality["year"] == tahun_dipilih) &
        (air_quality["month"] == month_dipilih) &
        (air_quality["station"] == station_dipilih)
    ]

    # Cek apakah ada data setelah filter
    if data_filtered.empty:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
    else:
        # Visualisasi Line Chart
        st.subheader(f"Tren {polutan_dipilih} di {station_dipilih} Bulan {nama_bulan} Tahun {tahun_dipilih}")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=data_filtered, x="day", y=polutan_dipilih, marker="o", ax=ax)
        ax.set_xlabel("Hari")
        ax.set_ylabel(f"Konsentrasi {polutan_dipilih}")
        ax.set_title(f"Tren {polutan_dipilih} di {station_dipilih} ({tahun_dipilih} - Bulan {nama_bulan})")
        ax.set_xticks(range(1, 32))  # Menampilkan angka tanggal 1-31
        ax.grid(True)
        st.pyplot(fig)


# Halaman Visualisasi Kualitas Udara Terbaik Dan Terburuk 
elif menu == "Kualitas Udara":
    st.title("Visualisasi Kualitas Udara Berdasarkan Tahun Dan Bulan")

    # Dictionary untuk konversi angka bulan ke nama bulan
    bulan_dict = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }

    # Membuat filter data
    tahun_list = ["All Year"] + sorted(air_quality["year"].unique())
    bulan_list = ["All Month"] + sorted(air_quality["month"].unique())
    tahun_dipilih = st.selectbox("Pilih Tahun", tahun_list)
    month_dipilih = st.selectbox("Pilih Bulan", bulan_list)

    # Mulai dengan data asli
    data_filtered = air_quality.copy()

    # Filter berdasarkan tahun yang dipilih
    if tahun_dipilih != "All Year":
        data_filtered = data_filtered[data_filtered["year"] == tahun_dipilih]

    # Filter berdasarkan bulan yang dipilih
    if month_dipilih != "All Month":
        data_filtered = data_filtered[data_filtered["month"] == month_dipilih]

    # Jika tidak ada data untuk bulan yang dipilih
    if data_filtered.empty:
        st.warning(f"Tidak ada data untuk bulan {month_dipilih}.")
    else:
        # Hitung AQI sebagai nilai tertinggi dari polutan
        data_filtered["AQI"] = data_filtered[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]].max(axis=1)

        # Hitung rata-rata AQI tiap kota
        AQI = data_filtered.groupby("station")["AQI"].mean().reset_index()

        # Urutkan berdasarkan AQI terbaik ke terburuk
        AQI = AQI.sort_values(by="AQI", ascending=True)
        best_city = AQI.iloc[0]
        worst_city = AQI.iloc[-1]

        # Data untuk plot
        kota = [best_city["station"], worst_city["station"]]
        aqi_values = [best_city["AQI"], worst_city["AQI"]]

        # Konversi angka bulan ke nama bulan
        nama_bulan = bulan_dict.get(month_dipilih, month_dipilih)

        # Tampilkan tabel polutan
        st.subheader(f"Air Quality Index ({nama_bulan}, {tahun_dipilih}) Kota Changping Dan Dingling")
        aqi_table = pd.DataFrame({
            "Kota": [best_city["station"], worst_city["station"]],
            "Air Quality Index": [round(best_city["AQI"], 2), round(worst_city["AQI"], 2)],
            "Kategori": ["Terbaik", "Terburuk"]
        })
        st.dataframe(aqi_table)

        # plot data
        colors = ["blue", "orange"]
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(kota, aqi_values, color=colors)
        ax.set_ylabel("Kota")
        ax.set_xlabel("Air Quality Index")
        ax.set_title(f"Kualitas Udara Terbaik & Terburuk ({nama_bulan}, {tahun_dipilih})")
        blue_patch = mpatches.Patch(color="blue", label="Udara terbaik")
        orange_patch = mpatches.Patch(color="orange", label="Udara terburuk")
        ax.legend(handles=[blue_patch, orange_patch], loc="lower right")
        st.pyplot(fig)


# Halaman Visualisasi Polutan Tertinggi Tiap Kota
elif menu == "Polutan Tertinggi":
    st.title("Visualisasi Polutan Tertinggi Tiap Kota")

    # Pilih kolom polutan
    polutan_kolom = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]

    # Dictionary untuk konversi angka bulan ke nama bulan
    bulan_dict = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }

    # Membuat filter data
    tahun_list = ["All Year"] + sorted(air_quality["year"].unique())
    bulan_list = ["All Month"] + sorted(air_quality["month"].unique())
    stasiun_list = sorted(air_quality["station"].unique())

    tahun_dipilih = st.selectbox("Pilih Tahun", tahun_list)
    bulan_dipilih = st.selectbox("Pilih Bulan", bulan_list)
    stasiun_dipilih = st.selectbox("Pilih Stasiun", stasiun_list)

    # Filter Data Berdasarkan Pilihan User
    data_filtered = air_quality[air_quality["station"] == stasiun_dipilih]

    if tahun_dipilih != "All Year":
        data_filtered = data_filtered[data_filtered["year"] == tahun_dipilih]

    if bulan_dipilih != "All Month":
        data_filtered = data_filtered[data_filtered["month"] == bulan_dipilih]

    # Periksa apakah data kosong setelah filter
    if data_filtered.empty:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
    else:
        # Hitung Rata-rata Polutan
        pollutant_avg = data_filtered[polutan_kolom].mean()

        # Konversi angka bulan ke nama bulan
        nama_bulan = bulan_dict.get(bulan_dipilih, bulan_dipilih)

        # Tampilkan Data di Streamlit
        st.subheader(f"Rata-rata Polutan di {stasiun_dipilih} ({nama_bulan}, {tahun_dipilih})")
        st.dataframe(pollutant_avg.to_frame(name="Rata-rata").reset_index().rename(columns={"index": "Polutan"}))

        # Buat Plot di Streamlit
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ["blue", "green", "red", "purple", "orange", "brown"]
        ax.bar(polutan_kolom, pollutant_avg, color=colors)
        ax.set_xlabel("Jenis Polutan")
        ax.set_ylabel("Konsentrasi Rata-rata")
        ax.set_title(f"Polutan Tertinggi di {stasiun_dipilih} ({nama_bulan}, {tahun_dipilih})")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        plt.xticks(rotation=45)
        st.pyplot(fig)