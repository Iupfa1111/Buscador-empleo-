import streamlit as st
from jobspy import scrape_jobs
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
    # Puntuación simple basada en solapamiento de palabras
    return round((len(intersection) / len(job_words)) * 100) if job_words else 0

# --- BARRA LATERAL ---
st.sidebar.header("Tus Requisitos")
puesto = st.sidebar.text_input("Puesto", value="Seguridad Patrimonial")
ubicacion = st.sidebar.text_input("Ubicación", value="Buenos Aires")
cv_file = st.sidebar.file_uploader("Sube tu CV (PDF)", type=["pdf"])

buscar = st.sidebar.button("Buscar Ofertas Reales", type="primary")

# --- LÓGICA PRINCIPAL ---
st.title("💼 Buscador de Empleo Automatizado")

if buscar:
    with st.spinner("Conectando con portales de empleo..."):
        try:
            # JobSpy realiza el scraping en tiempo real
            jobs = scrape_jobs(
                site_name=["linkedin", "indeed"],
                search_term=puesto,
                location=ubicacion,
                results_wanted=5
            )
            st.session_state.jobs = jobs
        except Exception as e:
            st.error(f"Error al buscar: {e}")

# --- MOSTRAR RESULTADOS ---
if "jobs" in st.session_state:
    cv_text = extract_text_from_pdf(cv_file) if cv_file else ""
    
    for _, job in st.session_state.jobs.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(job['title'])
                st.write(f"**Empresa:** {job['company']} | **Ubicación:** {job['location']}")
                
                # Análisis de Match
                score = calculate_match(cv_text, job['description'] or "")
                st.progress(score/100, text=f"Compatibilidad con tu CV: {score}%")
                
            with col2:
                st.link_button("Ver oferta", job['job_url'])
else:
    st.info("👈 Configura los parámetros y presiona buscar para iniciar.")
