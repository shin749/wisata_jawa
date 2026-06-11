import streamlit as st
import json
import os
from PIL import Image

# ──────────────────────────────────────────────
# CONFIG & LOAD DATA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Wisata Pulau Jawa",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(__file__)

@st.cache_data
def load_data():
    data_path = os.path.join(BASE_DIR, "data", "wisata.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

DATA = load_data()

def load_image(path_relatif):
    """Buka gambar lokal dan potong bagian tengahnya agar seragam tanpa gepeng."""
    full_path = os.path.join(BASE_DIR, path_relatif)
    img = Image.open(full_path)
    
    #(Lebar, Tinggi)
    target_width = 600
    target_height = 400
    
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height
    
    if img_ratio > target_ratio:
        new_width = int(target_ratio * img.height)
        offset = (img.width - new_width) // 2
        img_cropped = img.crop((offset, 0, img.width - offset, img.height))
    else:
        new_height = int(img.width / target_ratio)
        offset = (img.height - new_height) // 2
        img_cropped = img.crop((0, offset, img.width, img.height - offset))
        
    return img_cropped.resize((target_width, target_height))

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --hijau-tua:  #1a4a3a;
    --hijau-mid:  #2d7a5f;
    --hijau-muda: #4caf88;
    --emas:       #d4a843;
    --emas-muda:  #f0c875;
    --krem:       #faf6ef;
    --putih:      #ffffff;
    --abu-gelap:  #2a2a2a;
    --abu-mid:    #555555;
    --abu-muda:   #f0ede8;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--krem);
    color: var(--abu-gelap);
}

/* ── Hero Header ── */
.hero-header {
    background: linear-gradient(135deg, var(--hijau-tua) 0%, var(--hijau-mid) 60%, #1a5c45 100%);
    border-radius: 20px;
    padding: 50px 40px;
    margin-bottom: 30px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(26,74,58,0.3);
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 70% 30%, rgba(212,168,67,0.15) 0%, transparent 50%),
                radial-gradient(circle at 20% 70%, rgba(76,175,136,0.1) 0%, transparent 40%);
}
.hero-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 900;
    color: var(--putih);
    letter-spacing: -0.5px;
    margin: 0 0 10px 0;
    position: relative;
}
.hero-header h1 span { color: var(--emas-muda); }
.hero-header p {
    font-size: 1.1rem;
    color: rgba(255,255,255,0.85);
    margin: 0;
    font-weight: 300;
    position: relative;
}

/* ── Kartu Info (nama, lokasi, badge) ── */
.kartu-body {
    background: var(--putih);
    border-radius: 0 0 16px 16px;
    padding: 14px 16px 16px;
    border: 1px solid rgba(0,0,0,0.06);
    border-top: none;
    box-shadow: 0 4px 15px rgba(0,0,0,0.07);
}
.kartu-nama {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--hijau-tua);
    margin: 0 0 5px 0;
    line-height: 1.3;
}
.kartu-lokasi {
    font-size: 0.8rem;
    color: var(--abu-mid);
    margin: 0 0 10px 0;
}
.kartu-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.74rem;
    font-weight: 600;
}
.badge-alam    { background:#e8f5ee; color:#1a7a4a; }
.badge-budaya  { background:#fff4e0; color:#a06800; }
.badge-kuliner { background:#fce8e8; color:#c0392b; }
.kartu-rating  { font-size: 0.85rem; color: var(--emas); font-weight: 600; }

/* Bungkus gambar kartu */
.kartu-img-wrap {
    border-radius: 16px 16px 0 0;
    overflow: hidden;
    line-height: 0;
}
.kartu-img-wrap img {
    border-radius: 16px 16px 0 0 !important;
    width: 100% !important;
    height: 200px !important;
    object-fit: cover !important;
    display: block !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background: var(--hijau-tua) !important; }
section[data-testid="stSidebar"] * { color: var(--putih) !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextInput label {
    color: var(--emas-muda) !important;
    font-weight: 600;
}
section[data-testid="stSidebar"] input {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: var(--abu-gelap) !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    color: var(--abu-gelap) !important;
}
.sidebar-brand {
    text-align: center;
    padding: 10px 0 25px;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 25px;
}
.sidebar-brand h3 {
    font-family: 'Playfair Display', serif;
    color: var(--emas-muda) !important;
    font-size: 1.2rem;
    margin: 8px 0 4px;
}
.sidebar-brand p { font-size: 0.8rem; color: rgba(255,255,255,0.6) !important; margin: 0; }
.stat-box {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 12px 15px;
    text-align: center;
    margin-top: 20px;
}
.stat-box .stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--emas-muda) !important;
}
.stat-box .stat-label { font-size: 0.78rem; color: rgba(255,255,255,0.7) !important; }

/* ── Detail ── */
.detail-header {
    background: linear-gradient(180deg, rgba(26,74,58,0.03) 0%, transparent 100%);
    border-radius: 16px;
    padding: 25px;
    margin-bottom: 20px;
    border-left: 4px solid var(--hijau-mid);
}
.detail-nama {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.6rem, 4vw, 2.4rem);
    font-weight: 900;
    color: var(--hijau-tua);
    margin: 0 0 8px 0;
    line-height: 1.2;
}
.detail-lokasi { font-size: 1rem; color: var(--abu-mid); margin: 0; }
.info-chip {
    display: inline-flex;
    align-items: flex-start;
    gap: 6px;
    background: var(--abu-muda);
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 0.88rem;
    color: var(--abu-gelap);
    margin: 4px;
    flex-direction: column;
}
.info-chip .info-label {
    font-weight: 600;
    color: var(--hijau-tua);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.tips-box {
    background: linear-gradient(135deg, #fffbf0, #fff8e6);
    border: 1px solid var(--emas-muda);
    border-radius: 12px;
    padding: 18px 20px;
    margin-top: 15px;
}
.tips-box .tips-title {
    font-weight: 700;
    color: var(--emas);
    margin-bottom: 6px;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Tombol ── */
.stButton > button {
    background: var(--hijau-tua) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button:hover { background: var(--hijau-mid) !important; }

/* ── Misc ── */
.hasil-info {
    background: var(--abu-muda);
    border-radius: 10px;
    padding: 10px 18px;
    margin-bottom: 20px;
    font-size: 0.9rem;
    color: var(--abu-mid);
    border-left: 3px solid var(--hijau-mid);
}
.footer {
    text-align: center;
    padding: 30px 0 10px;
    color: var(--abu-mid);
    font-size: 0.82rem;
    border-top: 1px solid rgba(0,0,0,0.08);
    margin-top: 50px;
}
div[data-testid="stImage"] img { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────
if "halaman" not in st.session_state:
    st.session_state.halaman = "beranda"
if "wisata_terpilih" not in st.session_state:
    st.session_state.wisata_terpilih = None

def buka_detail(wisata_id):
    st.session_state.halaman = "detail"
    st.session_state.wisata_terpilih = wisata_id

def kembali_beranda():
    st.session_state.halaman = "beranda"
    st.session_state.wisata_terpilih = None

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div style="font-size:2.5rem;">🌴</div>
        <h3>Wisata Jawa</h3>
        <p>Jelajahi keindahan Pulau Jawa</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🔍 Cari Destinasi**")
    cari = st.text_input("", placeholder="Nama tempat atau kota...", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    provinsi_list = ["Semua Provinsi"] + sorted(set(w["provinsi"] for w in DATA))
    pilih_provinsi = st.selectbox("🗺️ Provinsi", provinsi_list)

    kategori_list = ["Semua Kategori"] + sorted(set(w["kategori"] for w in DATA))
    pilih_kategori = st.selectbox("🏷️ Kategori", kategori_list)

    total_filtered = len([
        w for w in DATA
        if (pilih_provinsi == "Semua Provinsi" or w["provinsi"] == pilih_provinsi)
        and (pilih_kategori == "Semua Kategori" or w["kategori"] == pilih_kategori)
        and (cari.lower() in w["nama"].lower() or cari.lower() in w["kota"].lower() if cari else True)
    ])
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-num">{total_filtered}</div>
        <div class="stat-label">Destinasi ditemukan</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    provinsi_counts = {}
    for w in DATA:
        provinsi_counts[w["provinsi"]] = provinsi_counts.get(w["provinsi"], 0) + 1

    st.markdown("**📊 Distribusi Provinsi**")
    for prov, jumlah in sorted(provinsi_counts.items(), key=lambda x: -x[1]):
        bar_width = int((jumlah / max(provinsi_counts.values())) * 100)
        st.markdown(f"""
        <div style="margin-bottom:6px;">
            <div style="display:flex;justify-content:space-between;font-size:0.78rem;
                        color:rgba(255,255,255,0.75);margin-bottom:2px;">
                <span>{prov}</span><span>{jumlah}</span>
            </div>
            <div style="background:rgba(255,255,255,0.15);border-radius:4px;height:5px;">
                <div style="background:#d4a843;width:{bar_width}%;height:100%;border-radius:4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def filter_data():
    hasil = DATA
    if cari:
        q = cari.lower()
        hasil = [w for w in hasil if q in w["nama"].lower() or q in w["kota"].lower()
                 or q in w["provinsi"].lower() or q in w["deskripsi"].lower()]
    if pilih_provinsi != "Semua Provinsi":
        hasil = [w for w in hasil if w["provinsi"] == pilih_provinsi]
    if pilih_kategori != "Semua Kategori":
        hasil = [w for w in hasil if w["kategori"] == pilih_kategori]
    return hasil

def badge_html(kategori):
    cls  = {"Alam": "badge-alam", "Budaya": "badge-budaya", "Kuliner": "badge-kuliner"}.get(kategori, "badge-alam")
    ikon = {"Alam": "🌿", "Budaya": "🏛️", "Kuliner": "🍜"}.get(kategori, "📍")
    return f'<span class="kartu-badge {cls}">{ikon} {kategori}</span>'

def tampilkan_kartu(w, key_prefix):
    """Render satu kartu wisata menggunakan st.image() untuk gambar lokal."""
    try:
        img = load_image(w["gambar"])
        st.markdown('<div class="kartu-img-wrap">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        st.markdown(
            f'<div class="kartu-img-wrap" style="background:#1a4a3a;height:200px;'
            f'display:flex;align-items:center;justify-content:center;'
            f'color:white;font-size:2rem;border-radius:16px 16px 0 0;">🏝️</div>',
            unsafe_allow_html=True,
        )

    # Info kartu
    st.markdown(f"""
    <div class="kartu-body">
        <p class="kartu-nama">{w['nama']}</p>
        <p class="kartu-lokasi">📍 {w['kota']}, {w['provinsi']}</p>
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:4px;">
            {badge_html(w['kategori'])}
            <span class="kartu-rating">⭐ {w['rating']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.button(
        "Lihat Detail →",
        key=f"{key_prefix}_{w['id']}",
        on_click=buka_detail,
        args=(w["id"],),
        use_container_width=True,
    )

# ──────────────────────────────────────────────
# HALAMAN BERANDA
# ──────────────────────────────────────────────
if st.session_state.halaman == "beranda":

    st.markdown("""
    <div class="hero-header">
        <h1>Jelajahi <span>Pulau Jawa</span></h1>
        <p>30 destinasi wisata terbaik dari 6 provinsi di Pulau Jawa — alam, budaya, dan sejarah</p>
    </div>
    """, unsafe_allow_html=True)

    wisata_tampil = filter_data()

    if not wisata_tampil:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;">
            <div style="font-size:4rem;">🔍</div>
            <h3 style="color:#555;font-family:'Playfair Display',serif;">Destinasi Tidak Ditemukan</h3>
            <p style="color:#888;">Coba kata kunci lain atau ubah filter di samping.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        if cari or pilih_provinsi != "Semua Provinsi" or pilih_kategori != "Semua Kategori":
            label_filter = []
            if cari:
                label_filter.append(f'pencarian "<b>{cari}</b>"')
            if pilih_provinsi != "Semua Provinsi":
                label_filter.append(f"provinsi <b>{pilih_provinsi}</b>")
            if pilih_kategori != "Semua Kategori":
                label_filter.append(f"kategori <b>{pilih_kategori}</b>")
            st.markdown(
                f'<div class="hasil-info">Menampilkan <b>{len(wisata_tampil)}</b> hasil '
                f'untuk {" · ".join(label_filter)}</div>',
                unsafe_allow_html=True,
            )

        for i in range(0, len(wisata_tampil), 3):
            cols = st.columns(3, gap="medium")
            for j, w in enumerate(wisata_tampil[i:i + 3]):
                with cols[j]:
                    tampilkan_kartu(w, "btn")

    st.markdown(
        '<div class="footer">🌴 Wisata Pulau Jawa · Data dari Wikipedia · Dibuat dengan Streamlit</div>',
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────
# HALAMAN DETAIL
# ──────────────────────────────────────────────
elif st.session_state.halaman == "detail" and st.session_state.wisata_terpilih:
    w = next((x for x in DATA if x["id"] == st.session_state.wisata_terpilih), None)

    if not w:
        st.error("Data tidak ditemukan.")
        st.button("← Kembali", on_click=kembali_beranda)
    else:
        col_back, _ = st.columns([1, 5])
        with col_back:
            st.button("← Kembali", on_click=kembali_beranda)

        col_img, col_info = st.columns([1.1, 1], gap="large")

        with col_img:
            try:
                img = load_image(w["gambar"])
                st.image(img, use_container_width=True)
            except Exception:
                st.markdown(
                    '<div style="background:#1a4a3a;height:350px;border-radius:16px;'
                    'display:flex;align-items:center;justify-content:center;'
                    'color:white;font-size:4rem;">🏝️</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)
            lat = w["koordinat"]["lat"]
            lon = w["koordinat"]["lon"]
            maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            st.markdown(f"""
            <a href="{maps_url}" target="_blank" style="
                display:block;text-align:center;
                background:#1a4a3a;color:white;
                padding:12px;border-radius:10px;
                text-decoration:none;font-weight:600;font-size:0.9rem;">
                🗺️ Buka di Google Maps
            </a>
            """, unsafe_allow_html=True)

        with col_info:
            st.markdown(f"""
            <div class="detail-header">
                <p class="detail-nama">{w['nama']}</p>
                <p class="detail-lokasi">📍 {w['kota']}, {w['provinsi']}</p>
                <div style="margin-top:12px;display:flex;align-items:center;gap:10px;">
                    {badge_html(w['kategori'])}
                    <span style="font-size:1rem;font-weight:700;color:#d4a843;">⭐ {w['rating']} / 5.0</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Deskripsi**")
            st.markdown(
                f'<p style="line-height:1.8;color:#444;font-size:0.95rem;">{w["deskripsi"]}</p>',
                unsafe_allow_html=True,
            )

            st.markdown("<br>**Informasi Kunjungan**", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;">
                <div class="info-chip">
                    <span class="info-label">Jam Buka</span>🕐 {w['jam_buka']}
                </div>
                <div class="info-chip">
                    <span class="info-label">Tiket Masuk</span>🎫 {w['harga_tiket']}
                </div>
                <div class="info-chip">
                    <span class="info-label">Alamat</span>📌 {w['alamat']}
                </div>
                <div class="info-chip">
                    <span class="info-label">Koordinat</span>🌐 {w['koordinat']['lat']}, {w['koordinat']['lon']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="tips-box" style="margin-top:18px;">
                <p class="tips-title">💡 Tips Perjalanan</p>
                <p style="margin:0;font-size:0.9rem;color:#555;line-height:1.7;">{w['tips']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Rekomendasi
        rekomendasi = [x for x in DATA if x["provinsi"] == w["provinsi"] and x["id"] != w["id"]][:3]
        if rekomendasi:
            st.markdown("---")
            st.markdown(f"### Wisata Lain di {w['provinsi']}")
            rec_cols = st.columns(3, gap="medium")
            for idx, r in enumerate(rekomendasi):
                with rec_cols[idx]:
                    tampilkan_kartu(r, "rec")
