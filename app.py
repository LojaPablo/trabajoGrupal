import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar y preparar datos
df = pd.read_csv('data.csv')  # Ajusta al nombre de tu archivo
df['Date'] = pd.to_datetime(df['Date'])

# 2. Filtro interactivo opcional
fecha_inicio = st.sidebar.date_input("Desde", df['Date'].min())
fecha_fin = st.sidebar.date_input("Hasta", df['Date'].max())
df_filtrado = df[(df['Date'] >= pd.to_datetime(fecha_inicio)) & (df['Date'] <= pd.to_datetime(fecha_fin))]

# 3. Crear pestañas para los análisis
tab1, tab2 = st.tabs(["📈 Evolución de Ventas Totales", "🧾 Ingresos por Línea de Producto"])

# ---------------------------------------------------------
# TAB 1: Evolución de Ventas Totales (Gráfico de Línea)
# ---------------------------------------------------------
with tab1:
    st.header("📈 Evolución Diaria de Ventas Totales")

    ventas_diarias = df_filtrado.groupby('Date')['Total'].sum().reset_index()

    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.set_style("whitegrid")

    sns.lineplot(
        data=ventas_diarias,
        x='Date',
        y='Total',
        marker='o',
        color='#4C72B0',
        linewidth=2.5,
        markersize=8,
        ax=ax1
    )

    ax1.set_title('Evolución Diaria de Ventas Totales', fontsize=16, pad=20, fontweight='bold')
    ax1.set_xlabel('Fecha', fontsize=12, labelpad=10)
    ax1.set_ylabel('Ventas Totales (USD)', fontsize=12, labelpad=10)
    ax1.yaxis.set_major_formatter('${x:,.0f}')
    plt.xticks(rotation=45, ha='right')

    # Anotaciones de máximo y mínimo
    max_idx = ventas_diarias['Total'].idxmax()
    min_idx = ventas_diarias['Total'].idxmin()
    max_point = ventas_diarias.loc[max_idx]
    min_point = ventas_diarias.loc[min_idx]

    ax1.annotate(f'Máximo: ${max_point["Total"]:,.0f}', 
                xy=(max_point['Date'], max_point['Total']),
                xytext=(10, 10), textcoords='offset points',
                arrowprops=dict(arrowstyle='->'))
    ax1.annotate(f'Mínimo: ${min_point["Total"]:,.0f}', 
                xy=(min_point['Date'], min_point['Total']),
                xytext=(10, -20), textcoords='offset points',
                arrowprops=dict(arrowstyle='->'))

    plt.tight_layout()
    st.pyplot(fig1)

# ---------------------------------------------------------
# TAB 2: Ingresos por Línea de Producto (Gráfico Circular)
# ---------------------------------------------------------
with tab2:
    st.header("🧾 Distribución % de Ingresos por Línea de Producto")

    ingresos_por_linea = df_filtrado.groupby('Product line')['Total'].sum().sort_values(ascending=True)

    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ax2.pie(
        ingresos_por_linea,
        labels=ingresos_por_linea.index,
        autopct='%1.1f%%',
        startangle=90
    )
    ax2.set_title('Distribución % de Ingresos por Línea')
    ax2.axis('equal')  # Asegura que el círculo sea perfecto

    st.pyplot(fig2)