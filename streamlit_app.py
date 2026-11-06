import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------
# Configuración de la página y colores (Opción 2)
# ---------------------------------------------------------
st.set_page_config(page_title="Impacto Tributario", layout="wide")

COLOR_ACTUAL = '#143642'  # Verde Bosque Oscuro / Gris Verdoso
COLOR_PL = '#e67e22'      # Naranja Quemado / Ámbar

# ---------------------------------------------------------
# 1. Carga de Datos
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("Base_Datos_Tributaria_Licores.xlsx")

df = load_data()

# ---------------------------------------------------------
# 2. Panel Lateral (Sidebar) - Filtros y Notas
# ---------------------------------------------------------
st.sidebar.markdown(f"<h3 style='color: {COLOR_ACTUAL};'>Filtros de Análisis</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border: 1px solid #e0e0e0; margin-top: 0px;'>", unsafe_allow_html=True)

opciones_producto = ["Todos los productos"] + df['Categoría'].tolist()
seleccion_prod = st.sidebar.selectbox("Seleccione el Producto:", opciones_producto)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("### Configuración del Modelo")
st.sidebar.checkbox("Mantener precios base constantes (2027)", value=True, disabled=True)
st.sidebar.checkbox("Traslado 100% al consumidor", value=True, disabled=True)
st.sidebar.checkbox("IVA constante al 19%", value=True, disabled=True)

st.sidebar.markdown("<br><hr>", unsafe_allow_html=True)

# Supuestos del Modelo en Bullets 
with st.sidebar.expander("Metodología y Supuestos", expanded=False):
    st.markdown("""
    **Parámetros Base:**
    * Partimos de precios de venta de 2026 (sin impoconsumo ni IVA).
    * Se incrementan un 5% para proyectar la base de 2027.
    * Se asume que estos precios base permanecen constantes.
    
    **Impacto y Traslado:**
    * Los incrementos tributarios se trasladan 100% al consumidor.
    * No se consideran cambios en demanda, márgenes o características.
    
    **Cálculo de Licores y Vinos:**
    * El impoconsumo integra los componentes específico y ad valorem de cada escenario.
    
    **Cálculo de Cervezas:**
    * **Actual:** 48% sobre precio al detallista (sin específico).
    * **PL Propuesto:** Específico de $330 por grado/330ml + 10% ad valorem sobre precio DANE (sin impuestos).
    
    **Constantes y Resultados:**
    * El IVA se mantiene constante en 19%.
    * **Precio Final:** Precio Base + Total Impuestos.
    * **Presión Fiscal:** Participación del Total de Impuestos sobre el Precio Final.
    """)

# ---------------------------------------------------------
# 3. Área Principal (Dashboard)
# ---------------------------------------------------------
st.markdown(f"<h2 style='color: {COLOR_ACTUAL};'>Impacto del Proyecto de Ley de Rescate Económico en Bebidas</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #e0e0e0; margin-top: -10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

if seleccion_prod != "Todos los productos":
    df_plot = df[df['Categoría'] == seleccion_prod]
else:
    df_plot = df.copy()

# Cuadrícula con 3 columnas (la última vacía para dar margen derecho)
col1, col2, col3 = st.columns([2.5, 2.5, 0.5], gap="large")

# --- GRÁFICO 1: PRESIÓN FISCAL ---
with col1:
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
        text=[f"{x:.0%}" for x in df_plot['PL_Presion_Fiscal']], textposition='outside', textfont=dict(weight='bold')
    ))
    fig_presion.update_layout(
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(t=20, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(tickformat='.0%', showgrid=True, gridcolor='#E5E5E5', range=[0, max(df['PL_Presion_Fiscal'])*1.2])
    )
    st.plotly_chart(fig_presion, use_container_width=True)
    st.caption("📌 **Nota:** Representa el porcentaje del precio de venta final que corresponde a la carga tributaria total.")

# --- GRÁFICO 2: TOTAL IMPUESTOS ---
with col2:
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
        text=[f"${x:,.0f}".replace(',', '.') for x in df_plot['PL_Total_Impuestos']], textposition='outside', textfont=dict(weight='bold')
    ))
    fig_impuestos.update_layout(
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(t=20, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False, range=[0, max(df['PL_Total_Impuestos'])*1.2])
    )
    st.plotly_chart(fig_impuestos, use_container_width=True)
    st.caption("📌 **Nota:** Suma de los componentes específico, ad valorem e IVA aplicable a cada presentación en pesos.")

# Separador
st.markdown("<br>", unsafe_allow_html=True)
col4, col5, col6 = st.columns([2.5, 2.5, 0.5], gap="large")

# --- GRÁFICO 3: PRECIO DE VENTA FINAL ---
with col4:
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
        text=[f"${x:,.0f}".replace(',', '.') for x in df_plot['PL_Precio_Final']], textposition='outside', textfont=dict(weight='bold')
    ))
    fig_precio.update_layout(
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(t=20, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False, range=[0, max(df['PL_Precio_Final'])*1.2])
    )
    st.plotly_chart(fig_precio, use_container_width=True)
    st.caption("📌 **Nota:** Precio de venta estimado al consumidor asumiendo el traslado completo del 100% de los incrementos tributarios.")

# --- GRÁFICO 4: CASCADAS COMPARATIVAS ---
with col5:
    if seleccion_prod != "Todos los productos":
        st.markdown(f"<h4 style='color: {COLOR_ACTUAL};'>4. Composición del Precio</h4>", unsafe_allow_html=True)
        prod_data = df_plot.iloc[0]
        
        tab1, tab2 = st.tabs(["Legislación Actual", "PL Rescate Económico"])
        
        with tab1:
            fig_wf_act = go.Figure(go.Waterfall(
                name="Actual", orientation="v", measure=["relative"]*4 + ["total"],
                x=["Base", "Ad Val.", "Espec.", "IVA", "Final"],
                y=[prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']],
                textposition="outside", text=[f"${x:,.0f}".replace(',','.') for x in [prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']]],
                connector={"line": {"color": "#e0e0e0"}}, decreasing={"marker": {"color": COLOR_ACTUAL}}, increasing={"marker": {"color": COLOR_ACTUAL}}, totals={"marker": {"color": COLOR_ACTUAL}}
            ))
            fig_wf_act.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(t=20, b=0, l=0, r=0), yaxis=dict(showticklabels=False))
            st.plotly_chart(fig_wf_act, use_container_width=True)
            
        with tab2:
            fig_wf_pl = go.Figure(go.Waterfall(
                name="PL Rescate", orientation="v", measure=["relative"]*4 + ["total"],
                x=["Base", "Ad Val.", "Espec.", "IVA", "Final"],
                y=[prod_data['Precio_Base_2027'], prod_data['PL_AdValorem_Valor'], prod_data['PL_Especifico_Valor'], prod_data['PL_IVA_Valor'], prod_data['PL_Precio_Final']],
                textposition="outside", text=[f"${x:,.0f}".replace(',','.') for x in [prod_data['Precio_Base_2027'], prod_data['PL_AdValorem_Valor'], prod_data['PL_Especifico_Valor'], prod_data['PL_IVA_Valor'], prod_data['PL_Precio_Final']]],
                connector={"line": {"color": "#e0e0e0"}}, decreasing={"marker": {"color": COLOR_ACTUAL}}, increasing={"marker": {"color": COLOR_ACTUAL}}, totals={"marker": {"color": COLOR_PL}}
            ))
            fig_wf_pl.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(t=20, b=0, l=0, r=0), yaxis=dict(showticklabels=False))
            st.plotly_chart(fig_wf_pl, use_container_width=True)
            
        st.caption("📌 **Nota:** Desglose escalonado de cómo interactúan los componentes tributarios sobre el precio base para conformar el valor final.")

    else:
        st.markdown(f"<h4 style='color: {COLOR_ACTUAL};'>4. Resumen de Incrementos</h4>", unsafe_allow_html=True)
        promedio_impuestos = (df['PL_Total_Impuestos'] - df['Actual_Total_Impuestos']).mean()
        promedio_precio = (df['PL_Precio_Final'] - df['Actual_Precio_Final']).mean()
        st.markdown(f"""
        <div style="border: 1px solid #e5e5e5; border-radius: 8px; padding: 20px; background-color: white; height: 300px; display: flex; flex-direction: column; justify-content: center; gap: 20px;">
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
        st.caption("📌 **Nota:** Aumento promedio absoluto del mercado en impuestos y precio final (calculado sobre el mix de productos evaluado).")

# ---------------------------------------------------------
# 4. Tabla de Tarifas Estática
# ---------------------------------------------------------
st.markdown("<br><br><hr style='border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)

html_tabla = f"""
<style>
.tg {{border-collapse:collapse; border-spacing:0; width:100%; text-align:center; font-family:sans-serif; font-size: 14px; margin-bottom: 10px;}}
.tg th {{border:1px solid #e0e0e0; padding:10px; font-weight:bold;}}
.tg td {{border:1px solid #e0e0e0; padding:8px;}}
.bg-actual {{background-color:{COLOR_ACTUAL}; color:white;}}
.bg-grey {{background-color:#e6e6e6; color:{COLOR_ACTUAL};}}
.bg-pl {{background-color:#fcf3eb; color:{COLOR_PL};}}
.text-pl {{color:{COLOR_PL}; font-weight:bold;}}
</style>
<table class="tg">
  <thead>
    <tr>
      <th rowspan="2" style="background-color:white; color:{COLOR_ACTUAL}; border: none;">Producto</th>
      <th colspan="2" class="bg-actual">Legislación actual</th>
      <th colspan="2" class="bg-grey">legislacion actual en 2027</th>
      <th colspan="2" class="bg-pl">PL rescate</th>
    </tr>
    <tr>
      <th class="bg-actual">Específico vigente 2026</th>
      <th class="bg-actual">Ad valorem vigente 2026</th>
      <th class="bg-grey">Específico vigente 2027</th>
      <th class="bg-grey">Ad valorem vigente 2027</th>
      <th class="bg-pl">Específico reforma 2027</th>
      <th class="bg-pl">Ad valorem reforma 2027</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Licores y aperitivos</td>
      <td class="bg-actual">$360 por grado</td><td class="bg-actual">25%</td>
      <td class="bg-grey">$378 por grado</td><td class="bg-grey">25%</td>
      <td class="text-pl">$750 por grado</td><td class="text-pl">35%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Vinos y aperitivos vínicos</td>
      <td class="bg-actual">$243 por grado</td><td class="bg-actual">20%</td>
      <td class="bg-grey">$255 por grado</td><td class="bg-grey">20%</td>
      <td class="text-pl">$750 por grado</td><td class="text-pl">35%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Cervezas y sifones</td>
      <td class="bg-actual">No existe</td><td class="bg-actual">48%*</td>
      <td class="bg-grey">No existe</td><td class="bg-grey">48%*</td>
      <td class="text-pl">$330 por grado</td><td class="text-pl">10%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Refajos y mezclas</td>
      <td class="bg-actual">No existe</td><td class="bg-actual">20%*</td>
      <td class="bg-grey">No existe</td><td class="bg-grey">20%*</td>
      <td class="text-pl">$330 por grado</td><td class="text-pl">10%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Cigarrillos</td>
      <td class="bg-actual">$4.446 por 20 unidades</td><td class="bg-actual">10%</td>
      <td class="bg-grey">$4.846 por 20 unidades</td><td class="bg-grey">10%</td>
      <td class="text-pl">$7.823 por 20 unidades</td><td class="text-pl">10%</td>
    </tr>
  </tbody>
</table>
"""
st.markdown(html_tabla, unsafe_allow_html=True)
st.caption("En licores y vinos, el componente específico se calcula por grado alcoholimétrico en 750 ml o su equivalente.<br>*En cervezas y refajos, la nueva tarifa específica se calcula por grado alcoholimétrico en 330 ml o su equivalente.<br>En cigarrillos, el específico propuesto aumenta a $11.200 por cajetilla desde 2028.", unsafe_allow_html=True)
