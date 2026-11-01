"""Türkçe, parametrik böcek illüstratörü."""

import random
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
import streamlit as st


st.set_page_config(page_title="Böcek Atölyesi", page_icon="🐛", layout="wide")

DEFAULTS = {
    "body_length": 120, "thorax_width": 60, "thorax_height": 35,
    "head_width": 40, "head_height": 24,
    "body_color": "#E53935", "detail_color": "#263238", "background": "#FFF7D6",
    "feelers": True, "legs": True, "wings": False, "pattern": "Benekli",
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def make_bug(seed: int | None = None) -> None:
    """Generate a vivid but readable new creature configuration."""
    rng = random.Random(seed)
    st.session_state.body_length = rng.randint(90, 140)
    st.session_state.thorax_width = rng.randint(45, 75)
    st.session_state.thorax_height = rng.randint(25, 50)
    st.session_state.head_width = rng.randint(28, 65)
    st.session_state.head_height = rng.randint(18, 42)
    st.session_state.body_color = rng.choice(["#E53935", "#F4511E", "#F9A825", "#D81B60", "#EF5350"])
    st.session_state.detail_color = "#263238"
    st.session_state.background = rng.choice(["#FFF7D6", "#E0F7FA", "#FCE4EC", "#F1F8E9"])
    st.session_state.feelers = rng.choice([True, False])
    st.session_state.legs = rng.choice([True, False])
    st.session_state.wings = False
    st.session_state.pattern = rng.choice(["Benekli", "Benekli", "Düz"])


def draw_bug(config: dict) -> tuple[plt.Figure, BytesIO]:
    # Keep the creature comfortably inside the canvas. The abdomen is short
    # and broad, like a ladybug's rounded shell.
    body_len = config["body_length"] / 40
    thorax_h = config["thorax_height"] / 70
    head_h = config["head_height"] / 45
    body_y = 2.7
    body_width = body_len * (.9 + (config["thorax_width"] - 45) / 100)
    thorax_y = body_y + body_len * .43
    head_y = thorax_y + thorax_h * .55 + head_h * .35
    fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
    fig.patch.set_facecolor(config["background"])
    ax.set_facecolor(config["background"])
    x = np.linspace(0, 10, 240)
    for i in range(-4, 13):
        y = np.sin(x * 0.8 + i * 0.45) * 0.22 + i * 0.72
        ax.plot(x, y, color="#9CCFC5", alpha=0.22, linewidth=1, zorder=0)

    # Wings sit behind the body.
    if config["wings"]:
        for cx, angle in ((4.25, 28), (5.75, -28)):
            ax.add_patch(Ellipse((cx, 3.55), 1.25, body_len * .72, angle=angle,
                                 facecolor="#FFFFFF", edgecolor="#FFFFFF", alpha=.72, zorder=1))
            ax.plot([5, cx], [3.3, 3.8], color="#FFFFFF", alpha=.75, linewidth=1, zorder=1.2)

    ax.add_patch(Ellipse((5, body_y), body_width, body_len, facecolor=config["body_color"],
                         edgecolor="#263238", linewidth=2, zorder=2))
    thorax_width = body_width * .63
    ax.add_patch(Ellipse((5, thorax_y), thorax_width, thorax_h,
                         facecolor=config["detail_color"], edgecolor="#263238", linewidth=1.5, zorder=3))
    ax.add_patch(Ellipse((5, head_y), config["head_width"] / 100, head_h,
                         facecolor=config["detail_color"], edgecolor="#263238", linewidth=1.2, zorder=4))

    # Patterns follow the abdomen's proportions.
    if config["pattern"] == "Çizgili":
        for frac in (.22, .40, .58, .76):
            y = body_y - body_len / 2 + body_len * frac
            half = body_width / 2 * np.sqrt(max(.1, 1 - ((y - body_y) / (body_len / 2)) ** 2)) * .9
            ax.plot([5 - half, 5 + half], [y, y], color="white", alpha=.9, linewidth=2.2, zorder=2.5)
    elif config["pattern"] == "Benekli":
        for xfrac, frac in ((-.24, .25), (.24, .25), (-.3, .48), (.3, .48),
                            (0, .52), (-.23, .75), (.23, .75)):
            y = body_y - body_len / 2 + body_len * frac
            ax.scatter([5 + body_width * xfrac], [y], s=48, color="#20252B",
                       edgecolors="#111820", linewidths=.7, zorder=2.7)
        # The center seam divides the red wing covers into the familiar shell.
        ax.plot([5, 5], [body_y - body_len * .42, body_y + body_len * .43],
                color="#263238", linewidth=1.25, alpha=.85, zorder=2.8)

    # Eyes are spaced and placed using the selected head size.
    eye_dx = .13
    eye_y = head_y + head_h * .10
    ax.scatter([5 - eye_dx, 5 + eye_dx], [eye_y, eye_y], s=64, color="white", edgecolors="#263238", linewidths=.7, zorder=5)
    ax.scatter([5 - eye_dx, 5 + eye_dx], [eye_y, eye_y], s=20, color="#263238", zorder=6)
    ax.plot([4.88, 5.12], [head_y - head_h * .2] * 2, color="#263238", linewidth=1, zorder=6)

    if config["feelers"]:
        base_y = head_y + head_h * .42
        ax.plot([4.92, 4.65], [base_y, base_y + .42], color="#263238", linewidth=1.7, zorder=4)
        ax.plot([5.08, 5.35], [base_y, base_y + .42], color="#263238", linewidth=1.7, zorder=4)
        ax.scatter([4.65, 5.35], [base_y + .42] * 2, s=28, color=config["body_color"], edgecolors="#263238", zorder=5)
    if config["legs"]:
        for y in (3.35, 2.75, 2.15):
            ax.plot([5 - body_width * .40, 4.0], [y, y - .25], color="#263238", linewidth=1.8, solid_capstyle="round", zorder=1.4)
            ax.plot([5 + body_width * .40, 6.0], [y, y - .25], color="#263238", linewidth=1.8, solid_capstyle="round", zorder=1.4)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout(pad=0.2)
    image = BytesIO()
    fig.savefig(image, format="png", facecolor=fig.get_facecolor(), bbox_inches="tight", dpi=180)
    image.seek(0)
    return fig, image


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Nunito:wght@700;800;900&display=swap');
.stApp { background: linear-gradient(145deg, #f8fbfa 0%, #edf6f3 100%); }
h1, h2, h3 { font-family: 'Nunito', sans-serif; }
.hero { padding: .4rem 0 .8rem; }
.hero p { color: #60736f; font-size: 1.05rem; }
.card { background: rgba(255,255,255,.78); border: 1px solid #e0ece8; border-radius: 18px; padding: 1rem 1.15rem; }
div[data-testid="stMetric"] { background:#fff; border:1px solid #e3ece9; padding:12px 16px; border-radius:14px; }
div.stButton > button { border-radius:12px; font-weight:700; min-height:2.8rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero">', unsafe_allow_html=True)
st.title("🐛 Böcek Atölyesi")
st.markdown("Renkleri, ölçüleri ve özellikleri seç; kendi minik türünü tasarla.")
st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🎨 Tasarım paneli")
    if st.button("🎲 Yeni bir tür üret", use_container_width=True, type="primary"):
        make_bug()
        st.rerun()
    st.caption("Her üretimde renkler ve anatomik özellikler yenilenir.")
    st.divider()
    with st.expander("Renkler", expanded=True):
        st.color_picker("Gövde", key="body_color")
        st.color_picker("Baş ve göğüs", key="detail_color")
        st.color_picker("Arka plan", key="background")
    with st.expander("Boyutlar", expanded=True):
        st.slider("Kabuk boyutu", 90, 140, key="body_length")
        st.slider("Göğüs genişliği", 45, 75, key="thorax_width")
        st.slider("Göğüs yüksekliği", 25, 50, key="thorax_height")
    with st.expander("Özellikler", expanded=True):
        st.checkbox("Antenler", key="feelers")
        st.checkbox("Kanatlar", key="wings")
        st.checkbox("Altı bacak", key="legs")
        st.selectbox("Gövde deseni", ["Çizgili", "Benekli", "Düz"], key="pattern")

config = {key: st.session_state[key] for key in DEFAULTS}
left, right = st.columns([1.8, 1], gap="large")
with left:
    fig, png = draw_bug(config)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.download_button("⬇️ Böceği PNG olarak indir", data=png, file_name="benim-bocegim.png",
                       mime="image/png", use_container_width=True)
with right:
    st.subheader("🧬 Tür kartı")
    st.caption("Şu anki tasarımının kısa özeti")
    st.metric("Gövde uzunluğu", f"{config['body_length']} px")
    st.metric("Gövde deseni", config["pattern"])
    features = [name for name, active in (("Anten", config["feelers"]), ("Kanat", config["wings"]), ("6 bacak", config["legs"])) if active]
    st.markdown("**Aktif özellikler**")
    st.write(" · ".join(features) if features else "Özel özellik seçilmedi")
    st.markdown("**Renk paleti**")
    st.markdown(f"<div style='display:flex;gap:8px'><span style='width:36px;height:26px;border-radius:8px;background:{config['body_color']}'></span><span style='width:36px;height:26px;border-radius:8px;background:{config['detail_color']}'></span><span style='width:36px;height:26px;border-radius:8px;background:{config['background']};border:1px solid #ddd'></span></div>", unsafe_allow_html=True)
    st.info("İpucu: Rastgele üret düğmesiyle yeni bir kombinasyon keşfet; beğendiğin tasarımı PNG olarak kaydet.", icon="✨")

st.divider()
st.caption("Böcek Atölyesi · Küçük tasarımlar, büyük hayal gücü")
