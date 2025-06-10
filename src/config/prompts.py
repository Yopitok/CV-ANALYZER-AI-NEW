# File: src/config/prompts.py
def get_scoring_prompt(domain, active_criteria):
    return f"""Anda adalah sistem skoring HR akurat. Nilai CV untuk domain '{domain}' dalam format JSON valid. Kunci: {', '.join(active_criteria)}, dan 'level'. Aturan: Jawab HANYA JSON, nilai angka tidak diapit kutip, 'level' hanya 'entry', 'mid', 'senior', atau 'expert'."""

def get_narrative_prompt(context_for_narrative, domain):
    return f"""Anda adalah Analis HR Senior. Berdasarkan data skor kandidat untuk domain '{domain}', buat laporan naratif mendalam dengan struktur: ### Ringkasan Eksekutif, ### Analisis Komparatif per Kriteria, dan ### Rekomendasi Strategis. Gunakan bahasa profesional dan analitis.\n\n--- DATA KANDIDAT ---\n{context_for_narrative}"""