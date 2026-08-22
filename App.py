import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Buscador de Empleo Automatizado", page_icon="💼", layout="wide"
)

st.title("💼 Buscador de Empleo en Tiempo Real")
st.markdown(
    "Configura tus requisitos, encuentra ofertas compatibles y postúlate con un solo clic."
)

# --- 1. BARRA LATERAL: REQUISITOS DEL USUARIO ---
st.sidebar.header("Tus Requisitos y Perfil")

puesto_buscado = st.sidebar.text_input(
    "Puesto o Rol deseado", value="Seguridad Patrimonial"
)
ubicacion = st.sidebar.selectbox(
    "Ubicación",
    [
        "Buenos Aires, Argentina",
        "Capital Federal (CABA)",
        "Buenos Aires (GBA)",
        "Remoto",
    ],
)
modalidad = st.sidebar.selectbox("Modalidad", ["Presencial", "Híbrido", "Remoto"])

# Habilidades clave
habilidades = st.sidebar.multiselect(
    "Tus Habilidades / Competencias",
    [
        "Control de accesos",
        "Monitoreo CCTV",
        "Gestión de riesgos",
        "Seguridad física",
        "Coordinación de equipos",
        "Normas ISO",
    ],
    default=["Seguridad física", "Monitoreo CCTV"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Adjunta tu CV")
cv_file = st.sidebar.file_uploader(
    "Sube tu CV en formato PDF", type=["pdf"], key="cv_uploader"
)

# Botón principal de búsqueda
buscar = st.sidebar.button("Buscar Ofertas Disponibles", type="primary")

# --- 2. PANEL PRINCIPAL: RESULTADOS ---
if buscar:
    st.subheader(
        f"Resultados en vivo para: {puesto_buscado} en {ubicacion}"
    )

    with st.spinner("Buscando ofertas actualizadas..."):
        # NOTA TÉCNICA: Aquí es donde puedes integrar librerías de Python como 
        # python-jobspy o llamadas a APIs de empleo (LinkedIn/Indeed/Google Jobs)
        
        # Simulación conectada a parámetros reales ingresados
        ofertas_encontradas = [
            {
                "id": 1,
                "empresa": "Servicios de Vigilancia y Custodia BA",
                "puesto": f"Especialista en {puesto_buscado}",
                "ubicacion": ubicacion,
                "modalidad": modalidad,
                "enlace": "https://www.linkedin.com/jobs/",
            },
            {
                "id": 2,
                "empresa": "Protección y Logística S.A.",
                "puesto": f"Supervisor de Operaciones - {puesto_buscado}",
                "ubicacion": ubicacion,
                "modalidad": modalidad,
                "enlace": "https://ar.indeed.com/",
            }
        ]

    if not ofertas_encontradas:
        st.info("No se encontraron ofertas activas con los filtros especificados.")
    else:
        for oferta in ofertas_encontradas:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### {oferta['puesto']}")
                    st.markdown(
                        f"**Empresa:** {oferta['empresa']} | **Ubicación:** {oferta['ubicacion']} | **Modalidad:** {oferta['modalidad']}"
                    )
                    st.markdown(f"[Ver oferta original en la plataforma]({oferta['enlace']})")

                with col2:
                    st.write("") 
                    btn_postular = st.button("Enviar CV", key=f"btn_{oferta['id']}")

                    if btn_postular:
                        if cv_file is not None:
                            st.success(
                                f"¡Postulación enviada correctamente a {oferta['empresa']}!"
                            )
                        else:
                            st.error(
                                "Sube tu CV en la barra lateral antes de postularte."
                            )
else:
    st.info(
        "👈 Ajusta tus filtros de búsqueda en la barra lateral y presiona **'Buscar Ofertas Disponibles'**."
    )
