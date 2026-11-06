import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Dashboard Impacto Tributario Licores", layout="wide")

# 1. Carga de Datos
@st.cache_data
def load_data():
    df = pd.read_excel("Base_Datos_Tributaria_Licores.xlsx")
    return df

df = load_data()

# 2. Navegación en el Menú Lateral
st.sidebar.title("Navegación")
opciones = ["Resumen General"] + df['Categoría'].tolist()
seleccion = st.sidebar.radio("Selecciona una vista:", opciones)

# Nota metodológica en el menú lateral
st.sidebar.markdown("---")
st.sidebar.caption(
    "**Nota Metodológica:** Simulación proyectada a 2027. "
    "Supone traslado completo de los incrementos tributarios al consumidor, "
    "asumiendo precios base constantes y omitiendo cambios en la demanda, "
    "márgenes de comercialización o características del producto."
)

# 3. Vista: Resumen General
if seleccion == "Resumen General":
    st.title("📈 Impacto del PL de Rescate Económico en Bebidas Alcohólicas")
    
    # Expander con la metodología detallada
    with st.expander("Ver Metodología y Supuestos del Cálculo"):
        st.info(
            "Para estimar el impacto, se parte de los precios de venta de 2026 (sin impuesto al consumo ni IVA), "
            "incrementados en un 5% para obtener la base de 2027. Se asume que estos precios base son constantes "
            "y que el incremento tributario se traslada 100% al consumidor final. La tarifa de IVA se mantiene al 19%. "
            "La presión fiscal corresponde a la participación del total de impuestos sobre el precio de venta final."
        )

    # Tabla General
    st.subheader("📋 Tabla General de Tarifas (Antes y Después)")
    columnas_mostrar = [
        'Producto', 'Precio_Base_2027', 
        'Actual_Total_Impuestos', 'Actual_Precio_Final', 'Actual_Presion_Fiscal',
        'PL_Total_Impuestos', 'PL_Precio_Final', 'PL_Presion_Fiscal', 'Incremento_Carga_Tributaria'
    ]
    df_mostrar = df[columnas_mostrar].copy()
    
    # Formatear porcentajes y monedas para la tabla visual
    for col in ['Actual_Presion_Fiscal', 'PL_Presion_Fiscal', 'Incremento_Carga_Tributaria']:
        df_mostrar[col] = (df_mostrar[col] * 100).round(1).astype(str) + '%'
    for col in ['Precio_Base_2027', 'Actual_Total_Impuestos', 'Actual_Precio_Final', 'PL_Total_Impuestos', 'PL_Precio_Final']:
        df_mostrar[col] = '$' + df_mostrar[col].apply(lambda x: f"{x:,.0f}").str.replace(',', '.')

    st.dataframe(df_mostrar, use_container_width=True)

    st.markdown("---")
    
    # Gráficos Comparativos Principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Precio de Venta Final y Total Impuestos")
        # Preparar datos para gráfico de barras agrupadas
        df_melt = pd.melt(df, id_vars=['Categoría'], 
                          value_vars=['Actual_Precio_Final', 'PL_Precio_Final', 'Actual_Total_Impuestos', 'PL_Total_Impuestos'],
                          var_name='Métrica', value_name='Valor')
        
        # Etiquetar limpiamente
        df_melt['Escenario'] = df_melt['Métrica'].apply(lambda x: 'Actual' if 'Actual' in x else 'PL Rescate')
        df_melt['Tipo'] = df_melt['Métrica'].apply(lambda x: 'Precio Final' if 'Precio' in x else 'Total Impuestos')
        
        fig_bar = px.bar(df_melt, x='Categoría', y='Valor', color='Escenario', barmode='group',
                         facet_col='Tipo', text_auto='.2s', color_discrete_sequence=['#4C78A8', '#E45756'])
        fig_bar.update_layout(showlegend=True, margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("⚖️ Presión Fiscal (Actual vs. PL)")
        # Gráfico Slope / Barras de Presión Fiscal
        fig_slope = go.Figure()
        for i, row in df.iterrows():
            fig_slope.add_trace(go.Scatter(
                x=[row['Actual_Presion_Fiscal'], row['PL_Presion_Fiscal']],
                y=[row['Categoría'], row['Categoría']],
                mode='lines+markers+text',
                name=row['Categoría'],
                text=[f"{row['Actual_Presion_Fiscal']:.0%}", f"{row['PL_Presion_Fiscal']:.0%}"],
                textposition=["middle left", "middle right"],
                marker=dict(size=10)
            ))
        fig_slope.update_layout(
            xaxis_title="Presión Fiscal (%)", yaxis_title="Categoría",
            showlegend=False, xaxis=dict(tickformat='.0%'),
            margin=dict(t=40, b=0, l=0, r=0)
        )
        st.plotly_chart(fig_slope, use_container_width=True)

# 4. Vistas: Hojas por Producto
else:
    # Filtrar datos del producto seleccionado
    prod_data = df[df['Categoría'] == seleccion].iloc[0]
    
    st.title(f"🥃 Detalle: {prod_data['Producto']}")
    
    # Notas Fiscales por Categoría
    if seleccion == "Cerveza":
         st.info("🍻 **Nota fiscal:** La ley vigente aplica un 48% ad valorem (sin específico). El proyecto propone $330 por grado/330ml más 10% ad valorem sobre el precio certificado por el DANE. IVA del 19% constante.")
    else:
         st.info("🍷 **Nota fiscal:** El impuesto al consumo proyectado se calcula integrando los componentes específico y ad valorem correspondientes a cada escenario, con un IVA fijo del 19%.")

    # Tarjetas de Indicadores (Métricas)
    st.subheader("KPIs del Escenario (PL Rescate)")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Precio Base (2027)", f"${prod_data['Precio_Base_2027']:,.0f}", 
                help="Partiendo de precios de 2026 (sin impuestos), incrementados un 5%.")
    
    delta_precio = prod_data['PL_Precio_Final'] - prod_data['Actual_Precio_Final']
    col2.metric("Precio Venta Final", f"${prod_data['PL_Precio_Final']:,.0f}", f"+${delta_precio:,.0f}")
    
    delta_impuestos = prod_data['PL_Total_Impuestos'] - prod_data['Actual_Total_Impuestos']
    col3.metric("Total Impuestos", f"${prod_data['PL_Total_Impuestos']:,.0f}", f"+${delta_impuestos:,.0f}")
    
    delta_presion = prod_data['PL_Presion_Fiscal'] - prod_data['Actual_Presion_Fiscal']
    col4.metric("Presión Fiscal", f"{prod_data['PL_Presion_Fiscal']:.0%}", f"{delta_presion:.0%} pt",
                help="Calculada como la participación del total de impuestos en el precio final al consumidor.")

    st.markdown("---")

    # Gráficos Waterfall comparativos
    st.subheader("💧 Desglose de Precios (Cascada)")
    col_w1, col_w2 = st.columns(2)

    with col_w1:
        st.markdown("**Legislación Actual**")
        fig_w1 = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Precio Base", "Ad Valorem", "Específico", "IVA", "Precio Final"],
            textposition="outside",
            text=[f"${x:,.0f}" for x in [prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], 
                                         prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']]],
            y=[prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], 
               prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        fig_w1.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_w1, use_container_width=True)

    with col_w2:
        st.markdown("**PL Rescate Económico**")
        fig_w2 = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Precio Base", "Ad Valorem", "Específico", "IVA", "Precio Final"],
            textposition="outside",
            text=[f"${x:,.0f}" for x in [prod_data['Precio_Base_2027'], prod_data['PL_AdValorem_Valor'], 
                                         prod_data['PL_Especifico_Valor'], prod_data['PL_IVA_Valor'], prod_data['PL_Precio_Final']]],
            y=[prod_data['Precio_Base_2027'], prod_data['PL_AdValorem_Valor'], 
               prod_data['PL_Especifico_Valor'], prod_data['PL_IVA_Valor'], prod_data['PL_Precio_Final']],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        fig_w2.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_w2, use_container_width=True)
