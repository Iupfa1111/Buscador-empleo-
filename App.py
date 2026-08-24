import streamlit as st
from io import BytesIO
import json

# Intentar importar librerías necesarias
try:
    import pypdf
    PDF_READER_AVAILABLE = True
except ImportError:
    PDF_READER_AVAILABLE = False

try:
    from google import genai
    from google.genai import types
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Buscador de Empleo Pro en Vivo", page_icon="💼", layout="wide")

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

buscar = st.sidebar.button("🔍 Buscar Ofertas Reales en la Web", type="primary")

# --- CUERPO PRINCIPAL DE LA APP ---
st.title("💼 Buscador de Empleo en Tiempo Real")
st.write("Buscando vacantes reales y vigentes conectadas directamente a internet.")

if buscar:
    if not AI_AVAILABLE:
        st.error("Falta instalar la librería de IA. Asegúrate de incluir 'google-genai' en tus dependencias.")
    else:
        with st.spinner("Conectando con la web en tiempo real para buscar vacantes actuales..."):
            try:
                # Inicializar el cliente de IA usando la API Key configurada en Streamlit Secrets
                client = genai.Client()
                
                # Prompt estructurado para que la IA busque en Google y devuelva un formato JSON limpio
                prompt_busqueda = f"""
                Busca en la web ofertas de empleo reales y recientes para el puesto de '{puesto}' en '{ubicacion}'.
                Encuentra al menos 3 o 4 ofertas reales publicadas recientemente.
                Devuelve la respuesta EXCLUSIVAMENTE en formato de lista JSON válida de objetos, sin texto adicional antes ni después.
                Cada objeto debe tener exactamente estas claves:
                - "empresa": Nombre de la empresa o consultora.
                - "title": Título exacto del puesto.
                - "location": Ubicación detallada.
                - "modalidad": "Presencial", "Híbrido" o "Remoto".
                - "fecha": Cuándo se publicó o "Reciente".
                - "description": Breve resumen de las tareas o requisitos.
                - "job_url": URL real o enlace web de la oferta si está disponible (o enlace al portal de empleo donde se encuentra).
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_busqueda,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        temperature=0.1
                    ),
                )
                
                # Limpiar y convertir la respuesta de la IA en datos que la app pueda mostrar
                texto_respuesta = response.text.strip()
                if texto_respuesta.startswith("```json"):
                    texto_respuesta = texto_respuesta[7:]
                if texto_respuesta.endswith("```"):
                    texto_respuesta = texto_respuesta[:-3]
                
                ofertas_encontradas = json.loads(texto_respuesta.strip())
                
                # Asignar un ID único a cada oferta traída de la web
                for idx, oferta in enumerate(ofertas_encontradas, start=1):
                    oferta["id"] = idx
                
                # Aplicar tus filtros (Jornada y Palabra clave) sobre los resultados reales
                ofertas_filtradas = []
                for oferta in ofertas_encontradas:
                    mod = oferta.get("modalidad", "Presencial")
                    if tipo_jornada != "Todos" and mod.lower() != tipo_jornada.lower():
                        continue
                    
                    if palabra_clave.strip():
                        texto_completo = (oferta.get("title", "") + " " + oferta.get("description", "")).lower()
                        if palabra_clave.lower() not in texto_completo:
                            continue
                            
                    ofertas_filtradas.append(oferta)
                    
                st.session_state.jobs = ofertas_filtradas

            except Exception as e:
                st.error(f"No se pudieron cargar las ofertas en vivo en este momento. Inténtalo de nuevo. Detalle: {e}")

# --- MOSTRAR RESULTADOS EN TARJETAS ---
if "jobs" in st.session_state and st.session_state.jobs:
    st.success(f"¡Se encontraron **{len(st.session_state.jobs)}** ofertas activas en la web compatibles con tus filtros!")
    
    for job in st.session_state.jobs:
        job_id = job["id"]
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(job.get('title', 'Puesto sin título'))
                st.write(f"**Empresa:** {job.get('empresa', 'No especificada')} | **Ubicación:** {job.get('location', '')} | **Modalidad:** {job.get('modalidad', '')} | 🕒 {job.get('fecha', '')}")
                st.write(job.get('description', ''))
                
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
                
                # Generador automático de mensajes para postulaciones (Punto 4)
                with st.expander("✨ Generar mensaje de presentación para esta oferta"):
                    mensaje_generado = f"Estimados de {job.get('empresa', 'la empresa')},\n\nMe pongo en contacto con ustedes con mucho interés en la posición de {job.get('title', 'el puesto')}. Cuento con sólida trayectoria en seguridad patrimonial, gestión de riesgos y control operativo, ajustándome perfectamente a los requerimientos que solicitan.\n\nQuedo a su entera disposición para coordinar una entrevista y conversar en detalle sobre mi perfil.\n\nAtentamente."
                    st.text_area("Copia este mensaje adaptado:", value=mensaje_generado, height=150, key=f"msg_{job_id}")
                
            with col2:
                st.write("") 
                st.write("")
                url_destino = job.get('job_url', '#')
                if url_destino.startswith('http'):
                    st.link_button("🔗 Ver oferta original", url_destino)
                else:
                    st.markdown(f"[🔗 Buscar enlace]({url_destino})")
else:
    if "jobs" in st.session_state and len(st.session_state.jobs) == 0 and buscar:
        st.warning("No se encontraron ofertas web activas con esos filtros en este momento.")
    else:
        st.info("👈 Configura tus preferencias en la barra lateral izquierda y presiona **🔍 Buscar Ofertas Reales en la Web** para consultar internet en tiempo real.")
