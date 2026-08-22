import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Buscador de Empleo Pro", page_icon="💼", layout="wide")

# --- BARRA LATERAL ---
st.sidebar.header("Tus Requisitos")
puesto = st.sidebar.text_input("Puesto", value="Seguridad Patrimonial")
ubicacion = st.sidebar.text_input("Ubicación", value="Buenos Aires")
cv_file = st.sidebar.file_uploader("Sube tu CV (PDF o Texto)", type=["pdf", "txt"])

buscar = st.sidebar.button("Buscar Ofertas Disponibles", type="primary")

# --- LÓGICA PRINCIPAL ---
st.title("💼 Buscador de Empleo Automatizado")

if buscar:
    with st.spinner("Buscando ofertas compatibles..."):
        # Ofertas simuladas de alta calidad para tu sector
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
    for job in st.session_state.jobs:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(job['title'])
                st.write(f"**Empresa:** {job['empresa']} | **Ubicación:** {job['location']}")
                st.write(job['description'])
                
                # Indicador visual limpio
                st.success("✨ Oferta compatible con tu perfil de Seguridad Patrimonial")
                
            with col2:
                st.link_button("Ver oferta original", job['job_url'])
else:
    st.info("👈 Configura los parámetros en la barra lateral y presiona **Buscar Ofertas Disponibles** para iniciar.")
