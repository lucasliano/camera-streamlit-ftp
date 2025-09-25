from datetime import datetime
import streamlit as st
from ftplib import FTP

# --- Configuración ---
FTP_HOST = '127.0.0.1'       # o la IP de tu host si estás en otra máquina
FTP_PORT = 21
FTP_USER = 'myuser'
FTP_PASS = 'mypassword'
REMOTE_FILEPATH = 'raw_images/'

# --- Enviar imagen por cliente FTP ---
def send_ftp(image):
    try:
        # Conexión FTP
        ftp = FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)

        # Subir archivo directamente desde memoria
        # ftp.storbinary(f'STOR {REMOTE_FILEPATH + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}', image)
        ftp.storbinary(f'STOR {datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}', image)

        ftp.quit()
        st.success("✅ Imagen subida con éxito.")

    except Exception as e:
        st.error(f"❌ Error al subir la imagen: {e}")


# --- Interfaz Streamlit ---
st.set_page_config(page_title="Galería", layout="wide")
st.markdown("<h1 style='text-align: center;'> Generador de Dataset</h1>", unsafe_allow_html=True)

# --- Subida desde cámara o galería ---
st.markdown("## 📤 Subir una imagen (cámara o galería)")
image = st.file_uploader("📁 Desde tu galería", type=["jpg", "jpeg", "png"])

if image:
    if st.button("Subir"):
        with st.spinner("Aguarde un instante...", show_time=True):
            send_ftp(image)
