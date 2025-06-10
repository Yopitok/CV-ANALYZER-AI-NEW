<p align="center">
  <a href="#">
    <img src="[LINK_KE_LOGO_ATAU_ICON_PROYEK_ANDA]" alt="CV Analyzer AI Logo" width="120" height="120">
  </a>
</p>

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

-   **Tujuan**: Mengimpor dan menyiapkan data mentah dari file-file CV untuk dianalisis.
-   **Cara Penggunaan**:
    1.  Navigasi ke tab **"Upload CV"**.
    2.  Klik tombol "Pilih file..." dan pilih satu atau beberapa file PDF.
    3.  Klik tombol **"Proses File"**.
-   **Di Balik Layar (`core/parsing.py`)**:
    -   Fungsi `parse_cvs` melakukan loop pada setiap file yang diunggah.
    -   Menggunakan `pdfplumber` untuk mengekstrak teks dari setiap halaman PDF secara aman.
    -   Menangani file yang gagal diproses dan mengembalikan daftar teks CV yang berhasil diekstrak.

    *Ganti gambar di bawah dengan screenshot tab upload Anda*
    ![Upload Tab]([LINK_SCREENSHOT_TAB_UPLOAD])

### **2. Analisis Kualitatif Cepat (Tabs: 🔍 Ringkasan & 🤖 Rekomendasi)**

-   **Tujuan**: Mendapatkan pemahaman cepat tentang kandidat secara individu tanpa proses skoring.
-   **Cara Penggunaan**:
    1.  Pilih tab **"Ringkasan"** atau **"Rekomendasi"**.
    2.  Pilih kandidat yang ingin dianalisis.
    3.  Klik tombol yang sesuai ("Buat Ringkasan" atau "Dapatkan Rekomendasi AI").
-   **Di Balik Layar (`core/services.py`)**:
    -   Fungsi `summarize_cv` atau `recommend_on_cv` dipanggil.
    -   Teks CV tunggal dikirim ke model AI (Llama3-8B untuk ringkasan, Llama3-70B untuk rekomendasi) dengan `temperature=0` untuk hasil yang konsisten.
    -   Hasil teks dari AI langsung ditampilkan di antarmuka.

    *Ganti gambar di bawah dengan screenshot tab rekomendasi*
    ![Recommendation Tab]([LINK_SCREENSHOT_TAB_REKOMENDASI])

### **3. Analisis Komparatif (Tab: ⚖️ Perbandingan)**

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
    -   **Visualisasi**: Radar Chart (kekuatan/kelemahan) dan Bar Chart (peringkat skor akhir).
    -   **Naratif**: Ulasan mendalam dari AI.

    *Ganti gambar di bawah dengan screenshot dashboard Anda*
    ![Dashboard Tab]([LINK_SCREENSHOT_TAB_DASHBOARD])

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