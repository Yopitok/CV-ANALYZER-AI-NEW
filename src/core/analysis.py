# File: src/core/analysis.py

import json, re, time, pandas as pd, streamlit as st
from src.config.prompts import get_scoring_prompt, get_narrative_prompt

def score_and_analyze_cvs(client, cv_texts, domain, active_criteria, user_weights, progress_callback):
    results = []
    scoring_prompt = get_scoring_prompt(domain, active_criteria)
    for i, cv in enumerate(cv_texts):
        progress_callback((i + 1) / len(cv_texts), f"Menilai {cv['filename']}...")
        try:
            # --- PERUBAHAN DI SINI ---
            response = client.chat.completions.create(
                model="llama3-70b-8192", 
                response_format={"type": "json_object"},
                temperature=0, # <-- Tambahkan ini untuk konsistensi
                messages=[{"role": "system", "content": scoring_prompt}, {"role": "user", "content": cv["text"]}]
            )
            result_data = json.loads(response.choices[0].message.content)
            result_data["nama_file"] = cv["filename"]
            results.append(result_data)
            time.sleep(1)
        except Exception as e: 
            _handle_json_error(e, cv, results)
    
    if not results: return {"scores": [], "narrative": "Tidak ada hasil."}

    df_scores = pd.DataFrame(results).fillna(0)
    
    valid_criteria = [c for c in user_weights.keys() if c in df_scores.columns]
    weighted_scores = (df_scores[valid_criteria] * pd.Series(user_weights)[valid_criteria])
    df_scores["total_score_raw"] = weighted_scores.sum(axis=1)

    max_possible_score = sum(10 * w for w in user_weights.values())
    if max_possible_score > 0:
        df_scores['skor_akhir_100'] = (df_scores['total_score_raw'] / max_possible_score) * 100
    else:
        df_scores['skor_akhir_100'] = 0

    df_scores = df_scores.sort_values("skor_akhir_100", ascending=False)
    
    narrative_report = _generate_narrative_report(client, df_scores.head(3), domain, active_criteria)
    
    return {"scores": df_scores.to_dict('records'), "narrative": narrative_report}

def _handle_json_error(e, cv, results):
    error_str = str(e)
    if 'json_validate_failed' in error_str and "'failed_generation':" in error_str:
        st.warning(f"JSON tidak valid untuk {cv['filename']}. Mencoba perbaikan...")
        try:
            failed_json_str = "{" + error_str.split("{", 1)[1].rsplit("}", 1)[0] + "}"
            cleaned_json_str = re.sub(r'(\d)"\s*,', r'\1,', failed_json_str)
            result_data = json.loads(cleaned_json_str)
            result_data["nama_file"] = cv["filename"]
            results.append(result_data)
            st.success(f"Berhasil memperbaiki {cv['filename']}!")
            time.sleep(1)
        except Exception as inner_e: 
            st.error(f"Perbaikan otomatis {cv['filename']} gagal. Detail: {inner_e}")
    else: 
        st.error(f"Error tak terduga pada {cv['filename']}: {e}")

def _generate_narrative_report(client, top_candidates_df, domain, active_criteria):
    if top_candidates_df.empty: return "Tidak ada kandidat untuk dilaporkan."
    try:
        context = f"Data skor {len(top_candidates_df)} kandidat teratas:\n\n"
        for _, row in top_candidates_df.iterrows():
            context += f"--- Kandidat: {row['nama_file']} | Level: {row.get('level', 'N/A')} | Skor Akhir (0-100): {row.get('skor_akhir_100', 0):.1f}\nRincian Skor Mentah (0-10):\n"
            for crit in active_criteria: 
                context += f"- {crit}: {row.get(crit, 'N/A')}\n"
            context += "\n"
        
        narrative_prompt = get_narrative_prompt(context, domain)
        # --- PERUBAHAN DI SINI ---
        response = client.chat.completions.create(
            model="llama3-70b-8192", 
            temperature=0, # <-- Tambahkan ini untuk konsistensi
            messages=[{"role": "user", "content": narrative_prompt}]
        )
        return response.choices[0].message.content
    except Exception:
        return "Gagal membuat laporan naratif."