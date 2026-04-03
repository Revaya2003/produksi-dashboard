import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
from utils import hitung_produksi, kebutuhan_pekerja, cari_optimal

st.set_page_config(page_title="Production Dashboard", page_icon="📊", layout="wide")

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="header-container">
    <h1 class="title">Production Planning Dashboard</h1>
    <p class="subtitle">Decision Support System by Revaya Rizqia Pasya</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### ⚙️ Parameter Input")
    total = st.number_input("Total Target (Lembar)", value=2600000, step=100000)
    target_tahun = st.number_input("Target Waktu (Tahun)", value=3.0, step=0.5)
    produktivitas = st.number_input("Produktivitas / Orang / Hari", value=135)
    
    st.markdown("---")
    mode = st.radio("Sistem Hari Kerja", ["Senin–Jumat", "Senin–Sabtu"])
    pekerja = st.slider("Pekerja (Senin-Jumat)", 1, 100, 15)
    
    if mode == "Senin–Sabtu":
        pekerja_sabtu = st.slider("Pekerja (Sabtu)", 0, 100, 5)
        hari = 6
    else:
        pekerja_sabtu = 0
        hari = 5

# HITUNG
weekly, weeks, years = hitung_produksi(total, pekerja, pekerja_sabtu, produktivitas)

# KPI CARDS
col1, col2, col3 = st.columns(3)
col1.markdown(f"""
<div class='card'>
    <div class='card-title'>⏱️ Estimasi Selesai</div>
    <div class='card-value'>{years:.2f} <span style="font-size:16px;">Tahun</span></div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class='card'>
    <div class='card-title'>📈 Output Mingguan</div>
    <div class='card-value'>{weekly:,.0f} <span style="font-size:16px;">Lembar</span></div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class='card'>
    <div class='card-title'>🎯 Target Manajemen</div>
    <div class='card-value'>{target_tahun} <span style="font-size:16px;">Tahun</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# INSIGHT & OPTIMASI (Dibuat sejajar)
col_insight, col_optimasi = st.columns(2)

with col_insight:
    st.markdown('<div class="section">📌 Status Pencapaian</div>', unsafe_allow_html=True)
    if years <= target_tahun:
        st.success("✅ **Aman!** Estimasi waktu lebih cepat atau sesuai dengan target.")
    else:
        st.error("⚠️ **Risiko!** Estimasi waktu melebihi batas target yang ditentukan.")
        butuh = kebutuhan_pekerja(total, target_tahun, produktivitas, hari)
        st.info(f"💡 **Saran Aksi:** Tambah pekerja menjadi sekitar **{butuh:.0f} orang**.")

with col_optimasi:
    st.markdown('<div class="section">🤖 Rekomendasi Optimal</div>', unsafe_allow_html=True)
    best = cari_optimal(total, target_tahun, produktivitas)
    if best:
        st.success(f"**Opsi Paling Efisien:**\n\n**{best[0]}** Pekerja Weekday + **{best[1]}** Pekerja Sabtu \n\n*(Estimasi selesai: {best[2]:.2f} tahun)*")
    else:
        st.warning("Pekerja maksimal masih belum cukup untuk mencapai target ini.")

st.markdown("---")

# GRAFIK INTERAKTIF
st.markdown('<div class="section">📊 Simulasi Progress Produksi</div>', unsafe_allow_html=True)

if weekly > 0:
    weeks_arr = np.arange(0, int(weeks) + 2)
    progress = weeks_arr * weekly

    df_plot = pd.DataFrame({"Minggu": weeks_arr, "Produksi": progress})
    fig = px.area(df_plot, x="Minggu", y="Produksi", 
                  labels={"Minggu": "Durasi (Minggu)", "Produksi": "Total Lembar"},
                  color_discrete_sequence=["#38bdf8"])
    
    fig.add_hline(y=total, line_dash="dash", line_color="#ef4444", annotation_text="Target Tercapai", annotation_position="top left")
    
    # Penyesuaian tampilan background grafik agar menyatu dengan dark mode
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)", 
        font_color="#e2e8f0", 
        margin=dict(l=0, r=0, t=20, b=0),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Masukkan jumlah pekerja untuk melihat simulasi.")
