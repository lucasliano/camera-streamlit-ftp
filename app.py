import logging
from datetime import datetime
import streamlit as st
from ftplib import FTP

# --- Configuración ---
FTP_HOST = '127.0.0.1'       # o la IP de tu host si estás en otra máquina
FTP_PORT = 21
FTP_USER = 'myuser'
FTP_PASS = 'mypassword'
REMOTE_FILEPATH = 'raw_images/'

# --- Configuración de Logging ---
# Esto imprimirá los logs en la consola donde se ejecuta Streamlit
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# --- Enviar imagen por cliente FTP ---
def send_ftp(image):
    try:
        logging.info("Iniciando proceso de subida FTP.")
        # Conexión FTP
        ftp = FTP()
        logging.info(f"Conectando a {FTP_HOST}:{FTP_PORT}...")
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        logging.info("Conexión establecida. Realizando login...")
        ftp.login(FTP_USER, FTP_PASS)
        logging.info(f"Login exitoso como usuario '{FTP_USER}'.")
        
        # Asegurarse de que el directorio remoto exista, si no, crearlo.
        try:
            ftp.cwd(REMOTE_FILEPATH)
            logging.info(f"Cambiado al directorio remoto: '{REMOTE_FILEPATH}'")
        except Exception:
            logging.warning(f"El directorio '{REMOTE_FILEPATH}' no existe. Intentando crearlo.")
            ftp.mkd(REMOTE_FILEPATH)
            ftp.cwd(REMOTE_FILEPATH)
            logging.info(f"Directorio '{REMOTE_FILEPATH}' creado y seleccionado.")

        # Obtener la extensión del archivo
        file_extension = image.name.split('.')[-1]
        remote_filename = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.{file_extension}'
        logging.info(f"Nombre de archivo remoto preparado: {remote_filename}")

        # Subir archivo directamente desde memoria
        logging.info(f"Ejecutando comando STOR para subir el archivo '{remote_filename}'...")
        ftp.storbinary(f'STOR {remote_filename}', image)
        logging.info("Comando STOR completado exitosamente.")

        logging.info("Cerrando conexión FTP.")
        ftp.quit()
        st.success("✅ Imagen subida con éxito.")

    except Exception as e:
        # Loguear el error completo con traceback para un diagnóstico detallado
        logging.error("Ocurrió un error durante la subida FTP.", exc_info=True)
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
