import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

PROMPT_FILE = Path("v1.0/prompt.txt")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, auth_status, username = authenticator.login("Login", location="main")

if auth_status:
    authenticator.logout("Logout", "sidebar")
    st.success(f"Welcome, {name}!")

    content = PROMPT_FILE.read_text(encoding="utf-8") if PROMPT_FILE.exists() else ""
    sections = {}
    current, buffer = None, []

    for line in content.splitlines():
        if line.startswith("## SECTION"):
            if current:
                sections[current] = "\n".join(buffer)
            current, buffer = line.strip(), []
        elif current:
            buffer.append(line)
    if current: sections[current] = "\n".join(buffer)

    selected = st.selectbox("Select Section", list(sections.keys()))
    st.code(sections[selected])

    if st.checkbox("Edit"):
        new_text = st.text_area("Edit Section", sections[selected], height=300)
        if st.button("Save"):
            sections[selected] = new_text
            with open(PROMPT_FILE, 'w', encoding="utf-8") as f:
                for sec, txt in sections.items():
                    f.write(f"{sec}\n{txt}\n")
            st.success("Saved.")
else:
    st.warning("Please login.")