import streamlit as st

st.sidebar.title("🎶 Danh sách nghệ sĩ")

selected_artist = st.sidebar.radio(
    "Chọn nghệ sĩ:",
    [
        "Low G",
        "Đen Vâu",
        "Sơn Tùng M-TP",
        "Những bản nhạc giúp tâm trạng vui vẻ hơn"
    ]
)

# ================= SPOTIFY EMBEDS =================

spotify_embeds = {

    "Low G": """
    <iframe
        style="border-radius:12px"
        src="https://open.spotify.com/embed/artist/6TITnFVRcl0AcZ4syE7Toe"
        width="100%"
        height="352"
        frameborder="0"
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
    </iframe>x
    """,

    "Đen Vâu": """
    <iframe
        style="border-radius:12px"
        src="https://open.spotify.com/embed/artist/1LEtM3AleYg1xabW6CRkpi"
        width="100%"
        height="352"
        frameborder="0"
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
    </iframe>
    """,

    "Sơn Tùng M-TP": """
    <iframe
        style="border-radius:12px"
        src="https://open.spotify.com/embed/artist/5dfZ5uSmzR7VQK0udbAVpf"
        width="100%"
        height="352"
        frameborder="0"
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
    </iframe>
    """
}

# ================= YOUTUBE VIDEOS =================

videos = {

    "Những bản nhạc giúp tâm trạng vui vẻ hơn": [
        (
            "Playlist vui vẻ",
            "https://www.youtube.com/watch?v=SlsH6PbDJZk"
        ),
        (
            "Lỡ Duyên",
            "https://www.youtube.com/watch?v=fq_H4A3HgD4"
        ),
        (
            "Nhạc quê hương",
            "https://www.youtube.com/watch?v=GOMGeUetqlI"
        ),
        (
            "Đi giữa trời rực rỡ",
            "https://www.youtube.com/watch?v=D1Uf9vREh6Q"
        ),
        (
            "Stay Happy",
            "https://www.youtube.com/watch?v=MMgPOQ9gJhM"
        ),
        (
            "Focus Time",
            "https://www.youtube.com/watch?v=Lcmlq9utGYk"
        )
    ]
}

# ================= DISPLAY =================

st.title(f"🎵 {selected_artist}")

if selected_artist in spotify_embeds:
    st.components.v1.html(
        spotify_embeds[selected_artist],
        height=380
    )

elif selected_artist in videos:
    for title, url in videos[selected_artist]:
        st.subheader(title)
        st.video(url)