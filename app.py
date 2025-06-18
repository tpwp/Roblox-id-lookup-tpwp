import streamlit as st
import requests
from datetime import datetime
import pyperclip

st.set_page_config(page_title="Roblox Username ➜ ID Lookup", layout="centered", page_icon="🔍")
st.title("🔍 Roblox Username ➜ ID Lookup")
st.markdown("Enter a Roblox username to get ID and account info.")

username = st.text_input("Roblox Username")

if st.button("Search") and username:
    with st.spinner("Fetching data..."):
        try:
            res = requests.get(f"https://api.roblox.com/users/get-by-username?username={username}")
            data = res.json()
            
            if 'Id' not in data:
                st.error("User not found.")
            else:
                user_id = data['Id']
                display_name = data.get('Username', username)

                user_info = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
                created = user_info.get("created")
                if created:
                    dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    days_ago = (datetime.utcnow() - dt).days
                    created_str = dt.strftime("%d/%m/%Y") + f" ({days_ago} days ago)"
                else:
                    created_str = "N/A"

                profile_link = f"https://www.roblox.com/users/{user_id}/profile"
                avatar_url = f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=150&height=150&format=png"
                copy_text = f"{username} - {user_id}"

                st.image(avatar_url, caption=f"{username}'s Avatar", use_column_width=False)
                st.markdown(f"**🧑 Username:** `{username}`")
                st.markdown(f"**🆔 User ID:** `{user_id}`")
                st.markdown(f"**📝 Display Name:** `{display_name}`")
                st.markdown(f"**📅 Joined Date:** `{created_str}`")
                st.markdown(f"[🔗 View Profile]({profile_link})", unsafe_allow_html=True)

                st.markdown("### 📋 Copy this:")
                st.code(copy_text, language="markdown")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
