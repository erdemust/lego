"""Çocukları sevindirecek, rengarenk ve eğlenceli parametrik yaratık atölyesi (Hata Düzeltilmiş)."""

import random
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
import streamlit as st

st.set_page_config(page_title="Sevimli Yaratık Atölyesi 🐛✨", page_icon="🎨", layout="wide")

# DÜZELTME: body_length minimum 80 ile uyumlu hale getirildi (örn: 130)
DEFAULTS = {
    "body_length": 130, "thorax_width": 60, "thorax_height": 45,
    "head_width": 50, "head_height": 30,
    "body_color": "#FF5964", "detail_color": "#35A7FF", "background": "#FFF1C1",
    "feelers": True, "legs": True, "wings": True, "pattern": "Benekli",
    "creature_name": "Boncuk"
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

def make_bug(seed: int | None = None) -> None:
    rng = random.Random(seed)
    st.session_state.body_length = rng.randint(90, 160)
    st.session_state.thorax_width = rng.randint(40, 80)
    st.session_state.thorax_height = rng.randint(30, 60)
    st.session_state.head_width = rng.randint(35, 65)
    st.session_state.head_height = rng.randint(22, 40)
    
    palettes = [
        ("#FF5964", "#FFD166"), ("#3A86EF", "#8338EC"),
        ("#FF006E", "#FB5607"), ("#06D6A0", "#118AB2"),
        ("#FFB703", "#FB8500"), ("#9b5de5", "#f15bb5")
    ]
    st.session_state.body_color, st.session_state.detail_color = rng.choice(palettes)
    st.session_state.background = rng.choice(["#FFF1C1", "#E0F7FA", "#FCE4EC", "#F1F8E9"])
    st.session_state.feelers = True
    st.session_state.legs = True
    st.session_state.wings = rng.choice([True, False])
    st.session_state.pattern = rng.choice(["Benekli", "Çizgili"])
    
    names = ["Pofuduk", "Zıpzıp", "Boncuk", "Minnoş", "Ciciş", "Tırtılcan", "Patikler", "Fındık"]
    st.session_state.creature_name = rng.choice(names)

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
        ax.plot(x, y, color="#FFE082", alpha=0.3, linewidth=1.5, zorder=0)

    if config["wings"]:
        for cx, angle in ((4.15, 32), (5.85, -32)):
            ax.add_patch(Ellipse((cx, 3.55), 1.4, body_len * .75, angle=angle,
                                 facecolor="#FFFFFF", edgecolor="#FFD166", linewidth=1.5, alpha=.85, zorder=1))

    body_width = config["thorax_width"] * 1.1 / 10
    ax.add_patch(Ellipse((5, 3), body_width, body_len, facecolor=config["body_color"],
                         edgecolor="#263238", linewidth=2, zorder=2))
    ax.add_patch(Ellipse((5, 3 + body_len / 2 - .2), config["thorax_width"] / 10, thorax_h,
                         facecolor=config["detail_color"], edgecolor="#263238", linewidth=2, zorder=3))
    ax.add_patch(Ellipse((5, head_y), config["head_width"] / 10, head_h,
                         facecolor=config["detail_color"], edgecolor="#263238", linewidth=2, zorder=4))

    if config["pattern"] == "Çizgili":
        for frac in (.22, .40, .58, .76):
            y = 3 - body_len / 2 + body_len * frac
            half = body_width / 2 * np.sqrt(max(.1, 1 - ((y - 3) / (body_len / 2)) ** 2)) * .9
            ax.plot([5 - half, 5 + half], [y, y], color="white", alpha=.9, linewidth=3, zorder=2.5)
    elif config["pattern"] == "Benekli":
        for xoff, frac in ((-.22, .28), (.22, .28), (0, .5), (-.2, .72), (.2, .72)):
            ax.scatter([5 + xoff], [3 - body_len / 2 + body_len * frac], s=80,
                       color="#FFFFFF", edgecolors="#263238", linewidths=1.5, zorder=2.6)

    eye_dx = min(config["head_width"] / 35, .45)
    eye_y = head_y + head_h * .12
    ax.scatter([5 - eye_dx, 5 + eye_dx], [eye_y, eye_y], s=120, color="white", edgecolors="#263238", linewidths=1.5, zorder=5)
    ax.scatter([5 - eye_dx, 5 + eye_dx], [eye_y, eye_y], s=50, color="#263238", zorder=6)
    ax.scatter([5 - eye_dx + 0.05, 5 + eye_dx + 0.05], [eye_y + 0.05, eye_y + 0.05], s=15, color="white", zorder=7)
    
    ax.plot([4.85, 5.0, 5.15], [head_y - head_h * .15, head_y - head_h * .28, head_y - head_h * .15], color="#263238", linewidth=2, solid_capstyle="round", zorder=6)

    if config["feelers"]:
        base_y = head_y + head_h * .45
        ax.plot([4.85, 4.3], [base_y, base_y + .85], color="#263238", linewidth=2.5, zorder=4)
        ax.plot([5.15, 5.7], [base_y, base_y + .85], color="#263238", linewidth=2.5, zorder=4)
        ax.scatter([4.3, 5.7], [base_y + .85] * 2, s=70, color=config["body_color"], edgecolors="#263238", linewidths=1.5, zorder=5)
        
    if config["legs"]:
        for y in (3.3, 2.8, 2.3):
            ax.plot([5 - body_width / 2, 4.0], [y, y - .4], color="#263238", linewidth=2.5, solid_capstyle="round", zorder=1.4)
            ax.plot([5 + body_width / 2, 6.0], [y, y - .4], color="#263238", linewidth=2.5, solid_capstyle="round", zorder=1.4)

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
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&display=swap');
.stApp { background: linear-gradient(135deg, #FFF9C4 0%, #E0F7FA 100%); }
h1, h2, h3, h4 { font-family: 'Fredoka', cursive, sans-serif; color: #FF5964; }
.hero { text-align: center; padding: 0.5rem; }
.card { background: white; border-radius: 20px; padding: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); }
div.stButton > button { border-radius: 16px; font-weight: 700; font-family: 'Fredoka', cursive; font-size: 18px; min-height: 3.2rem; background: #FF5964; color: white; border: none; box-shadow: 0 4px 10px rgba(255,89,100,0.3); }
div.stButton > button:hover { background: #FF2E43; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero">', unsafe_allow_html=True)
st.title("🐞 Sevimli Yaratık Atölyesi 🐛")
st.markdown("### Kendi neşeli dostunu tasarla, ona bir isim ver ve eğlenceye katıl!")
st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🎨 Sihirli Kontroller")
    
    if st.button("🎲 Sürpriz Yaratık Üret!", use_container_width=True):
        make_bug()
        st.rerun()
        
    st.divider()
    
    st.text_input("Yaratığının Adı:", key="creature_name")
    
    with st.expander("🌈 Renk Dünyası", expanded=True):
        st.color_picker("Gövde Rengi", key="body_color")
        st.color_picker("Kafalık Rengi", key="detail_color")
        st.color_picker("Arka Plan", key="background")
        
    with st.expander("📏 Boyut Büyücüsü", expanded=True):
        st.slider("Boy uzunluğu", 80, 160, key="body_length")
        st.slider("Karnının genişliği", 30, 90, key="thorax_width")
        st.slider("Kafasının büyüklüğü", 30, 70, key="head_width")
        
    with st.expander("✨ Eğlenceli Aksesuarlar", expanded=True):
        st.checkbox("Antenler", key="feelers")
        st.checkbox("Uçan Kanatlar", key="wings")
        st.checkbox("Komik Ayaklar", key="legs")
        st.selectbox("Süslü Desen", ["Benekli", "Çizgili"], key="pattern")

config = {key: st.session_state[key] for key in DEFAULTS if key != "creature_name"}
config["pattern"] = st.session_state["pattern"]
config["feelers"] = st.session_state["feelers"]
config["wings"] = st.session_state["wings"]
config["legs"] = st.session_state["legs"]

left, right = st.columns([1.6, 1], gap="large")

with left:
    fig, png = draw_bug(config)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.download_button(
        f"📥 {st.session_state.creature_name}'i Resim Olarak İndir!", 
        data=png, 
        file_name=f"{st.session_state.creature_name.lower()}-yaratik.png",
        mime="image/png", 
        use_container_width=True
    )

with right:
    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"🌟 Tanışın: {st.session_state.creature_name}!")
    st.markdown("Bu sevimli dostumuz seninle oynamaya hazır! 🎉")
    
    features = []
    if st.session_state.wings: features.append("🦋 Kanatlı Uçucu")
    if st.session_state.feelers: features.append(" antennae Antenli Dinleyici")
    if st.session_state.legs: features.append("🐾 Koşucu Ayaklar")
    
    st.markdown(f"**Özellikleri:** " + (" · ".join(features) if features else "Sakin Dost"))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍎 Besle"):
            st.balloons()
            st.success(f"{st.session_state.creature_name} karnını doyurdu ve çok mutlu oldu! 😋")
    with col2:
        if st.button("🎈 Eğlendir"):
            st.snow()
            st.success(f"{st.session_state.creature_name} neşeyle zıplıyor! Yuppi! 🦘")
            
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #555; font-weight: bold;'>Minik Hayaller, Büyük Renkler! 🌟</div>", unsafe_allow_html=True)
