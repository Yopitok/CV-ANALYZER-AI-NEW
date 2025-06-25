# File: src/config/prompts.py
def get_scoring_prompt(domain, active_criteria, jd_text=None):
    base_prompt = f"Anda adalah sistem skoring HR akurat. Nilai CV untuk domain '{domain}' dalam format JSON valid. Kunci JSON: {', '.join(active_criteria)}, dan 'level'."
    if jd_text and jd_text.strip():
        context_prompt = f"Gunakan Deskripsi Pekerjaan (JD) berikut sebagai acuan utama penilaian:\n\n--- JD START ---\n{jd_text}\n--- JD END ---\n\n"
        final_prompt = context_prompt + base_prompt
    else:
        final_prompt = base_prompt
    rules_prompt = f"""\n\nAturan Sangat Penting:\n- Jawab HANYA dengan objek JSON tunggal.\n- Nilai skor harus antara 0 hingga 10.\n- 'level' hanya bisa 'entry', 'mid', 'senior', atau 'expert'."""
    return final_prompt + rules_prompt

def get_narrative_prompt(context_for_narrative, domain):
    return f"""Anda adalah Analis HR Senior. Berdasarkan data skor kandidat untuk domain '{domain}', buat laporan analisis naratif mendalam dengan struktur: ### Ringkasan Eksekutif, ### Analisis Komparatif per Kriteria, dan ### Rekomendasi Strategis. Gunakan bahasa profesional dan analitis.\n\n--- DATA KANDIDAT ---\n{context_for_narrative}"""