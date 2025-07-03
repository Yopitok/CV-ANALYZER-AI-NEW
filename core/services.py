# File: core/services.py

# Tidak perlu import streamlit di sini

def summarize_cv(client, cv_text: str) -> str:
    """Fungsi sederhana untuk meringkas CV."""
    try:
        # Prompt bisa langsung ditulis di sini untuk kesederhanaan
        prompt = "Ringkas CV ini dalam Bahasa Indonesia (3-4 poin utama). Pastikan jawaban dalam Bahasa Indonesia."
        response = client.chat.completions.create(
            model="llama3-8b-8192", 
            temperature=0, 
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": cv_text}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Gagal meringkas: {e}"

def recommend_on_cv(client, cv_text: str) -> str:
    """Fungsi sederhana untuk rekomendasi."""
    try:
        prompt = "Sebagai HR, berikan analisis CV ini (sub-judul: 'Kekuatan Utama', 'Area Peningkatan') dalam Bahasa Indonesia."
        response = client.chat.completions.create(
            model="llama3-70b-8192", 
            temperature=0, 
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": cv_text}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Gagal memberi rekomendasi: {e}"

def compare_cvs(client, cv_data: list, role: str) -> str:
    """Fungsi sederhana untuk perbandingan."""
    try:
        cv_list_text = "\n\n---\n\n".join([f"CV {i+1} ({cv['filename']}):\n{cv['text'][:2000]}" for i, cv in enumerate(cv_data)])
        prompt = (f"Anda adalah manajer rekrutmen dari Indonesia. Bandingkan CV berikut untuk peran '{role}'. Tentukan kandidat terbaik dan berikan justifikasi yang jelas. **PENTING: Seluruh jawaban dan analisis Anda HARUS dalam Bahasa Indonesia.**\n\n{cv_list_text}")
        response = client.chat.completions.create(
            model="llama3-70b-8192", 
            temperature=0, 
            messages=[{"role": "system", "content": "Anda adalah asisten HR yang menjawab dalam Bahasa Indonesia."}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Gagal membandingkan: {e}"