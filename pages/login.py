import streamlit as st

image_path = "images/sanisidrologo.png"

def login_screen(text_alignment):
    st.header("Esta aplicación es privada.", text_alignment=text_alignment)
    if st.button("Iniciar sesión"):
        st.login("google")

if not st.user.is_logged_in:
    with st.container(border=True, horizontal_alignment="center"):
        st.image(image=image_path)
        login_screen(text_alignment="center")
else:
    st.switch_page("app.py")