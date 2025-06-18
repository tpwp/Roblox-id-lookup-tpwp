import streamlit as st
import requests
import pyperclip

def get_user_data(username):
    url = "https://users.roblox.com/v1/usernames/users"
    data = {"usernames": [username], "excludeBannedUsers": False}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        users = response.json().get("data", [])
        if users:
            user = users[0]
            return {
                "username": user["name"],
                "display_name": user.get("displayName", ""),
                "user_id": user["id"]
            }
    return None

st.set_page_config(page_title="Roblox ID Lookup", page_icon="🎮", layout="centered")

st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stButton > button {
        background-color: #262730;
        color: white;
        border: 1px solid white;
    }
    a {
        color: #00aaff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔍 Roblox Username → ID Lookup")

username = st.text_input("Enter Roblox Username")

if st.button("Search") and username:
    user = get_user_data(username)
    if user:
        profile_link = f"https://www.roblox.com/users/{user['user_id']}/profile"
        avatar_url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user['user_id']}&size=150x150&format=Png&isCircular=true"

        st.image(avatar_url, caption=f"{user['username']}'s Avatar", width=150)
        st.markdown(f"""
        **🔤 Username:** `{user['username']}`  
        **🪪 User ID:** `{user['user_id']}`  
        **💬 Display Name:** `{user['display_name']}`  
        **🔗 [View Profile]({profile_link})**
        """)

        if st.button("📋 Copy Username - ID"):
            pyperclip.copy(f"{user['username']} - {user['user_id']}")
            st.success("Copied to clipboard!")
    else:
        st.error("User not found. Please check the username.")
