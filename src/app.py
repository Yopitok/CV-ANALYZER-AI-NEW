# File: src/app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import logging

# Impor dari package 'src' yang sudah kita install
from src.core.utils import initialize_client, init_session_state
from src.core.parsing import parse_cvs
from src.core.services import summarize_cv, recommend_on_cv, compare_cvs
from src.core.analysis import score_and_analyze_cvs
from src.config import settings

# --- Fungsi Render untuk setiap Tab ---

def render_upload_tab():
    st.header("1. Upload CV (Format PDF)")
    st.info("Unggah satu atau lebih file CV di sini untuk memulai analisis.")
    uploaded_files = st.file_uploader(
        "Pilih file...", type=["pdf"], 
        accept_multiple_files=True, key="main_uploader"
    )
    if st.button("Proses File", type="primary", disabled=not uploaded_files, use_container_width=True):
        with st.spinner("Mengekstrak teks..."):
            cv_data, errors = parse_cvs(uploaded_files)
            st.session_state.cv_texts = cv_data
            for error in errors: st.error(error)
        if st.session_state.cv_texts:
            st.success(f"✅ {len(st.session_state['cv_texts'])} CV berhasil diproses!")
            st.session_state.analysis_results = None

def render_summary_tab(client):
    st.header("🔍 Ringkasan CV Cepat")
    if not st.session_state.get("cv_texts"): st.info("⬅️ Silakan upload CV di Tab 1."); return
    for cv in st.session_state.cv_texts:
        with st.expander(f"Tampilkan Ringkasan untuk: **{cv['filename']}**"):
            if st.button("Buat Ringkasan", key=f"summary_btn_{cv['filename']}"):
                with st.spinner("AI meringkas..."): st.markdown(summarize_cv(client, cv['text']))

def render_recommend_tab(client):
    st.header("🤖 Rekomendasi AI per Kandidat")
    if not st.session_state.get("cv_texts"): st.info("⬅️ Silakan upload CV di Tab 1."); return
    for cv in st.session_state.cv_texts:
        with st.container(border=True):
            st.subheader(f"Analisis untuk: {cv['filename']}")
            if st.button("Dapatkan Rekomendasi AI", key=f"rec_btn_{cv['filename']}", use_container_width=True):
                with st.spinner(f"Menganalisis {cv['filename']}..."): st.markdown(recommend_on_cv(client, cv['text']))

def render_compare_tab(client):
    st.header("⚖️ Perbandingan Antar Kandidat")
    if not st.session_state.get("cv_texts") or len(st.session_state.get("cv_texts", [])) < 2:
        st.info("⬆️ Upload minimal 2 CV di Tab 1 untuk perbandingan."); return
    role = st.text_input("Bandingkan untuk posisi:", placeholder="Contoh: Senior Data Scientist")
    if st.button("Bandingkan Kandidat", type="primary", use_container_width=True):
        if not role: st.warning("Mohon masukkan posisi."); return
        with st.spinner("AI membandingkan..."):
            st.success("✅ Hasil Perbandingan:"); st.markdown(compare_cvs(client, st.session_state.cv_texts, role))

def render_dashboard_tab(client):
    """Merender konten untuk Tab 5, diadaptasi dari kode referensi."""
    st.header("🏆 Dashboard Analisis & Peringkat Kandidat")
    if not st.session_state.get("cv_texts"): st.info("⬅️ Silakan upload CV di Tab 1."); return
    
    with st.container(border=True):
        st.subheader("⚙️ Konfigurasi Analisis & Pembobotan")
        domain = st.selectbox("Pilih Domain Target:", settings.DOMAINS, key="domain_selector")
        active_criteria = settings.CRITERIA_MAP.get(domain, settings.CRITERIA_MAP["general"])
        default_weights = settings.WEIGHTS_MAP.get(domain, {c: 5 for c in active_criteria})
        
        st.markdown("---"); st.markdown("**Atur Pembobotan Kriteria (Skala 1 - 10)**")
        user_weights = {}
        cols = st.columns(3)
        for i, crit in enumerate(active_criteria):
            with cols[i % 3]:
                user_weights[crit] = st.slider(f"Bobot {crit}", 1, 10, int(default_weights.get(crit, 5)), 1, key=f"w_{domain}_{crit}")
        st.markdown("---")
        
        if st.button("🚀 Jalankan Analisis & Buat Peringkat", type="primary", use_container_width=True):
            progress_bar = st.progress(0.0, "Memulai..."); 
            def progress_callback(p, t): progress_bar.progress(p,t)
            output = score_and_analyze_cvs(client, st.session_state.cv_texts, domain, active_criteria, user_weights, progress_callback)
            st.session_state.analysis_results = {**output, "criteria": active_criteria, "domain": domain}
            progress_bar.empty(); st.success("Analisis selesai!")

    if st.session_state.get('analysis_results') and st.session_state.analysis_results['domain'] == domain:
        _display_dashboard_results(st.session_state.analysis_results)

def _display_dashboard_results(results_data):
    """Fungsi helper untuk menampilkan semua hasil dashboard."""
    st.markdown("---"); st.subheader(f"💡 Hasil Analisis (Domain: {results_data['domain'].upper()})")
    if not results_data['scores']: st.warning("Tidak ada data skor."); return
    
    df = pd.DataFrame(results_data['scores'])
    res_tab_rank, res_tab_vis, res_tab_narrative = st.tabs(["🏆 Ranking (Terbobot)", "📊 Visualisasi", "📝 Analisis Naratif"])

    with res_tab_rank:
        df['Rank'] = range(1, len(df) + 1)
        display_cols = ['Rank', 'nama_file', 'skor_akhir_100'] + results_data['criteria'] + ['level']
        st.dataframe(
            df[[c for c in display_cols if c in df.columns]],
            use_container_width=True, hide_index=True,
            column_config={"skor_akhir_100": st.column_config.ProgressColumn(
                "Skor Akhir (0-100)", format="%.1f", min_value=0, max_value=100
            )}
        )

    with res_tab_vis:
        df_top = df.head(5)
        col_vis1, col_vis2 = st.columns(2)
        with col_vis1:
            st.markdown("**Perbandingan Kriteria (Skor Mentah)**")
            fig_radar = go.Figure()
            for _, row in df_top.iterrows():
                values = [row.get(cat, 0) for cat in results_data['criteria']]
                fig_radar.add_trace(go.Scatterpolar(r=values, theta=results_data['criteria'], fill='toself', name=row['nama_file']))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=True, title="Perbandingan Skor Mentah")
            st.plotly_chart(fig_radar, use_container_width=True)
        with col_vis2:
            st.markdown("**Skor Akhir Kandidat (0-100)**")
            fig_bar = go.Figure(data=[go.Bar(x=df_top['nama_file'], y=df_top['skor_akhir_100'], text=df_top['skor_akhir_100'].round(1), textposition='auto')])
            fig_bar.update_yaxes(range=[0, 101]); fig_bar.update_layout(title="Peringkat Skor Akhir")
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with res_tab_narrative:
        st.markdown("#### Analisis Naratif Mendalam")
        st.markdown(results_data['narrative'], unsafe_allow_html=True)

# --- Fungsi Utama Aplikasi ---
def main():
    st.set_page_config(page_title="CV Analyzer Pro", page_icon="🌟", layout="wide")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    st.title("📄 CV Analyzer AI")
    client = initialize_client()
    init_session_state()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📤 Upload CV", "🔍 Ringkasan", "🤖 Rekomendasi", "⚖️ Perbandingan", "🏆 Dashboard Analisis"])

    with tab1: render_upload_tab()
    if client:
        with tab2: render_summary_tab(client)
        with tab3: render_recommend_tab(client)
        with tab4: render_compare_tab(client)
        with tab5: render_dashboard_tab(client)
    else:
        st.warning("Harap periksa konfigurasi API Key Anda di `.streamlit/secrets.toml` untuk mengaktifkan semua fitur.")

if __name__ == "__main__":
    main()