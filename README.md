# 1 Bitcoin = ¿Cuántos años de trabajo en Perú? ₿

Visualización interactiva del poder adquisitivo de Bitcoin en Perú, mostrando cuántos años de ingreso promedio se necesitan para comprar 1 BTC en cada departamento y distrito de Lima.

## 🎯 Características

- **Vista por Departamento**: Compara los 25 departamentos del Perú
- **Vista por Distrito**: Análisis detallado de 39 distritos de Lima Metropolitana
- **Comparación San Isidro vs Villa El Salvador**: Visualiza la desigualdad económica
- **Precio en Tiempo Real**: Se actualiza automáticamente desde CoinGecko API
- **Gráficos Interactivos**: Visualizaciones con Plotly

## 📊 Fuentes de Datos

- **Precio Bitcoin**: CoinGecko API
- **Ingresos Departamentos**: INEI - EPEN 2024
- **Ingresos Distritos**: Estimaciones basadas en NSE (CPI 2024)

## 🚀 Cómo deployar en Streamlit Cloud

### Paso 1: Crear repositorio en GitHub

1. Ve a [github.com](https://github.com) y crea un nuevo repositorio
2. Nómbralo: `bitcoin-peru` (o el nombre que prefieras)
3. Hazlo público
4. No inicialices con README (ya lo tienes aquí)

### Paso 2: Subir archivos

Necesitas subir estos 5 archivos a tu repositorio:

```
bitcoin-peru/
├── app.py
├── requirements.txt
├── ingresos_departamentos.csv
├── ingresos_lima_distritos.csv
└── README.md
```

**Opción A - Desde la web de GitHub:**
1. En tu repositorio, click en "Add file" → "Upload files"
2. Arrastra los 5 archivos
3. Click en "Commit changes"

**Opción B - Desde la terminal (si tienes Git instalado):**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/bitcoin-peru.git
git push -u origin main
```

### Paso 3: Deploy en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Click en "New app"
3. Conecta tu cuenta de GitHub
4. Selecciona:
   - **Repository**: `tu-usuario/bitcoin-peru`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click en "Deploy!"

⏳ **El deploy toma 2-3 minutos**

Tu app estará disponible en: `https://tu-usuario-bitcoin-peru.streamlit.app`

## 💡 Uso Local (Opcional)

Si quieres probar la app localmente antes de deployar:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Correr la app
streamlit run app.py
```

## 📱 Compartir en LinkedIn

Una vez deployed, comparte con un post tipo:

```
🚀 Proyecto nuevo: "1 Bitcoin = ¿Cuántos años de trabajo en Perú?"

Creé una herramienta interactiva que muestra el poder adquisitivo de Bitcoin 
en cada departamento y distrito de Lima.

📊 Datos clave:
• En Huancavelica: ~26 años de trabajo
• En Lima (San Isidro): ~5 años
• La brecha es abismal

✨ Features:
✅ Precio de BTC en tiempo real
✅ Vista por 25 departamentos
✅ Vista por 39 distritos de Lima
✅ Comparación interactiva

🔗 Pruébalo aquí: [TU LINK]

#Bitcoin #DataVisualization #Peru #Streamlit #Python
```

## 🛠️ Tech Stack

- **Python**: 3.9+
- **Streamlit**: Framework web
- **Plotly**: Gráficos interactivos
- **Pandas**: Manipulación de datos
- **CoinGecko API**: Precio BTC en tiempo real

## 📝 Notas

- Los datos de distritos son estimaciones basadas en NSE
- El precio de Bitcoin se actualiza cada 5 minutos
- Los datos del INEI son del 2024

## 🤝 Contribuciones

¿Tienes datos más precisos o sugerencias? ¡Pull requests bienvenidos!

## 📄 Licencia

MIT License - Libre para usar y modificar

---

**Desarrollado con ❤️ para visualizar la economía peruana**
