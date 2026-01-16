# 1 Bitcoin = ¿Cuántos años de trabajo en Perú? ₿

> **[🚀 Ver App en Vivo](https://bitcoin-peru-dvb4s3vkwbsfkzjdwbtac4.streamlit.app)**

Visualización interactiva del poder adquisitivo de Bitcoin en Perú, mostrando cuántos años de ingreso promedio se necesitan para comprar 1 BTC en cada departamento y distrito de Lima.

---

## 🤔 ¿Por qué este proyecto?

Bitcoin se cotiza globalmente al mismo precio, pero el **poder adquisitivo** varía enormemente entre regiones. 

En Perú:
- Una persona de **Huancavelica** necesitaría trabajar **~26 años** para comprar 1 BTC
- Una persona de **San Isidro (Lima)** solo necesitaría **~5 años**

Este proyecto visualiza esa desigualdad económica de forma clara, interactiva e impactante usando datos oficiales del INEI.

---

## ✨ Características

- 📍 **Vista por Departamento**: Compara los 25 departamentos del Perú con datos oficiales INEI
- 🏙️ **Vista por Distrito**: Análisis detallado de 38 distritos de Lima Metropolitana
- 🔍 **Comparación Directa**: San Isidro vs Villa El Salvador - visualiza la brecha económica
- ₿ **Precio en Tiempo Real**: Se actualiza automáticamente cada 5 minutos desde CoinGecko API
- 📊 **Gráficos Interactivos**: Visualizaciones profesionales con Plotly
- 📱 **Responsive**: Funciona en desktop y móvil

---

## 📊 Fuentes de Datos

- **Precio Bitcoin**: [CoinGecko API](https://www.coingecko.com/es/api) - Actualización cada 5 minutos
- **Ingresos por Departamento**: INEI - EPEN (Encuesta Permanente de Empleo Nacional) Oct 2024-Sep 2025 ⭐ Datos oficiales
- **Ingresos por Distrito Lima**: Metodología híbrida basada en:
  - Datos oficiales por conos/zonas (INEI 2024)
  - Nivel Socioeconómico (CPI/APEIM 2024)

**📖 Ver metodología completa y referencias:** [METODOLOGIA_DATOS.md](METODOLOGIA_DATOS.md)

---

## 🚀 Deploy en Streamlit Cloud

### Archivos del Proyecto
```
bitcoin-peru/
├── app.py                           # Aplicación principal
├── requirements.txt                 # Dependencias Python
├── ingresos_departamentos.csv       # Datos por departamento (INEI)
├── ingresos_lima_distritos.csv      # Datos por distrito Lima
├── README.md                        # Este archivo
└── METODOLOGIA_DATOS.md            # Documentación de fuentes
```

---
## 🛠️ Tech Stack

- **Python 3.9+**: Lenguaje principal
- **Streamlit**: Framework para aplicaciones web de datos
- **Plotly**: Biblioteca de visualización interactiva
- **Pandas**: Manipulación y análisis de datos
- **Requests**: Consumo de APIs (CoinGecko)

### Dependencias (requirements.txt)
```
streamlit
pandas
plotly
requests
```

---
## 📝 Notas Metodológicas

### Departamentos
✅ Datos **100% oficiales** del INEI (Encuesta Permanente de Empleo Nacional, período Oct 2024 - Sep 2025)

### Distritos de Lima
⚠️ El INEI no publica datos desagregados por distrito individual. 

Solución implementada:
1. Base oficial: Datos por "conos" o zonas de Lima (INEI 2024)
2. Ajuste: Nivel Socioeconómico por distrito (CPI/APEIM 2024)

Los valores son **aproximaciones razonables** basadas en fuentes oficiales. La diferencia relativa entre distritos (ej: San Isidro vs Villa El Salvador) es estadísticamente significativa y representativa de la realidad económica peruana.

**Documentación completa:** [METODOLOGIA_DATOS.md](METODOLOGIA_DATOS.md)

---

## 🤝 Contribuciones

¿Tienes datos más precisos, sugerencias o encontraste un bug?

- 🐛 **Issues**: [Reportar un problema](https://github.com/JulioDC207/bitcoin-peru/issues)
- 🔧 **Pull Requests**: ¡Bienvenidos!
- 💡 **Ideas**: Abre una discusión en Issues

---

## 📄 Licencia

MIT License - Libre para usar, modificar y distribuir.

---

## 👨‍💻 Autor Julio Conza

Desarrollado con ❤️ para visualizar la economía peruana y el poder adquisitivo de Bitcoin.
