import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import json

# Configuración de la página
st.set_page_config(
    page_title="1 Bitcoin = ¿Cuántos años de trabajo en Perú?",
    page_icon="₿",
    layout="wide"
)

# Función MEJORADA para obtener precio de Bitcoin (funciona en Render)
@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_bitcoin_price():
    """
    Obtiene precio de BTC en PEN usando APIs que funcionan desde Render.
    Prioriza APIs públicas sin rate limit estricto.
    """
    
    # API 1: Blockchain.info (sin rate limit, muy confiable)
    try:
        url = "https://blockchain.info/ticker"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        btc_usd = float(data['USD']['last'])
        
        # Tipo de cambio PEN (API pública sin límites)
        url_tc = "https://open.er-api.com/v6/latest/USD"
        response_tc = requests.get(url_tc, timeout=8)
        usd_to_pen = response_tc.json()['rates']['PEN']
        
        btc_pen = btc_usd * usd_to_pen
        
        if 200000 < btc_pen < 2000000:
            st.success("✅ Precio actualizado desde Blockchain.info")
            return round(btc_pen, 2)
    except Exception as e:
        st.warning(f"⚠️ Blockchain.info: {str(e)[:100]}")
    
    # API 2: CoinAPI (versión gratuita, sin rate limit agresivo)
    try:
        url = "https://rest.coinapi.io/v1/exchangerate/BTC/USD"
        headers = {'X-CoinAPI-Key': 'FREE-DEMO-KEY'}  # Demo key pública
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        btc_usd = float(response.json()['rate'])
        
        # Tipo de cambio
        url_tc = "https://open.er-api.com/v6/latest/USD"
        response_tc = requests.get(url_tc, timeout=8)
        usd_to_pen = response_tc.json()['rates']['PEN']
        
        btc_pen = btc_usd * usd_to_pen
        
        if 200000 < btc_pen < 2000000:
            st.info("ℹ️ Precio actualizado desde CoinAPI")
            return round(btc_pen, 2)
    except Exception as e:
        st.warning(f"⚠️ CoinAPI: {str(e)[:100]}")
    
    # API 3: CryptoCompare (API pública, generosa con rate limits)
    try:
        url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        btc_usd = float(response.json()['USD'])
        
        # Tipo de cambio
        url_tc = "https://open.er-api.com/v6/latest/USD"
        response_tc = requests.get(url_tc, timeout=8)
        usd_to_pen = response_tc.json()['rates']['PEN']
        
        btc_pen = btc_usd * usd_to_pen
        
        if 200000 < btc_pen < 2000000:
            st.info("ℹ️ Precio actualizado desde CryptoCompare")
            return round(btc_pen, 2)
    except Exception as e:
        st.warning(f"⚠️ CryptoCompare: {str(e)[:100]}")
    
    # API 4: Coinbase (API pública sin autenticación)
    try:
        url = "https://api.coinbase.com/v2/exchange-rates?currency=BTC"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        btc_usd = 1 / float(response.json()['data']['rates']['USD'])
        
        # Tipo de cambio
        url_tc = "https://open.er-api.com/v6/latest/USD"
        response_tc = requests.get(url_tc, timeout=8)
        usd_to_pen = response_tc.json()['rates']['PEN']
        
        btc_pen = btc_usd * usd_to_pen
        
        if 200000 < btc_pen < 2000000:
            st.info("ℹ️ Precio actualizado desde Coinbase")
            return round(btc_pen, 2)
    except Exception as e:
        st.warning(f"⚠️ Coinbase: {str(e)[:100]}")
    
    # Si todo falla
    st.error("❌ No se pudo conectar a ninguna API. Usando precio de referencia.")
    # Precio actualizado manualmente cada semana
    return 382500

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
    ["🗺️ Por Departamento (Todo Perú)", "🏙️ Por Distrito (Lima Metropolitana)", "🔍 Comparación Detallada"],
    horizontal=True
)

if vista == "🗺️ Por Departamento (Todo Perú)":
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
    st.markdown("## 🔍 Comparación Personalizada entre Distritos")
    st.markdown("**Compara el poder adquisitivo entre dos distritos de Lima**")
    
    # Filtros para seleccionar distritos
    col1, col2 = st.columns(2)
    
    # Lista de distritos ordenados alfabéticamente
    distritos_disponibles = sorted(df_lima['distrito'].tolist())
    
    with col1:
        distrito_1 = st.selectbox(
            "Selecciona el primer distrito:",
            distritos_disponibles,
            index=distritos_disponibles.index('San Isidro') if 'San Isidro' in distritos_disponibles else 0
        )
    
    with col2:
        # Asegurar que el segundo distrito sea diferente al primero
        distritos_disponibles_2 = [d for d in distritos_disponibles if d != distrito_1]
        distrito_2 = st.selectbox(
            "Selecciona el segundo distrito:",
            distritos_disponibles_2,
            index=distritos_disponibles_2.index('Villa El Salvador') if 'Villa El Salvador' in distritos_disponibles_2 else 0
        )
    
    # Obtener datos de los distritos seleccionados
    datos_distrito_1 = df_lima[df_lima['distrito'] == distrito_1].iloc[0]
    datos_distrito_2 = df_lima[df_lima['distrito'] == distrito_2].iloc[0]
    
    st.markdown("---")
    
    # Métricas lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 📍 {distrito_1}")
        st.metric("Ingreso Mensual", f"S/ {datos_distrito_1['ingreso_mensual_soles']:,.0f}")
        st.metric("Ingreso Anual", f"S/ {datos_distrito_1['ingreso_mensual_soles']*12:,.0f}")
        st.metric("Años para comprar 1 BTC", f"{datos_distrito_1['años_trabajo']:.1f} años")
        st.info(f"NSE: {datos_distrito_1['nse_predominante']}")
    
    with col2:
        st.markdown(f"### 📍 {distrito_2}")
        st.metric("Ingreso Mensual", f"S/ {datos_distrito_2['ingreso_mensual_soles']:,.0f}")
        st.metric("Ingreso Anual", f"S/ {datos_distrito_2['ingreso_mensual_soles']*12:,.0f}")
        st.metric("Años para comprar 1 BTC", f"{datos_distrito_2['años_trabajo']:.1f} años")
        st.info(f"NSE: {datos_distrito_2['nse_predominante']}")
    
    # Comparación visual
    st.markdown("### Comparación Visual")
    
    comparacion = pd.DataFrame({
        'Distrito': [distrito_1, distrito_2],
        'Años de Trabajo': [datos_distrito_1['años_trabajo'], datos_distrito_2['años_trabajo']],
        'Ingreso Mensual': [datos_distrito_1['ingreso_mensual_soles'], datos_distrito_2['ingreso_mensual_soles']]
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
    if datos_distrito_1['años_trabajo'] > datos_distrito_2['años_trabajo']:
        distrito_mayor = distrito_1
        distrito_menor = distrito_2
        años_mayor = datos_distrito_1['años_trabajo']
        años_menor = datos_distrito_2['años_trabajo']
    else:
        distrito_mayor = distrito_2
        distrito_menor = distrito_1
        años_mayor = datos_distrito_2['años_trabajo']
        años_menor = datos_distrito_1['años_trabajo']
    
    ratio = años_mayor / años_menor
    diferencia_años = años_mayor - años_menor
    
    st.warning(f"⚠️ **Una persona de {distrito_mayor} necesita trabajar {ratio:.1f}x más tiempo que una de {distrito_menor} para comprar 1 Bitcoin**")
    st.error(f"📊 **Diferencia: {diferencia_años:.1f} años más de trabajo**")

# Footer
st.markdown("---")
st.markdown("""
### 📊 Fuentes de Datos
- **Precio de Bitcoin**: APIs públicas (Blockchain.info, CryptoCompare, Coinbase) actualizadas cada 5 minutos
- **Ingresos por Departamento**: ⭐ INEI - EPEN Oct 2024-Sep 2025 (Datos oficiales)
- **Ingresos por Distrito**: Metodología híbrida basada en:
  - Conos de Lima (INEI 2024) - Dato oficial
  - Nivel Socioeconómico (CPI/APEIM 2024)

### 📖 Nota Metodológica
**Departamentos**: Datos 100% oficiales del INEI (Encuesta Permanente de Empleo Nacional).

**Distritos de Lima**: El INEI no publica datos desagregados por distrito individual. 
Utilizamos una metodología híbrida que combina:
- Datos oficiales por "conos" o zonas de Lima (INEI)
- Ajustes por Nivel Socioeconómico (NSE) según estudios de mercado

### ⚠️ Disclaimer
Este proyecto tiene fines educativos y de visualización de datos. 
Los ingresos reales pueden variar por factores individuales (educación, experiencia, sector).

### 👨‍💻 Desarrollado con
- Python + Streamlit
- Plotly para visualizaciones
- APIs: Blockchain.info, CryptoCompare, Coinbase, Open Exchange Rates
- Datos: INEI, CPI, APEIM

---
*Última actualización: {}*  
*Código abierto: [Ver en GitHub](https://github.com/JulioDC207/bitcoin-peru)*
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
