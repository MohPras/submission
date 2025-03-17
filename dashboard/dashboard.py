import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import matplotlib.patches as mpatches
sns.set(style='dark')
import os




# Judul Dashboard
st.title("Dashboard Kualitas Udara di Kota Changping dan Dongling")

# Load Data
# Dapatkan path absolut dari folder tempat dashboard.py berada
base_path = os.path.dirname(__file__)
# Gabungkan dengan nama file
main_data_path = os.path.join(base_path, "..", "dashboard", "main_data.csv")
changping_data_path = os.path.join(base_path, "..", "data", "Data_Changping.csv")
dingling_data_path = os.path.join(base_path, "..", "data", "Data_Dingling.csv")

# Baca file CSV
air_quality = pd.read_csv(main_data_path)
Data_Changping_df = pd.read_csv(changping_data_path)
Data_Dingling_df = pd.read_csv(dingling_data_path)

# Sidebar Menu
st.sidebar.title("Menu Navigasi")
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
    st.dataframe(data_filtered, height=500)

    # Menampilkan statistik jumlah data yang difilter
    st.write(f"Menampilkan statistik data untuk tahun **{tahun_dipilih}**. Jumlah data: **{len(data_filtered)}**. Pada station: **{state_dipilih}**")
    st.write(data_filtered.describe(), height=500)

# Halaman Filter Visualisasi Polutan Data
elif menu == "Visualisasi polutan":
    st.title("Visualisasi Polutan")

    # Membuat filter data
    tahun_dipilih = st.selectbox("Pilih tahun: ", sorted(air_quality["year"].unique()))
    month_dipilih = st.selectbox("Pilih bulan: ", sorted(air_quality["month"].unique()))
    station_dipilih = st.selectbox("Pilih station: ", sorted(air_quality["station"].unique()))
    polutan_options = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "wd", "WSPM"]
    polutan_dipilih = st.selectbox("Pilih polutan: ", polutan_options)

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
        st.subheader(f"Tren {polutan_dipilih} di {station_dipilih} - {tahun_dipilih} Bulan {month_dipilih}")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=data_filtered, x="day", y=polutan_dipilih, marker="o", ax=ax)
        ax.set_xlabel("Hari")
        ax.set_ylabel(f"Konsentrasi {polutan_dipilih}")
        ax.set_title(f"Tren {polutan_dipilih} di {station_dipilih} ({tahun_dipilih} - Bulan {month_dipilih})")
        ax.set_xticks(range(1, 32))  # Menampilkan angka tanggal 1-31
        ax.grid(True)
        st.pyplot(fig)


# Halaman Visualisasi Kualitas Udara Terbaik Dan Terburuk 
elif menu == "Kualitas Udara":
    st.title("Visualisasi Kualitas Udara Berdasarkan Tahun Dan Bulan")

    # Membuat filter data
    tahun_dipilih = st.selectbox("Pilih tahun: ", sorted(air_quality["year"].unique()))
    month_dipilih = st.selectbox("Pilih bulan: ", sorted(air_quality["month"].unique()))

    # Filter Data berdasarkan tahun, bulan dan station yang dipilih
    data_filtered = air_quality[
        (air_quality["year"] == tahun_dipilih) &
        (air_quality["month"] == month_dipilih)
    ]
    
    # Jika tidak ada data untuk bulan yang dipilih
    if data_filtered.empty:
        st.warning(f"Tidak ada data untuk bulan {month_dipilih}.")
    else:
        # visualisasi kota terbaik dan terburuk dalam filter tahun dan bulan
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

        # Set warna biru = terbaik, oranye = terburuk
        colors = ["blue", "orange"]

        # Plot hasilnya
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(kota, aqi_values, color=colors)
        ax.set_ylabel("Kota")
        ax.set_xlabel("Air Quality Index")
        ax.set_title(f"Kualitas Udara Terbaik & Terburuk pada Bulan {month_dipilih} tahun {tahun_dipilih}")

        # Tambahkan legenda
        blue_patch = mpatches.Patch(color="blue", label="Udara terbaik")
        orange_patch = mpatches.Patch(color="orange", label="Udara terburuk")
        ax.legend(handles=[blue_patch, orange_patch], loc="lower right")

        # Tampilkan plot di Streamlit
        st.pyplot(fig)

        # Tampilkan tabel polutan
        st.subheader(f"Air Index Quality Pada Bulan {month_dipilih} Tahun {tahun_dipilih} Kota Changping Dan Dingling")
        aqi_table = pd.DataFrame({
            "Kota": [best_city["station"], worst_city["station"]],
            "Air Quality Index": [round(best_city["AQI"], 2), round(worst_city["AQI"], 2)],
            "Kategori": ["Terbaik", "Terburuk"]
        })
        st.dataframe(aqi_table)


# Halaman Visualisasi Polutan Tertinggi Tiap Kota
elif menu == "Polutan Tertinggi":
    st.title("Visualisasi Polutan Tertinggi Tiap Kota") 

    # Membuat filter data
    tahun_dipilih = st.selectbox("Pilih tahun: ", sorted(air_quality["year"].unique()))
    month_dipilih = st.selectbox("Pilih bulan: ", sorted(air_quality["month"].unique()))
    station_dipilih = st.selectbox("Pilih station: ", sorted(air_quality["station"].unique()))


    # Filter Data berdasarkan tahun, bulan dan station yang dipilih
    data_filtered = air_quality[
        (air_quality["year"] == tahun_dipilih) &
        (air_quality["month"] == month_dipilih) &
        (air_quality["station"] == station_dipilih)
    ]

    # Cek apakah ada data setelah filter
    if data_filtered.empty:
        st.warning(f"Tidak ada data untuk {station_dipilih} pada bulan {month_dipilih} tahun {tahun_dipilih}.")
    else:
        st.subheader(f"Polutan Tertinggi di {station_dipilih} ({month_dipilih}/{tahun_dipilih})")

        # Ambil nilai maksimum tiap polutan
        polutan_cols = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
        max_polutan = data_filtered[polutan_cols].max()

        # Buat dataframe untuk tabel
        polutan_table = pd.DataFrame({
            "Polutan": max_polutan.index,
            "Konsentrasi Maksimum": max_polutan.values
        })

        # Tampilkan tabel
        st.dataframe(polutan_table)

        # Visualisasi bar chart polutan tertinggi
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(max_polutan.index, max_polutan.values, color="skyblue")
        ax.set_xlabel("Konsentrasi Maksimum")
        ax.set_title(f"Polutan Tertinggi di {station_dipilih} ({month_dipilih}/{tahun_dipilih})")
        st.pyplot(fig)