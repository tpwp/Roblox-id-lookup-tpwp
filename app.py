import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Roblox Username ➜ ID", page_icon="🎮", layout="centered")
st.image("logo.png", width=100) 
st.title("🔍 Roblox Username ➜ ID Lookup")
st.markdown("Enter a Roblox username to get user ID and account info.")

username = st.text_input("Roblox Username")

if st.button("Search") and username:
    with st.spinner("Fetching info..."):
        try:
            # Roblox username lookup
            res = requests.post(
                "https://users.roblox.com/v1/usernames/users",
                json={"usernames": [username]}
            )
            data = res.json()

            if "data" in data and len(data["data"]) > 0:
                user = data["data"][0]
                user_id = user["id"]
                display_name = user["displayName"]

                # Get account creation date
                user_info = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
                created_raw = user_info.get("created")
                if created_raw:
                    created_dt = datetime.fromisoformat(created_raw.replace("Z", "+00:00"))
                    days_ago = (datetime.now(created_dt.tzinfo) - created_dt).days
                    created_str = created_dt.strftime("%d/%m/%Y") + f" ({days_ago} days ago)"
                else:
                    created_str = "N/A"

                # Get avatar
                thumb_url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png"
                thumb_data = requests.get(thumb_url).json()
                avatar_data = thumb_data.get("data", [{}])[0]
                if avatar_data.get("state") == "Completed":
                    avatar_url = avatar_data.get("imageUrl")
                    st.image(avatar_url, caption=f"{username}'s Avatar")
                else:
                    st.warning("⚠️ Avatar not available or still processing.")

                # Other info
                profile = f"https://www.roblox.com/users/{user_id}/profile"

                st.markdown(f"**🧑 Username:** `{username}`")
                st.markdown(f"**🆔 User ID:** `{user_id}`")
                st.markdown(f"**📛 Display Name:** `{display_name}`")
                st.markdown(f"**📅 Joined:** `{created_str}`")
                st.markdown(f"[🔗 Profile Link]({profile})", unsafe_allow_html=True)

                st.markdown("### 📋 Copy this:")
                st.code(f"{username} - {user_id}", language="markdown")

            else:
                st.error("❌ User not found. Double-check the username.")

        except Exception as e:
            st.error(f"Error: {e}")
