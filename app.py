import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="1 Bitcoin = ¿Cuántos años de trabajo en Perú?",
    page_icon="₿",
    layout="wide"
)

# Función para obtener precio de Bitcoin
@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_bitcoin_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=pen"
        response = requests.get(url)
        data = response.json()
        return data['bitcoin']['pen']
    except:
        # Precio de respaldo en caso de error
        return 350000  # Aproximado

# Función para cargar datos
@st.cache_data
def load_data():
    df_dept = pd.read_csv('ingresos_departamentos.csv')
    df_lima = pd.read_csv('ingresos_lima_distritos.csv')
    return df_dept, df_lima

# Título principal
st.title("₿ 1 Bitcoin = ¿Cuántos años de trabajo en Perú?")
st.markdown("### Poder adquisitivo de Bitcoin por departamento y distrito")

# Obtener precio de Bitcoin
btc_price = get_bitcoin_price()
st.metric("Precio actual de Bitcoin", f"S/ {btc_price:,.2f} PEN", delta=None)

# Cargar datos
df_departamentos, df_lima = load_data()

# Calcular años de ingreso
df_departamentos['años_trabajo'] = btc_price / (df_departamentos['ingreso_mensual_soles'] * 12)
df_lima['años_trabajo'] = btc_price / (df_lima['ingreso_mensual_soles'] * 12)

# Selector de vista
st.markdown("---")
vista = st.radio(
    "Selecciona la vista:",
    ["📍 Por Departamento (Todo Perú)", "🏙️ Por Distrito (Lima Metropolitana)", "🔍 Comparación Detallada"],
    horizontal=True
)

if vista == "📍 Por Departamento (Todo Perú)":
    st.markdown("## Vista por Departamento")
    
    # Ordenar por años de trabajo
    df_dept_sorted = df_departamentos.sort_values('años_trabajo', ascending=False)
    
    # Gráfico de barras
    fig = px.bar(
        df_dept_sorted,
        x='departamento',
        y='años_trabajo',
        title='Años de ingreso equivalentes a 1 Bitcoin por Departamento',
        labels={'años_trabajo': 'Años de trabajo', 'departamento': 'Departamento'},
        color='años_trabajo',
        color_continuous_scale='RdYlGn_r',
        text='años_trabajo'
    )
    
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig.update_layout(height=600, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla detallada
    st.markdown("### Tabla Detallada")
    
    df_display = df_dept_sorted[['departamento', 'ingreso_mensual_soles', 'años_trabajo']].copy()
    df_display['ingreso_mensual_soles'] = df_display['ingreso_mensual_soles'].apply(lambda x: f"S/ {x:,.0f}")
    df_display['años_trabajo'] = df_display['años_trabajo'].apply(lambda x: f"{x:.1f} años")
    df_display.columns = ['Departamento', 'Ingreso Mensual', 'Años de Trabajo = 1 BTC']
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Stats destacadas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dept_max = df_departamentos.loc[df_departamentos['años_trabajo'].idxmax()]
        st.metric(
            "Departamento con MÁS años",
            dept_max['departamento'],
            f"{dept_max['años_trabajo']:.1f} años"
        )
    
    with col2:
        dept_min = df_departamentos.loc[df_departamentos['años_trabajo'].idxmin()]
        st.metric(
            "Departamento con MENOS años",
            dept_min['departamento'],
            f"{dept_min['años_trabajo']:.1f} años"
        )
    
    with col3:
        promedio = df_departamentos['años_trabajo'].mean()
        st.metric(
            "Promedio Nacional",
            f"{promedio:.1f} años",
            delta=None
        )

elif vista == "🏙️ Por Distrito (Lima Metropolitana)":
    st.markdown("## Vista por Distrito de Lima")
    
    # Ordenar por años de trabajo
    df_lima_sorted = df_lima.sort_values('años_trabajo', ascending=False)
    
    # Gráfico de barras
    fig = px.bar(
        df_lima_sorted,
        x='distrito',
        y='años_trabajo',
        title='Años de ingreso equivalentes a 1 Bitcoin por Distrito de Lima',
        labels={'años_trabajo': 'Años de trabajo', 'distrito': 'Distrito'},
        color='años_trabajo',
        color_continuous_scale='RdYlGn_r',
        text='años_trabajo',
        hover_data=['nse_predominante']
    )
    
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig.update_layout(height=700, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla detallada
    st.markdown("### Tabla Detallada")
    
    df_display = df_lima_sorted[['distrito', 'ingreso_mensual_soles', 'nse_predominante', 'años_trabajo']].copy()
    df_display['ingreso_mensual_soles'] = df_display['ingreso_mensual_soles'].apply(lambda x: f"S/ {x:,.0f}")
    df_display['años_trabajo'] = df_display['años_trabajo'].apply(lambda x: f"{x:.1f} años")
    df_display.columns = ['Distrito', 'Ingreso Mensual', 'NSE', 'Años de Trabajo = 1 BTC']
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Stats destacadas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dist_max = df_lima.loc[df_lima['años_trabajo'].idxmax()]
        st.metric(
            "Distrito con MÁS años",
            dist_max['distrito'],
            f"{dist_max['años_trabajo']:.1f} años"
        )
    
    with col2:
        dist_min = df_lima.loc[df_lima['años_trabajo'].idxmin()]
        st.metric(
            "Distrito con MENOS años",
            dist_min['distrito'],
            f"{dist_min['años_trabajo']:.1f} años"
        )
    
    with col3:
        promedio_lima = df_lima['años_trabajo'].mean()
        st.metric(
            "Promedio Lima",
            f"{promedio_lima:.1f} años",
            delta=None
        )

else:  # Comparación Detallada
    st.markdown("## Comparación: San Isidro vs Villa El Salvador")
    st.markdown("**La desigualdad del poder adquisitivo en Lima**")
    
    # Obtener datos
    san_isidro = df_lima[df_lima['distrito'] == 'San Isidro'].iloc[0]
    villa_salvador = df_lima[df_lima['distrito'] == 'Villa El Salvador'].iloc[0]
    
    # Métricas lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💎 San Isidro")
        st.metric("Ingreso Mensual", f"S/ {san_isidro['ingreso_mensual_soles']:,.0f}")
        st.metric("Ingreso Anual", f"S/ {san_isidro['ingreso_mensual_soles']*12:,.0f}")
        st.metric("Años para comprar 1 BTC", f"{san_isidro['años_trabajo']:.1f} años")
        st.info(f"NSE: {san_isidro['nse_predominante']}")
    
    with col2:
        st.markdown("### 🏘️ Villa El Salvador")
        st.metric("Ingreso Mensual", f"S/ {villa_salvador['ingreso_mensual_soles']:,.0f}")
        st.metric("Ingreso Anual", f"S/ {villa_salvador['ingreso_mensual_soles']*12:,.0f}")
        st.metric("Años para comprar 1 BTC", f"{villa_salvador['años_trabajo']:.1f} años")
        st.info(f"NSE: {villa_salvador['nse_predominante']}")
    
    # Comparación visual
    st.markdown("### Comparación Visual")
    
    comparacion = pd.DataFrame({
        'Distrito': ['San Isidro', 'Villa El Salvador'],
        'Años de Trabajo': [san_isidro['años_trabajo'], villa_salvador['años_trabajo']],
        'Ingreso Mensual': [san_isidro['ingreso_mensual_soles'], villa_salvador['ingreso_mensual_soles']]
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Años de Trabajo para 1 BTC',
        x=comparacion['Distrito'],
        y=comparacion['Años de Trabajo'],
        text=comparacion['Años de Trabajo'].apply(lambda x: f'{x:.1f}'),
        textposition='auto',
        marker_color=['#2E86AB', '#A23B72']
    ))
    
    fig.update_layout(
        title='¿Cuántos años de trabajo se necesitan para comprar 1 Bitcoin?',
        yaxis_title='Años',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Cálculo de brecha
    ratio = villa_salvador['años_trabajo'] / san_isidro['años_trabajo']
    st.warning(f"⚠️ **Una persona de Villa El Salvador necesita trabajar {ratio:.1f}x más tiempo que una de San Isidro para comprar 1 Bitcoin**")
    
    diferencia_años = villa_salvador['años_trabajo'] - san_isidro['años_trabajo']
    st.error(f"📊 **Diferencia: {diferencia_años:.1f} años más de trabajo**")

# Footer con información y disclaimer
st.markdown("---")
st.markdown("""
### 📊 Fuentes de Datos
- **Precio de Bitcoin**: API de CoinGecko (actualizado cada 5 minutos)
- **Ingresos por Departamento**: INEI - Encuesta Permanente de Empleo Nacional (EPEN) 2024
- **Ingresos por Distrito**: Estimaciones basadas en NSE según CPI 2024 y INEI

### ⚠️ Disclaimer
Los datos de ingresos por distrito son **estimaciones** basadas en Niveles Socioeconómicos (NSE) y estudios de mercado.
Los ingresos reales pueden variar. Este proyecto tiene fines educativos y de visualización.

### 👨‍💻 Desarrollado con
- Python + Streamlit
- Plotly para visualizaciones
- CoinGecko API

---
*Última actualización: {}*
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
