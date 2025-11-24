import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import httpx

# Configuration Keycloak
KEYCLOAK_URL = "https://iam.karned.bzh/realms/Amazone"
CLIENT_ID = "streamlit"
REDIRECT_URI = "http://localhost:8501"
SCOPE = "openid email profile"

# Initialiser la session OAuth2 avec PKCE
def get_oauth_client():
    client = OAuth2Session(
        CLIENT_ID,
        scope=SCOPE,
        redirect_uri=REDIRECT_URI,
    )
    return client

# Générer l'URL d'autorisation
def get_authorization_url():
    client = get_oauth_client()
    uri, state = client.create_authorization_url(KEYCLOAK_URL + "/protocol/openid-connect/auth")
    return uri, state

# Échanger le code contre un token
def fetch_token(code):
    client = get_oauth_client()
    token = client.fetch_token(
        KEYCLOAK_URL + "/protocol/openid-connect/token",
        code=code,
        grant_type="authorization_code",
    )
    return token

# Vérifier si l'utilisateur est authentifié
def is_authenticated():
    return "token" in st.session_state

# Interface Streamlit
def main():
    if not is_authenticated():

        uri, state = get_authorization_url()
        st.session_state["oauth_state"] = state
        st.markdown(f"[Se connecter]({uri})", unsafe_allow_html=True)

        # Après redirection, récupérer le code
        if "code" in st.query_params:
            code = st.query_params["code"]
            token = fetch_token(code)
            st.session_state["token"] = token
            st.query_params.clear()  # Nettoie les paramètres de l'URL
            st.rerun()
    else:
        st.write("Vous êtes connecté !")
        st.json(st.session_state["token"])
        if st.button("Se déconnecter"):
            del st.session_state["token"]
            st.rerun()

if __name__ == "__main__":
    main()
