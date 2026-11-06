import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------
# Configuración de la página y colores
# ---------------------------------------------------------
st.set_page_config(page_title="Impacto Tributario", layout="wide")

# Colores institucionales
COLOR_ACTUAL = '#131d36'  # Azul Marino
COLOR_PL = '#bb4029'      # Rojo Óxido

# ---------------------------------------------------------
# 1. Carga de Datos
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("Base_Datos_Tributaria_Licores.xlsx")

df = load_data()

# ---------------------------------------------------------
# 2. Panel Lateral (Sidebar) - Filtros
# ---------------------------------------------------------
st.sidebar.markdown(f"<h3 style='color: {COLOR_ACTUAL};'>Filtros de Análisis</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border: 1px solid #e0e0e0; margin-top: 0px;'>", unsafe_allow_html=True)

# Filtro principal de producto
opciones_producto = ["Todos los productos"] + df['Categoría'].tolist()
seleccion_prod = st.sidebar.selectbox("Seleccione el Producto:", opciones_producto)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("### Configuración del Modelo")
# Checkboxes simulando los filtros de la imagen de referencia (solo visuales/informativos para el contexto)
st.sidebar.checkbox("Mantener precios base constantes (2027)", value=True, disabled=True)
st.sidebar.checkbox("Traslado 100% al consumidor", value=True, disabled=True)
st.sidebar.checkbox("IVA constante al 19%", value=True, disabled=True)

st.sidebar.markdown("<br><hr>", unsafe_allow_html=True)
st.sidebar.caption("Para estimar el impacto de las modificaciones tributarias, se parte de los precios de venta de 2026, los cuales se incrementan un 5% para 2027. Se asume que el incremento se traslada completamente al consumidor sin cambios en la demanda.")

# ---------------------------------------------------------
# 3. Área Principal (Dashboard)
# ---------------------------------------------------------
st.markdown(f"<h2 style='color: {COLOR_ACTUAL};'>Impacto del Proyecto de Ley de Rescate Económico en Bebidas</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #e0e0e0; margin-top: -10px; margin-bottom: 30px;'>", unsafe_allow_html=True)

# Filtrar datos según selección
if seleccion_prod != "Todos los productos":
    df_plot = df[df['Categoría'] == seleccion_prod]
else:
    df_plot = df.copy()

# Cuadrícula de 2 columnas para los gráficos (estilo referencia)
row1_col1, row1_col2 = st.columns(2)
st.markdown("<br>", unsafe_allow_html=True)
row2_col1, row2_col2 = st.columns(2)

# --- GRÁFICO 1: PRESIÓN FISCAL (AHORA EN BARRAS) ---
with row1_col1:
    st.markdown(f"<h4 style='color: {COLOR_ACTUAL};'>1. Presión Fiscal (%)</h4>", unsafe_allow_html=True)
    fig_presion = go.Figure()
    fig_presion.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['Actual_Presion_Fiscal'],
        name='Actual', marker_color=COLOR_ACTUAL,
        text=[f"{x:.0%}" for x in df_plot['Actual_Presion_Fiscal']], textposition='outside'
    ))
    fig_presion.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['PL_Presion_Fiscal'],
        name='PL Rescate', marker_color=COLOR_PL,
        text=[f"{x:.0%}" for x in df_plot['PL_Presion_Fiscal']], textposition='outside',
        textfont=dict(weight='bold')
    ))
    fig_presion.update_layout(
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', height=320, margin=dict(t=10, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(tickformat='.0%', showgrid=True, gridcolor='#E5E5E5', range=[0, max(df['PL_Presion_Fiscal'])*1.2])
    )
    st.plotly_chart(fig_presion, use_container_width=True)

# --- GRÁFICO 2: TOTAL IMPUESTOS ---
with row1_col2:
    st.markdown(f"<h4 style='color: {COLOR_ACTUAL};'>2. Total de Impuestos por Botella</h4>", unsafe_allow_html=True)
    fig_impuestos = go.Figure()
    fig_impuestos.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['Actual_Total_Impuestos'],
        name='Actual', marker_color=COLOR_ACTUAL,
        text=[f"${x:,.0f}".replace(',', '.') for x in df_plot['Actual_Total_Impuestos']], textposition='outside'
    ))
    fig_impuestos.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['PL_Total_Impuestos'],
        name='PL Rescate', marker_color=COLOR_PL,
        text=[f"${x:,.0f}".replace(',', '.') for x in df_plot['PL_Total_Impuestos']], textposition='outside',
        textfont=dict(weight='bold')
    ))
    fig_impuestos.update_layout(
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', height=320, margin=dict(t=10, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False, range=[0, max(df['PL_Total_Impuestos'])*1.2])
    )
    st.plotly_chart(fig_impuestos, use_container_width=True)

# --- GRÁFICO 3: PRECIO DE VENTA FINAL ---
with row2_col1:
    st.markdown(f"<h4 style='color: {COLOR_ACTUAL};'>3. Precio de Venta Final</h4>", unsafe_allow_html=True)
    fig_precio = go.Figure()
    fig_precio.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['Actual_Precio_Final'],
        name='Actual', marker_color=COLOR_ACTUAL,
        text=[f"${x:,.0f}".replace(',', '.') for x in df_plot['Actual_Precio_Final']], textposition='outside'
    ))
    fig_precio.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['PL_Precio_Final'],
        name='PL Rescate', marker_color=COLOR_PL,
        text=[f"${x:,.0f}".replace(',', '.') for x in df_plot['PL_Precio_Final']], textposition='outside',
        textfont=dict(weight='bold')
    ))
    fig_precio.update_layout(
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', height=320, margin=dict(t=10, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False, range=[0, max(df['PL_Precio_Final'])*1.2])
    )
    st.plotly_chart(fig_precio, use_container_width=True)

# --- GRÁFICO 4: CASCADA (Solo si se selecciona un producto) o ESPACIO EN BLANCO ---
with row2_col2:
    if seleccion_prod != "Todos los productos":
        st.markdown(f"<h4 style='color: {COLOR_ACTUAL};'>4. Composición del Precio (Actual)</h4>", unsafe_allow_html=True)
        prod_data = df_plot.iloc[0]
        fig_wf = go.Figure(go.Waterfall(
            name="Actual", orientation="v", measure=["relative"]*4 + ["total"],
            x=["Base", "Ad Val.", "Espec.", "IVA", "Final"],
            y=[prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']],
            textposition="outside", text=[f"${x:,.0f}".replace(',','.') for x in [prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']]],
            connector={"line": {"color": "#e0e0e0"}}, decreasing={"marker": {"color": COLOR_ACTUAL}}, increasing={"marker": {"color": COLOR_ACTUAL}}, totals={"marker": {"color": COLOR_PL}}
        ))
        fig_wf.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=320, margin=dict(t=10, b=0, l=0, r=0))
        st.plotly_chart(fig_wf, use_container_width=True)
    else:
        # Tarjetas resumen de incremento promedio
        st.markdown(f"<h4 style='color: {COLOR_ACTUAL};'>4. Resumen de Incrementos</h4>", unsafe_allow_html=True)
        promedio_impuestos = (df['PL_Total_Impuestos'] - df['Actual_Total_Impuestos']).mean()
        promedio_precio = (df['PL_Precio_Final'] - df['Actual_Precio_Final']).mean()
        
        st.markdown(f"""
        <div style="border: 1px solid #e5e5e5; border-radius: 8px; padding: 20px; background-color: white; height: 320px; display: flex; flex-direction: column; justify-content: center; gap: 20px;">
            <div>
                <div style="color: {COLOR_ACTUAL}; font-size: 16px;">Incremento Promedio Impuestos:</div>
                <div style="color: {COLOR_PL}; font-size: 28px; font-weight: bold;">+${promedio_impuestos:,.0f}</div>
            </div>
            <div>
                <div style="color: {COLOR_ACTUAL}; font-size: 16px;">Incremento Promedio Precio Final:</div>
                <div style="color: {COLOR_PL}; font-size: 28px; font-weight: bold;">+${promedio_precio:,.0f}</div>
            </div>
        </div>
        """.replace(',', '.'), unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. Tabla de Tarifas Estática
# ---------------------------------------------------------
st.markdown("<br><hr style='border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color: {COLOR_ACTUAL};'>📋 Tabla Resumen de Tarifas</h3>", unsafe_allow_html=True)

html_tabla = f"""
<style>
.tg {{border-collapse:collapse; border-spacing:0; width:100%; text-align:center; font-family:sans-serif; font-size: 14px;}}
.tg th {{border:1px solid #e0e0e0; padding:10px; font-weight:bold;}}
.tg td {{border:1px solid #e0e0e0; padding:8px;}}
.bg-blue {{background-color:{COLOR_ACTUAL}; color:white;}}
.bg-grey {{background-color:#f4f4f4; color:{COLOR_ACTUAL};}}
.bg-red {{background-color:#fef5f4; color:{COLOR_PL};}}
.text-red {{color:{COLOR_PL}; font-weight:bold;}}
</style>
<table class="tg">
  <thead>
    <tr>
      <th rowspan="2" style="background-color:white; color:{COLOR_ACTUAL}; border: none;">Producto</th>
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
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Licores y aperitivos</td>
      <td class="bg-blue">$360 por grado</td><td class="bg-blue">25%</td>
      <td class="bg-grey">$378 por grado</td><td class="bg-grey">25%</td>
      <td class="text-red">$750 por grado</td><td class="text-red">35%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Vinos y aperitivos vínicos</td>
      <td class="bg-blue">$243 por grado</td><td class="bg-blue">20%</td>
      <td class="bg-grey">$255 por grado</td><td class="bg-grey">20%</td>
      <td class="text-red">$750 por grado</td><td class="text-red">35%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Cervezas y sifones</td>
      <td class="bg-blue">No existe</td><td class="bg-blue">48%*</td>
      <td class="bg-grey">No existe</td><td class="bg-grey">48%*</td>
      <td class="text-red">$330 por grado</td><td class="text-red">10%</td>
    </tr>
  </tbody>
</table>
"""
st.markdown(html_tabla, unsafe_allow_html=True)
st.caption("En licores y vinos, el componente específico se calcula por grado alcoholimétrico en 750 ml o su equivalente. *En cervezas y refajos, la nueva tarifa específica se calcula por grado alcoholimétrico en 330 ml o su equivalente.")
