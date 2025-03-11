# 📊 Dashboard Pemantauan Kualitas Udara Changping dan Dingling

Dashboard ini digunakan untuk memvisualisasikan data kualitas udara menggunakan Streamlit.  

---

## 🚀 **Instalasi & Menjalankan Aplikasi**  

### 1. Clone Repository (Opsional, jika dari GitHub)
Jika proyek ini ada di GitHub, jalankan:  
```
bash
git clone https://github.com/username/repo-dashboard.git
cd repo-dashboard
```
### 2. Buat Virtual Environment (Opsional, tapi direkomendasikan)
```
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```
### 3. Install Dependensi
Pastikan semua package yang dibutuhkan sudah terinstal, cara installnya cukup jalankan code dibawah.
```
pip install -r requirements.txt
```
### 4. Jalankan Dasboard**
Catatan pastikan posisi anda ada di folder dashboard agar runing aplikasi tidak eror.
- Gunakan pwd untuk menampilkan path yang lagi dipakai
- Gunakan ls untuk menampilkan file dalam folder
- Gunakan cd untuk masuk atau keluar dari folder
```
streamlit run dashboard/dashboard.py
```
### 5. Catatan
Pastikan Python versi 3.8 atau lebih baru sudah terinstal.
Jika ada error terkait package, coba update pip
```
pip install --upgrade pip
```
### 6. Penyesuaian:
- Ganti **`dashboard.py`** sesuai dengan nama file utama dashboard kamu.  
- Kalau pakai **dataset atau API**, tambahkan cara mendapatkan atau menghubungkannya. 