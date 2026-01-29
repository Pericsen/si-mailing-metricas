import streamlit as st
import os

# Parsear la variable de entorno como lista
ALLOWED_USERS = os.getenv("ALLOWED_USERS", "").split(",")
# Limpiar espacios en blanco
ALLOWED_USERS = [email.strip() for email in ALLOWED_USERS if email.strip()]

login_page = st.Page(
    "pages/login.py",
    title="Inicio de sesion"
)

dash_page = st.Page(
    "pages/dash.py",
    title="Tablero"
)

if not st.user.is_logged_in:
    pg = st.navigation([login_page], position="hidden")
else:
    # Verificar si el usuario está autorizado
    if st.user.email not in ALLOWED_USERS:
        st.error(f"Acceso denegado. El usuario {st.user.email} no tiene permisos para acceder a esta aplicación.")
        st.info("Contactá al administrador del sistema.")
        if st.button("Cerrar sesión"):
            st.logout()
        st.stop()
    
    # Si llegó acá, está autorizado
    pg = st.navigation([dash_page])
    
    with st.sidebar:
        st.write(f"Hola, {st.user.name}!")
        if st.button("Cerrar sesión"):
            st.logout()

pg.run()