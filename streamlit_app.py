import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------
# Configuración de la página
# ---------------------------------------------------------
st.set_page_config(page_title="Impacto Tributario", layout="wide")

COLOR_BASE_AZUL = '#1c2045'  # Azul Marino Oscuro (Legislación Actual)
COLOR_BASE_ARENA = '#deb173' # Arena / Mostaza (PL Rescate)
COLOR_TEXTO_ARENA = '#a67d3e' # Tono mostaza para legibilidad en texto

# ---------------------------------------------------------
# FORZAR MODO BLANCO Y ELIMINAR MENÚ DE COLOR (SOLO CÓDIGO)
# ---------------------------------------------------------
st.markdown(f"""
<style>
    /* 1. Ocultar menú de 3 puntos, selector de temas y encabezado de Streamlit */
    #MainMenu {{visibility: hidden !important; display: none !important;}}
    header {{visibility: hidden !important; display: none !important;}}
    footer {{visibility: hidden !important; display: none !important;}}
    [data-testid="stToolbar"] {{visibility: hidden !important; display: none !important;}}
    [data-testid="stHeader"] {{background-color: transparent !important; display: none !important;}}
    
    /* 2. Forzar fondo blanco y texto oscuro en toda la pantalla */
    html, body, .stApp, [data-testid="stAppViewContainer"] {{
        background-color: #FFFFFF !important;
        color: {COLOR_BASE_AZUL} !important;
    }}
    
    /* 3. Forzar sidebar en fondo claro y texto oscuro */
    section[data-testid="stSidebar"] {{
        background-color: #F8F9FA !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {COLOR_BASE_AZUL} !important;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. Carga de Datos (Sin caché para lectura en tiempo real)
# ---------------------------------------------------------
def load_data():
    return pd.read_excel("Base_Datos_Tributaria_Licores.xlsx")

df = load_data()

# ---------------------------------------------------------
# 2. Panel Lateral (Sidebar)
# ---------------------------------------------------------
st.sidebar.markdown(f"<h3 style='color: {COLOR_BASE_AZUL};'>Filtros de Análisis</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border: 1px solid #e0e0e0; margin-top: 0px;'>", unsafe_allow_html=True)

opciones_producto = ["Todos los productos"] + df['Categoría'].tolist()
seleccion_prod = st.sidebar.selectbox("Seleccione el Producto:", opciones_producto)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("### Configuración del Modelo")
st.sidebar.checkbox("Mantener precios base constantes (2027)", value=True, disabled=True)
st.sidebar.checkbox("Traslado 100% al consumidor", value=True, disabled=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.caption("**Nota general:** Los resultados corresponden a un ejercicio ilustrativo para productos seleccionados y no constituyen estimaciones representativas del mercado nacional de bebidas alcohólicas.")

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. HTML de la Tabla de Tarifas (Definición)
# ---------------------------------------------------------
html_tabla = f"""
<style>
.tg {{border-collapse:collapse; border-spacing:0; width:100%; text-align:center; font-family:sans-serif; font-size: 12px; margin-bottom: 10px;}}
.tg th {{border:1px solid #e0e0e0; padding:6px; font-weight:bold;}}
.tg td {{border:1px solid #e0e0e0; padding:5px;}}
.bg-actual {{background-color:{COLOR_BASE_AZUL}; color:white;}}
.bg-grey {{background-color:#e6e6e6; color:{COLOR_BASE_AZUL};}}
.bg-pl {{background-color:#fcf9f2; color:{COLOR_BASE_AZUL};}}
.text-pl {{color:{COLOR_TEXTO_ARENA}; font-weight:bold;}}
</style>
<table class="tg">
  <thead>
    <tr>
      <th rowspan="2" style="background-color:white; color:{COLOR_BASE_AZUL}; border: none;">Producto</th>
      <th colspan="2" class="bg-actual">Legislación actual</th>
      <th colspan="2" class="bg-grey">Legislación 2027</th>
      <th colspan="2" class="bg-pl">PL rescate</th>
    </tr>
    <tr>
      <th class="bg-actual">Esp. 2026</th>
      <th class="bg-actual">Ad val.</th>
      <th class="bg-grey">Esp. 2027</th>
      <th class="bg-grey">Ad val.</th>
      <th class="bg-pl">Esp. 2027</th>
      <th class="bg-pl">Ad val.</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="color: {COLOR_BASE_AZUL}; font-weight: bold;">Licores</td>
      <td class="bg-actual">$360/gr</td><td class="bg-actual">25%</td>
      <td class="bg-grey">$378/gr</td><td class="bg-grey">25%</td>
      <td class="text-pl">$750/gr</td><td class="text-pl">35%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_BASE_AZUL}; font-weight: bold;">Vinos</td>
      <td class="bg-actual">$243/gr</td><td class="bg-actual">20%</td>
      <td class="bg-grey">$255/gr</td><td class="bg-grey">20%</td>
      <td class="text-pl">$750/gr</td><td class="text-pl">35%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_BASE_AZUL}; font-weight: bold;">Cervezas</td>
      <td class="bg-actual">N/A</td><td class="bg-actual">48%*</td>
      <td class="bg-grey">N/A</td><td class="bg-grey">48%*</td>
      <td class="text-pl">$330/gr</td><td class="text-pl">10%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_BASE_AZUL}; font-weight: bold;">Refajos</td>
      <td class="bg-actual">N/A</td><td class="bg-actual">20%*</td>
      <td class="bg-grey">N/A</td><td class="bg-grey">20%*</td>
      <td class="text-pl">$330/gr</td><td class="text-pl">10%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_BASE_AZUL}; font-weight: bold;">Cigarrillos</td>
      <td class="bg-actual">$4.446/20u</td><td class="bg-actual">10%</td>
      <td class="bg-grey">$4.846/20u</td><td class="bg-grey">10%</td>
      <td class="text-pl">$7.823/20u</td><td class="text-pl">10%</td>
    </tr>
  </tbody>
</table>
"""

# ---------------------------------------------------------
# 4. Área Principal (Dashboard)
# ---------------------------------------------------------
st.markdown(f"<h2 style='color: {COLOR_BASE_AZUL};'>Impacto del Proyecto de Ley de Rescate Económico en Bebidas</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #e0e0e0; margin-top: -10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

if seleccion_prod != "Todos los productos":
    df_plot = df[df['Categoría'] == seleccion_prod]
else:
    df_plot = df.copy()

col1, col2, col3 = st.columns([2.5, 2.5, 0.5], gap="large")

# --- GRÁFICO 1: PRESIÓN FISCAL ---
with col1:
    st.markdown(f"<h4 style='color: {COLOR_BASE_AZUL};'>1. Presión Fiscal (%)</h4>", unsafe_allow_html=True)
    fig_presion = go.Figure()
    fig_presion.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['Actual_Presion_Fiscal'],
        name='Actual', marker_color=COLOR_BASE_AZUL,
        text=[f"{x:.0%}" for x in df_plot['Actual_Presion_Fiscal']], textposition='outside'
    ))
    fig_presion.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['PL_Presion_Fiscal'],
        name='PL Rescate', marker_color=COLOR_BASE_ARENA,
        text=[f"{x:.0%}" for x in df_plot['PL_Presion_Fiscal']], textposition='outside', textfont=dict(weight='bold')
    ))
    fig_presion.update_layout(
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(t=20, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=COLOR_BASE_AZUL)),
        yaxis=dict(tickformat='.0%', showgrid=True, gridcolor='#E5E5E5', tickfont=dict(color=COLOR_BASE_AZUL), range=[0, max(df['PL_Presion_Fiscal'])*1.2]),
        xaxis=dict(tickfont=dict(color=COLOR_BASE_AZUL))
    )
    st.plotly_chart(fig_presion, use_container_width=True)
    st.caption("**Nota:** Representa la participación de los impuestos en el precio final al consumidor. Se seleccionó una sola marca por categoría, por lo que los resultados son ilustrativos y no representan la presión fiscal de todos los productos, dada la diversidad de marcas, precios, presentaciones y grados alcoholimétricos.")

# --- GRÁFICO 2: TOTAL IMPUESTOS ---
with col2:
    st.markdown(f"<h4 style='color: {COLOR_BASE_AZUL};'>2. Total de Impuestos por Botella</h4>", unsafe_allow_html=True)
    fig_impuestos = go.Figure()
    fig_impuestos.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['Actual_Total_Impuestos'],
        name='Actual', marker_color=COLOR_BASE_AZUL,
        text=[f"${x:,.0f}".replace(',', '.') for x in df_plot['Actual_Total_Impuestos']], textposition='outside'
    ))
    fig_impuestos.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['PL_Total_Impuestos'],
        name='PL Rescate', marker_color=COLOR_BASE_ARENA,
        text=[f"${x:,.0f}".replace(',', '.') for x in df_plot['PL_Total_Impuestos']], textposition='outside', textfont=dict(weight='bold')
    ))
    fig_impuestos.update_layout(
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(t=20, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=COLOR_BASE_AZUL)),
        yaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False, range=[0, max(df['PL_Total_Impuestos'])*1.2]),
        xaxis=dict(tickfont=dict(color=COLOR_BASE_AZUL))
    )
    st.plotly_chart(fig_impuestos, use_container_width=True)
    st.caption("**Nota:** Incluye el impuesto al consumo y el IVA. En licores, vinos y aperitivos, el proyecto contempla un aumento del IVA del 5 % al 19 %. En cervezas, la legislación vigente aplica un impuesto del 48 % sobre el precio de venta al detallista, mientras que el proyecto establece un componente específico y un ad valorem del 10 % sobre el precio de venta al público sin impuestos, certificado por el DANE.")

# Separador
st.markdown("<br>", unsafe_allow_html=True)
col4, col5, col6 = st.columns([2.5, 2.5, 0.5], gap="large")

# --- GRÁFICO 3: PRECIO DE VENTA FINAL ---
with col4:
    st.markdown(f"<h4 style='color: {COLOR_BASE_AZUL};'>3. Precio de Venta Final</h4>", unsafe_allow_html=True)
    fig_precio = go.Figure()
    fig_precio.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['Actual_Precio_Final'],
        name='Actual', marker_color=COLOR_BASE_AZUL,
        text=[f"${x:,.0f}".replace(',', '.') for x in df_plot['Actual_Precio_Final']], textposition='outside'
    ))
    fig_precio.add_trace(go.Bar(
        x=df_plot['Categoría'], y=df_plot['PL_Precio_Final'],
        name='PL Rescate', marker_color=COLOR_BASE_ARENA,
        text=[f"${x:,.0f}".replace(',', '.') for x in df_plot['PL_Precio_Final']], textposition='outside', textfont=dict(weight='bold')
    ))
    fig_precio.update_layout(
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(t=20, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=COLOR_BASE_AZUL)),
        yaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False, range=[0, max(df['PL_Precio_Final'])*1.2]),
        xaxis=dict(tickfont=dict(color=COLOR_BASE_AZUL))
    )
    st.plotly_chart(fig_precio, use_container_width=True)
    st.caption("**Nota:** Se proyecta un incremento del 5 % en los precios antes de impuestos para 2027. Se supone que los precios base permanecen constantes entre escenarios y que el 100 % del incremento tributario se traslada al consumidor, sin considerar cambios en los márgenes de comercialización ni en la demanda.")

# --- GRÁFICO 4: CASCADAS COMPARATIVAS O TABLA DE TARIFAS ---
with col5:
    if seleccion_prod != "Todos los productos":
        st.markdown(f"<h4 style='color: {COLOR_BASE_AZUL};'>4. Composición del Precio</h4>", unsafe_allow_html=True)
        prod_data = df_plot.iloc[0]
        
        tab1, tab2 = st.tabs(["Legislación Actual", "PL Rescate Económico"])
        
        with tab1:
            fig_wf_act = go.Figure(go.Waterfall(
                name="Actual", orientation="v", measure=["relative"]*4 + ["total"],
                x=["Base", "Ad Val.", "Espec.", "IVA", "Final"],
                y=[prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']],
                textposition="outside", text=[f"${x:,.0f}".replace(',','.') for x in [prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']]],
                connector={"line": {"color": "#e0e0e0"}}, decreasing={"marker": {"color": COLOR_BASE_AZUL}}, increasing={"marker": {"color": COLOR_BASE_AZUL}}, totals={"marker": {"color": COLOR_BASE_AZUL}}
            ))
            fig_wf_act.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                height=250, margin=dict(t=20, b=0, l=0, r=0),
                yaxis=dict(showticklabels=False), xaxis=dict(tickfont=dict(color=COLOR_BASE_AZUL))
            )
            st.plotly_chart(fig_wf_act, use_container_width=True)
            
        with tab2:
            fig_wf_pl = go.Figure(go.Waterfall(
                name="PL Rescate", orientation="v", measure=["relative"]*4 + ["total"],
                x=["Base", "Ad Val.", "Espec.", "IVA", "Final"],
                y=[prod_data['Precio_Base_2027'], prod_data['PL_AdValorem_Valor'], prod_data['PL_Especifico_Valor'], prod_data['PL_IVA_Valor'], prod_data['PL_Precio_Final']],
                textposition="outside", text=[f"${x:,.0f}".replace(',','.') for x in [prod_data['Precio_Base_2027'], prod_data['PL_AdValorem_Valor'], prod_data['PL_Especifico_Valor'], prod_data['PL_IVA_Valor'], prod_data['PL_Precio_Final']]],
                connector={"line": {"color": "#e0e0e0"}}, decreasing={"marker": {"color": COLOR_BASE_AZUL}}, increasing={"marker": {"color": COLOR_BASE_AZUL}}, totals={"marker": {"color": COLOR_BASE_ARENA}}
            ))
            fig_wf_pl.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                height=250, margin=dict(t=20, b=0, l=0, r=0),
                yaxis=dict(showticklabels=False), xaxis=dict(tickfont=dict(color=COLOR_BASE_AZUL))
            )
            st.plotly_chart(fig_wf_pl, use_container_width=True)

    else:
        st.markdown(f"<h4 style='color: {COLOR_BASE_AZUL};'>4. Tabla Resumen de Tarifas</h4>", unsafe_allow_html=True)
        st.markdown(html_tabla, unsafe_allow_html=True)
        st.caption("**Nota:** Se comparan las tarifas vigentes en 2026, su proyección para 2027 y las propuestas en el PL de Rescate Económico. Para 2027 se supone un IPC del 5 % y, en cigarrillos, una actualización del IPC más cuatro puntos porcentuales. Las tarifas específicas se expresan por grado alcoholimétrico y 750 ml para licores y vinos, por grado y 330 ml para cervezas y refajos, y por cajetilla de 20 unidades para cigarrillos. El proyecto propone aumentar la tarifa de estos últimos a $11.200 en 2028.")
