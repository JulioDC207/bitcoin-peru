# ₿ 1 Bitcoin = ¿Cuántos años puedes vivir en Perú?

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bitcoin-peru.onrender.com/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> Visualización interactiva que muestra cuántos años podrías vivir en cada departamento y distrito de Lima con 1 Bitcoin, basándose en datos oficiales de ingresos del INEI.

**🌐 App en vivo:** [bitcoin-peru.onrender.com](https://bitcoin-peru.onrender.com/)

---

## 📊 ¿Qué hace esta app?

Esta aplicación responde a la pregunta: **"Si tengo 1 Bitcoin, ¿cuántos años puedo vivir en Perú?"**

Compara el poder adquisitivo de Bitcoin en diferentes ubicaciones del Perú usando datos oficiales de ingresos. Por ejemplo:
- Con 1 BTC puedes vivir **~5 años** en San Isidro (Lima)
- Con 1 BTC puedes vivir **~18 años** en Villa El Salvador (Lima)
- Con 1 BTC puedes vivir **~10.5 años** según el promedio nacional

**Inspirado en:** [pricedinbitcoin21.com](https://pricedinbitcoin21.com/bitcoin-income)

---

## ✨ Características

- 🗺️ **Vista por Departamento**: Compara todos los departamentos del Perú
- 🏙️ **Vista por Distrito**: Explora distritos de Lima Metropolitana
- 🔍 **Comparador Interactivo**: Compara cualquier par de distritos
- 💰 **Precio actualizado**: Bitcoin en tiempo real desde múltiples APIs
- 📊 **Visualizaciones interactivas**: Gráficos con Plotly
- 🇵🇪 **Datos oficiales**: INEI (Instituto Nacional de Estadística e Informática)

---

## 🚀 Demo

**Pruébalo aquí:** [bitcoin-peru.onrender.com](https://bitcoin-peru.onrender.com/)

---

## 📖 Metodología

### Cálculo
```
Años de vida = Valor de 1 BTC / (Ingreso mensual promedio × 12)
```

### Interpretación
Si en un distrito sale **5.1 años**, significa que con 1 Bitcoin podrías vivir **5.1 años** manteniendo el nivel de vida promedio de ese distrito (usando el ingreso mensual promedio como referencia de gasto).

### Fuentes de Datos

**Ingresos por Departamento:**
- ⭐ **INEI - EPEN** (Encuesta Permanente de Empleo Nacional)
- Período: Octubre 2024 - Septiembre 2025
- Datos oficiales 100%

**Ingresos por Distrito (Lima):**
- Metodología híbrida basada en:
  - Conos de Lima (INEI 2024) - Dato oficial
  - Nivel Socioeconómico NSE (CPI/APEIM 2024)
- Los valores son aproximaciones razonables basadas en fuentes oficiales

**Precio de Bitcoin:**
- APIs: Blockchain.info, CryptoCompare, Coinbase
- Actualización: Cada 5 minutos
- Tipo de cambio: Open Exchange Rates

---

## 💡 Ejemplo Práctico

Si tienes **1 BTC** (≈ S/ 320,000):

| Ubicación | Ingreso Promedio | Años de Vida | NSE |
|-----------|------------------|--------------|-----|
| **San Isidro** | S/ 5,200/mes | ~5 años | A |
| **Miraflores** | S/ 4,800/mes | ~5.5 años | A/B |
| **San Juan de Lurigancho** | S/ 1,800/mes | ~15 años | C/D |
| **Villa El Salvador** | S/ 1,500/mes | ~18 años | D |
| **Promedio Nacional** | S/ 2,538/mes | ~10.5 años | - |

---

## 🛠️ Tecnologías

- **Frontend**: [Render](https://render.com/)
- **Visualizaciones**: [Plotly](https://plotly.com/)
- **Datos**: Pandas, NumPy
- **APIs**: Blochain.info


---

## 📂 Estructura del Proyecto

```
bitcoin-peru/
├── app.py                              # Aplicación principal
├── requirements.txt                    # Dependencias de Python
├── ingresos_departamentos.csv          # Datos de departamentos (INEI)
├── ingresos_lima_distritos.csv         # Datos de distritos de Lima
└── README.md                           # Este archivo
```

---

## 📊 Archivos de Datos

### `ingresos_departamentos.csv`
Contiene ingresos mensuales promedio por departamento del Perú (INEI).

### `ingresos_lima_distritos.csv`
Contiene ingresos mensuales estimados por distrito de Lima con NSE predominante.

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la app:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Agregar mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

---

## ⚠️ Disclaimer

Este proyecto tiene **fines educativos y de visualización de datos**. 

Los cálculos son aproximaciones basadas en:
- Ingresos promedio oficiales del INEI
- Tipo de cambio actual
- Precio de Bitcoin en tiempo real

Los gastos reales pueden variar significativamente según:
- Estilo de vida personal
- Composición familiar
- Gastos de salud
- Gastos de vivienda
- Y otros factores individuales

**No es asesoría financiera.** Los datos históricos no garantizan resultados futuros.

---

## 📜 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**Julio D. Conza**
- GitHub: [@JulioDC207](https://github.com/JulioDC207)
- LinkedIn: [https://www.linkedin.com/in/julio-david-conza-zelada-129890151/]

---

## 🙏 Agradecimientos

- **CLAUDE**
- **INEI** - Por los datos oficiales de ingresos
- **pricedinbitcoin21.com** - Inspiración para el enfoque
- **CPI/APEIM** - Datos de NSE
- **Anthropic Claude** - Asistencia en desarrollo

---

## 📈 Estadísticas

![GitHub stars](https://img.shields.io/github/stars/JulioDC207/bitcoin-peru?style=social)
![GitHub forks](https://img.shields.io/github/forks/JulioDC207/bitcoin-peru?style=social)

---

**¿Te gustó el proyecto? ¡Dale una ⭐ en GitHub!**

**¿Tienes sugerencias?** Abre un [issue](https://github.com/JulioDC207/bitcoin-peru/issues)

---

*Última actualización: Enero 2025*
