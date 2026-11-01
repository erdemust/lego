"""Türkçe, parametrik böcek illüstratörü."""

import random
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
import streamlit as st


st.set_page_config(page_title="Böcek Atölyesi", page_icon="🐛", layout="wide")

DEFAULTS = {
    "body_length": 120, "thorax_width": 50, "thorax_height": 40,
    "head_width": 40, "head_height": 25,
    "body_color": "#FF6B6B", "detail_color": "#FFD166", "background": "#F1F8F6",
    "feelers": True, "legs": True, "wings": True, "pattern": "Çizgili",
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def make_bug(seed: int | None = None) -> None:
    """Generate a vivid but readable new creature configuration."""
    rng = random.Random(seed)
    st.session_state.body_length = rng.randint(70, 175)
    st.session_state.thorax_width = rng.randint(30, 85)
    st.session_state.thorax_height = rng.randint(25, 70)
    st.session_state.head_width = rng.randint(28, 65)
    st.session_state.head_height = rng.randint(18, 42)
    palettes = [("#FF6B6B", "#FFD166"), ("#6C63FF", "#A8E6CF"),
                ("#F72585", "#4CC9F0"), ("#2A9D8F", "#E9C46A"),
                ("#F77F00", "#D62828"), ("#845EC2", "#FFC75F")]
    st.session_state.body_color, st.session_state.detail_color = rng.choice(palettes)
    st.session_state.background = rng.choice(["#F1F8F6", "#FFF1F2", "#F2F0FF", "#FFF7E8"])
    st.session_state.feelers = rng.choice([True, False])
    st.session_state.legs = rng.choice([True, False])
    st.session_state.wings = rng.choice([True, False])
    st.session_state.pattern = rng.choice(["Çizgili", "Benekli", "Düz"])


def draw_bug(config: dict) -> tuple[plt.Figure, BytesIO]:
    body_len = config["body_length"] / 10
    thorax_h = config["thorax_height"] / 10
    head_h = config["head_height"] / 10
    head_y = 3 + body_len / 2 + thorax_h - 0.1
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

    body_width = config["thorax_width"] * 1.1 / 10
    ax.add_patch(Ellipse((5, 3), body_width, body_len, facecolor=config["body_color"],
                         edgecolor="#263238", linewidth=1.2, zorder=2))
    ax.add_patch(Ellipse((5, 3 + body_len / 2 - .2), config["thorax_width"] / 10, thorax_h,
                         facecolor=config["detail_color"], edgecolor="#263238", linewidth=1.2, zorder=3))
    ax.add_patch(Ellipse((5, head_y), config["head_width"] / 10, head_h,
                         facecolor=config["detail_color"], edgecolor="#263238", linewidth=1.2, zorder=4))

    # Patterns follow the abdomen's proportions.
    if config["pattern"] == "Çizgili":
        for frac in (.22, .40, .58, .76):
            y = 3 - body_len / 2 + body_len * frac
            half = body_width / 2 * np.sqrt(max(.1, 1 - ((y - 3) / (body_len / 2)) ** 2)) * .9
            ax.plot([5 - half, 5 + half], [y, y], color="white", alpha=.9, linewidth=2.2, zorder=2.5)
    elif config["pattern"] == "Benekli":
        for xoff, frac in ((-.22, .28), (.22, .28), (0, .5), (-.2, .72), (.2, .72)):
            ax.scatter([5 + xoff], [3 - body_len / 2 + body_len * frac], s=30,
                       color="#FFF3A3", edgecolors="#263238", linewidths=.45, zorder=2.6)

    # Eyes are spaced and placed using the selected head size.
    eye_dx = min(config["head_width"] / 36, .42)
    eye_y = head_y + head_h * .12
    ax.scatter([5 - eye_dx, 5 + eye_dx], [eye_y, eye_y], s=64, color="white", edgecolors="#263238", linewidths=.7, zorder=5)
    ax.scatter([5 - eye_dx, 5 + eye_dx], [eye_y, eye_y], s=20, color="#263238", zorder=6)
    ax.plot([4.88, 5.12], [head_y - head_h * .2] * 2, color="#263238", linewidth=1, zorder=6)

    if config["feelers"]:
        base_y = head_y + head_h * .45
        ax.plot([4.85, 4.35], [base_y, base_y + .75], color="#263238", linewidth=2, zorder=4)
        ax.plot([5.15, 5.65], [base_y, base_y + .75], color="#263238", linewidth=2, zorder=4)
        ax.scatter([4.35, 5.65], [base_y + .75] * 2, s=35, color=config["body_color"], edgecolors="#263238", zorder=5)
    if config["legs"]:
        for y in (3.25, 2.8, 2.35):
            ax.plot([5 - body_width / 2, 4.05], [y, y - .38], color="#263238", linewidth=2, solid_capstyle="round", zorder=1.4)
            ax.plot([5 + body_width / 2, 5.95], [y, y - .38], color="#263238", linewidth=2, solid_capstyle="round", zorder=1.4)
            ax.plot([4.05, 3.92], [y - .38, y - .48], color="#263238", linewidth=1.5, zorder=1.4)
            ax.plot([5.95, 6.08], [y - .38, y - .48], color="#263238", linewidth=1.5, zorder=1.4)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, max(7.5, head_y + 1.35))
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
        st.slider("Gövde uzunluğu", 60, 190, key="body_length", format="%d px")
        st.slider("Göğüs genişliği", 20, 95, key="thorax_width")
        st.slider("Göğüs yüksekliği", 15, 85, key="thorax_height")
        st.slider("Baş genişliği", 20, 75, key="head_width")
        st.slider("Baş yüksekliği", 12, 50, key="head_height")
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
