import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import datetime

# --- KONFIGURASI HALAMAN STREAMLIT ---
st.set_page_config(
    page_title="Sistem Antrian Puskesmas",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]


def waktu_sekarang():
    n = datetime.now()
    tanggal = f"{HARI[n.weekday()]}, {n.day} {BULAN[n.month - 1]} {n.year}"
    jam = n.strftime("%H:%M:%S")
    return tanggal, jam


def tambah_log(tiket, kejadian, jenis):
    """Catat satu riwayat (ditampilkan sebagai baris tabel)."""
    tgl, jam = waktu_sekarang()
    st.session_state.logs.append(
        {"waktu": f"{tgl} • {jam}", "tiket": tiket, "kejadian": kejadian, "jenis": jenis}
    )


# =========================================================================
# FUNGSI SUARA (BUNYI "TING-TING" + SUARA "SILAHKAN AMBIL KARTU")
# =========================================================================
def mainkan_suara(teks="Silahkan ambil kartu di loket"):
    # time.time() dimasukkan supaya script dianggap baru dan suara diputar tiap klik
    components.html(
        f"""
<script>
/* {time.time()} */
(function () {{
    try {{
        const AC = window.AudioContext || window.webkitAudioContext;
        const ctx = new AC();
        ctx.resume();
        function beep(freq, start, dur) {{
            const o = ctx.createOscillator();
            const g = ctx.createGain();
            o.type = 'sine';
            o.frequency.value = freq;
            o.connect(g);
            g.connect(ctx.destination);
            const t = ctx.currentTime + start;
            g.gain.setValueAtTime(0.0001, t);
            g.gain.exponentialRampToValueAtTime(0.5, t + 0.02);
            g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
            o.start(t);
            o.stop(t + dur + 0.05);
        }}
        beep(880, 0, 0.25);
        beep(1175, 0.3, 0.4);
    }} catch (e) {{}}

    try {{
        let sudah = false;
        function ucapkan() {{
            if (sudah) {{ return; }}
            sudah = true;
            const u = new SpeechSynthesisUtterance('{teks}');
            u.lang = 'id-ID';
            u.pitch = 1.8;   // nada tinggi = lebih imut
            u.rate = 1.05;
            u.volume = 1;

            // Cari suara cewek berbahasa Indonesia
            const semua = window.speechSynthesis.getVoices();
            const indo = semua.filter(function (v) {{
                return v.lang && v.lang.toLowerCase().replace('_', '-').indexOf('id') === 0;
            }});
            const cowok = /ardi|\\bmale\\b|pria|andika/i;
            const cewek = /gadis|female|wanita|damayanti|google/i;
            const pilih =
                indo.find(function (v) {{ return cewek.test(v.name) && !cowok.test(v.name); }}) ||
                indo.find(function (v) {{ return !cowok.test(v.name); }}) ||
                indo[0];
            if (pilih) {{ u.voice = pilih; }}

            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(u);
        }}

        setTimeout(function () {{
            if (window.speechSynthesis.getVoices().length === 0) {{
                window.speechSynthesis.onvoiceschanged = ucapkan;
                setTimeout(ucapkan, 400);
            }} else {{
                ucapkan();
            }}
        }}, 800);
    }} catch (e) {{}}
}})();
</script>
""",
        height=0,
    )


# =========================================================================
# CSS CUSTOM (HANYA TAMPILAN)
# =========================================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Roboto+Mono:wght@500;700&display=swap');

/* Font hanya di elemen teks, supaya ikon bawaan Streamlit tidak tertimpa */
.stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label, .stApp button, .stApp li {
    font-family: 'Poppins', sans-serif;
}

/* ---------- BACKGROUND BERGAMBAR PUSKESMAS ---------- */
.stApp {
    background-image:
        /* 1. Ilustrasi gedung puskesmas + pohon di bagian bawah */
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 260'%3E%3Cg opacity='0.20'%3E%3Crect x='0' y='240' width='1200' height='20' fill='%230f766e'/%3E%3Crect x='96' y='185' width='9' height='55' fill='%230f766e'/%3E%3Ccircle cx='100' cy='170' r='34' fill='%2314b8a6'/%3E%3Ccircle cx='72' cy='195' r='22' fill='%2314b8a6'/%3E%3Ccircle cx='130' cy='195' r='22' fill='%2314b8a6'/%3E%3Crect x='1094' y='185' width='9' height='55' fill='%230f766e'/%3E%3Ccircle cx='1098' cy='170' r='34' fill='%2314b8a6'/%3E%3Ccircle cx='1070' cy='195' r='22' fill='%2314b8a6'/%3E%3Ccircle cx='1128' cy='195' r='22' fill='%2314b8a6'/%3E%3Crect x='250' y='165' width='130' height='75' fill='%230891b2'/%3E%3Crect x='820' y='165' width='130' height='75' fill='%230891b2'/%3E%3Crect x='380' y='120' width='440' height='120' fill='%230d9488'/%3E%3Cpolygon points='360,120 600,70 840,120' fill='%230f766e'/%3E%3Ccircle cx='600' cy='106' r='22' fill='white'/%3E%3Crect x='595' y='92' width='10' height='28' rx='2' fill='%23dc2626'/%3E%3Crect x='586' y='101' width='28' height='10' rx='2' fill='%23dc2626'/%3E%3Crect x='410' y='150' width='50' height='38' rx='3' fill='white'/%3E%3Crect x='480' y='150' width='50' height='38' rx='3' fill='white'/%3E%3Crect x='670' y='150' width='50' height='38' rx='3' fill='white'/%3E%3Crect x='740' y='150' width='50' height='38' rx='3' fill='white'/%3E%3Crect x='568' y='172' width='64' height='68' rx='4' fill='%230891b2'/%3E%3Crect x='598' y='172' width='4' height='68' fill='white'/%3E%3Crect x='275' y='190' width='40' height='30' rx='3' fill='white'/%3E%3Crect x='325' y='190' width='40' height='30' rx='3' fill='white'/%3E%3Crect x='835' y='190' width='40' height='30' rx='3' fill='white'/%3E%3Crect x='885' y='190' width='40' height='30' rx='3' fill='white'/%3E%3C/g%3E%3C/svg%3E"),
        /* 2. Pola palang medis tipis */
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'%3E%3Cg fill='%230d9488' fill-opacity='0.07'%3E%3Crect x='56' y='46' width='8' height='28' rx='2'/%3E%3Crect x='46' y='56' width='28' height='8' rx='2'/%3E%3C/g%3E%3Ccircle cx='10' cy='10' r='3' fill='%230891b2' fill-opacity='0.08'/%3E%3Ccircle cx='110' cy='110' r='3' fill='%230891b2' fill-opacity='0.08'/%3E%3C/svg%3E"),
        /* 3. Cahaya lembut + gradasi dasar */
        radial-gradient(circle at 10% 0%, rgba(20,184,166,.12) 0, transparent 40%),
        radial-gradient(circle at 100% 20%, rgba(14,165,233,.12) 0, transparent 40%),
        linear-gradient(160deg, #ccfbf1 0%, #e0f2fe 50%, #dbeafe 100%);
    background-repeat: no-repeat, repeat, no-repeat, no-repeat, no-repeat;
    background-position: center bottom, 0 0, 0 0, 0 0, 0 0;
    background-size: 100% auto, 120px 120px, auto, auto, auto;
    background-attachment: fixed, fixed, fixed, fixed, fixed;
}
.block-container { padding-top: 2rem; max-width: 1200px; }
header[data-testid="stHeader"] { background: transparent; }

/* TAMBAHAN: sembunyikan tombol "Deploy" dan menu titik tiga (⋮) di kanan atas
   (stToolbar sengaja DIHAPUS dari daftar ini karena ikut menyembunyikan tombol sidebar) */
[data-testid="stAppDeployButton"],
[data-testid="stDeployButton"],
[data-testid="stMainMenu"],
.stDeployButton,
#MainMenu {
    display: none !important;
    visibility: hidden !important;
}

/* Tombol buka sidebar saat sidebar tertutup (dibuat selalu tampil di kiri atas) */
[data-testid="stExpandSidebarButton"],
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 12px !important;
    left: 12px !important;
    z-index: 999999 !important;
    background: #0f172a !important;
    border-radius: 12px !important;
    padding: 6px !important;
}
[data-testid="stExpandSidebarButton"] *,
[data-testid="collapsedControl"] * {
    color: white !important;
    fill: white !important;
}

/* ---------- HEADER PUSKESMAS ---------- */
.hero {
    position: relative;
    background: linear-gradient(120deg, #0f766e 0%, #0d9488 45%, #0891b2 100%);
    border-radius: 24px;
    padding: 26px 34px;
    color: white;
    box-shadow: 0 14px 34px rgba(13, 148, 136, 0.30);
    margin-bottom: 18px;
    overflow: hidden;
    display: flex; align-items: center; gap: 22px; flex-wrap: wrap;
}
.hero::before {
    content: ""; position: absolute; right: -60px; top: -60px;
    width: 260px; height: 260px; border-radius: 50%;
    background: rgba(255,255,255,.08);
}
.hero::after {
    content: ""; position: absolute; right: 110px; bottom: -90px;
    width: 200px; height: 200px; border-radius: 50%;
    background: rgba(255,255,255,.06);
}
.logo-cross {
    flex: 0 0 auto;
    width: 78px; height: 78px; border-radius: 22px;
    background: white;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 8px 20px rgba(0,0,0,.18);
    position: relative; z-index: 1;
}
.logo-cross::before, .logo-cross::after {
    content: ""; position: absolute; background: #dc2626; border-radius: 4px;
}
.logo-cross::before { width: 14px; height: 44px; }
.logo-cross::after  { width: 44px; height: 14px; }
.hero-text { position: relative; z-index: 1; flex: 1 1 320px; }
.hero-text .instansi {
    font-size: .78rem; font-weight: 600; letter-spacing: 2px; opacity: .9;
}
.hero h1 { margin: 2px 0 0 0; font-size: 2rem; font-weight: 800; color: white; padding: 0; line-height: 1.2; }
.hero p  { margin: 6px 0 0 0; opacity: .92; font-size: .98rem; }
.hero-info {
    position: relative; z-index: 1;
    background: rgba(255,255,255,.16);
    border: 1px solid rgba(255,255,255,.28);
    border-radius: 16px; padding: 12px 18px;
    font-size: .85rem; line-height: 1.6;
    backdrop-filter: blur(4px);
}
.hero-info b { font-weight: 700; }

/* ---------- LANGKAH PENGGUNAAN ---------- */
.steps {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;
    margin-bottom: 26px;
}
.step {
    background: white; border-radius: 16px; padding: 14px 18px;
    border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(15,23,42,.05);
    display: flex; align-items: center; gap: 12px;
}
.step .num {
    flex: 0 0 auto; width: 34px; height: 34px; border-radius: 50%;
    background: linear-gradient(135deg, #0d9488, #0891b2); color: white;
    font-weight: 700; display: flex; align-items: center; justify-content: center;
}
.step .txt { color: #334155; font-size: .88rem; font-weight: 500; line-height: 1.35; }

/* ---------- JUDUL SEKSI ---------- */
.section-title {
    font-size: 1.15rem; font-weight: 700; color: #0f172a;
    margin: 4px 0 14px 0; display: flex; align-items: center; gap: 8px;
}
.section-title::after {
    content: ""; flex: 1; height: 2px; border-radius: 2px;
    background: linear-gradient(90deg, #99f6e4, transparent);
}

/* ---------- TOMBOL KIOS ---------- */
div[class*="st-key-btn_"] button {
    height: 92px;
    border-radius: 18px;
    border: none;
    font-size: 1.1rem;
    font-weight: 700;
    color: white;
    box-shadow: 0 8px 18px rgba(0,0,0,.14);
    transition: transform .15s ease, box-shadow .15s ease, filter .15s ease;
}
div[class*="st-key-btn_"] button p { font-size: 1.1rem; font-weight: 700; }
div[class*="st-key-btn_"] button:hover:not(:disabled) {
    transform: translateY(-3px);
    box-shadow: 0 14px 26px rgba(0,0,0,.2);
    filter: brightness(1.06);
    color: white;
}
div[class*="st-key-btn_"] button:active:not(:disabled) { transform: translateY(0) scale(.98); }
div[class*="st-key-btn_"] button:disabled {
    background: #cbd5e1 !important; color: #64748b !important;
    box-shadow: none; cursor: not-allowed;
}
.st-key-btn_bpjs button    { background: linear-gradient(135deg, #16a34a, #22c55e); }
.st-key-btn_mandiri button {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    color: #0f172a; border: 2px solid #cbd5e1;
}
.st-key-btn_mandiri button p { color: #0f172a; }
.st-key-btn_mandiri button:hover:not(:disabled) { color: #0f172a; }
.st-key-btn_online button  { background: linear-gradient(135deg, #1d4ed8, #3b82f6); }

/* ---------- TIKET (GAYA STRUK PRINTER) ---------- */
.ticket {
    position: relative;
    background: white;
    border-radius: 14px 14px 4px 4px;
    padding: 0;
    box-shadow: 0 16px 36px rgba(15, 23, 42, .16);
    border: 1px solid #e2e8f0;
    animation: pop .35s ease;
    overflow: hidden;
}
.ticket::after {
    /* tepi bergerigi seperti kertas sobek */
    content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 10px;
    background:
        linear-gradient(135deg, transparent 75%, #f1f5f9 75%) 0 0 / 14px 10px,
        linear-gradient(225deg, transparent 75%, #f1f5f9 75%) 0 0 / 14px 10px;
}
@keyframes pop {
    from { transform: translateY(-14px) scale(.96); opacity: 0; }
    to   { transform: translateY(0) scale(1);       opacity: 1; }
}
.ticket-head {
    background: linear-gradient(120deg, #0f766e, #0891b2);
    color: white; padding: 14px 22px;
    font-weight: 600; letter-spacing: 1px; font-size: .85rem;
    display: flex; justify-content: space-between; align-items: center;
}
.ticket-head .mini-cross {
    display: inline-block; position: relative; width: 20px; height: 20px;
    background: white; border-radius: 6px; margin-right: 8px; vertical-align: middle;
}
.ticket-head .mini-cross::before, .ticket-head .mini-cross::after {
    content: ""; position: absolute; background: #dc2626; border-radius: 1px;
    left: 50%; top: 50%; transform: translate(-50%, -50%);
}
.ticket-head .mini-cross::before { width: 4px; height: 12px; }
.ticket-head .mini-cross::after  { width: 12px; height: 4px; }
.ticket-sub {
    text-align: center; padding: 10px 20px 0 20px;
    color: #64748b; font-size: .75rem; line-height: 1.4;
}
.ticket-body {
    text-align: center; padding: 14px 20px 16px 20px;
    border-bottom: 3px dashed #cbd5e1; position: relative;
}
.ticket-body::before, .ticket-body::after {
    content: ""; position: absolute; bottom: -12px; width: 22px; height: 22px;
    border-radius: 50%; background: #f1f5f9; border: 1px solid #e2e8f0;
}
.ticket-body::before { left: -12px; }
.ticket-body::after  { right: -12px; }
.ticket-label { color: #64748b; font-size: .85rem; font-weight: 600; letter-spacing: 1.5px; }
.ticket-number {
    font-family: 'Roboto Mono', monospace;
    font-size: 5.2rem; font-weight: 700; line-height: 1.1;
    background: linear-gradient(120deg, #0f766e, #2563eb);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.ticket-layanan {
    display: inline-block; margin-top: 4px;
    padding: 4px 16px; border-radius: 999px; font-size: .8rem; font-weight: 600;
    background: var(--lc); color: var(--lt);
}
.ticket-meta {
    display: flex; justify-content: space-between;
    padding: 14px 24px 4px 24px; color: #475569; font-size: .8rem;
    font-family: 'Roboto Mono', monospace;
}
.ticket-foot {
    text-align: center; padding: 8px 20px 24px 20px;
    color: #475569; font-size: .85rem;
}
.ticket-foot b { color: #0f766e; }
.ticket-empty {
    background: white; border: 2px dashed #94a3b8; border-radius: 20px;
    padding: 50px 24px; text-align: center; color: #64748b;
}
.ticket-empty .icon { font-size: 3rem; margin-bottom: 8px; }

/* ---------- KARTU JUMLAH ANTRIAN ---------- */
.stat-card {
    background: white; border-radius: 18px; padding: 18px 20px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, .08);
    border: 1px solid #e2e8f0; border-top: 6px solid var(--c);
    position: relative; overflow: hidden;
}
.stat-card .ico {
    position: absolute; right: 14px; top: 12px; font-size: 1.6rem; opacity: .85;
}
.stat-name  { color: #64748b; font-size: .82rem; font-weight: 600; padding-right: 34px; }
.stat-value { font-size: 2.2rem; font-weight: 800; color: #0f172a; line-height: 1.2; }
.stat-value span { font-size: 1rem; font-weight: 500; color: #94a3b8; }
.stat-last  { font-size: .78rem; color: #64748b; margin-top: 2px; }
.stat-last b { color: var(--c); }
.bar { height: 8px; background: #e2e8f0; border-radius: 999px; margin-top: 10px; overflow: hidden; }
.bar > div { height: 100%; background: var(--c); border-radius: 999px; }
.stat-total {
    background: linear-gradient(135deg, #0f766e, #0891b2);
    border: none; border-top: 6px solid #5eead4;
}
.stat-total .stat-name, .stat-total .stat-value, .stat-total .stat-last { color: white; }
.stat-total .stat-value span { color: rgba(255,255,255,.7); }

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}
section[data-testid="stSidebar"] * { color: #e2e8f0; }
section[data-testid="stSidebar"] h2 { color: white; font-size: 1.1rem; }
section[data-testid="stSidebar"] .stButton button {
    background: #ef4444; border: none; color: white; border-radius: 12px;
    font-weight: 600; width: 100%;
}
section[data-testid="stSidebar"] .stButton button:hover { background: #dc2626; color: white; }
section[data-testid="stSidebar"] .stButton button p { color: white; }

/* ---------- LOG AKTIVITAS (teks dipaksa gelap supaya terbaca) ---------- */
div[data-testid="stExpander"] {
    background: white; border-radius: 14px; border: 1px solid #e2e8f0;
}
div[data-testid="stExpander"] *,
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] [data-testid="stText"],
div[data-testid="stExpander"] [data-testid="stText"] * {
    color: #0f172a !important;
}
div[data-testid="stExpander"] svg { fill: #0f172a !important; color: #0f172a !important; }

/* Header "Lihat Log Aktivitas Cetak" tetap terang (tidak jadi hitam)
   saat kursor diarahkan ke bagian lain, di-hover, difokus, atau diklik */
div[data-testid="stExpander"] details,
div[data-testid="stExpander"] details:hover,
div[data-testid="stExpander"] details:focus,
div[data-testid="stExpander"] details:focus-within,
div[data-testid="stExpander"] details[open],
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary:hover,
div[data-testid="stExpander"] summary:focus,
div[data-testid="stExpander"] summary:focus-visible,
div[data-testid="stExpander"] summary:active,
div[data-testid="stExpander"] details:hover > summary,
div[data-testid="stExpander"] details[open] > summary,
div[data-testid="stExpander"] details[open] > summary:hover {
    background: #f1f5f9 !important;
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    outline: none !important;
}
div[data-testid="stExpander"] summary:hover *,
div[data-testid="stExpander"] summary:focus *,
div[data-testid="stExpander"] summary:active * {
    color: #0f172a !important;
}

hr { border-color: #e2e8f0; }

/* ---------- KOTAK KUOTA PENUH ---------- */
.kuota-penuh {
    display: flex; align-items: center; gap: 12px;
    background: white; border: 1px solid #fecaca; border-left: 6px solid #ef4444;
    border-radius: 14px; padding: 12px 16px; margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(239, 68, 68, .12);
}
.kuota-penuh .kp-ico { font-size: 1.5rem; }
.kuota-penuh .kp-judul { color: #b91c1c; font-weight: 700; font-size: .9rem; line-height: 1.35; }
.kuota-penuh .kp-sub { color: #475569; font-size: .82rem; margin-top: 2px; }

/* ---------- TABEL LOG AKTIVITAS ---------- */
.log-wrap { max-height: 380px; overflow-y: auto; border: 1px solid #e2e8f0; border-radius: 12px; }
.log-table { width: 100%; border-collapse: collapse; font-size: .85rem; margin: 0; }
div[data-testid="stExpander"] .log-table td.kosong { color: #94a3b8 !important; }
div[data-testid="stExpander"] .log-table th {
    position: sticky; top: 0; z-index: 1;
    background: linear-gradient(120deg, #0f766e, #0891b2) !important;
    color: white !important; text-align: left; padding: 10px 14px; font-weight: 600;
}
.log-table td { padding: 8px 14px; border-top: 1px solid #e2e8f0; background: white; }
.log-table tbody tr:nth-child(even) td { background: #f8fafc; }
.log-table .c { text-align: center; width: 64px; }
.log-table .w { white-space: nowrap; }
.log-table .kosong { text-align: center; color: #94a3b8; padding: 18px 14px; }
.lg { display: inline-block; padding: 2px 12px; border-radius: 999px; font-weight: 600; font-size: .78rem; }
div[data-testid="stExpander"] .lg-cetak  { background: #ccfbf1; color: #0f766e !important; }
div[data-testid="stExpander"] .lg-panggil { background: #dbeafe; color: #1e40af !important; }
div[data-testid="stExpander"] .lg-hadir  { background: #dcfce7; color: #166534 !important; }
div[data-testid="stExpander"] .lg-lewat  { background: #fee2e2; color: #b91c1c !important; }

/* ---------- RESPONSIF ---------- */
@media (max-width: 760px) {
    .steps { grid-template-columns: 1fr; }
    .hero h1 { font-size: 1.5rem; }
    .ticket-number { font-size: 4rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# --- INISIALISASI STATE VARIABEL (Mengingat nomor antrian berjalan) ---
if "antrian_A" not in st.session_state:
    st.session_state.antrian_A = 0
if "antrian_B" not in st.session_state:
    st.session_state.antrian_B = 0
if "antrian_C" not in st.session_state:
    st.session_state.antrian_C = 0
if "antrian_tercetak" not in st.session_state:
    st.session_state.antrian_tercetak = None
if "waktu_cetak" not in st.session_state:
    st.session_state.waktu_cetak = None
if "logs" not in st.session_state:
    st.session_state.logs = []
if "sedang_dipanggil" not in st.session_state:
    st.session_state.sedang_dipanggil = {"A": None, "B": None, "C": None}
if "hitung_panggil" not in st.session_state:
    st.session_state.hitung_panggil = {"A": 0, "B": 0, "C": 0}
if "terakhir_dipanggil" not in st.session_state:
    st.session_state.terakhir_dipanggil = {"A": 0, "B": 0, "C": 0}
if "dilewati" not in st.session_state:
    st.session_state.dilewati = {"A": [], "B": [], "C": []}
if "suara_pending" not in st.session_state:
    st.session_state.suara_pending = None

# Antrian otomatis dimulai dari nol lagi setiap ganti hari (kuota harian)
_hari_ini = datetime.now().strftime("%Y-%m-%d")
if st.session_state.get("tanggal_antrian") != _hari_ini:
    if "tanggal_antrian" in st.session_state:
        st.session_state.antrian_A = 0
        st.session_state.antrian_B = 0
        st.session_state.antrian_C = 0
        st.session_state.antrian_tercetak = None
        st.session_state.waktu_cetak = None
        st.session_state.logs = []
        st.session_state.sedang_dipanggil = {"A": None, "B": None, "C": None}
        st.session_state.hitung_panggil = {"A": 0, "B": 0, "C": 0}
        st.session_state.terakhir_dipanggil = {"A": 0, "B": 0, "C": 0}
        st.session_state.dilewati = {"A": [], "B": [], "C": []}
        st.session_state.suara_pending = None
    st.session_state.tanggal_antrian = _hari_ini

MAX_ANTRIAN = 999

# =========================================================================
# HEADER PUSKESMAS
# =========================================================================
tgl_hari_ini, _ = waktu_sekarang()

st.markdown(
    '<div class="hero">'
    '<div class="logo-cross"></div>'
    '<div class="hero-text">'
    '<div class="instansi">PEMERINTAH DAERAH • DINAS KESEHATAN</div>'
    '<h1>PUSKESMAS SEHAT SEJAHTERA</h1>'
    '<p>Ambil Nomor Antrian • Melayani dengan Sepenuh Hati</p>'
    '</div>'
    '<div class="hero-info">'
    f'📅 <b>{tgl_hari_ini}</b><br>'
    '🕗 Senin - Kamis: 08.00 - 14.00 WIB<br>'
    '🕗 Jumat - Sabtu: 08.00 - 11.00 WIB'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="steps">'
    '<div class="step"><div class="num">1</div><div class="txt">Pilih tombol sesuai jenis pasien Anda</div></div>'
    '<div class="step"><div class="num">2</div><div class="txt">Ambil kartu antrian yang tercetak</div></div>'
    '<div class="step"><div class="num">3</div><div class="txt">Tunggu di ruang tunggu hingga nomor Anda dipanggil</div></div>'
    '</div>',
    unsafe_allow_html=True,
)

# =========================================================================
# SIDEBAR: ENVIRONMENT CONTROL
# =========================================================================
st.sidebar.header("🛠️ Environment & Hardware Control")
suplai_listrik = st.sidebar.toggle("⚡ Suplai Listrik", value=True)
kertas_tersedia = st.sidebar.toggle("🧻 Ketersediaan Kertas", value=True)
tombol_mekanis_ok = st.sidebar.toggle("🔘 Tombol Mekanis", value=True)

# Cek kelayakan sistem berdasarkan Environment
system_ready = suplai_listrik and kertas_tersedia and tombol_mekanis_ok

if not system_ready:
    st.sidebar.error("🔴 LAMPU MERAH: Mesin Error / Kertas Habis / Masalah Listrik!")
else:
    st.sidebar.success("🟢 LAMPU HIJAU: Sistem Siap Digunakan")

# =========================================================================
# KUOTA PASIEN PER HARI  ->  UBAH ANGKANYA DI SINI
# (contoh normal: A = 100, B = 50, C = 50. Sekarang 3 untuk uji coba)
# =========================================================================
KUOTA = {
    "A": 3,   # Pasien BPJS
    "B": 3,   # Pasien Mandiri / Asuransi
    "C": 3,   # Pasien Daftar Online
}
NAMA_JENIS = {"A": "BPJS", "B": "Mandiri / Asuransi", "C": "Daftar Online"}


def kotak_kuota_penuh(kode):
    return (
        '<div class="kuota-penuh">'
        '<div class="kp-ico">⛔</div>'
        '<div>'
        f'<div class="kp-judul">Kuota Pasien {NAMA_JENIS[kode]} hari ini sudah penuh ({KUOTA[kode]} antrian)</div>'
        '<div class="kp-sub">Mohon maaf, silahkan datang kembali besok.</div>'
        '</div>'
        '</div>'
    )


def catat_panggilan_pertama(kode):
    """Saat tiket dicetak: kalau loket sedang kosong dan tiket ini adalah urutan berikutnya,
    tiket langsung dihitung sebagai panggilan ke-1 (tombol Pasien Hadir/Selesai langsung aktif)."""
    nomor_baru = st.session_state[f"antrian_{kode}"]
    if (
        st.session_state.sedang_dipanggil[kode] is None
        and st.session_state.terakhir_dipanggil[kode] == nomor_baru - 1
    ):
        st.session_state.terakhir_dipanggil[kode] = nomor_baru
        st.session_state.sedang_dipanggil[kode] = nomor_baru
        st.session_state.hitung_panggil[kode] = 1


# Tombol Reset Antrian di Sidebar
if st.sidebar.button("🔄 Reset Semua Nomor Antrian"):
    st.session_state.antrian_A = 0
    st.session_state.antrian_B = 0
    st.session_state.antrian_C = 0
    st.session_state.antrian_tercetak = None
    st.session_state.waktu_cetak = None
    st.session_state.logs = []
    st.session_state.sedang_dipanggil = {"A": None, "B": None, "C": None}
    st.session_state.hitung_panggil = {"A": 0, "B": 0, "C": 0}
    st.session_state.terakhir_dipanggil = {"A": 0, "B": 0, "C": 0}
    st.session_state.dilewati = {"A": [], "B": [], "C": []}
    st.session_state.suara_pending = None
    st.rerun()

# =========================================================================
# PANEL UTAMA: KIOS TOMBOL & MONITOR CETAK
# =========================================================================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-title">👇 Silahkan Tekan Tombol:</div>', unsafe_allow_html=True)

    for _k in ("A", "B", "C"):
        if st.session_state[f"antrian_{_k}"] >= KUOTA[_k]:
            st.markdown(kotak_kuota_penuh(_k), unsafe_allow_html=True)

    # A. Tombol Hijau - BPJS
    btn_bpjs = st.button("🟢 TOMBOL HIJAU (Pasien BPJS)", key="btn_bpjs", use_container_width=True, disabled=(not system_ready) or st.session_state.antrian_A >= KUOTA["A"])
    if btn_bpjs and system_ready:
        if st.session_state.antrian_A < KUOTA["A"]:
            st.session_state.antrian_A += 1
            st.session_state.antrian_tercetak = f"A-{st.session_state.antrian_A}"
            st.session_state.waktu_cetak = waktu_sekarang()
            st.toast("🔊 Bunyi Mesin: 'Silahkan ambil kartu!'", icon="🔊")
            tambah_log(st.session_state.antrian_tercetak, "Dicetak", "cetak")
            catat_panggilan_pertama("A")
            mainkan_suara()
        else:
            st.markdown(kotak_kuota_penuh("A"), unsafe_allow_html=True)

    # B. Tombol Putih - Mandiri/Swasta
    btn_mandiri = st.button("⚪ TOMBOL PUTIH (Pasien Mandiri / Asuransi)", key="btn_mandiri", use_container_width=True, disabled=(not system_ready) or st.session_state.antrian_B >= KUOTA["B"])
    if btn_mandiri and system_ready:
        if st.session_state.antrian_B < KUOTA["B"]:
            st.session_state.antrian_B += 1
            st.session_state.antrian_tercetak = f"B-{st.session_state.antrian_B}"
            st.session_state.waktu_cetak = waktu_sekarang()
            st.toast("🔊 Bunyi Mesin: 'Silahkan ambil kartu!'", icon="🔊")
            tambah_log(st.session_state.antrian_tercetak, "Dicetak", "cetak")
            catat_panggilan_pertama("B")
            mainkan_suara()
        else:
            st.markdown(kotak_kuota_penuh("B"), unsafe_allow_html=True)

    # C. Tombol Biru - Daftar Online
    btn_online = st.button("🔵 TOMBOL BIRU (Pasien Daftar Online)", key="btn_online", use_container_width=True, disabled=(not system_ready) or st.session_state.antrian_C >= KUOTA["C"])
    if btn_online and system_ready:
        if st.session_state.antrian_C < KUOTA["C"]:
            st.session_state.antrian_C += 1
            st.session_state.antrian_tercetak = f"C-{st.session_state.antrian_C}"
            st.session_state.waktu_cetak = waktu_sekarang()
            st.toast("🔊 Bunyi Mesin: 'Silahkan ambil kartu!'", icon="🔊")
            tambah_log(st.session_state.antrian_tercetak, "Dicetak (Online)", "cetak")
            catat_panggilan_pertama("C")
            mainkan_suara()
        else:
            st.markdown(kotak_kuota_penuh("C"), unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-title">🖨️ Printer Tiket:</div>', unsafe_allow_html=True)
    if st.session_state.antrian_tercetak and system_ready:
        # Menentukan label layanan dari kode tiket
        kode = st.session_state.antrian_tercetak[0]
        info_layanan = {
            "A": ("Pasien BPJS", "#dcfce7", "#166534"),
            "B": ("Pasien Mandiri / Asuransi", "#e2e8f0", "#0f172a"),
            "C": ("Pasien Daftar Online", "#dbeafe", "#1e40af"),
        }
        nama_layanan, warna_bg, warna_teks = info_layanan[kode]
        tgl_cetak, jam_cetak = st.session_state.waktu_cetak

        # Menampilkan desain visual box tiket yang baru dicetak
        st.markdown(
            '<div class="ticket">'
            '<div class="ticket-head"><span><span class="mini-cross"></span>PUSKESMAS SEHAT SEJAHTERA</span><span>TIKET ANTRIAN</span></div>'
            '<div class="ticket-sub">Jl. Kesehatan No. 1 • Layanan Kesehatan Masyarakat</div>'
            '<div class="ticket-body">'
            '<div class="ticket-label">NOMOR ANTRIAN ANDA</div>'
            f'<div class="ticket-number">{st.session_state.antrian_tercetak}</div>'
            f'<div class="ticket-layanan" style="--lc:{warna_bg};--lt:{warna_teks}">{nama_layanan}</div>'
            '</div>'
            f'<div class="ticket-meta"><span>{tgl_cetak}</span><span>{jam_cetak}</span></div>'
            '<div class="ticket-foot">Silahkan ambil kertas antrian Anda dan tunggu di ruang tunggu.<br><b>Terima kasih & semoga lekas sembuh 🙏</b></div>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="ticket-empty">'
            '<div class="icon">🖨️</div>'
            'Silahkan tekan salah satu tombol di sebelah kiri untuk mencetak nomor antrian.'
            '</div>',
            unsafe_allow_html=True,
        )

# =========================================================================
# JUMLAH ANTRIAN SAAT INI & LOGS SISTEM (DATA HISTORI)
# =========================================================================
st.divider()
st.markdown('<div class="section-title">👥 Jumlah Antrian Saat Ini</div>', unsafe_allow_html=True)


def kartu_statistik(nama, nilai, warna, ikon, kode, total=False):
    persen = min(nilai / KUOTA[kode] * 100, 100)
    terakhir = f"{kode}-{nilai}" if nilai > 0 else "-"
    sisa = max(KUOTA[kode] - nilai, 0)
    info_sisa = "⛔ KUOTA PENUH" if sisa == 0 else f"Sisa kuota: {sisa}"
    kelas = "stat-card stat-total" if total else "stat-card"
    return (
        f'<div class="{kelas}" style="--c:{warna}">'
        f'<div class="ico">{ikon}</div>'
        f'<div class="stat-name">{nama}</div>'
        f'<div class="stat-value">{nilai} <span>/ {KUOTA[kode]} antrian</span></div>'
        f'<div class="stat-last">Nomor terakhir: <b>{terakhir}</b><br>{info_sisa}</div>'
        f'<div class="bar"><div style="width:{persen}%"></div></div>'
        '</div>'
    )


total_antrian = st.session_state.antrian_A + st.session_state.antrian_B + st.session_state.antrian_C

c1, c2, c3, c4 = st.columns(4, gap="medium")
c1.markdown(kartu_statistik("Antrian Pasien BPJS (A)", st.session_state.antrian_A, "#22c55e", "🟢", "A"), unsafe_allow_html=True)
c2.markdown(kartu_statistik("Antrian Pasien Mandiri (B)", st.session_state.antrian_B, "#64748b", "⚪", "B"), unsafe_allow_html=True)
c3.markdown(kartu_statistik("Antrian Pasien Online (C)", st.session_state.antrian_C, "#3b82f6", "🔵", "C"), unsafe_allow_html=True)
c4.markdown(
    f'<div class="stat-card stat-total" style="--c:#5eead4">'
    f'<div class="ico">🏥</div>'
    f'<div class="stat-name">Total Seluruh Antrian</div>'
    f'<div class="stat-value">{total_antrian} <span>/ {sum(KUOTA.values())} antrian</span></div>'
    f'<div class="stat-last">Gabungan layanan A + B + C</div>'
    f'<div class="bar"><div style="width:{min(total_antrian / sum(KUOTA.values()) * 100, 100)}%"></div></div>'
    '</div>',
    unsafe_allow_html=True,
)

# =========================================================================
# PANEL LOKET: PEMANGGILAN ANTRIAN (MAKS 3x PANGGIL, LALU DILEWATI)
# =========================================================================
MAX_PANGGIL = 3

st.markdown(
    """
<style>
/* Teks keterangan panel loket dipaksa gelap supaya terbaca */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] * {
    color: #334155 !important;
}
/* Tombol panggil: teal, teks putih */
div[class*="st-key-panggil_"] button {
    background: linear-gradient(135deg, #0f766e, #0891b2) !important;
    border: none !important;
    border-radius: 14px !important;
    min-height: 52px;
    box-shadow: 0 6px 14px rgba(13,148,136,.25);
}
div[class*="st-key-panggil_"] button,
div[class*="st-key-panggil_"] button * { color: white !important; font-weight: 600; }
div[class*="st-key-panggil_"] button:hover:not(:disabled) { filter: brightness(1.08); }
/* Tombol hadir: HIJAU (aktif) supaya jelas beda dengan abu-abu (nonaktif) */
div[class*="st-key-hadir_"] button {
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    border: none !important;
    border-radius: 14px !important;
    min-height: 46px;
    box-shadow: 0 6px 14px rgba(34,197,94,.30);
}
div[class*="st-key-hadir_"] button,
div[class*="st-key-hadir_"] button * { color: white !important; font-weight: 600; }
div[class*="st-key-hadir_"] button:hover:not(:disabled) { filter: brightness(1.08); }
/* Tombol nonaktif */
div[class*="st-key-panggil_"] button:disabled,
div[class*="st-key-hadir_"] button:disabled {
    background: #e2e8f0 !important; border: 2px solid #cbd5e1 !important;
    box-shadow: none; cursor: not-allowed;
}
div[class*="st-key-panggil_"] button:disabled,
div[class*="st-key-panggil_"] button:disabled *,
div[class*="st-key-hadir_"] button:disabled,
div[class*="st-key-hadir_"] button:disabled * { color: #64748b !important; }
.call-card {
    background: white; border-radius: 18px; padding: 16px 18px; margin-top: 10px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, .08);
    border: 1px solid #e2e8f0; border-top: 6px solid var(--c);
    text-align: center;
}
.call-title { color: #64748b; font-size: .82rem; font-weight: 600; }
.call-num {
    font-family: 'Roboto Mono', monospace; font-size: 2.8rem; font-weight: 700;
    color: var(--c); line-height: 1.2;
}
.call-none { color: #94a3b8; font-size: 1rem; padding: 14px 0; }
.call-dots { margin: 4px 0; }
.dot {
    display: inline-block; width: 14px; height: 14px; border-radius: 50%;
    background: #e2e8f0; margin: 0 4px; border: 1px solid #cbd5e1;
}
.dot.on { background: var(--c); border-color: var(--c); }
.call-sub { color: #475569; font-size: .8rem; }
.call-meta { color: #64748b; font-size: .78rem; margin-top: 8px; border-top: 1px dashed #e2e8f0; padding-top: 8px; }
</style>
""",
    unsafe_allow_html=True,
)

st.divider()
st.markdown('<div class="section-title">📣 Panel Loket: Pemanggilan Antrian</div>', unsafe_allow_html=True)


def aksi_panggil(kode):
    maks = st.session_state[f"antrian_{kode}"]
    cur = st.session_state.sedang_dipanggil[kode]
    hit = st.session_state.hitung_panggil[kode]

    # Sudah 3x dipanggil dan tetap tidak datang -> LEWATI, lanjut nomor berikutnya
    if cur is not None and hit >= MAX_PANGGIL:
        st.session_state.dilewati[kode].append(cur)
        tambah_log(f"{kode}-{cur}", f"Dilewati (tidak datang {MAX_PANGGIL}x)", "lewat")
        cur = None

    # Belum ada nomor yang sedang dipanggil -> ambil nomor berikutnya
    if cur is None:
        if st.session_state.terakhir_dipanggil[kode] < maks:
            st.session_state.terakhir_dipanggil[kode] += 1
            cur = st.session_state.terakhir_dipanggil[kode]
            hit = 0
        else:
            # Tidak ada lagi antrian yang menunggu
            st.session_state.sedang_dipanggil[kode] = None
            st.session_state.hitung_panggil[kode] = 0
            return

    hit += 1
    st.session_state.sedang_dipanggil[kode] = cur
    st.session_state.hitung_panggil[kode] = hit
    tambah_log(f"{kode}-{cur}", f"Panggilan ke-{hit}", "panggil")
    st.session_state.suara_pending = f"Nomor antrian {kode} {cur}, silahkan menuju loket"


def aksi_hadir(kode):
    cur = st.session_state.sedang_dipanggil[kode]
    hit = st.session_state.hitung_panggil[kode]
    if cur is not None:
        tambah_log(f"{kode}-{cur}", f"Hadir (panggilan ke-{hit})", "hadir")
        st.session_state.sedang_dipanggil[kode] = None
        st.session_state.hitung_panggil[kode] = 0


info_loket = [
    ("A", "Loket Pasien BPJS", "#22c55e"),
    ("B", "Loket Pasien Mandiri", "#64748b"),
    ("C", "Loket Pasien Online", "#3b82f6"),
]
kolom_loket = st.columns(3, gap="medium")

for kol, (kode, nama, warna) in zip(kolom_loket, info_loket):
    with kol:
        cur = st.session_state.sedang_dipanggil[kode]
        hit = st.session_state.hitung_panggil[kode]
        maks = st.session_state[f"antrian_{kode}"]
        terakhir = st.session_state.terakhir_dipanggil[kode]
        menunggu = maks - terakhir

        if cur is None:
            label = f"📢 Panggil Antrian {kode} Berikutnya"
        elif hit < MAX_PANGGIL:
            label = f"🔁 Panggil Ulang {kode}-{cur} (panggilan ke-{hit + 1})"
        else:
            label = f"⏭️ Tidak Datang → Lewati & Panggil Berikutnya"

        st.button(
            label, key=f"panggil_{kode}", use_container_width=True,
            disabled=(cur is None and menunggu <= 0),
            on_click=aksi_panggil, args=(kode,),
        )
        st.button(
            "✅ Pasien Hadir / Selesai", key=f"hadir_{kode}_{'aktif' if cur is not None else 'mati'}", use_container_width=True,
            disabled=(cur is None),
            on_click=aksi_hadir, args=(kode,),
        )

        if cur is None:
            isi = '<div class="call-none">Belum ada panggilan</div>'
        else:
            titik = "".join(
                '<span class="dot on"></span>' if i < hit else '<span class="dot"></span>'
                for i in range(MAX_PANGGIL)
            )
            keterangan = f"Panggilan ke-{hit} dari {MAX_PANGGIL}"
            if hit >= MAX_PANGGIL:
                keterangan += " • belum datang, tekan tombol lewati"
            isi = (
                f'<div class="call-num">{kode}-{cur}</div>'
                f'<div class="call-dots">{titik}</div>'
                f'<div class="call-sub">{keterangan}</div>'
            )

        dilewati_txt = ", ".join(f"{kode}-{n}" for n in st.session_state.dilewati[kode]) or "-"
        st.markdown(
            f'<div class="call-card" style="--c:{warna}">'
            f'<div class="call-title">{nama}</div>'
            f'{isi}'
            f'<div class="call-meta">Menunggu: <b>{max(menunggu, 0)}</b> antrian<br>Dilewati: {dilewati_txt}</div>'
            '</div>',
            unsafe_allow_html=True,
        )

# Putar suara panggilan (sekali saja setelah tombol panggil ditekan)
if st.session_state.suara_pending:
    mainkan_suara(st.session_state.suara_pending)
    st.session_state.suara_pending = None

st.write("")
with st.expander("Lihat Log Aktivitas Cetak", expanded=bool(st.session_state.logs)):
    if st.session_state.logs:
        baris = "".join(
            f'<tr><td class="c">{n}</td><td class="w">{lg["waktu"]}</td>'
            f'<td><b>{lg["tiket"]}</b></td>'
            f'<td><span class="lg lg-{lg["jenis"]}">{lg["kejadian"]}</span></td></tr>'
            for n, lg in enumerate(st.session_state.logs, start=1)
        )
    else:
        baris = '<tr><td colspan="4" class="kosong">Belum ada riwayat</td></tr>'
    st.markdown(
        '<div class="log-wrap"><table class="log-table">'
        '<thead><tr><th class="c">No</th><th>Waktu</th><th>Tiket</th><th>Status</th></tr></thead>'
        f'<tbody>{baris}</tbody></table></div>',
        unsafe_allow_html=True,
    )