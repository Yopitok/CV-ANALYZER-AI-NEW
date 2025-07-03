# File: config/prompts.py

def get_scoring_prompt(domain, criteria_list, jd_text=""):
    """Membuat prompt yang sangat terstruktur untuk menilai CV dan menghasilkan JSON."""
    
    # Membuat daftar kriteria untuk format JSON
    criteria_json = ",\n".join([f'    "{crit}": "skor_numerik_antara_0_hingga_10"' for crit in criteria_list])
    
    # Bagian prompt yang hanya muncul jika ada Job Description
    jd_section = f"""
---
**KONTEKS UTAMA (Job Description):**
Gunakan Deskripsi Pekerjaan (JD) berikut sebagai acuan utama dan paling penting dalam penilaian Anda. Kandidat yang cocok dengan JD ini harus mendapat skor lebih tinggi.
<JD>
{jd_text}
</JD>
---
""" if jd_text and jd_text.strip() else ""

    # Prompt utama yang digabungkan
    return f"""
**PERAN ANDA:**
Anda adalah Sistem Perekrutan AI (AI Recruitment System) yang sangat akurat, objektif, dan teliti. Anda HANYA berkomunikasi menggunakan format JSON.

**TUGAS ANDA:**
Nilai CV yang diberikan berdasarkan kriteria yang relevan untuk domain '{domain}'.
{jd_section}
**FORMAT OUTPUT (WAJIB):**
Respons Anda HARUS berupa satu objek JSON yang valid, tanpa teks pembuka atau penutup apa pun. Strukturnya harus seperti ini:

{{
  "level": "level_kandidat_disini",
{criteria_json}
}}

**ATURAN MUTLAK:**
- Skor untuk setiap kriteria HARUS berupa angka (integer atau float) antara 0 dan 10.
- Nilai untuk "level" HARUS salah satu dari string berikut: 'entry-level', 'junior', 'mid-level', 'senior', 'lead', atau 'principal'.
- JANGAN menyertakan komentar atau karakter tambahan di luar objek JSON.
"""

def get_narrative_prompt(context_for_narrative, domain):
    """Membuat prompt untuk laporan naratif dari Manajer HR."""
    return f"""
**PERAN ANDA:**
Anda adalah seorang Analis Perekrutan Senior yang sangat berpengalaman. Gaya tulisan Anda profesional, analitis, dan langsung ke intinya. Anda selalu memberikan justifikasi berdasarkan data.

**TUGAS ANDA:**
Berdasarkan data skor kandidat yang diberikan untuk domain '{domain}', buat laporan analisis naratif mendalam dalam format Markdown.

**STRUKTUR LAPORAN (WAJIB):**
Gunakan struktur berikut dengan tepat:

### Ringkasan Eksekutif
Ringkasan singkat tentang kualitas umum para kandidat teratas dan siapa yang paling menonjol secara sekilas.

### Analisis Komparatif
Bandingkan kandidat teratas secara langsung. Bahas kekuatan dan kelemahan relatif mereka pada kriteria-kriteria kunci.

### Rekomendasi Strategis
Berikan rekomendasi akhir yang jelas. Sebutkan siapa (1-2 kandidat) yang harus diprioritaskan untuk wawancara dan mengapa.

**DATA SKOR KANDIDAT:**
---
{context_for_narrative}
---
"""

# --- REVISI: MENAMBAHKAN FUNGSI-FUNGSI YANG DIBUTUHKAN OLEH services.py ---

def get_summary_prompt() -> str:
    """Mengembalikan prompt untuk meringkas CV."""
    return "Anda adalah asisten AI yang efisien. Tugas Anda adalah meringkas CV yang diberikan. Fokus pada 3-4 pencapaian atau poin paling signifikan dari kandidat. Gunakan format poin-poin (bullet points). Jawaban harus dalam Bahasa Indonesia."

def get_recommendation_prompt() -> str:
    """Mengembalikan prompt untuk analisis kekuatan & area peningkatan."""
    return "Anda adalah seorang Manajer HR yang bijaksana dan suportif. Berdasarkan CV yang diberikan, berikan analisis singkat. Gunakan format Markdown dengan dua sub-judul berikut: '### Kekuatan Utama' dan '### Area untuk Ditingkatkan'. Berikan masukan yang konstruktif. Seluruh jawaban harus dalam Bahasa Indonesia."

def get_comparison_prompt(role: str, cv_list_text: str) -> tuple[str, str]:
    """Mengembalikan system prompt dan user prompt untuk perbandingan CV."""
    system_prompt = "Anda adalah seorang Direktur Perekrutan senior di sebuah perusahaan teknologi terkemuka di Indonesia. Analisis Anda tajam, to-the-point, dan profesional. Seluruh output Anda harus dalam Bahasa Indonesia."
    user_prompt = f"""
**TUGAS ANDA:**
Saya sedang melakukan rekrutmen untuk posisi: **{role}**.

Berikut adalah potongan CV dari beberapa kandidat yang masuk dalam daftar pendek. Tolong berikan analisis perbandingan dan rekomendasi Anda.

**STRUKTUR JAWABAN (WAJIB):**
Gunakan format Markdown dengan struktur berikut:

1.  **Analisis Singkat per Kandidat**:
    - **Kandidat (nama file):** Poin-poin singkat kekuatan utama.

2.  **Perbandingan Langsung (Head-to-Head)**:
    - Bandingkan kandidat berdasarkan aspek kunci yang paling relevan untuk posisi tersebut.

3.  **Rekomendasi Utama**:
    - Sebutkan 1-2 kandidat yang paling Anda rekomendasikan untuk maju ke tahap wawancara dan berikan justifikasi yang kuat mengapa mereka yang terpilih.

**DATA CV KANDIDAT:**
---
{cv_list_text}
---
"""
    return system_prompt, user_prompt