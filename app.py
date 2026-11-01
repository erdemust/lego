import matplotlib.patches as patches
import matplotlib.pyplot as dal_ax
import numpy as np
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Adjustable Bug Generator", page_icon="🐛", layout="wide"
)

st.title("🐛 Parametrik Böcek Üreticisi (Adjustable Bug Generator)")
st.write(
    "Sol taraftaki paneli kullanarak böceğin özelliklerini değiştirebilir ve anlık olarak güncellenmesini sağlayabilirsiniz."
)

# --- KONTROL PANELİ (SIDEBAR) ---
st.sidebar.header("🎨 Renkler")
primary_color = st.sidebar.color_picker("Gövde Rengi", "#FF4B4B")
secondary_color = st.sidebar.color_picker("Kafa/Detay Rengi", "#00CC96")
bg_color = st.sidebar.color_picker("Arka Plan Rengi", "#E6F4F1")

st.sidebar.header("📏 Gövde Boyutları")
neck_width = st.sidebar.slider("Boyun / Göğüs Genişliği", 10, 100, 50)
neck_height = st.sidebar.slider("Boyun Yüksekliği", 10, 100, 40)
body_length = st.sidebar.slider("Gövde Uzunluğu", 50, 200, 120)
head_width = st.sidebar.slider("Kafa Genişliği", 20, 80, 40)
head_height = st.sidebar.slider("Kafa Yüksekliği", 10, 50, 25)

st.sidebar.header("⚙️ Özellikler")
feelers = st.sidebar.checkbox("Antenler (Feelers)", value=True)
feet = st.sidebar.checkbox("Ayaklar (Feet)", value=True)
pattern = st.sidebar.selectbox("Desen (Pattern)", ["Çizgili", "Benekli", "Düz"])

# --- ÇİZİM ALANI ---
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = dal_ax.subplots(figsize=(7, 5))
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Arka plan dalgalı çizgileri
    x = np.linspace(0, 10, 200)
    for i in range(-5, 10):
        y_wave = np.sin(x + i * 0.5) * 1.5 + i
        ax.plot(x, y_wave, color="#B2DFDB", alpha=0.4, linewidth=2)

    # Böcek Bileşenleri
    # 1. Gövde (Abdomen)
    b_len_scaled = body_length / 10.0
    body = patches.Ellipse(
        (5, 3),
        (neck_width * 1.1) / 10.0,
        b_len_scaled,
        color=primary_color,
        zorder=1,
    )
    ax.add_patch(body)

    # 2. Göğüs (Thorax)
    thorax = patches.Ellipse(
        (5, 3 + b_len_scaled / 2 - 0.2),
        neck_width / 10.0,
        neck_height / 10.0,
        color=secondary_color,
        zorder=2,
    )
    ax.add_patch(thorax)

    # 3. Kafa (Head)
    head_y = 3 + b_len_scaled / 2 + neck_height / 10.0 - 0.1
    head = patches.Ellipse(
        (5, head_y),
        head_width / 10.0,
        head_height / 10.0,
        color="black",
        zorder=3,
    )
    ax.add_patch(head)

    # 4. Desenler
    if pattern == "Çizgili":
        for j in np.linspace(2, 3.5, 3):
            ax.plot(
                [4.6, 5.4],
                [j, j],
                color=secondary_color,
                linewidth=4,
                zorder=4,
            )
    elif pattern == "Benekli":
        ax.scatter([4.8, 5.2], [3.2, 3.2], color="yellow", s=40, zorder=4)
        ax.scatter([4.8, 5.2], [2.5, 2.5], color="yellow", s=40, zorder=4)

    # 5. Antenler
    if feelers:
        ax.plot([5, 4.3], [head_y + head_height / 20.0, head_y + 0.8], color="black", linewidth=2)
        ax.plot([5, 5.7], [head_y + head_height / 20.0, head_y + 0.8], color="black", linewidth=2)

    # 6. Ayaklar (X merkez offset düzeltildi: 4->5 ve 6->5)
    if feet:
        for fy in [3.2, 2.7, 2.2]:
            ax.plot([5 - neck_width / 20.0, 3.4], [fy, fy - 0.4], color="black", linewidth=2)
            ax.plot([5 + neck_width / 20.0, 6.6], [fy, fy - 0.4], color="black", linewidth=2)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    st.pyplot(fig)
    dal_ax.close(fig)

with col2:
    st.subheader("Özet Bilgiler")
    st.markdown(f"**Seçilen Desen:** {pattern}")
    st.markdown(f"**Gövde Boyu:** {body_length} px")
    st.markdown(f"**Anten Durumu:** {'Aktif' if feelers else 'Pasif'}")
    st.markdown(f"**Ayak Durumu:** {'Aktif' if feet else 'Pasif'}")
    
    if st.button("🎲 Rastgele Böcek Üret"):
        st.toast("Yeni böcek parametreleri yüklendi!", icon="✨")
