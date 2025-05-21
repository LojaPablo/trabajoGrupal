import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial
st.set_page_config(page_title="Análisis de Ventas", layout="wide")
st.title("📊 Análisis Visual de Ventas de Tienda de Conveniencia")
df = pd.read_csv('data.csv')
df['Date'] = pd.to_datetime(df['Date'])


st.sidebar.header("Filtros")
fecha_inicio = st.sidebar.date_input("Desde", df['Date'].min())
fecha_fin = st.sidebar.date_input("Hasta", df['Date'].max())
df_filtrado = df[(df['Date'] >= pd.to_datetime(fecha_inicio)) & (df['Date'] <= pd.to_datetime(fecha_fin))]

# Pestañas
tab1, tab2, tab3 = st.tabs([
    "📈 Evolución de Ventas Totales",
    "🥧 Ingresos por Línea de Producto",
    "⭐ Distribución de Calificaciones"
])

# Evolución de Ventas Totales
with tab1:
    st.subheader("📈 Evolución Diaria de Ventas Totales")
    st.markdown("El presente gráfico indica cómo varían las ventas totales a lo largo del tiempo según el rango de fechas seleccionado.")
    ventas_diarias = df_filtrado.groupby('Date')['Total'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=ventas_diarias, x='Date', y='Total', marker='o', ax=ax1, color='#4C72B0')
    ax1.set_title("Ventas Totales por Día", fontsize=16)
    ax1.set_xlabel("Fecha")
    ax1.set_ylabel("Ventas Totales (USD)")
    ax1.yaxis.set_major_formatter('${x:,.0f}')
    plt.xticks(rotation=45)
    st.pyplot(fig1)

# Ingresos por Línea de Producto
with tab2:
    st.subheader("🥧 Distribución de Ingresos por Línea de Producto")
    st.markdown("El siguiente gráfico indica el porcentaje de ingresos generados por cada categoría de producto.")
    ingresos_por_linea = df_filtrado.groupby('Product line')['Total'].sum()
    fig2, ax2 = plt.subplots(figsize=(7, 7))
    ingresos_por_linea.plot.pie(autopct='%1.1f%%', startangle=90, ax=ax2, colormap='Pastel1')
    ax2.set_ylabel("")
    ax2.set_title("Distribución % de Ingresos")
    st.pyplot(fig2)

# Calificación de Clientes
with tab3:
    st.subheader("⭐ Distribución de Calificaciones de Clientes")
    st.markdown("El siguiente gráfico muestra cómo se distribuyen las calificaciones dadas por los clientes (Rating).")
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    sns.histplot(df_filtrado['Rating'], bins=10, kde=True, color='#55A868', ax=ax3)
    ax3.set_title("Distribución de Calificaciones")
    ax3.set_xlabel("Rating")
    ax3.set_ylabel("Frecuencia")
    st.pyplot(fig3)
