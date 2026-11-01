import random
import matplotlib.patches as patches
import matplotlib.pyplot as dal_ax
import numpy as np
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Adjustable Bug Generator", page_icon="🐛", layout="wide"
)

# --- SESSION STATE İLKLENDİRME (Rastgele Üretim İçin) ---
if "body_length" not in st.session_state:
    st.session_state.body_length = 120
    st.session_state.neck_width = 50
    st.session_state.neck_height = 40
    st.session_state.head_width = 40
    st.session_state.head_height = 25
    st.session_state.primary_color = "#FF4B4B"
    st.session_state.secondary_color = "#00CC96"
    st.session_state.bg_color = "#E6F4F1"
    st.session_state.feelers = True
    st.session_state.feet = True
    st.session_state.wings = True
    st.session_state.pattern = "Çizgili"

st.title("🐛 Gelişmiş Parametrik Böcek Üreticisi")
st.write(
    "Sol paneli kullanarak böceğinizi özelleştirin ya da rastgele butonuna basarak sürpriz bir tür yaratın!"
)

# --- KONTROL PANELİ (SIDEBAR) ---
st.sidebar.header("🎨 Renk Paleti")
primary_color = st.sidebar.color_picker("Gövde Rengi", st.session_state.primary_color)
secondary_color = st.sidebar.color_picker("Detay / Göğüs Rengi", st.session_state.secondary_color)
bg_color = st.sidebar.color_picker("Arka Plan Rengi", st.session_state.bg_color)

st.sidebar.header("📏 Anatomik Boyutlar")
neck_width = st.sidebar.slider("Boyun / Göğüs Genişliği", 10, 100, st.session_state.neck_width)
neck_height = st.sidebar.slider("Boyun Yüksekliği", 10, 100, st.session_state.neck_height)
body_length = st.sidebar.slider("Gövde Uzunluğu", 50, 200, st.session_state.body_length)
head_width = st.sidebar.slider("Kafa Genişliği", 20, 80, st.session_state.head_width)
head_height = st.sidebar.slider("Kafa Yüksekliği", 10, 50, st.session_state.head_height)

st.sidebar.header("⚙️ Özellikler & Organlar")
feelers = st.sidebar.checkbox("Antenler (Feelers)", value=st.session_state.feelers)
wings = st.sidebar.checkbox("Kanatlar (Wings)", value=st.session_state.wings)
feet = st.sidebar.checkbox("Ayaklar (Feet)", value=st.session_state.feet)
pattern = st.sidebar.selectbox("Gövde Deseni", ["Çizgili", "Benekli", "Düz"], index=["Çizgili", "Benekli", "Düz"].index(st.session_state.pattern))

# --- ÇİZİM ALANI ---
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = dal_ax.subplots(figsize=(7, 6))
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Arka plan yumuşak doğa dalgaları
    x = np.linspace(0, 10, 200)
    for i in range(-5, 12):
        y_wave = np.sin(x + i * 0.4) * 1.2 + i * 0.8
        ax.plot(x, y_wave, color="#B2DFDB", alpha=0.3, linewidth=1.5)

    # Böcek Bileşenleri Hesaplamaları
    b_len_scaled = body_length / 10.0
    
    # 1. Kanatlar (Gövdenin altında kalması için zorder=1.5)
    if wings:
        wing_left = patches.Ellipse((3.8, 3.2), 2.2, b_len_scaled * 0.7, angle=25, color="white", alpha=0.6, zorder=1.5)
        wing_right = patches.Ellipse((6.2, 3.2), 2.2, b_len_scaled * 0.7, angle=-25, color="white", alpha=0.6, zorder=1.5)
        ax.add_patch(wing_left)
        ax.add_patch(wing_right)

    # 2. Gövde (Abdomen)
    body = patches.Ellipse(
        (5, 3),
        (neck_width * 1.1) / 10.0,
        b_len_scaled,
        color=primary_color,
        zorder=2,
    )
    ax.add_patch(body)

    # 3. Göğüs (Thorax)
    thorax = patches.Ellipse(
        (5, 3 + b_len_scaled / 2 - 0.2),
        neck_width / 10.0,
        neck_height / 10.0,
        color=secondary_color,
        zorder=3,
    )
    ax.add_patch(thorax)

    # 4. Kafa (Head)
    head_y = 3 + b_len_scaled / 2 + neck_height / 10.0 - 0.1
    head = patches.Ellipse(
        (5, head_y),
        head_width / 10.0,
        head_height / 10.0,
        color=secondary_color,
        zorder=4,
    )
    ax.add_patch(head)

    # 5. Gözler
    eye_offset = head_width / 30.0
    ax.scatter([5 - eye_offset, 5 + eye_offset], [head_y + head_height/30.0, head_y + head_height/30.0], color="white", s=35, zorder=5)
    ax.scatter([5 - eye_offset, 5 + eye_offset], [head_y + head_height/30.0, head_y + head_height/30.0], color="black", s=12, zorder=6)

    # 6. Desenler
    if pattern == "Çizgili":
        for j in np.linspace(2, 3.5, 4):
            ax.plot(
                [4.5, 5.5],
                [j, j],
                color="white",
                alpha=0.6,
                linewidth=3,
                zorder=3,
            )
    elif pattern == "Benekli":
        ax.scatter([4.7, 5.3], [3.3, 3.3], color="yellow", s=50, zorder=3)
        ax.scatter([4.8, 5.2], [2.4, 2.4], color="yellow", s=40, zorder=3)

    # 7. Antenler
    if feelers:
        ax.plot([5, 4.2], [head_y + head_height / 20.0, head_y + 0.9], color="black", linewidth=2.5, zorder=4)
        ax.plot([5, 5.8], [head_y + head_height / 20.0, head_y + 0.9], color="black", linewidth=2.5, zorder=4)
        # Anten uçları (topuzcuk)
        ax.scatter([4.2, 5.8], [head_y + 0.9, head_y + 0.9], color="black", s=25, zorder=5)

    # 8. Ayaklar (Düzeltilmiş X merkez koordinatları ile)
    if feet:
        for fy in [3.3, 2.8, 2.3]:
            ax.plot([5 - neck_width / 20.0, 3.2], [fy, fy - 0.5], color="black", linewidth=2, zorder=1)
            ax.plot([5 + neck_width / 20.0, 6.8], [fy, fy - 0.5], color="black", linewidth=2, zorder=1)

    # Dinamik Eksen Sınırları (Kesilmeyi önler)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, max(8, head_y + 2.0))
    ax.axis("off")

    st.pyplot(fig)
    dal_ax.close(fig)

with col2:
    st.subheader("🧬 Tür Bilgileri")
    st.markdown(f"**Desen Tipi:** `{pattern}`")
    st.markdown(f"**Gövde Uzunluğu:** `{body_length} px`")
    st.markdown(f"**Anten Durumu:** `{'Aktif ✨' if feelers else 'Yok'}`")
    st.markdown(f"**Kanat Durumu:** `{'Aktif 🦋' if wings else 'Yok'}`")
    st.markdown(f"**Ayak Sayısı:** `{'6 Ayaklı 🕷️' if feet else 'Ayaksız'}`")
    
    st.write("---")
    
    if st.button("🎲 Rastgele Böcek Üret", use_container_width=True):
        st.session_state.body_length = random.randint(60, 180)
        st.session_state.neck_width = random.randint(25, 90)
        st.session_state.neck_height = random.randint(20, 70)
        st.session_state.head_width = random.randint(25, 65)
        st.session_state.head_height = random.randint(15, 40)
        st.session_state.primary_color = f"#{random.randint(0, 0xFFFFFF):06x}"
        st.session_state.secondary_color = f"#{random.randint(0, 0xFFFFFF):06x}"
        st.session_state.bg_color = random.choice(["#E6F4F1", "#FCE4EC", "#E8F5E9", "#FFF3E0", "#EDE7F6"])
        st.session_state.feelers = random.choice([True, False])
        st.session_state.feet = random.choice([True, False])
        st.session_state.wings = random.choice([True, False])
        st.session_state.pattern = random.choice(["Çizgili", "Benekli", "Düz"])
        st.rerun()
