# ==============================================================================
# PEOPLE ANALYTICS - Informe de Kpis de reclutamiento
# AUTOR: Milton Vivero
# ==============================================================================

import os  # Administración del sistema de archivos y validación de rutas locales
import pandas as pd  # Procesamiento, limpieza y agrupación avanzada de datos tabulares
import plotly.graph_objects as go  # Creación de objetos visuales interactivos de alto impacto
from plotly.subplots import make_subplots  # Construcción de matrices organizadas de gráficos (Subplots)
import webbrowser  # Despliegue automático del informe final en el navegador web por defecto

# ==============================================================================
# 1. ENTRADA DE DATOS Y CONFIGURACIÓN DE ENTORNO CORPORATIVO
# ==============================================================================
folder_process = 'Data proccess'
folder_informe = 'Informe'

# Automatización: Si las carpetas no existen en tu entorno, las creamos de inmediato
for folder in [folder_process, folder_informe]:
    os.makedirs(folder, exist_ok=True)

# Apuntamos a la base de datos
file_input = os.path.join(folder_process, 'Data_Talento.xlsx')

# Control de riesgos: Validamos que la fuente de datos exista antes de procesar
if not os.path.exists(file_input):
    raise FileNotFoundError(f"Error: Asegúrate de guardar tu Excel como 'Data_Talento.xlsx' en '{folder_process}'.")

# Cargamos el archivo histórico de postulaciones del año consolidado
df = pd.read_excel(file_input)

# Auditoría de Calidad: Removemos filas de cabeceras duplicadas que puedan dañar los cálculos
df = df[df['CODIGO_CANDIDATO'] != 'CODIGO_CANDIDATO']

# Ingeniería de Datos: Forzamos el formato de tiempo (Datetime) para calcular KPIs cronológicos
df['FECHA_APERTURA'] = pd.to_datetime(df['FECHA_APERTURA'], errors='coerce')
df['FECHA_CONTRATACION'] = pd.to_datetime(df['FECHA_CONTRATACION'], errors='coerce')

# ==============================================================================
# 2. PROCESAMIENTO ANALÍTICO E INDICADORES CLAVE (KPIs AUDITADOS)
# ==============================================================================
# Universo de éxito: Candidatos que completaron el embudo de selección
contratados = df[df['ESTADO_FINAL_PROCESO'] == 'Contratado / Incorporado']

# KPIs de Conversión globales
tasa_contratacion = round(len(contratados) / len(df) * 100, 1)
tasa_abandono = round(len(df[df['ESTADO_FINAL_PROCESO'] == 'Candidato Desistió']) / len(df) * 100, 1)

# KPIs cronológicos corregidos metodológicamente (exclusivos sobre procesos cerrados con éxito)
time_to_fill = round(contratados['DIAS_VACANTE_ABIERTA'].mean(), 1)
time_to_hire = round(contratados['DIAS_PROCESO_EVALUACION'].mean(), 1)

# --- Agrupación Estadística por Puesto Requerido ---
analisis_cargo = df.groupby('PUESTO_REQUERIDO').agg(
    total_postulantes=('CODIGO_CANDIDATO', 'count'),
    total_contratados=('ESTADO_FINAL_PROCESO', lambda x: (x == 'Contratado / Incorporado').sum()),
    salario_promedio=('SUELDO_MENSUAL_USD', 'mean'),
    avg_time_to_hire=('DIAS_PROCESO_EVALUACION', 'mean')
).reset_index()

analisis_cargo['tasa_contratacion'] = round((analisis_cargo['total_contratados'] / analisis_cargo['total_postulantes']) * 100, 1)
analisis_cargo['salario_promedio'] = round(analisis_cargo['salario_promedio'], 2)
analisis_cargo['avg_time_to_hire'] = round(analisis_cargo['avg_time_to_hire'], 1)
analisis_cargo = analisis_cargo.sort_values('salario_promedio', ascending=False)

# --- Agrupación Estadística por Fuente de Reclutamiento ---
fuente = df.groupby('FUENTE_RECLUTAMIENTO').agg(
    total=('CODIGO_CANDIDATO', 'count'),
    contratados=('ESTADO_FINAL_PROCESO', lambda x: (x == 'Contratado / Incorporado').sum())
).reset_index()
fuente['tasa'] = round(fuente['contratados'] / fuente['total'] * 100, 1)
fuente = fuente.sort_values('tasa', ascending=False)

# ==============================================================================
# 3. MAQUETACIÓN VISUAL INTERACTIVA (PLOTLY SUBPLOTS)
# ==============================================================================
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=[
        'Sueldo Promedio por Puesto (USD $)', 'Tasa de Contratación por Puesto (%)',
        'Tiempo Promedio de Evaluación (Días)', 'Efectividad por Fuente de Reclutamiento (%)'
    ],
    specs=[[{'type': 'xy'}, {'type': 'xy'}], [{'type': 'xy'}, {'type': 'xy'}]]
)

fig.add_trace(go.Bar(x=analisis_cargo['PUESTO_REQUERIDO'], y=analisis_cargo['salario_promedio'], name='Sueldo', marker_color='#2c3e50'), row=1, col=1)
fig.add_trace(go.Bar(x=analisis_cargo['PUESTO_REQUERIDO'], y=analisis_cargo['tasa_contratacion'], name='Conversión', marker_color='#27ae60'), row=1, col=2)
fig.add_trace(go.Bar(x=analisis_cargo['PUESTO_REQUERIDO'], y=analisis_cargo['avg_time_to_hire'], name='Evaluación', marker_color='#e74c3c'), row=2, col=1)
fig.add_trace(go.Bar(x=fuente['FUENTE_RECLUTAMIENTO'], y=fuente['tasa'], name='Canales', marker_color='#2980b9'), row=2, col=2)

fig.update_layout(height=720, showlegend=False, template='plotly_white')
div_graficos = fig.to_html(full_html=False, include_plotlyjs='cdn')

# Mapeo estético de cabeceras en español corporativo para la tabla de datos duros
analisis_cargo_print = analisis_cargo.rename(columns={
    'PUESTO_REQUERIDO': 'Puesto Requerido',
    'total_postulantes': 'Total Postulantes',
    'total_contratados': 'Total Contratados',
    'salario_promedio': 'Sueldo Promedio (USD)',
    'avg_time_to_hire': 'Tiempo Promedio Eval. (Días)',
    'tasa_contratacion': 'Tasa Éxito %'
})
columnas_tabla = ['Puesto Requerido', 'Total Postulantes', 'Total Contratados', 'Tasa Éxito %', 'Sueldo Promedio (USD)', 'Tiempo Promedio Eval. (Días)']
analisis_cargo_print = analisis_cargo_print[columnas_tabla]
tabla_html = analisis_cargo_print.to_html(classes='table table-striped', index=False)

# ==============================================================================
# 4. COMPILACIÓN DE TU INFORME EXECUTIVE PREMIUM HTML (ESTILOS SEPARADOS)
# ==============================================================================
# Declaramos las reglas de diseño CSS en una variable aislada para evitar conflictos de formato
css = """
body { font-family: 'Segoe UI', sans-serif; margin: 40px; color: #333; background-color: #f4f6f7; }
.container { max-width: 1200px; margin: auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 12px; }
.subtitle { color: #7f8c8d; font-style: italic; margin-bottom: 30px; }
h2 { color: #34495e; margin-top: 40px; border-left: 5px solid #2980b9; padding-left: 10px; }
.kpi-container { display: flex; justify-content: space-between; margin: 25px 0; gap: 20px; }
.kpi-card { flex: 1; background: #f8f9f9; padding: 25px; border-radius: 6px; text-align: center; box-shadow: inset 0 -3px 0 #3498db; border: 1px solid #e5e8e8; }
.kpi-card h3 { margin: 0; color: #7f8c8d; font-size: 13px; text-transform: uppercase; }
.kpi-card .value { font-size: 32px; font-weight: bold; color: #2c3e50; margin-top: 10px; }
.table { width: 100%; border-collapse: collapse; margin-top: 20px; }
.table th, .table td { padding: 14px; text-align: left; border-bottom: 1px solid #eaeded; }
.table th { background-color: #2c3e50; color: white; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }
.table-striped tbody tr:nth-of-type(odd) { background-color: #f9f9f9; }
.insights { background-color: #fef9e7; border-left: 5px solid #f1c40f; padding: 25px; margin-top: 40px; border-radius: 4px; }
.insights li { margin-bottom: 12px; line-height: 1.6; }
"""

# CONSTRUCCIÓN BLINDADA: Usamos comillas triples limpias sin paréntesis para evitar el SyntaxError de cierre
html_report = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<title>People Analytics Ecuador</title>
<style>{css}</style>
</head>
<body>
<div class='container'>
<h1>Informe Ejecutivo de Reclutamiento y Selección</h1>
<div class='subtitle'>Análisis avanzado de estructuras salariales mensuales fijos y eficiencia de canales en el mercado ecuatoriano</div>
<h2>1. Indicadores Globales de Rendimiento (KPIs)</h2>
<div class='kpi-container'>
<div class='kpi-card'><h3>Tasa de Contratación</h3><div class='value'>{tasa_contratacion}%</div></div>
<div class='kpi-card'><h3>Tasa de Abandono</h3><div class='value'>{tasa_abandono}%</div></div>
<div class='kpi-card'><h3>Días para Cubrir Vacante</h3><div class='value'>{time_to_fill} días</div></div>
<div class='kpi-card'><h3>Días de Evaluación</h3><div class='value'>{time_to_hire} días</div></div>
</div>
<h2>2. Cuadro de Mando Visual e Interactivo</h2>
{div_graficos}
<h2>3. Datos Duros y Desglose por Estructura de Cargos Locales</h2>
{tabla_html}
<h2>4. Conclusiones y Plan de Acción Estratégico</h2>
<div class='insights'><ul>
<li><strong>Metodología de Reclutamiento Auditada:</strong> Los indicadores globales de tiempo se calculan con base en las posiciones cerradas con éxito, eliminando sesgos de vacantes huerfanas o canceladas.</li>
<li><strong>Eficiencia de Operaciones:</strong> El balance entre el Time to Fill y el Time to Hire demuestra que el proceso interno de entrevistas es ágil, permitiendo enfocar esfuerzos en mejorar los canales de captación inicial.</li>
</ul></div>
</div>
</body>
</html>"""

# ==============================================================================
# 5. ALMACENAMIENTO Y DESPLIEGUE AUTOMÁTICO EN PANTALLA
# ==============================================================================
file_html = os.path.join(folder_informe, 'informe_final_reclutamiento_ecuador.html')

with open(file_html, 'w', encoding='utf-8') as f:
    f.write(html_report)

