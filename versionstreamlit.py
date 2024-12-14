import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Simulador ACIDHYDROCHEM",
    page_icon="⚗️",
    layout="wide"
)

# Título principal
st.title("⚗️ Simulador de Procesos Químicos: ACIDHYDROCHEM")

# Sidebar para parámetros interactivos
st.sidebar.header("Parámetros de Entrada")
liquid_ratio = st.sidebar.slider("Fracción líquida (L)", min_value=0.0, max_value=20.0, value=10.0, step=1.0)
solid_ratio = st.sidebar.slider("Biomasa sólida (kg)", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
acid_concentration = st.sidebar.slider("Concentración de ácido (% v/v)", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
residence_time = st.sidebar.slider("Tiempo de residencia (min)", min_value=0.0, max_value=200.0, value=120.0, step=10.0)

# Simulación de los resultados
def simulate(liquid_ratio, solid_ratio, acid_concentration, residence_time):
    kH0, EH, βH, R, kX0, EX, βX, T, ρa = 7.709e8, 20301.9, 1, 1.98, 2.6e8, 20312, 0.15, 121.1 + 273.15, 1.84
    RL, Φ = liquid_ratio * ρa, liquid_ratio * ρa / solid_ratio
    t = np.linspace(0, residence_time, 100)
    hemicellulose = 70 * np.exp(-kH0 * acid_concentration**βH * np.exp(-EH / (R * T)) * Φ * t)
    xylose = kH0 * acid_concentration**βH * np.exp(-EH / (R * T)) * Φ * hemicellulose * t - kX0 * acid_concentration**βX * np.exp(-EX / (R * T)) * Φ * t
    furfural = xylose * 0.7
    return pd.DataFrame({"time": t, "Hemicellulose": hemicellulose, "Xylose": xylose, "Furfural": furfural})

# Botón para realizar la simulación
if st.sidebar.button("Simular"):
    simulation_data = simulate(liquid_ratio, solid_ratio, acid_concentration, residence_time)
    st.success("Simulación completada exitosamente.")

    # Mostrar resultados como tabla
    st.subheader("📋 Resultados de la Simulación")
    st.dataframe(simulation_data)

    # Gráficas Interactivas con Plotly
    st.subheader("📊 Gráfica Interactiva de Concentraciones")
    fig = px.line(
        simulation_data,
        x="time",
        y=["Hemicellulose", "Xylose", "Furfural"],
        labels={"time": "Tiempo (min)", "value": "Concentración (g/L)", "variable": "Componentes"},
        title="Concentraciones en función del tiempo"
    )
    st.plotly_chart(fig)

    # Descarga de datos
    csv = simulation_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="💾 Descargar Resultados como CSV",
        data=csv,
        file_name="simulacion_acidhydrochem.csv",
        mime="text/csv"
    )

    # Exploración de Datos
    st.subheader("🔍 Exploración de Datos")
    selected_variable = st.selectbox("Selecciona una variable para explorar:", ["Hemicellulose", "Xylose", "Furfural"])
    st.write(simulation_data[["time", selected_variable]])

    # Información adicional
    st.markdown("""
    ---
    **Autores**:
    - M.Sc. Luis Antonio Velázquez Herrera
    - Ph.D. Leticia López Zamora
    - Ph.D. Eusebio Bolaños Reynoso

    **Institución**:
    Tecnológico Nacional de México / Instituto Tecnológico de Orizaba, Veracruz  
    División de Estudios de Posgrado e Investigación
    """)