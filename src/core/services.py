# File: src/core/services.py

import time

def summarize_cv(client, cv_text: str) -> str:
    """Memanggil AI untuk meringkas sebuah CV secara konsisten."""
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            temperature=0, # <-- Tambahkan ini
            messages=[
                {"role": "system", "content": "Ringkas CV ini dalam Bahasa Indonesia dalam 3-4 poin utama, fokus pada pengalaman, keahlian, dan pendidikan terakhir."},
                {"role": "user", "content": cv_text}
            ]
        )
        time.sleep(1)
        return response.choices[0].message.content
    except Exception as e:
        return f"Gagal membuat ringkasan: {e}"

def recommend_on_cv(client, cv_text: str) -> str:
    """Memanggil AI untuk memberikan rekomendasi pada sebuah CV secara konsisten."""
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            temperature=0, # <-- Tambahkan ini
            messages=[
                {"role": "system", "content": "Sebagai seorang HR profesional, berikan analisis singkat mengenai CV ini. Gunakan format Markdown dengan sub-judul 'Kekuatan Utama' dan 'Area untuk Peningkatan'."},
                {"role": "user", "content": cv_text}
            ]
        )
        time.sleep(1)
        return response.choices[0].message.content
    except Exception as e:
        return f"Gagal mendapatkan rekomendasi: {e}"

def compare_cvs(client, cv_data: list, role: str) -> str:
    """Memanggil AI untuk membandingkan beberapa CV secara konsisten."""
    try:
        cv_list_text = "\n\n---\n\n".join(
            [f"CV {i+1} ({cv['filename']}):\n{cv['text'][:2000]}" for i, cv in enumerate(cv_data)]
        )
        prompt = (
            f"Anda adalah manajer rekrutmen. Bandingkan CV berikut untuk peran '{role}'. "
            f"Tentukan kandidat terbaik dan berikan justifikasi yang jelas.\n\n{cv_list_text}"
        )
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            temperature=0, # <-- Tambahkan ini
            messages=[{"role": "system", "content": "Bandingkan CV secara objektif, detail, dan profesional."}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Gagal membandingkan CV: {e}"