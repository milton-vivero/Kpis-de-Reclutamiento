# 📊 People Analytics: Optimización del Proceso de Reclutamiento

Este proyecto implementa un ecosistema automatizado de análisis de datos enfocado en la adquisición de talento técnico y la optimización de presupuestos de Recursos Humanos.

---

## 🔎 1. Problema que busca solucionar

El proyecto resuelve la **falta de visibilidad y optimización** en el proceso de atracción de talento. Responde directamente a tres problemáticas críticas:
* **Efectividad de canales:** Identificar qué fuentes tienen mayor conversión real de contratación.
* **Cuellos de botella:** Monitorear los días requeridos para cubrir cada vacante (*Time to Fill*).
* **Fricción en el embudo:** Controlar y reducir la tasa de deserción voluntaria de candidatos.

---

## 🛠️ 2. Arquitectura del Proyecto (Scripts)

El ecosistema está dividido en 3 scripts con responsabilidades únicas:

*   **`1_reclutamiento.py`**: Consume el Excel procesado, calcula métricas agregadas por puesto/canal y compila el informe web interactivo en **`Informe/informe_final_reclutamiento.html`**.
*   **`3_powerbi_prep.py`**: Enriquece el dataset con inteligencia de tiempo (Mes, Año, Trimestre) y banderas binarias de conteo para su consumo directo en Power BI.(pendiente)

---

## 📊 4. Conclusiones e Insights de Negocio

Tras procesar el set de datos históricos, se identificaron los siguientes hallazgos estratégicos:

*   🥇 **La mina de oro son los Referidos:** Es el canal más efectivo con una **tasa de contratación del 56.2%** y un tiempo de cierre ágil de **14.7 días**.
*   ⚖️ **LinkedIn y Universidad:** Son canales estables y consistentes, con conversiones del **37.8%** y **36.4%** respectivamente.
*   📉 **Instagram y Ferias drenan recursos:** Las Ferias registran la conversión más baja (**12.7%**). Instagram es costoso, convierte poco (**17.4%**) y es el proceso más lento (**16.7 días**).
*   ⚠️ **Alerta en la experiencia del candidato:** La tasa de abandono global es críticamente alta (**22.8%**). Casi 1 de cada 4 profesionales deserta voluntariamente del proceso.

---

## 💡 5. Recomendaciones Estratégicas

*   ➡️ **Potenciar referidos:** Implementar un programa formal de incentivos para los empleados que recomienden talento interno.
*   ➡️ **Auditar Instagram y Ferias:** Pausar temporalmente la inversión de horas-hombre y presupuesto en estos canales hasta optimizar los filtros iniciales.
*   ➡️ **Mitigar abandonos:** Aplicar encuestas de salida a candidatos desertores para evaluar si las ofertas salariales están bajas o si las pruebas técnicas son extensas.

## 💡 6. Imagenes

<img width="482" height="438" alt="image" src="https://github.com/user-attachments/assets/9a4a4a94-abd4-4b9d-a69c-59cfa4fb702e" />

<img width="460" height="314" alt="image" src="https://github.com/user-attachments/assets/b1df43d6-b2b9-4164-83e7-141fe68245bb" />

