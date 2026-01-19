import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import json

# Configuración de la página
st.set_page_config(
    page_title="1 Bitcoin = ¿Cuántos años puedes vivir en Perú?",
    page_icon="₿",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .comparison-title {
        font-size: 28px;
        font-weight: 600;
        color: #1f1f1f;
        margin-bottom: 10px;
    }
    
    .comparison-subtitle {
        font-size: 18px;
        color: #555;
        margin-bottom: 25px;
    }
    
    .stSelectbox label {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #1f1f1f !important;
    }
    
    h3 {
        font-size: 26px !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Función para obtener precio de Bitcoin
@st.cache_data(ttl=300)
def get_bitcoin_price():
    """Obtiene precio de BTC en PEN"""
    
    # API 1: Blockchain.info
    try:
        url = "https://blockchain.info/ticker"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        btc_usd = float(data['USD']['last'])
        
        url_tc = "https://open.er-api.com/v6/latest/USD"
        response_tc = requests.get(url_tc, timeout=8)
        usd_to_pen = response_tc.json()['rates']['PEN']
        
        btc_pen = btc_usd * usd_to_pen
        
        if 200000 < btc_pen < 2000000:
            st.success("✅ Precio actualizado desde Blockchain.info")
            return round(btc_pen, 2)
    except Exception as e:
        st.warning(f"⚠️ Blockchain.info: {str(e)[:100]}")
    
    # API 2: CryptoCompare
    try:
        url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        btc_usd = float(response.json()['USD'])
        
        url_tc = "https://open.er-api.com/v6/latest/USD"
        response_tc = requests.get(url_tc, timeout=8)
        usd_to_pen = response_tc.json()['rates']['PEN']
        
        btc_pen = btc_usd * usd_to_pen
        
        if 200000 < btc_pen < 2000000:
            st.info("ℹ️ Precio actualizado desde CryptoCompare")
            return round(btc_pen, 2)
    except Exception as e:
        st.warning(f"⚠️ CryptoCompare: {str(e)[:100]}")
    
    # API 3: Coinbase
    try:
        url = "https://api.coinbase.com/v2/exchange-rates?currency=BTC"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        btc_usd = 1 / float(response.json()['data']['rates']['USD'])
        
        url_tc = "https://open.er-api.com/v6/latest/USD"
        response_tc = requests.get(url_tc, timeout=8)
        usd_to_pen = response_tc.json()['rates']['PEN']
        
        btc_pen = btc_usd * usd_to_pen
        
        if 200000 < btc_pen < 2000000:
            st.info("ℹ️ Precio actualizado desde Coinbase")
            return round(btc_pen, 2)
    except Exception as e:
        st.warning(f"⚠️ Coinbase: {str(e)[:100]}")
    
    st.error("❌ No se pudo conectar a ninguna API. Usando precio de referencia.")
    return 382500

# Función para cargar datos
@st.cache_data
def load_data():
    df_dept = pd.read_csv('ingresos_departamentos.csv')
    df_lima = pd.read_csv('ingresos_lima_distritos.csv')
    return df_dept, df_lima

# ============================================
# TÍTULO PRINCIPAL - ENFOQUE HOLDER
# ============================================
st.title("₿ 1 Bitcoin = ¿Cuántos años puedes vivir en Perú?")
st.markdown("### Poder adquisitivo de Bitcoin en cada departamento y distrito")

# Obtener precio y datos
btc_price = get_bitcoin_price()
df_departamentos, df_lima = load_data()

# Calcular años que puedes vivir
df_departamentos['años_vivir'] = btc_price / (df_departamentos['ingreso_mensual_soles'] * 12)
df_lima['años_vivir'] = btc_price / (df_lima['ingreso_mensual_soles'] * 12)

# Métricas destacadas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Valor de 1 Bitcoin", f"S/ {btc_price:,.2f} PEN")

with col2:
    promedio_nacional = df_departamentos['años_vivir'].mean()
    st.metric(
        "🇵🇪 Promedio Nacional", 
        f"{promedio_nacional:.1f} años",
        help="Años que puedes vivir con 1 BTC según ingreso promedio de Perú"
    )

with col3:
    ingreso_promedio_nacional = df_departamentos['ingreso_mensual_soles'].mean()
    st.metric(
        "📊 Ingreso Promedio Perú",
        f"S/ {ingreso_promedio_nacional:,.0f}/mes"
    )

st.caption("💡 Con **1 Bitcoin** puedes vivir **{:.1f} años** en Perú según el ingreso promedio nacional (basado en datos de todos los departamentos)".format(promedio_nacional))

# Selector de vista
st.markdown("---")
vista = st.radio(
    "Selecciona la vista:",
    ["🗺️ Por Departamento (Todo Perú)", "🏙️ Por Distrito (Lima Metropolitana)", "🔍 Comparación Detallada"],
    horizontal=True
)

# ============================================
# VISTA 1: POR DEPARTAMENTO
# ============================================
if vista == "🗺️ Por Departamento (Todo Perú)":
    st.markdown("## Vista por Departamento")
    
    # Ordenar por años que puedes vivir (de menor a mayor = de más pobre a más rico)
    df_dept_sorted = df_departamentos.sort_values('años_vivir', ascending=False)
    
    # Gráfico de barras
    fig = px.bar(
        df_dept_sorted,
        x='departamento',
        y='años_vivir',
        title='¿Cuántos años puedes vivir con 1 Bitcoin en cada departamento?',
        labels={'años_vivir': 'Años de vida', 'departamento': 'Departamento'},
        color='años_vivir',
        color_continuous_scale='RdYlGn',
        text='años_vivir'
    )
    
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig.update_layout(height=600, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla detallada
    st.markdown("### Tabla Detallada")
    
    df_display = df_dept_sorted[['departamento', 'ingreso_mensual_soles', 'años_vivir']].copy()
    df_display['ingreso_mensual_soles'] = df_display['ingreso_mensual_soles'].apply(lambda x: f"S/ {x:,.0f}")
    df_display['años_vivir'] = df_display['años_vivir'].apply(lambda x: f"{x:.1f} años")
    df_display.columns = ['Departamento', 'Ingreso Mensual Promedio', 'Años de Vida con 1 BTC']
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Stats destacadas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dept_max = df_departamentos.loc[df_departamentos['años_vivir'].idxmax()]
        st.metric(
            "Puedes vivir MÁS años en",
            dept_max['departamento'],
            f"{dept_max['años_vivir']:.1f} años"
        )
    
    with col2:
        dept_min = df_departamentos.loc[df_departamentos['años_vivir'].idxmin()]
        st.metric(
            "Puedes vivir MENOS años en",
            dept_min['departamento'],
            f"{dept_min['años_vivir']:.1f} años"
        )
    
    with col3:
        promedio = df_departamentos['años_vivir'].mean()
        st.metric(
            "Promedio Nacional",
            f"{promedio:.1f} años",
            delta=None
        )

# ============================================
# VISTA 2: POR DISTRITO DE LIMA
# ============================================
elif vista == "🏙️ Por Distrito (Lima Metropolitana)":
    st.markdown("## Vista por Distrito de Lima")
    
    # Ordenar por años que puedes vivir
    df_lima_sorted = df_lima.sort_values('años_vivir', ascending=False)
    
    # Gráfico de barras
    fig = px.bar(
        df_lima_sorted,
        x='distrito',
        y='años_vivir',
        title='¿Cuántos años puedes vivir con 1 Bitcoin en cada distrito de Lima?',
        labels={'años_vivir': 'Años de vida', 'distrito': 'Distrito'},
        color='años_vivir',
        color_continuous_scale='RdYlGn',
        text='años_vivir',
        hover_data=['nse_predominante']
    )
    
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig.update_layout(height=700, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla detallada
    st.markdown("### Tabla Detallada")
    
    df_display = df_lima_sorted[['distrito', 'ingreso_mensual_soles', 'nse_predominante', 'años_vivir']].copy()
    df_display['ingreso_mensual_soles'] = df_display['ingreso_mensual_soles'].apply(lambda x: f"S/ {x:,.0f}")
    df_display['años_vivir'] = df_display['años_vivir'].apply(lambda x: f"{x:.1f} años")
    df_display.columns = ['Distrito', 'Ingreso Mensual Promedio', 'NSE', 'Años de Vida con 1 BTC']
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Stats destacadas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dist_max = df_lima.loc[df_lima['años_vivir'].idxmax()]
        st.metric(
            "Puedes vivir MÁS años en",
            dist_max['distrito'],
            f"{dist_max['años_vivir']:.1f} años"
        )
    
    with col2:
        dist_min = df_lima.loc[df_lima['años_vivir'].idxmin()]
        st.metric(
            "Puedes vivir MENOS años en",
            dist_min['distrito'],
            f"{dist_min['años_vivir']:.1f} años"
        )
    
    with col3:
        promedio_lima = df_lima['años_vivir'].mean()
        st.metric(
            "Promedio Lima",
            f"{promedio_lima:.1f} años",
            delta=None
        )

# ============================================
# VISTA 3: COMPARACIÓN DETALLADA
# ============================================
else:
    st.markdown('<p class="comparison-title">🔍 Comparación Personalizada entre Distritos</p>', unsafe_allow_html=True)
    st.markdown('<p class="comparison-subtitle">Compara cuántos años puedes vivir con 1 Bitcoin en diferentes distritos de Lima</p>', unsafe_allow_html=True)
    
    st.markdown("")
    
    # Filtros para seleccionar distritos
    col1, col2 = st.columns(2)
    
    distritos_disponibles = sorted(df_lima['distrito'].tolist())
    
    with col1:
        st.markdown("#### 📍 Primer Distrito")
        distrito_1 = st.selectbox(
            "Selecciona el primer distrito:",
            distritos_disponibles,
            index=distritos_disponibles.index('San Isidro') if 'San Isidro' in distritos_disponibles else 0,
            key="distrito_1"
        )
    
    with col2:
        st.markdown("#### 📍 Segundo Distrito")
        distritos_disponibles_2 = [d for d in distritos_disponibles if d != distrito_1]
        distrito_2 = st.selectbox(
            "Selecciona el segundo distrito:",
            distritos_disponibles_2,
            index=distritos_disponibles_2.index('Villa El Salvador') if 'Villa El Salvador' in distritos_disponibles_2 else 0,
            key="distrito_2"
        )
    
    # Obtener datos
    datos_distrito_1 = df_lima[df_lima['distrito'] == distrito_1].iloc[0]
    datos_distrito_2 = df_lima[df_lima['distrito'] == distrito_2].iloc[0]
    
    st.markdown("---")
    
    # Métricas lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 📍 {distrito_1}")
        st.metric("💰 Ingreso Mensual Promedio", f"S/ {datos_distrito_1['ingreso_mensual_soles']:,.0f}")
        st.metric("📅 Ingreso Anual Promedio", f"S/ {datos_distrito_1['ingreso_mensual_soles']*12:,.0f}")
        st.metric("⏱️ Años que puedes vivir con 1 BTC", f"{datos_distrito_1['años_vivir']:.1f} años")
        st.info(f"🏘️ NSE: {datos_distrito_1['nse_predominante']}")
    
    with col2:
        st.markdown(f"### 📍 {distrito_2}")
        st.metric("💰 Ingreso Mensual Promedio", f"S/ {datos_distrito_2['ingreso_mensual_soles']:,.0f}")
        st.metric("📅 Ingreso Anual Promedio", f"S/ {datos_distrito_2['ingreso_mensual_soles']*12:,.0f}")
        st.metric("⏱️ Años que puedes vivir con 1 BTC", f"{datos_distrito_2['años_vivir']:.1f} años")
        st.info(f"🏘️ NSE: {datos_distrito_2['nse_predominante']}")
    
    # Comparación visual
    st.markdown("### 📊 Comparación Visual")
    
    comparacion = pd.DataFrame({
        'Distrito': [distrito_1, distrito_2],
        'Años de Vida con 1 BTC': [datos_distrito_1['años_vivir'], datos_distrito_2['años_vivir']],
        'Ingreso Mensual': [datos_distrito_1['ingreso_mensual_soles'], datos_distrito_2['ingreso_mensual_soles']]
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Años que puedes vivir con 1 BTC',
        x=comparacion['Distrito'],
        y=comparacion['Años de Vida con 1 BTC'],
        text=comparacion['Años de Vida con 1 BTC'].apply(lambda x: f'{x:.1f}'),
        textposition='auto',
        marker_color=['#2E86AB', '#A23B72']
    ))
    
    fig.update_layout(
        title='¿Cuántos años puedes vivir con 1 Bitcoin en cada distrito?',
        yaxis_title='Años',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Cálculo de diferencia
    if datos_distrito_1['años_vivir'] > datos_distrito_2['años_vivir']:
        distrito_mayor = distrito_1
        distrito_menor = distrito_2
        años_mayor = datos_distrito_1['años_vivir']
        años_menor = datos_distrito_2['años_vivir']
    else:
        distrito_mayor = distrito_2
        distrito_menor = distrito_1
        años_mayor = datos_distrito_2['años_vivir']
        años_menor = datos_distrito_1['años_vivir']
    
    ratio = años_mayor / años_menor
    diferencia_años = años_mayor - años_menor
    
    st.success(f"✅ **Con 1 Bitcoin puedes vivir {ratio:.1f}x más tiempo en {distrito_mayor} que en {distrito_menor}**")
    st.info(f"📊 **Diferencia: {diferencia_años:.1f} años más de vida**")

# Footer
st.markdown("---")
st.markdown("""
### 📊 Fuentes de Datos
- **Precio de Bitcoin**: APIs públicas (Blockchain.info, CryptoCompare, Coinbase) actualizadas cada 5 minutos
- **Ingresos por Departamento**: ⭐ INEI - EPEN Oct 2024-Sep 2025 (Datos oficiales)
- **Ingresos por Distrito**: Metodología híbrida basada en:
  - Conos de Lima (INEI 2024) - Dato oficial
  - Nivel Socioeconómico (CPI/APEIM 2024)

### 📖 Metodología
**Cálculo**: Años de vida = Valor de 1 BTC / (Ingreso mensual promedio × 12)

Este cálculo muestra cuántos años podrías vivir en cada ubicación con 1 Bitcoin, 
asumiendo que mantienes el nivel de vida promedio del lugar (usando el ingreso mensual promedio como referencia de gasto).

**Interpretación**: Si en San Isidro sale 5.1 años, significa que con 1 BTC podrías vivir 5.1 años 
manteniendo el nivel de vida promedio de ese distrito. En Villa El Salvador (17.7 años), 
el mismo Bitcoin te alcanzaría para más tiempo debido al menor costo de vida.

**Promedio Nacional**: Calculado como el promedio simple de todos los departamentos del Perú.

### 💡 Ejemplo Práctico
Si tienes 1 BTC (≈ S/ 319,600):
- En **San Isidro**: Podrías vivir ~5 años con nivel de vida promedio (NSE A)
- En **Villa El Salvador**: Podrías vivir ~18 años con nivel de vida promedio (NSE D)
- **Promedio Perú**: Podrías vivir ~10.5 años con nivel de vida promedio nacional

### ⚠️ Disclaimer
Este proyecto tiene fines educativos y de visualización de datos. 
Los cálculos son aproximaciones basadas en ingresos promedio oficiales del INEI.
Los gastos reales pueden variar significativamente según estilo de vida, familia, salud, etc.

### 👨‍💻 Desarrollado por Julio Conza con
- Claude
- Python + Streamlit/Render
- Plotly para visualizaciones
- APIs: Blockchain.info, CryptoCompare, Coinbase, Open Exchange Rates
- Datos: INEI, CPI, APEIM

---
*Última actualización: {}*  
*Inspirado en: [pricedinbitcoin21.com](https://pricedinbitcoin21.com/bitcoin-income)*  
*Código abierto: [Ver en GitHub](https://github.com/JulioDC207/bitcoin-peru)*
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
