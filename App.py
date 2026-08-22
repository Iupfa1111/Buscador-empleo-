import streamlit as st
from pypdf import PdfReader

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Buscador de Empleo Pro", page_icon="💼", layout="wide")

# --- FUNCIONES DE AYUDA ---
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def calculate_match(cv_text, job_description):
    if not cv_text or not job_description: return 0
    cv_words = set(cv_text.lower().split())
    job_words = set(job_description.lower().split())
    intersection = cv_words.intersection(job_words)
    return round((len(intersection) / len(job_words)) * 100) if job_words else 0

# --- BARRA LATERAL ---
st.sidebar.header("Tus Requisitos")
puesto = st.sidebar.text_input("Puesto", value="Seguridad Patrimonial")
ubicacion = st.sidebar.text_input("Ubicación", value="Buenos Aires")
cv_file = st.sidebar.file_uploader("Sube tu CV (PDF)", type=["pdf"])

buscar = st.sidebar.button("Buscar Ofertas Disponibles", type="primary")

# --- LÓGICA PRINCIPAL ---
st.title("💼 Buscador de Empleo Automatizado")

if buscar:
    with st.spinner("Buscando ofertas compatibles..."):
        # Base de ofertas en tiempo real simulada de alta calidad para tu sector
        ofertas_encontradas = [
            {
                "id": 1,
                "empresa": "Servicios de Vigilancia y Custodia BA",
                "title": f"Especialista en {puesto}",
                "location": ubicacion,
                "description": "Buscamos experto en seguridad patrimonial, control de accesos, monitoreo CCTV y gestión de riesgos físicos para instalaciones corporativas en Buenos Aires.",
                "job_url": "https://www.linkedin.com/jobs/"
            },
            {
                "id": 2,
                "empresa": "Protección y Logística S.A.",
                "title": f"Supervisor de Operaciones - {puesto}",
                "location": ubicacion,
                "description": "Se requiere supervisor con experiencia en coordinación de equipos de seguridad, normas ISO y prevención de pérdidas.",
                "job_url": "https://ar.indeed.com/"
            },
            {
                "id": 3,
                "empresa": "Seguridad Integral Metropolitana",
                "title": f"Asesor de Seguridad Física",
                "location": ubicacion,
                "description": "Orientamos la búsqueda a profesionales en seguridad patrimonial con manejo de circuitos cerrados de televisión y protocolos de respuesta.",
                "job_url": "https://www.zonajobs.com.ar/"
            }
        ]
        st.session_state.jobs = ofertas_encontradas

# --- MOSTRAR RESULTADOS ---
if "jobs" in st.session_state:
    cv_text = extract_text_from_pdf(cv_file) if cv_file else ""
    
    for job in st.session_state.jobs:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(job['title'])
                st.write(f"**Empresa:** {job['empresa']} | **Ubicación:** {job['location']}")
                st.write(job['description'])
                
                # Análisis de Match con el CV subido
                score = calculate_match(cv_text, job['description'])
                st.progress(score/100, text=f"Compatibilidad con tu CV: {score}%")
                
            with col2:
                st.link_button("Ver oferta original", job['job_url'])
else:
    st.info("👈 Sube tu CV, configura los parámetros y presiona buscar para iniciar.")
