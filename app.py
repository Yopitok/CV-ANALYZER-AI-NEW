# File: app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import logging

# Impor dengan struktur folder baru yang sudah benar
from core.utils import initialize_client, init_session_state
from core.parsing import parse_cvs, parse_single_document
from core.services import summarize_cv, recommend_on_cv, compare_cvs
from core.analysis import score_and_analyze_cvs
from config import settings

# ==============================================================================
# --- Definisi Fungsi untuk Setiap Tab (Logika Kembali ke Awal) ---
# ==============================================================================

def render_upload_tab():
    """Merender konten untuk Tab 1: Upload CV."""
    st.header("1. Upload CV (Format PDF)")
    st.info("Unggah satu atau lebih file CV di sini untuk mengaktifkan fitur analisis di tab lainnya.")
    uploaded_files = st.file_uploader(
        "Pilih file...", type=["pdf"], 
        accept_multiple_files=True, key="main_uploader"
    )
    if st.button("Proses File", type="primary", disabled=not uploaded_files, use_container_width=True):
        with st.spinner("Mengekstrak teks dari semua file PDF..."):
            # Reset state lama sebelum mengisi yang baru
            st.session_state.cv_texts = []
            st.session_state.analysis_results = None 
            for key in list(st.session_state.keys()):
                if key.startswith('summary_') or key.startswith('recommendation_'):
                    del st.session_state[key]

            cv_data, errors = parse_cvs(uploaded_files)
            st.session_state.cv_texts = cv_data
            for error in errors:
                st.error(error)
        if st.session_state.cv_texts:
            st.success(f"✅ {len(st.session_state.cv_texts)} CV berhasil diproses!")

def render_summary_tab(client):
    """Merender konten untuk Tab 2: Ringkasan (Gaya Lama dengan Tombol)."""
    st.header("🔍 Ringkasan CV Cepat")
    if not st.session_state.get("cv_texts"):
        st.info("⬅️ Silakan upload dan proses CV di Tab 1 terlebih dahulu.")
        return
        
    cv_filenames = [cv['filename'] for cv in st.session_state.cv_texts]
    selected_filename = st.selectbox("Pilih CV untuk dilihat ringkasannya:", cv_filenames, key="summary_selectbox")
    selected_cv = next((cv for cv in st.session_state.cv_texts if cv['filename'] == selected_filename), None)

    if selected_cv:
        with st.container(border=True):
            st.subheader(f"Ringkasan untuk: {selected_cv['filename']}")
            cache_key = f"summary_{selected_cv['filename']}"
            if cache_key in st.session_state:
                st.markdown(st.session_state[cache_key])
            else:
                st.info("Klik tombol di bawah untuk membuat ringkasan dengan AI.")
            
            if st.button("Buat / Perbarui Ringkasan", key=f"summary_btn_{selected_cv['filename']}", use_container_width=True):
                with st.spinner("AI sedang meringkas..."):
                    summary = summarize_cv(client, selected_cv['text'])
                    st.session_state[cache_key] = summary
                    st.rerun()

def render_recommend_tab(client):
    """Merender konten untuk Tab 3: Rekomendasi (Gaya Lama dengan Tombol)."""
    st.header("🤖 Rekomendasi AI per Kandidat")
    if not st.session_state.get("cv_texts"):
        st.info("⬅️ Silakan upload dan proses CV di Tab 1 terlebih dahulu.")
        return
        
    cv_filenames = [cv['filename'] for cv in st.session_state.cv_texts]
    selected_filename = st.selectbox("Pilih CV untuk mendapatkan rekomendasi:", cv_filenames, key="recommend_selectbox")
    selected_cv = next((cv for cv in st.session_state.cv_texts if cv['filename'] == selected_filename), None)
    
    if selected_cv:
        with st.container(border=True):
            st.subheader(f"Analisis untuk: {selected_cv['filename']}")
            cache_key = f"recommendation_{selected_cv['filename']}"
            if cache_key in st.session_state:
                st.markdown(st.session_state[cache_key])
            else:
                st.info("Klik tombol di bawah untuk mendapatkan rekomendasi dari AI.")
                
            if st.button("Dapatkan / Perbarui Rekomendasi AI", key=f"rec_btn_{selected_cv['filename']}", use_container_width=True, type="primary"):
                with st.spinner(f"Menganalisis {selected_cv['filename']}..."):
                    recommendation = recommend_on_cv(client, selected_cv['text'])
                    st.session_state[cache_key] = recommendation
                    st.rerun()

def render_compare_tab(client):
    """Merender konten untuk Tab 4: Perbandingan."""
    st.header("⚖️ Perbandingan Antar Kandidat")
    if not st.session_state.get("cv_texts") or len(st.session_state.get("cv_texts", [])) < 2:
        st.info("⬆️ Upload minimal 2 CV di Tab 1 untuk menggunakan fitur perbandingan.")
        return
    role = st.text_input("Bandingkan untuk posisi:", placeholder="Contoh: Senior Data Scientist")
    if st.button("Bandingkan Kandidat Sekarang", type="primary", use_container_width=True):
        if not role: st.warning("Mohon masukkan posisi yang dicari."); return
        with st.spinner("AI sedang membandingkan semua CV..."):
            comparison = compare_cvs(client, st.session_state.cv_texts, role)
            st.success("✅ Hasil Perbandingan:")
            st.markdown(comparison)

def render_dashboard_tab(client):
    """Merender konten untuk Tab 5, dengan pilihan input JD via teks atau file."""
    st.header("🏆 Dashboard Analisis & Peringkat (LLM)")
    if not st.session_state.get("cv_texts"):
        st.info("⬅️ Silakan upload CV di Tab 1 untuk analisis LLM.")
        return
    
    with st.container(border=True):
        st.subheader("⚙️ Konfigurasi Analisis")
        st.markdown("**1. (Opsional) Masukkan Deskripsi Pekerjaan (JD)**")
        jd_text = st.text_area("Tempelkan deskripsi pekerjaan di sini...", height=150, key="jd_text_area", placeholder="Contoh: Dicari seorang Data Scientist...")
        
        st.markdown("**2. Pilih Domain & Atur Bobot**")
        domain = st.selectbox("Pilih Domain Target:", settings.DOMAINS, key="domain_selector")
        active_criteria = settings.CRITERIA_MAP.get(domain, settings.CRITERIA_MAP["general"])
        default_weights = settings.WEIGHTS_MAP.get(domain, {c: 5 for c in active_criteria})
        
        with st.expander("Atur Pembobotan Kriteria (Opsional)"):
            user_weights = {}
            cols = st.columns(3)
            for i, crit in enumerate(active_criteria):
                with cols[i % 3]:
                    user_weights[crit] = st.slider(f"Bobot {crit}", 1, 10, int(default_weights.get(crit, 5)), 1, key=f"w_{domain}_{crit}")
        
        st.markdown("---")
        st.markdown("**3. Jalankan Analisis**")
        if st.button("🚀 Jalankan Analisis & Peringkat", type="primary", use_container_width=True):
            progress_bar = st.progress(0.0, "Memulai..."); 
            def progress_callback(p, t): progress_bar.progress(p,t)
            output = score_and_analyze_cvs(client, st.session_state.cv_texts, domain, active_criteria, user_weights, progress_callback, jd_text)
            st.session_state.analysis_results = {**output, "criteria": active_criteria, "domain": domain}
            progress_bar.empty()
            st.success("Analisis selesai!")

    if st.session_state.get('analysis_results'):
        _display_dashboard_results(st.session_state.analysis_results)

# --- REVISI: Mengembalikan fungsi _display_dashboard_results ke versi lengkap ---
def _display_dashboard_results(results_data):
    """Fungsi helper untuk menampilkan semua hasil dashboard dengan visualisasi lengkap."""
    st.markdown("---")
    st.subheader(f"💡 Hasil Analisis LLM (Domain: {results_data['domain'].upper()})")
    
    if not results_data.get('scores'):
        st.warning("Tidak ada data skor untuk ditampilkan.")
        return
        
    df = pd.DataFrame(results_data['scores'])
    if 'level' in df.columns:
        df['level'] = df['level'].fillna('N/A').astype(str)
    df.fillna(0, inplace=True)
    
    # Tampilkan KPI dengan st.metric
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Kandidat Dianalisis", value=len(df))
    with col2:
        avg_score = df['skor_akhir_100'].mean() if 'skor_akhir_100' in df and not df.empty else 0
        st.metric(label="Skor Rata-Rata", value=f"{avg_score:.1f} / 100")
    with col3:
        top_candidate = df.iloc[0]['nama_file'] if not df.empty else "N/A"
        st.metric(label="Kandidat Teratas", value=top_candidate)
    st.divider()

    # Tampilkan tab untuk detail
    tab_rank, tab_vis, tab_narrative = st.tabs(["🏆 Ranking", "📊 Visualisasi", "📝 Naratif"])

    with tab_rank:
        df_display = df.copy()
        df_display['Rank'] = range(1, len(df_display) + 1)
        # Pastikan kolom 'skor_akhir_100' ada sebelum digunakan di ProgressColumn
        if 'skor_akhir_100' not in df_display.columns:
            df_display['skor_akhir_100'] = 0

        display_cols = ['Rank', 'nama_file', 'skor_akhir_100'] + results_data['criteria']
        if 'level' in df_display.columns:
            display_cols.append('level')

        st.dataframe(
            df_display[[c for c in display_cols if c in df_display.columns]],
            use_container_width=True, hide_index=True,
            column_config={
                "skor_akhir_100": st.column_config.ProgressColumn(
                    "Skor AI (0-100)", format="%.1f", min_value=0, max_value=100
                )
            }
        )
        csv_data = df_display[[c for c in display_cols if c in df_display.columns]].to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Ranking (CSV)", csv_data, f"ranking_{results_data['domain']}.csv", "text/csv")

    with tab_vis:
        df_top = df.head(5).copy()
        if df_top.empty:
            st.info("Tidak ada kandidat untuk divisualisasikan.")
            return

        col1_vis, col2_vis = st.columns(2)
        with col1_vis:
            st.markdown("**Perbandingan Kriteria (Skor Mentah)**")
            fig = go.Figure()
            for _, row in df_top.iterrows():
                values = [row.get(cat, 0) for cat in results_data['criteria']]
                fig.add_trace(go.Scatterpolar(r=values, theta=results_data['criteria'], fill='toself', name=row['nama_file']))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=True, margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig, use_container_width=True)
        with col2_vis:
            st.markdown("**Skor Akhir AI (0-100)**")
            if 'skor_akhir_100' in df_top.columns:
                fig_bar = go.Figure(data=[go.Bar(x=df_top['nama_file'], y=df_top['skor_akhir_100'], text=df_top['skor_akhir_100'].round(1), textposition='auto')])
                fig_bar.update_yaxes(range=[0, 101])
                st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab_narrative:
        st.markdown("#### Analisis Naratif Mendalam")
        narrative_text = results_data.get('narrative', 'Laporan naratif tidak tersedia.')
        st.markdown(narrative_text, unsafe_allow_html=True)

# --- FUNGSI MAIN TIDAK BERUBAH ---
def main():
    st.set_page_config(page_title="CV Analyzer Pro", page_icon="🌟", layout="wide")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    st.title("📄 CV Analyzer AI")
    client = initialize_client()
    init_session_state()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📤 Upload CV", "🔍 Ringkasan", "🤖 Rekomendasi", 
        "⚖️ Perbandingan", "🏆 Dashboard Analisis"
    ])

    with tab1:
        render_upload_tab()

    if client:
        with tab2:
            render_summary_tab(client)
        with tab3:
            render_recommend_tab(client)
        with tab4:
            render_compare_tab(client)
        with tab5:
            render_dashboard_tab(client)
    else:
        st.sidebar.error("Klien API tidak dapat diinisialisasi. Periksa `secrets.toml` Anda.")

if __name__ == "__main__":
    main()