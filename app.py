import streamlit as st
import requests
from datetime import datetime

# ---------- EASTER EGGS ----------
EASTER_EGGS = {
    "tpwp2012": "🚨 UNBAN TPWP! 🚨",
    "bxn_vi": "Not tuff 🤣🤣🤣",
    "builderman": "🗿 RESPECT THE OG",
    "vgaiza1234": "Tuff guy ngl peak",
}

# ---------- PAGE CONFIG (STATIC ONLY) ----------
st.set_page_config(
    page_title="#UnbanTPWP / Roblox ID Lookup",
    page_icon="🤫",
    layout="centered"
)

# ---------- COPY BUTTON ----------
def copy_button(text):
    escaped = text.replace("'", "\\'")
    st.markdown(f"""
    <button onclick="navigator.clipboard.writeText('{escaped}')"
    style="
        background:#3cff88;
        color:#000;
        border:none;
        padding:10px 18px;
        border-radius:10px;
        font-weight:700;
        cursor:pointer;
    ">
        📋 Copy
    </button>
    """, unsafe_allow_html=True)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.main-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 800;
}

.subtext {
    text-align: center;
    color: #9aa4b2;
    margin-bottom: 25px;
}

.card {
    background: #161b22;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.45);
    margin-top: 20px;
}

.label {
    color: #9aa4b2;
    font-size: 0.85rem;
}

.value {
    color: #3cff88;
    font-weight: 600;
    font-size: 1.05rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- INPUT ----------
username = st.text_input("Roblox Username", placeholder="Enter username here…")

search = st.button("🔎 Search User", use_container_width=True)

# ---------- DYNAMIC TITLE (EASTER EGGS) ----------
display_title = EASTER_EGGS.get(
    username.lower().strip() if username else "",
    "🔍 Roblox Username → ID Lookup"
)

st.markdown(f"<div class='main-title'>{display_title}</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtext'>Fast, clean, no BS. Get Roblox user info instantly. Made with love by tpwp.</div>",
    unsafe_allow_html=True
)

# ---------- LOGIC ----------
if search and username:
    with st.spinner("Fetching Roblox data..."):
        try:
            res = requests.post(
                "https://users.roblox.com/v1/usernames/users",
                json={"usernames": [username]}
            )
            data = res.json()

            if "data" not in data or len(data["data"]) == 0:
                st.error("❌ User not found. Check spelling and try again.")
            else:
                user = data["data"][0]
                user_id = user["id"]
                display_name = user["displayName"]

                user_info = requests.get(
                    f"https://users.roblox.com/v1/users/{user_id}"
                ).json()

                created_raw = user_info.get("created")
                if created_raw:
                    created_dt = datetime.fromisoformat(created_raw.replace("Z", "+00:00"))
                    days_ago = (datetime.now(created_dt.tzinfo) - created_dt).days
                    created_str = created_dt.strftime("%d %b %Y") + f" • {days_ago} days ago"
                else:
                    created_str = "N/A"

                thumb_url = (
                    "https://thumbnails.roblox.com/v1/users/avatar-headshot"
                    f"?userIds={user_id}&size=150x150&format=Png"
                )
                thumb_data = requests.get(thumb_url).json()
                avatar = thumb_data.get("data", [{}])[0].get("imageUrl")

                profile = f"https://www.roblox.com/users/{user_id}/profile"

                # ---------- OUTPUT CARD ----------
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                col1, col2 = st.columns([1, 2])

                with col1:
                    if avatar:
                        st.image(avatar, width=120)
                    else:
                        st.caption("Avatar unavailable")

                with col2:
                    st.markdown(f"<div class='label'>Username</div><div class='value'>{username}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='label'>User ID</div><div class='value'>{user_id}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='label'>Display Name</div><div class='value'>{display_name}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='label'>Joined</div><div class='value'>{created_str}</div>", unsafe_allow_html=True)
                    st.markdown(f"[🔗 View Profile]({profile})")

                st.markdown("---")

                st.markdown("### 📋 Copy")
                copy_button(f"{username} - {user_id}")

                st.markdown("</div>", unsafe_allow_html=True)
                st.success("✔️ User found")

        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")
