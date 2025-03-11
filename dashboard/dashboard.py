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
    ["Data", "Statistik Data", "Kualitas Udara", "Polutan Tertinggi"]
)

# Halaman Data 
if menu == "Data":
    st.title("Data Air Quality Kota Changping Dan Dingling")

    # Membuat filter tahun 
    tahun_tersedia = sorted(air_quality["year"].unique()) 
    tahun_dipilih = st.selectbox("Pilih Tahun:", tahun_tersedia, index=len(tahun_tersedia)-1) 

    # Filter dataset berdasarkan tahun yang dipilih
    data_filtered = air_quality[air_quality["year"] == tahun_dipilih]

    # Menampilkan jumlah data yang difilter
    st.write(f"Menampilkan data untuk tahun **{tahun_dipilih}**. Jumlah data: **{len(data_filtered)}**")

    # Menampilkan data dengan ukuran tabel yang bisa di-scroll
    st.dataframe(data_filtered, height=500) 


# Halaman Statistik Data
elif menu == "Statistik Data":
    st.title("Statistik Data")
    st.write(air_quality.describe())

# Halaman Visualisasi Kualitas Udara Terbaik Dan Terburuk 
elif menu == "Kualitas Udara":
    st.title("Visualisasi Kota Dengan Kualitas Udara Terbaik Dan Terburuk")
    # ambil nilai tertinggi tiap polutan
    air_quality["AQI"] = air_quality[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]].max(axis=1)

    # hitung rata-rata AQI
    AQI = air_quality.groupby("station")["AQI"].mean().reset_index()

    # Urutkan berdasarkan AQI terbaik ke terburuk
    AQI = AQI.sort_values(by="AQI", ascending=True)
    best_city = AQI.iloc[0]
    worst_city = AQI.iloc[-1]

    # Data untuk plot
    kota = [best_city["station"], worst_city["station"]]
    aqi_values = [best_city["AQI"], worst_city["AQI"]]

    # Set Biru = terbaik, Oranye = terburuk
    colors = ["blue", "orange"]

    # Plot kota terbaik dan terburuk kualitas udaranya
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(kota, aqi_values, color=colors)
    ax.set_ylabel("Kota")
    ax.set_xlabel("AQI")
    ax.set_title("Kota dengan Kualitas Udara Terbaik & Terburuk")
    blue_patch = mpatches.Patch(color="blue", label="Udara baik")
    orange_patch = mpatches.Patch(color="orange", label="Udara buruk")
    ax.legend(handles=[blue_patch, orange_patch], loc="lower right")
    st.pyplot(fig)

    st.title("Kesimpulan")
    st.write("Berdasarkan hasil analisa dan juga visualisasi grafik, kota Dingling memiliki kualitas udara terbaik dengan nilai AQI yang lebih rendah, menunjukkan udara yang lebih bersih dan sehat untuk dihuni. Sebaliknya kota Changping memiliki kualitas udara terburuk dengan nilai AQI yang lebih tinggi yang mengindikasikan tingkat polusi yang lebih tinggi karena jumlah polutanya banyak. Perbedaan ini menunjukkan bahwa faktor banyaknya polutan itu mempengaruhi kulitas udara kota.")


# Halaman Visualisasi Polutan Tertinggi Tiap Kota
elif menu == "Polutan Tertinggi":
    st.title("Visualisasi Polutan Tertinggi Tiap Kota") 

    # Pilih kolom polutan
    polutan_kolom = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    # Hitung rata-rata setiap polutan di Changping
    changping_pollutants = Data_Changping_df[polutan_kolom].mean()

    # Visualisasi Polutan tertinggi atau sering muncul di kota Changping
    fig, ax = plt.subplots(figsize=(8, 5))
    changping_pollutants.plot(kind="bar", color="blue")
    ax.set_xlabel("Jenis Polutan")
    ax.set_ylabel("Konsentrasi Rata-rata")
    ax.set_title("Polutan Tertinggi di Changping")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)


    # Pilih hanya kolom polutan
    polutan_kolom = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    # Hitung rata-rata setiap polutan di Changping
    dongling_pollutants = Data_Dingling_df[polutan_kolom].mean()

    # Visualisasi Polutan tertinggi atau sering muncul di kota Dongling
    fig, ax = plt.subplots(figsize=(8, 5))
    dongling_pollutants.plot(kind="bar", color="blue")
    ax.set_xlabel("Jenis Polutan")
    ax.set_ylabel("Konsentrasi Rata-rata")
    ax.set_title("Polutan Tertinggi di Dongling")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)


    st.title("Visualisasi Polutan Paling Sering Muncul di Setiap Kota")

    # Pilih hanya kolom polutan
    polutan_kolom = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    air_quality[polutan_kolom] = air_quality[polutan_kolom].apply(pd.to_numeric, errors='coerce')

    # Kelompokkan berdasarkan kota dan hitung rata-rata setiap polutan
    total_polutan = air_quality.groupby("station")[polutan_kolom].mean()

    # Menentukan polutan tertinggi di setiap kota
    dominan_polutan = total_polutan.idxmax(axis=1)

    # Visualisasi distribusi polutan tiap kota
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(total_polutan, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5)
    ax.set_title("Polutan Paling Sering Muncul di Setiap Kota")
    ax.set_xlabel("Jenis Polutan")
    ax.set_ylabel("Kota")
    st.pyplot(fig)

    st.title("Kesimpulan")
    st.write("Berdasarkan analisis data dan juga visualisasi grafik, polutan yang paling dominan di Changping adalah CO (Karbon Monoksida) dengan konsentrasi tertinggi sebesar 1160.04. Sementara itu, di Dingling polutan yang paling dominan juga adalah CO (Karbon Monoksida) dengan konsentrasi 924.76. Hal ini menunjukkan bahwa CO merupakan polutan yang paling banyak ditemukan di kedua kota tersebut.")