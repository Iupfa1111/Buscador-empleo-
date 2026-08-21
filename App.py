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
    "Ubicación", ["Buenos Aires (GBA)", "CABA", "Remoto", "Otro"]
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
        f"Resultados para: {puesto_buscado} en {ubicacion} ({modalidad})"
    )

    # Simulación de ofertas en tiempo real (Aquí es donde conectarías una API de empleo en el futuro)
    ofertas_simuladas = [
        {
            "id": 1,
            "empresa": "Protección Integral S.A.",
            "puesto": "Asesor de Seguridad Patrimonial",
            "ubicacion": "CABA",
            "modalidad": "Presencial",
            "match": "95%",
        },
        {
            "id": 2,
            "empresa": "Logística y Custodia Austral",
            "puesto": "Supervisor de Operaciones de Seguridad",
            "ubicacion": "Buenos Aires (GBA)",
            "modalidad": "Híbrido",
            "match": "88%",
        },
        {
            "id": 3,
            "empresa": "Corporación de Seguridad Global",
            "puesto": "Analista de Riesgos y Control",
            "ubicacion": "Remoto",
            "modalidad": "Remoto",
            "match": "80%",
        },
    ]

    if not ofertas_simuladas:
        st.info(
            "No se encontraron ofertas en este momento con los filtros seleccionados."
        )
    else:
        for oferta in ofertas_simuladas:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### {oferta['puesto']}")
                    st.markdown(
                        f"**Empresa:** {oferta['empresa']} | **Ubicación:** {oferta['ubicacion']} | **Modalidad:** {oferta['modalidad']}"
                    )
                    st.caption(
                        f"Compatibilidad estimada con tu perfil: {oferta['match']}"
                    )

                with col2:
                    st.write("")  # Espaciador visual
                    # Botón de postulación única
                    btn_postular = st.button(
                        "Enviar CV", key=f"btn_{oferta['id']}"
                    )

                    if btn_postular:
                        if cv_file is not None:
                            # Lógica para enviar el CV por correo o API
                            st.success(
                                f"¡CV enviado con éxito a {oferta['empresa']}!"
                            )
                        else:
                            st.error(
                                "Por favor, sube tu CV en la barra lateral antes de postularte."
                            )
else:
    st.info(
        "👈 Define tus requisitos en la barra lateral y haz clic en **'Buscar Ofertas Disponibles'** para comenzar."
    )
