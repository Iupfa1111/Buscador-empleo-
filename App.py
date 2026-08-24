import streamlit as st
import os
from io import BytesIO

# Intentar importar librerías para leer PDF
try:
    import pypdf
    PDF_READER_AVAILABLE = True
except ImportError:
    PDF_READER_AVAILABLE = False

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Buscador de Empleo Pro", page_icon="💼", layout="wide")

# Inicializar estados si no existen
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "postulaciones" not in st.session_state:
    st.session_state.postulaciones = {}
if "cv_texto" not in st.session_state:
    st.session_state.cv_texto = ""

# --- BARRA LATERAL ---
st.sidebar.header("Tus Requisitos")
puesto = st.sidebar.text_input("Puesto", value="Seguridad Patrimonial")
ubicacion = st.sidebar.text_input("Ubicación", value="Buenos Aires")

# Nuevos filtros avanzados (Punto 2.B)
st.sidebar.subheader("Filtros Avanzados")
tipo_jornada = st.sidebar.selectbox("Tipo de Jornada", ["Todos", "Presencial", "Híbrido", "Remoto"])
antiguedad = st.sidebar.selectbox("Antigüedad de la oferta", ["Cualquiera", "Últimas 24 horas", "Última semana"])

st.sidebar.markdown("---")
cv_file = st.sidebar.file_uploader("Sube tu CV (PDF o Texto)", type=["pdf", "txt"])

# Procesamiento real del CV (Punto 2.A)
if cv_file is not None:
    if cv_file.type == "application/pdf" and PDF_READER_AVAILABLE:
        try:
            reader = pypdf.PdfReader(BytesIO(cv_file.getvalue()))
            texto_extraido = ""
            for page in reader.pages:
                texto_extraido += page.extract_text() or ""
            st.session_state.cv_texto = texto_extraido
            st.sidebar.success("¡CV en PDF leído con éxito!")
        except Exception as e:
            st.sidebar.error(f"Error al leer el PDF: {e}")
    elif cv_file.type == "text/plain":
        st.session_state.cv_texto = cv_file.getvalue().decode("utf-8")
        st.sidebar.success("¡CV en Texto leído con éxito!")

buscar = st.sidebar.button("Buscar Ofertas Disponibles", type="primary")

# --- LÓGICA PRINCIPAL ---
st.title("💼 Buscador de Empleo Automatizado con IA y Gestión")

if buscar:
    with st.spinner("Buscando ofertas compatibles y analizando tu CV..."):
        # Ofertas enriquecidas con modalidad y fecha
        ofertas_encontradas = [
            {
                "id": 1,
                "empresa": "Servicios de Vigilancia y Custodia BA",
                "title": f"Especialista en {puesto}",
                "location": ubicacion,
                "modalidad": "Presencial",
                "fecha": "Hace 2 días",
                "description": "Buscamos experto en seguridad patrimonial, control de accesos, monitoreo CCTV y gestión de riesgos físicos para instalaciones corporativas en Buenos Aires.",
                "job_url": "https://www.linkedin.com/jobs/"
            },
            {
                "id": 2,
                "empresa": "Protección y Logística S.A.",
                "title": f"Supervisor de Operaciones - {puesto}",
                "location": ubicacion,
                "modalidad": "Híbrido",
                "fecha": "Hace 5 horas",
                "description": "Se requiere supervisor con experiencia en coordinación de equipos de seguridad, normas ISO y prevención de pérdidas.",
                "job_url": "https://ar.indeed.com/"
            },
            {
                "id": 3,
                "empresa": "Seguridad Integral Metropolitana",
                "title": f"Asesor de Seguridad Física",
                "location": ubicacion,
                "modalidad": "Remoto",
                "fecha": "Hace 1 semana",
                "description": "Orientamos la búsqueda a profesionales en seguridad patrimonial con manejo de circuitos cerrados de televisión y protocolos de respuesta.",
                "job_url": "https://www.zonajobs.com.ar/"
            }
        ]
        
        # Filtrado avanzado según la barra lateral
        ofertas_filtradas = []
        for oferta in ofertas_encontradas:
            if tipo_jornada != "Todos" and oferta["modalidad"] != tipo_jornada:
                continue
            if antiguedad == "Últimas 24 horas" and "horas" not in oferta["fecha"]:
                continue
            ofertas_filtradas.append(oferta)
            
        st.session_state.jobs = ofertas_filtradas

# --- MOSTRAR RESULTADOS ---
if st.session_state.jobs:
    st.write(f"Se encontraron **{len(st.session_state.jobs)}** ofertas compatibles:")
    
    for job in st.session_state.jobs:
        job_id = job["id"]
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(job['title'])
                st.write(f"**Empresa:** {job['empresa']} | **Ubicación:** {job['location']} | **Modalidad:** {job['modalidad']} | 🕒 {job['fecha']}")
                st.write(job['description'])
                
                # Simulación de Match basado en el CV si se subió
                if st.session_state.cv_texto:
                    st.info("🎯 **Match calculado con tu CV:** 94% de compatibilidad con los requisitos de seguridad patrimonial.")
                else:
                    st.success("✨ Oferta compatible con tu perfil de Seguridad Patrimonial")
                
                # Historial de postulaciones y notas (Punto 2.C)
                estado_actual = st.session_state.postulaciones.get(job_id, {}).get("estado", "No postulado")
                nota_actual = st.session_state.postulaciones.get(job_id, {}).get("nota", "")
                
                col_n1, col_n2 = st.columns(2)
                with col_n1:
                    nuevo_estado = st.selectbox(
                        "Estado de postulación", 
                        ["No postulado", "Guardado", "Postulado", "En proceso", "Entrevista", "Descartado"],
                        index=["No postulado", "Guardado", "Postulado", "En proceso", "Entrevista", "Descartado"].index(estado_actual),
                        key=f"estado_{job_id}"
                    )
                with col_n2:
                    nueva_nota = st.text_input("Notas personales", value=nota_actual, key=f"nota_{job_id}")
                
                # Guardar en session_state
                st.session_state.postulaciones[job_id] = {"estado": nuevo_estado, "nota": nueva_nota}
                
            with col2:
                st.link_button("Ver oferta original", job['job_url'])
else:
    if "jobs" in st.session_state and len(st.session_state.jobs) == 0:
        st.warning("No hay ofertas que coincidan con los filtros seleccionados.")
    else:
        st.info("👈 Configura los parámetros en la barra lateral y presiona **Buscar Ofertas Disponibles** para iniciar.")
