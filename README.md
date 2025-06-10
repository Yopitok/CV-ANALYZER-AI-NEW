
<h1 align="center">
  🚀 CV Analyzer AI 🌟
</h1>

<p align="center">
  Aplikasi web komprehensif untuk memproses, menganalisis, menilai, dan membandingkan CV kandidat menggunakan Large Language Models (LLMs) dan antarmuka interaktif.
</p>

<p align="center">
  <img alt="Python Version" src="https://img.shields.io/badge/python-3.9+-blue.svg">
  <img alt="Streamlit Version" src="https://img.shields.io/badge/streamlit-1.35.0-red.svg">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg">
</p>

---

## 📝 Gambaran Umum Proyek

CV Analyzer AI adalah alat bantu strategis untuk tim HR dan manajer rekrutmen. Aplikasi ini mengotomatiskan tugas-tugas manual yang memakan waktu dalam proses screening CV, dengan menyediakan analisis kuantitatif dan kualitatif yang konsisten. Dengan memanfaatkan kecepatan Groq API (menjalankan Llama3) dan antarmuka Streamlit yang dinamis, pengguna dapat membuat keputusan rekrutmen yang lebih cepat dan berbasis data.

## ✨ Fitur Utama
1.  **Pemrosesan CV Batch**: Upload dan ekstrak teks dari beberapa file PDF sekaligus.
2.  **Analisis AI Cepat**: Dapatkan ringkasan, rekomendasi kekuatan/kelemahan, dan perbandingan antar CV secara on-demand.
3.  **Dashboard Skoring Dinamis**: Peringkatkan kandidat secara kuantitatif berdasarkan domain pekerjaan yang spesifik.
4.  **Pembobotan Kriteria Interaktif**: Pengguna dapat mengatur tingkat kepentingan setiap kriteria untuk analisis yang disesuaikan.
5.  **Normalisasi Skor**: Hasil akhir disajikan dalam skala 0-100 yang intuitif untuk perbandingan yang adil.
6.  **Visualisasi Data Interaktif**: Bandingkan kandidat dengan mudah melalui Radar Chart dan Bar Chart.
7.  **Laporan Naratif Otomatis**: Dapatkan laporan analisis mendalam yang ditulis oleh AI, lengkap dengan rekomendasi.

## 🏗️ Struktur Sistem Inti
Arsitektur proyek ini dirancang secara modular untuk memisahkan logika inti, konfigurasi, dan antarmuka pengguna.

```bash
CV_ANALYZER_FINAL/
├── .streamlit/
│   └── secrets.toml         # Menyimpan API Key
│
├── src/                     # Folder utama source code
│   ├── app.py               # Entry point dan logika UI Streamlit
│   │
│   ├── config/              # Modul untuk semua data konfigurasi
│   │   ├── prompts.py       # Kumpulan template prompt untuk AI
│   │   └── settings.py      # Peta kriteria, bobot, dan domain
│   │
│   └── core/                # Modul untuk semua logika bisnis inti
│       ├── analysis.py      # Logika skoring, normalisasi, dan narasi
│       ├── parsing.py       # Fungsi untuk parsing file PDF
│       ├── services.py      # Layanan AI sederhana (ringkasan, dll)
│       └── utils.py         # Utilitas setup (inisialisasi klien & state)
│
├── requirements.txt         # Daftar dependensi Python
└── setup.py                 # File setup untuk instalasi paket lokal
```

## 🛠️ Teknologi Utama
-   **Backend & LLM**: Groq API (Llama3-70B & Llama3-8B)
-   **Frontend**: Streamlit
-   **Data Processing**: Pandas
-   **Visualisasi**: Plotly
-   **PDF Parsing**: pdfplumber

---

## ⚙️ Detail Fungsi & Cara Penggunaan

Berikut adalah rincian fungsionalitas utama aplikasi, dari pemrosesan hingga analisis.

### **1. Pemrosesan CV (Tab: 📤 Upload CV)**
  ![image](https://github.com/user-attachments/assets/a2fd5e14-efb9-4462-ab91-553709b91373)

  
-   **Tujuan**: Mengimpor dan menyiapkan data mentah dari file-file CV untuk dianalisis.
-   **Cara Penggunaan**:
    1.  Navigasi ke tab **"Upload CV"**.
    2.  Klik tombol "Pilih file..." dan pilih satu atau beberapa file PDF.
    3.  Klik tombol **"Proses File"**.
-   **Di Balik Layar (`core/parsing.py`)**:
    -   Fungsi `parse_cvs` melakukan loop pada setiap file yang diunggah.
    -   Menggunakan `pdfplumber` untuk mengekstrak teks dari setiap halaman PDF secara aman.
    -   Menangani file yang gagal diproses dan mengembalikan daftar teks CV yang berhasil diekstrak.


### **2. Analisis Kualitatif Cepat (Tabs: 🔍 Ringkasan & 🤖 Rekomendasi)**
   ![image](https://github.com/user-attachments/assets/ca9efaf8-c53c-470e-8d36-98561b6e64f4) 
   ![image](https://github.com/user-attachments/assets/f3e6ff33-0c3f-407a-b073-ac40a13b999f)

   
-   **Tujuan**: Mendapatkan pemahaman cepat tentang kandidat secara individu tanpa proses skoring.
-   **Cara Penggunaan**:
    1.  Pilih tab **"Ringkasan"** atau **"Rekomendasi"**.
    2.  Pilih kandidat yang ingin dianalisis.
    3.  Klik tombol yang sesuai ("Buat Ringkasan" atau "Dapatkan Rekomendasi AI").
-   **Di Balik Layar (`core/services.py`)**:
    -   Fungsi `summarize_cv` atau `recommend_on_cv` dipanggil.
    -   Teks CV tunggal dikirim ke model AI (Llama3-8B untuk ringkasan, Llama3-70B untuk rekomendasi) dengan `temperature=0` untuk hasil yang konsisten.
    -   Hasil teks dari AI langsung ditampilkan di antarmuka.


### **3. Analisis Komparatif (Tab: ⚖️ Perbandingan)**
  ![image](https://github.com/user-attachments/assets/3f5331d5-6100-4dcc-b56f-d8beadef3819)

  
-   **Tujuan**: Membandingkan semua kandidat secara langsung untuk sebuah posisi spesifik.
-   **Cara Penggunaan**:
    1.  Pilih tab **"Perbandingan"**.
    2.  Ketik nama jabatan di kolom **"Bandingkan untuk posisi"**.
    3.  Klik tombol **"Bandingkan Kandidat Sekarang"**.
-   **Di Balik Layar (`core/services.py`)**:
    -   Fungsi `compare_cvs` menggabungkan semua teks CV yang ada.
    -   Prompt khusus yang berisi nama jabatan dan semua data CV dikirim ke AI.
    -   AI memberikan analisis perbandingan dan rekomendasi kandidat terbaik.


### **4. Dashboard Analisis Kuantitatif (Tab: 🏆 Dashboard Analisis)**
![image](https://github.com/user-attachments/assets/49537413-756a-48b8-9237-8c778799e60e)
Ini adalah fitur inti untuk pemeringkatan berbasis data yang objektif.

-   **Tujuan**: Memberikan skor kuantitatif, memeringkat, dan memvisualisasikan performa kandidat berdasarkan kriteria yang dapat disesuaikan.
-   **Cara Penggunaan**:
    1.  Pilih **Domain Target** (misal: "IT"). Ini akan mengubah kriteria penilaian.
    2.  (Opsional) Buka `Atur Pembobotan Kriteria` dan geser slider untuk menyesuaikan prioritas Anda.
    3.  Klik tombol **"Jalankan Analisis & Peringkat"**.
-   **Di Balik Layar (`core/analysis.py` & `config/`)**:
    1.  **Skoring AI**: Fungsi `score_and_analyze_cvs` mengambil `active_criteria` dari `config/settings.py` dan membuat prompt dari `config/prompts.py`. Setiap CV dikirim ke AI untuk dinilai (skor mentah 0-10 per kriteria). Penanganan error JSON otomatis disertakan.
    2.  **Pembobotan & Normalisasi**: Skor mentah dari AI dikalikan dengan bobot dari slider UI. Skor total ini kemudian dinormalisasi menjadi skala **0-100** untuk perbandingan yang adil.
    3.  **Laporan Naratif**: Data 3 kandidat teratas (termasuk skor rinci) dikirim kembali ke AI untuk menghasilkan laporan naratif yang terstruktur.
-   **Hasil Analisis**:
    -   **Ranking**: Tabel peringkat kandidat berdasarkan skor akhir 0-100.
![image](https://github.com/user-attachments/assets/6a294617-4635-44df-b1ce-c876f4c5e4c2)
    -   **Visualisasi**: Radar Chart (kekuatan/kelemahan) dan Bar Chart (peringkat skor akhir).
![image](https://github.com/user-attachments/assets/68600ec6-9895-4b04-96e8-9f8726a26472)

    -   **Naratif**: Ulasan mendalam dari AI.
![image](https://github.com/user-attachments/assets/f210abfa-11fb-4098-bb51-987bdbb7c700)

   

---

## 📦 Deployment & Setup

**1. Persyaratan**
- Python 3.9+
- API Key dari [Groq](https://console.groq.com/keys)
- RAM 8GB direkomendasikan

**2. Langkah-langkah**

- **Clone Repositori & Masuk ke Folder**
  ```bash
  git clone [LINK_REPOSITORI_GITHUB_ANDA]
  cd [NAMA_FOLDER_PROYEK_ANDA]
  ```

- **Setup Virtual Environment**
  ```bash
  # Windows
  python -m venv venv
  .\venv\Scripts\activate

  # MacOS/Linux
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Install Dependensi**
  ```bash
  pip install -r requirements.txt
  ```

- **Install Proyek (Penting!)**
  ```bash
  pip install -e .
  ```

- **Atur API Key**
  Buat file `.streamlit/secrets.toml` dan isi dengan:
  ```toml
  GROQ_API_KEY="gsk_xxxxxx"
  ```

- **Jalankan Aplikasi**
  ```bash
  streamlit run src/app.py
  ```
