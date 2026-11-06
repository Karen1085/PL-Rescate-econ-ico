import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Impacto Tributario Licores", layout="wide")

# Colores institucionales para los gráficos
COLOR_ACTUAL = '#707070'  # Gris para legislación actual
COLOR_PL = '#8A1C30'      # Tinto/Rojo para PL Rescate

# 1. Carga de Datos de la Base de Excel
@st.cache_data
def load_data():
    return pd.read_excel("Base_Datos_Tributaria_Licores.xlsx")

df = load_data()

# 2. Encabezado y Menú Desplegable
st.title("📊 Impacto del PL de Rescate Económico en Bebidas")
st.markdown("---")

# Menú desplegable estilo Datexco
opciones = ["Todos los productos"] + df['Categoría'].tolist()
seleccion = st.selectbox("Seleccione el nivel de análisis:", opciones)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# VISTA: TODOS LOS PRODUCTOS
# ==========================================
if seleccion == "Todos los productos":
    
    # --- GRÁFICO 1: PRESIÓN FISCAL ---
    st.subheader("⚖️ 1. Presión Fiscal (% del precio que son impuestos)")
    fig_presion = go.Figure()
    
    for i, row in df.iterrows():
        # Línea conectora (Dumbbell)
        fig_presion.add_trace(go.Scatter(
            x=[row['Actual_Presion_Fiscal'], row['PL_Presion_Fiscal']],
            y=[row['Categoría'], row['Categoría']],
            mode='lines', line=dict(color='#d3d3d3', width=4), showlegend=False
        ))
        # Punto Actual (Gris)
        fig_presion.add_trace(go.Scatter(
            x=[row['Actual_Presion_Fiscal']], y=[row['Categoría']],
            mode='markers+text', marker=dict(color=COLOR_ACTUAL, size=14),
            text=[f"{row['Actual_Presion_Fiscal']:.0%}"], textposition='middle left',
            name='Legislación Actual' if i == 0 else "", showlegend=(i==0)
        ))
        # Punto PL (Rojo)
        fig_presion.add_trace(go.Scatter(
            x=[row['PL_Presion_Fiscal']], y=[row['Categoría']],
            mode='markers+text', marker=dict(color=COLOR_PL, size=14),
            text=[f"{row['PL_Presion_Fiscal']:.0%}"], textposition='middle right',
            textfont=dict(color=COLOR_PL, weight='bold'),
            name='PL Rescate Económico' if i == 0 else "", showlegend=(i==0)
        ))

    fig_presion.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(t=20, b=20, l=0, r=0),
        xaxis=dict(showgrid=True, gridcolor='#E5E5E5', tickformat='.0%', range=[0.2, 0.65]),
        yaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_presion, use_container_width=True)
    st.markdown("---")

    # --- GRÁFICO 2: TOTAL IMPUESTOS ---
    st.subheader("💰 2. Total de Impuestos por Botella")
    col_graf, col_cards = st.columns([3, 1])
    
    with col_graf:
        fig_impuestos = go.Figure()
        fig_impuestos.add_trace(go.Bar(
            x=df['Categoría'], y=df['Actual_Total_Impuestos'],
            name='Legislación Actual', marker_color=COLOR_ACTUAL,
            text=[f"${x:,.0f}".replace(',', '.') for x in df['Actual_Total_Impuestos']],
            textposition='outside', textfont=dict(size=12)
        ))
        fig_impuestos.add_trace(go.Bar(
            x=df['Categoría'], y=df['PL_Total_Impuestos'],
            name='PL Rescate Económico', marker_color=COLOR_PL,
            text=[f"${x:,.0f}".replace(',', '.') for x in df['PL_Total_Impuestos']],
            textposition='outside', textfont=dict(size=12, color=COLOR_PL, weight='bold')
        ))
        fig_impuestos.update_layout(
            barmode='group', plot_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(t=20, b=0, l=0, r=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False)
        )
        st.plotly_chart(fig_impuestos, use_container_width=True)
        
    with col_cards:
        st.markdown("<br>", unsafe_allow_html=True)
        for _, row in df.iterrows():
            incremento = row['PL_Total_Impuestos'] - row['Actual_Total_Impuestos']
            st.info(f"**{row['Categoría']}**\n\n+${incremento:,.0f} por botella".replace(',', '.'))
            
    st.markdown("---")

    # --- GRÁFICO 3: PRECIO DE VENTA FINAL ---
    st.subheader("🏷️ 3. Precio de Venta Final al Consumidor")
    fig_precio = go.Figure()
    fig_precio.add_trace(go.Bar(
        y=df['Categoría'], x=df['Actual_Precio_Final'],
        name='Legislación Actual', orientation='h', marker_color=COLOR_ACTUAL,
        text=[f"${x:,.0f}".replace(',', '.') for x in df['Actual_Precio_Final']],
        textposition='inside', insidetextanchor='end'
    ))
    fig_precio.add_trace(go.Bar(
        y=df['Categoría'], x=df['PL_Precio_Final'],
        name='PL Rescate Económico', orientation='h', marker_color=COLOR_PL,
        text=[f"${x:,.0f}".replace(',', '.') for x in df['PL_Precio_Final']],
        textposition='outside', textfont=dict(color=COLOR_PL, weight='bold')
    ))
    fig_precio.update_layout(
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(t=20, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False)
    )
    st.plotly_chart(fig_precio, use_container_width=True)

# ==========================================
# VISTA: PRODUCTO INDIVIDUAL
# ==========================================
else:
    prod_data = df[df['Categoría'] == seleccion].iloc[0]
    st.subheader(f"Análisis Individual: {prod_data['Producto']}")
    
    col1, col2, col3 = st.columns(3)
    delta_imp = prod_data['PL_Total_Impuestos'] - prod_data['Actual_Total_Impuestos']
    delta_pre = prod_data['PL_Precio_Final'] - prod_data['Actual_Precio_Final']
    delta_fis = prod_data['PL_Presion_Fiscal'] - prod_data['Actual_Presion_Fiscal']
    
    col1.metric("Total Impuestos (PL)", f"${prod_data['PL_Total_Impuestos']:,.0f}".replace(',', '.'), f"+${delta_imp:,.0f}".replace(',', '.'))
    col2.metric("Precio Final (PL)", f"${prod_data['PL_Precio_Final']:,.0f}".replace(',', '.'), f"+${delta_pre:,.0f}".replace(',', '.'))
    col3.metric("Presión Fiscal (PL)", f"{prod_data['PL_Presion_Fiscal']:.0%}", f"+{delta_fis:.0%} pt")

    # Cascada comparativa para el producto
    st.markdown("<br><b>Desglose de la construcción del precio:</b>", unsafe_allow_html=True)
    fig_wf = go.Figure()
    fig_wf.add_trace(go.Waterfall(
        name="Actual", orientation="v", measure=["relative"]*4 + ["total"],
        x=["Base", "Ad Valorem", "Específico", "IVA", "Precio Final"],
        y=[prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']],
        textposition="outside", text=[f"${x:,.0f}".replace(',','.') for x in [prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']]],
        connector={"line": {"color": "gray"}}, decreasing={"marker": {"color": COLOR_ACTUAL}}, increasing={"marker": {"color": COLOR_ACTUAL}}, totals={"marker": {"color": "#404040"}}
    ))
    fig_wf.update_layout(title="Composición bajo Legislación Actual", plot_bgcolor='rgba(0,0,0,0)', height=350)
    st.plotly_chart(fig_wf, use_container_width=True)

# ==========================================
# TABLA DE TARIFAS ESTÁTICA (Estilo Imagen)
# ==========================================
st.markdown("---")
st.subheader("📋 Tabla Resumen de Tarifas")

# HTML inyectado para replicar los colores exactos: Azul oscuro, Gris y Rojo claro
html_tabla = """
<style>
.tg {border-collapse:collapse; border-spacing:0; width:100%; text-align:center; font-family:sans-serif; font-size: 14px;}
.tg th {border:1px solid #a0a0a0; padding:10px; font-weight:bold;}
.tg td {border:1px solid #a0a0a0; padding:8px;}
.bg-blue {background-color:#1a3b6c; color:white;}
.bg-grey {background-color:#c0c0c0; color:black;}
.bg-red {background-color:#f9dbd3; color:#8a1c30;}
.text-red {color:#8a1c30; font-weight:bold;}
</style>
<table class="tg">
  <thead>
    <tr>
      <th rowspan="2" style="background-color:white; color:black;">Producto</th>
      <th rowspan="2" style="background-color:white; color:black;">Origen</th>
      <th colspan="2" class="bg-blue">Legislación actual</th>
      <th colspan="2" class="bg-grey">Legislación actual en 2027</th>
      <th colspan="2" class="bg-red">PL rescate</th>
    </tr>
    <tr>
      <th class="bg-blue">Específico vigente 2024</th>
      <th class="bg-blue">Ad valorem vigente</th>
      <th class="bg-grey">Específico vigente 2027</th>
      <th class="bg-grey">Ad valorem vigente</th>
      <th class="bg-red">Específico reforma 2027</th>
      <th class="bg-red">Ad valorem reforma 2027</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Licores y aperitivos</td><td>Nacional</td>
      <td class="bg-blue">$360 por grado</td><td class="bg-blue">25%</td>
      <td class="bg-grey">$378 por grado</td><td class="bg-grey">25%</td>
      <td class="text-red">$750 por grado</td><td class="text-red">35%</td>
    </tr>
    <tr>
      <td>Licores y aperitivos</td><td>Extranjero</td>
      <td class="bg-blue">$360 por grado</td><td class="bg-blue">25%</td>
      <td class="bg-grey">$378 por grado</td><td class="bg-grey">25%</td>
      <td class="text-red">$750 por grado</td><td class="text-red">35%</td>
    </tr>
    <tr>
      <td>Vinos y aperitivos vínicos</td><td>Nacional</td>
      <td class="bg-blue">$243 por grado</td><td class="bg-blue">20%</td>
      <td class="bg-grey">$255 por grado</td><td class="bg-grey">20%</td>
      <td class="text-red">$750 por grado</td><td class="text-red">35%</td>
    </tr>
    <tr>
      <td>Vinos y aperitivos vínicos</td><td>Extranjero</td>
      <td class="bg-blue">$243 por grado</td><td class="bg-blue">20%</td>
      <td class="bg-grey">$255 por grado</td><td class="bg-grey">20%</td>
      <td class="text-red">$750 por grado</td><td class="text-red">35%</td>
    </tr>
    <tr>
      <td>Cervezas y sifones</td><td>Nacional</td>
      <td class="bg-blue">No existe</td><td class="bg-blue">48%*</td>
      <td class="bg-grey">No existe</td><td class="bg-grey">48%*</td>
      <td class="text-red">$330 por grado</td><td class="text-red">10%</td>
    </tr>
    <tr>
      <td>Cervezas y sifones</td><td>Extranjero</td>
      <td class="bg-blue">No existe</td><td class="bg-blue">48%*</td>
      <td class="bg-grey">No existe</td><td class="bg-grey">48%*</td>
      <td class="text-red">$330 por grado</td><td class="text-red">10%</td>
    </tr>
    <tr>
      <td>Refajos y mezclas</td><td>Nacional y ext.</td>
      <td class="bg-blue">No existe</td><td class="bg-blue">20%*</td>
      <td class="bg-grey">No existe</td><td class="bg-grey">20%*</td>
      <td class="text-red">$330 por grado</td><td class="text-red">10%</td>
    </tr>
    <tr>
      <td>Cigarrillos</td><td>Nacional y ext.</td>
      <td class="bg-blue">$4.446 por 20 un.</td><td class="bg-blue">10%</td>
      <td class="bg-grey">$4.846 por 20 un.</td><td class="bg-grey">10%</td>
      <td class="text-red">$7.823 por 20 un.</td><td class="text-red">10%</td>
    </tr>
  </tbody>
</table>
"""
st.markdown(html_tabla, unsafe_allow_html=True)
st.caption("En licores y vinos, el componente específico se calcula por grado alcoholimétrico en 750 ml o su equivalente. *En cervezas y refajos, la nueva tarifa específica se calcula por grado alcoholimétrico en 330 ml o su equivalente. En cigarrillos, el específico propuesto aumenta a $11.200 por cajetilla desde 2028.")
