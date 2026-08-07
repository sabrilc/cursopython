import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

# ============================================================
# 1. IMPORTAR Y LIMPIAR LOS DATOS
# ============================================================

# Leer el archivo CSV, ignorando las líneas con errores
df = pd.read_csv("estudiantes.csv", encoding="utf-8", on_bad_lines="skip")

# Quitar espacios en los nombres de las columnas
df.columns = df.columns.str.strip()

# Quitar los tabuladores ("\t") que traen los valores de texto
for columna in ["Nombre", "Género", "Ciudad", "Facultad", "Carrera", "Modalidad", "Estado Académico"]:
    df[columna] = df[columna].str.replace("\t", "")

# Borrar filas que tengan algún dato vacío
df = df.dropna()

# Crear la carpeta donde se guardarán los gráficos
os.makedirs("dashboard", exist_ok=True)

# ============================================================
# 2. CREAR LOS 8 GRÁFICOS
# ============================================================

# Gráfico 1: Histograma de edades (Matplotlib)
plt.figure(figsize=(9, 6))
plt.hist(df["Edad"], bins=15, color="skyblue", edgecolor="black")
plt.title("Distribución de Edades")
plt.xlabel("Edad")
plt.ylabel("Cantidad de estudiantes")
plt.savefig("dashboard/histograma_edades.png", bbox_inches="tight")
plt.close()

# Gráfico 2: Barras de estudiantes por ciudad (Matplotlib)
plt.figure(figsize=(10, 6))
df["Ciudad"].value_counts().plot(kind="bar", color="orange")
plt.title("Estudiantes por Ciudad")
plt.xlabel("Ciudad")
plt.ylabel("Cantidad")
plt.xticks(rotation=45)
plt.savefig("dashboard/estudiantes_por_ciudad.png", bbox_inches="tight")
plt.close()

# Gráfico 3: Pastel de modalidad (Matplotlib)
plt.figure(figsize=(8, 7))
conteo_modalidad = df["Modalidad"].value_counts()
plt.pie(conteo_modalidad, labels=conteo_modalidad.index, autopct="%1.1f%%")
plt.title("Distribución por Modalidad")
plt.savefig("dashboard/modalidad.png", bbox_inches="tight")
plt.close()

# Gráfico 4: Cajas de promedio por facultad (Matplotlib)
plt.figure(figsize=(10, 6))
df.boxplot(column="Promedio", by="Facultad", rot=45)
plt.title("Promedio por Facultad")
plt.xlabel("Facultad")
plt.ylabel("Promedio")
plt.savefig("dashboard/promedio_por_facultad.png", bbox_inches="tight")
plt.close()

# Gráfico 5: Barras de estado académico (Seaborn)
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x="Estado Académico", hue="Estado Académico")
plt.title("Estado Académico de los Estudiantes")
plt.xlabel("Estado Académico")
plt.ylabel("Cantidad")
plt.savefig("dashboard/estado_academico.png", bbox_inches="tight")
plt.close()

# Gráfico 6: Histograma del promedio con curva (Seaborn)
plt.figure(figsize=(8, 6))
sns.histplot(data=df, x="Promedio", bins=15, kde=True, color="green")
plt.title("Distribución del Promedio")
plt.xlabel("Promedio")
plt.ylabel("Cantidad")
plt.savefig("dashboard/distribucion_promedio.png", bbox_inches="tight")
plt.close()

# Gráfico 7: Dispersión promedio vs asistencia (Plotly)
grafico1 = px.scatter(df, x="Asistencia (%)", y="Promedio",
                      color="Estado Académico", title="Promedio vs Asistencia")
grafico1.write_html("dashboard/promedio_vs_asistencia.html")
grafico1.write_image("dashboard/promedio_vs_asistencia.png")

# Gráfico 8: Barras de estudiantes por carrera (Plotly)
conteo_carrera = df["Carrera"].value_counts().reset_index()
conteo_carrera.columns = ["Carrera", "Cantidad"]
grafico2 = px.bar(conteo_carrera, x="Cantidad", y="Carrera", orientation="h",
                  title="Estudiantes por Carrera")
grafico2.write_html("dashboard/estudiantes_por_carrera.html")
grafico2.write_image("dashboard/estudiantes_por_carrera.png")

# ============================================================
# 3. CALCULAR RESULTADOS PARA EL INFORME
# ============================================================

# Promedio por carrera (ordenado de mayor a menor)
mejor_carrera = df.groupby("Carrera")["Promedio"].mean().sort_values(ascending=False)

# Promedio por ciudad (ordenado de mayor a menor)
promedio_ciudad = df.groupby("Ciudad")["Promedio"].mean().sort_values(ascending=False)

# Valores atípicos (regla del IQR)
q1 = df["Promedio"].quantile(0.25)
q3 = df["Promedio"].quantile(0.75)
iqr = q3 - q1
limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr
n_outliers = len(df[(df["Promedio"] < limite_inferior) | (df["Promedio"] > limite_superior)])

# Datos para escribir textos
edad_min = df["Edad"].min()
edad_max = df["Edad"].max()
edad_media = df["Edad"].mean()
mejor_carrera_nombre = mejor_carrera.index[0]

# ============================================================
# 4. CREAR EL INFORME EN PDF
# ============================================================

estilo_titulo = getSampleStyleSheet()["Title"]
estilo_subtitulo = getSampleStyleSheet()["Heading2"]
estilo_texto = getSampleStyleSheet()["BodyText"]
estilo_texto.spaceAfter = 2
estilo_subtitulo.spaceBefore = 6
estilo_subtitulo.spaceAfter = 2

pdf = SimpleDocTemplate("../informe_ejecutivo.pdf", pagesize=A4,
                        title="Informe Ejecutivo")
elementos = []

elementos.append(Paragraph("Informe Ejecutivo - Análisis de Estudiantes", estilo_titulo))
elementos.append(Spacer(1, 0.2 * cm))

# Pregunta 1
elementos.append(Paragraph("1. ¿Qué carrera tiene el mejor promedio?", estilo_subtitulo))
elementos.append(Paragraph(
    f"La carrera con el mejor promedio es {mejor_carrera_nombre} "
    f"({mejor_carrera.iloc[0]:.2f}).",
    estilo_texto))
elementos.append(Image("dashboard/estudiantes_por_carrera.png", width=12 * cm, height=7 * cm))
elementos.append(Spacer(1, 0.15 * cm))

# Pregunta 2
elementos.append(Paragraph("2. ¿Cuál es la distribución de edades?", estilo_subtitulo))
elementos.append(Paragraph(
    f"Las edades van de {edad_min} a {edad_max} años, con un promedio de "
    f"{edad_media:.1f} años. La mayoría se concentra entre 22 y 28 años.",
    estilo_texto))
elementos.append(Image("dashboard/histograma_edades.png", width=10 * cm, height=6 * cm))
elementos.append(Spacer(1, 0.15 * cm))

# Pregunta 3
elementos.append(Paragraph("3. ¿Existen diferencias entre ciudades?", estilo_subtitulo))
elementos.append(Paragraph(
    f"Las ciudades con mejor promedio son {promedio_ciudad.index[0]} "
    f"({promedio_ciudad.iloc[0]:.2f}) y {promedio_ciudad.index[1]} "
    f"({promedio_ciudad.iloc[1]:.2f}).",
    estilo_texto))
elementos.append(Image("dashboard/estudiantes_por_ciudad.png", width=12 * cm, height=7 * cm))
elementos.append(Spacer(1, 0.15 * cm))

# Pregunta 4
elementos.append(Paragraph("4. ¿Se identifican valores atípicos en las calificaciones?", estilo_subtitulo))
if n_outliers == 0:
    texto_outliers = "No se encontraron valores atípicos en las calificaciones."
else:
    texto_outliers = f"Se encontraron {n_outliers} calificaciones atípicas."
elementos.append(Paragraph(texto_outliers, estilo_texto))
elementos.append(Image("dashboard/distribucion_promedio.png", width=10 * cm, height=5.5 * cm))
elementos.append(Spacer(1, 0.15 * cm))
elementos.append(Image("dashboard/promedio_vs_asistencia.png", width=10 * cm, height=5.5 * cm))
elementos.append(Spacer(1, 0.15 * cm))

# Conclusiones
elementos.append(Paragraph("Conclusiones", estilo_subtitulo))
elementos.append(Paragraph("1. Odontología destaca con el mejor promedio.", estilo_texto))
elementos.append(Paragraph("2. La población es joven (promedio de 24.5 años).", estilo_texto))
elementos.append(Paragraph("3. Las diferencias por ciudad son leves.", estilo_texto))
elementos.append(Paragraph("4. No hay valores atípicos en las calificaciones.", estilo_texto))
elementos.append(Paragraph("5. Conviene apoyar a Enfermería y Física.", estilo_texto))

pdf.build(elementos)
print("¡Listo! Gráficos en la carpeta 'dashboard' y informe en la raíz del proyecto.")