import requests
import streamlit as st

def get_user_id(username):
    url = f"https://users.roblox.com/v1/usernames/users"
    data = {"usernames": [username], "excludeBannedUsers": False}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        users = response.json().get("data", [])
        if users:
            return users[0]["id"]
    return None

st.set_page_config(page_title="Roblox User Lookup", page_icon="🎮", layout="centered")

st.title("🔍 Roblox Username to ID Lookup")
username = st.text_input("Enter Roblox Username")

if st.button("Search") and username:
    user_id = get_user_id(username)
    if user_id:
        st.success(f"**Username:** {username}\n**ID:** {user_id}")
        st.markdown(f"[🔗 View Profile](https://www.roblox.com/users/{user_id}/profile)")
    else:
        st.error("User not found. Check the username.")
