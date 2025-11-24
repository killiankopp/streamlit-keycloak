from dataclasses import asdict
from streamlit_keycloak import login
import streamlit as st


def main():
    st.subheader(f"Welcome {keycloak.user_info['preferred_username']}!")
    st.write(f"Here is your user information:")
    st.write(asdict(keycloak))
    if st.button("Disconnect"):
        keycloak.authenticated = False


st.title("Streamlit Keycloak example")
keycloak = login(
    url="https://keycloak.amazone.lan",
    realm="koden",
    client_id="streamlit",
)

if keycloak.authenticated:
    main()