# File: core/analysis.py

import json
import re
import time
import pandas as pd
import streamlit as st
from config.prompts import get_scoring_prompt, get_narrative_prompt
from config.settings import MODEL_SCORING, MODEL_NARRATIVE

# --- REVISI 3: Mengembalikan fungsi _handle_json_error seperti versi awal Anda ---
def _handle_json_error(e, cv, result_data, active_criteria):
    """Mencoba memperbaiki JSON yang rusak dari LLM, atau memberi skor 0."""
    st.warning(f"Terjadi masalah format JSON pada {cv['filename']}. Mencoba perbaikan...")
    error_str = str(e)
    match = re.search(r'\{.*\}', error_str, re.DOTALL)
    
    if match:
        failed_json_str = match.group(0)
        try:
            # Mencoba membersihkan string JSON yang umum rusak
            cleaned_str = re.sub(r',\s*\}', '}', failed_json_str.replace('\\n', ' ').replace('\\', ''))
            result_data.update(json.loads(cleaned_str))
            st.success(f"Perbaikan JSON untuk {cv['filename']} berhasil!")
            return
        except Exception:
            pass # Gagal memperbaiki, lanjut ke penanganan di bawah

    st.error(f"Perbaikan otomatis {cv['filename']} gagal. CV ini akan diberi skor 0.")
    for crit in active_criteria:
        result_data[crit] = 0
    result_data['level'] = 'Gagal Diproses'

def _generate_narrative_report(client, top_candidates_df, domain, active_criteria):
    """Fungsi untuk membuat laporan naratif, sekarang diaktifkan kembali."""
    if top_candidates_df.empty:
        return "Tidak ada kandidat untuk dilaporkan."
    try:
        context = f"Data skor {len(top_candidates_df)} kandidat teratas untuk domain '{domain}':\n\n"
        for _, row in top_candidates_df.iterrows():
            context += f"--- Kandidat: {row['nama_file']} | Level: {row.get('level', 'N/A')} | Skor Akhir: {row.get('skor_akhir_100', 0):.1f}/100\nRincian Skor Mentah (0-10):\n"
            for crit in active_criteria:
                context += f"- {crit}: {row.get(crit, 0)}\n"
            context += "\n"
        
        narrative_prompt = get_narrative_prompt(context, domain)
        response = client.chat.completions.create(
            model=MODEL_NARRATIVE,
            temperature=0.3,
            messages=[{"role": "user", "content": narrative_prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"**[Peringatan]** Gagal membuat laporan naratif: `{e}`"

def score_and_analyze_cvs(client, cv_texts, domain, active_criteria, user_weights, progress_callback, jd_text=None):
    """Fungsi analisis dengan loop for biasa dan logika skor yang sudah benar."""
    results = []
    scoring_prompt = get_scoring_prompt(domain, active_criteria, jd_text)
    
    for i, cv in enumerate(cv_texts):
        progress_callback((i + 1) / len(cv_texts), f"Menilai {cv['filename']}...")
        result_data = {"nama_file": cv["filename"]}
        try:
            response = client.chat.completions.create(
                model=MODEL_SCORING, 
                response_format={"type": "json_object"}, 
                temperature=0, 
                messages=[{"role": "system", "content": scoring_prompt}, {"role": "user", "content": cv["text"]}]
            )
            result_data.update(json.loads(response.choices[0].message.content))
        except Exception as e:
            _handle_json_error(e, cv, result_data, active_criteria)

        results.append(result_data)
        time.sleep(1)

    if not results: return {"scores": [], "narrative": "Tidak ada hasil."}
    
    df_scores = pd.DataFrame(results).fillna(0)
    if 'level' in df_scores.columns:
        df_scores['level'] = df_scores['level'].astype(str)
    
    # --- REVISI 1: Logika skoring diperbaiki agar menghitung dengan benar ---
    valid_criteria = [c for c in active_criteria if c in df_scores.columns]
    
    if not valid_criteria: # Jika tidak ada kriteria yang valid, beri skor 0
        df_scores['skor_akhir_100'] = 0
    else:
        # Konversi skor mentah ke tipe numerik, paksa error menjadi NaN lalu isi dengan 0
        for crit in valid_criteria:
            df_scores[crit] = pd.to_numeric(df_scores[crit], errors='coerce').fillna(0)
            
        # Perhitungan skor dengan bobot
        weighted_scores = df_scores[valid_criteria].mul(pd.Series(user_weights)[valid_criteria], axis=1)
        df_scores["total_score_raw"] = weighted_scores.sum(axis=1)
        
        # Hitung skor maksimal yang mungkin berdasarkan bobot
        max_possible_score = sum(10 * user_weights.get(crit, 0) for crit in valid_criteria)
        
        # Hitung skor akhir dari 100
        if max_possible_score > 0:
            df_scores['skor_akhir_100'] = (df_scores['total_score_raw'] / max_possible_score) * 100
        else:
            df_scores['skor_akhir_100'] = 0
    
    df_scores = df_scores.sort_values("skor_akhir_100", ascending=False).reset_index(drop=True)
    
    # --- REVISI 2: Memanggil kembali fungsi laporan naratif ---
    narrative_report = _generate_narrative_report(client, df_scores.head(3), domain, active_criteria)
    
    return {"scores": df_scores.to_dict('records'), "narrative": narrative_report}