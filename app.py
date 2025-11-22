import streamlit as st
from streamlit_keycloak import login

keycloak = login(
    url="https://keycloak.amazone.lan",
    realm="koden",
    client_id="streamlit",
)

st.title("Bienvenue sur Streamlit")


if not keycloak.authenticated:
    st.warning("Utilisateur non authentifié")
    st.stop()

# Si authentifié :
user_info = keycloak.user_info
access_token = keycloak.access_token
refresh_token = keycloak.refresh_token

st.write("Connecté en tant que :", user_info["preferred_username"])
st.write("Token d'accès :", access_token)