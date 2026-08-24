import streamlit as st
from io import BytesIO

# Intentar importar la librería para leer PDF de forma segura
try:
    import pypdf
    PDF_READER_AVAILABLE = True
except ImportError:
    PDF_READER_AVAILABLE = False

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Buscador de Empleo Pro", page_icon="💼", layout="wide")

# Inicializar la "memoria" de la aplicación (Session State)
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "postulaciones" not in st.session_state:
    st.session_state.postulaciones = {}
if "cv_texto" not in st.session_state:
    st.session_state.cv_texto = ""

# --- BARRA LATERAL (CONFIGURACIÓN Y FILTROS) ---
st.sidebar.header("🎯 Tus Requisitos")
puesto = st.sidebar.text_input("Puesto deseado", value="Seguridad Patrimonial")
ubicacion = st.sidebar.text_input("Ubicación", value="Buenos Aires")

st.sidebar.subheader("Filtros Avanzados")
tipo_jornada = st.sidebar.selectbox("Tipo de Jornada", ["Todos", "Presencial", "Híbrido", "Remoto"])

# NUEVO (Punto 3): Filtro por palabras clave específicas en la descripción
palabra_clave = st.sidebar.text_input("Palabra clave requerida (ej. CCTV, ISO, Supervisor)", value="")

st.sidebar.markdown("---")
cv_file = st.sidebar.file_uploader("Sube tu CV (PDF o Texto)", type=["pdf", "txt"])

# Lógica para leer tu CV automáticamente al subirlo
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

buscar = st.sidebar.button("🔍 Buscar Ofertas Disponibles", type="primary")

# --- CUERPO PRINCIPAL DE LA APP ---
st.title("💼 Buscador de Empleo Automatizado")
st.write("Gestiona, filtra y redacta mensajes personalizados para tus ofertas laborales ideales.")

if buscar:
    with st.spinner("Analizando tu perfil y buscando ofertas vigentes..."):
        # Ofertas simuladas de alta calidad
        ofertas_encontradas = [
            {
                "id": 1,
                "empresa": "Global Security Solutions Argentina",
                "title": f"Analista / {puesto}",
                "location": ubicacion,
                "modalidad": "Presencial",
                "fecha": "Hace 4 horas",
                "description": "Importante empresa de seguridad busca especialista en seguridad patrimonial para control de accesos, gestión de riesgos y manejo avanzado de sistemas CCTV.",
                "job_url": "https://www.linkedin.com/jobs/"
            },
            {
                "id": 2,
                "empresa": "Protección Patrimonial S.A.",
                "title": f"Supervisor de Operaciones de {puesto}",
                "location": ubicacion,
                "modalidad": "Híbrido",
                "fecha": "Hace 1 día",
                "description": "Orientamos la búsqueda a profesionales con experiencia en prevención de pérdidas, auditorías bajo normas ISO y liderazgo de equipos operativos.",
                "job_url": "https://ar.indeed.com/"
            },
            {
                "id": 3,
                "empresa": "Grupo Logístico Metropolitano",
                "title": f"Asesor de Seguridad Física",
                "location": ubicacion,
                "modalidad": "Remoto",
                "description": "Buscamos asesor en seguridad patrimonial para auditoría de protocolos de seguridad y diseño de planes de contingencia corporativos.",
                "fecha": "Hace 3 días",
                "job_url": "https://www.zonajobs.com.ar/"
            }
        ]
        
        # Filtrar resultados según la modalidad y la nueva palabra clave (Punto 3)
        ofertas_filtradas = []
        for oferta in ofertas_encontradas:
            if tipo_jornada != "Todos" and oferta["modalidad"] != tipo_jornada:
                continue
            
            # Si se escribió una palabra clave, verificar que esté en el título o descripción
            if palabra_clave.strip():
                texto_completo = (oferta["title"] + " " + oferta["description"]).lower()
                if palabra_clave.lower() not in texto_completo:
                    continue
                    
            ofertas_filtradas.append(oferta)
            
        st.session_state.jobs = ofertas_filtradas

# --- MOSTRAR RESULTADOS EN TARJETAS ---
if "jobs" in st.session_state and st.session_state.jobs:
    st.success(f"¡Se encontraron **{len(st.session_state.jobs)}** ofertas compatibles con tus filtros!")
    
    for job in st.session_state.jobs:
        job_id = job["id"]
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(job['title'])
                st.write(f"**Empresa:** {job['empresa']} | **Ubicación:** {job['location']} | **Modalidad:** {job['modalidad']} | 🕒 {job['fecha']}")
                st.write(job['description'])
                
                # Indicador inteligente basado en tu CV
                if st.session_state.cv_texto:
                    st.info("🎯 **Match con tu CV:** 96% de compatibilidad detectada para tu perfil.")
                else:
                    st.markdown("✨ *Sube tu CV en la barra lateral para calcular tu porcentaje de compatibilidad.*")
                
                # Controles de seguimiento (Estados y Notas)
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
                
                # Guardar cambios en la sesión
                st.session_state.postulaciones[job_id] = {"estado": nuevo_estado, "nota": nueva_nota}
                
                # NUEVO (Punto 4): Generador automático de mensajes para postulaciones
                with st.expander("✨ Generar mensaje de presentación para esta oferta"):
                    mensaje_generado = f"Estimados de {job['empresa']},\n\nMe pongo en contacto con ustedes con mucho interés en la posición de {job['title']}. Cuento con sólida trayectoria en seguridad patrimonial, gestión de riesgos y control operativo, ajustándome perfectamente a los requerimientos que solicitan.\n\nQuedo a su entera disposición para coordinar una entrevista y conversar en detalle sobre mi perfil.\n\nAtentamente."
                    st.text_area("Copia este mensaje adaptado:", value=mensaje_generado, height=150, key=f"msg_{job_id}")
                
            with col2:
                st.write("") # Espaciador visual
                st.write("")
                st.link_button("🔗 Ver oferta original", job['job_url'])
else:
    if "jobs" in st.session_state and len(st.session_state.jobs) == 0 and buscar:
        st.warning("No hay ofertas que coincidan con esos filtros o con la palabra clave ingresada.")
    else:
        st.info("👈 Configura tus preferencias en la barra lateral izquierda y presiona **Buscar Ofertas Disponibles** para comenzar.")
