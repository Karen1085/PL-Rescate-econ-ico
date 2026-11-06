import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Impacto Tributario Licores", layout="wide")

# Colores extraídos del estilo FND-Datexco
COLOR_ACTUAL = '#131d36'  # Azul Marino Oscuro
COLOR_PL = '#bb4029'      # Rojo Óxido / Teja
COLOR_ACENTO = '#c99b53'  # Dorado / Mostaza

# 1. Carga de Datos de la Base de Excel
@st.cache_data
def load_data():
    return pd.read_excel("Base_Datos_Tributaria_Licores.xlsx")

df = load_data()

# 2. Encabezado y Menú Desplegable
st.markdown(f"<h1 style='color: {COLOR_ACTUAL};'>📊 Impacto del PL de Rescate Económico en Bebidas</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)

# Menú desplegable
opciones = ["Todos los productos"] + df['Categoría'].tolist()
seleccion = st.selectbox("Seleccione el nivel de análisis:", opciones)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# VISTA: TODOS LOS PRODUCTOS
# ==========================================
if seleccion == "Todos los productos":
    
    # --- GRÁFICO 1: PRESIÓN FISCAL ---
    st.markdown(f"<h3 style='color: {COLOR_ACTUAL};'>⚖️ 1. Presión Fiscal (% del precio que son impuestos)</h3>", unsafe_allow_html=True)
    fig_presion = go.Figure()
    
    for i, row in df.iterrows():
        # Línea conectora (Dumbbell - color dorado de acento)
        fig_presion.add_trace(go.Scatter(
            x=[row['Actual_Presion_Fiscal'], row['PL_Presion_Fiscal']],
            y=[row['Categoría'], row['Categoría']],
            mode='lines', line=dict(color=COLOR_ACENTO, width=3), showlegend=False
        ))
        # Punto Actual (Azul Marino)
        fig_presion.add_trace(go.Scatter(
            x=[row['Actual_Presion_Fiscal']], y=[row['Categoría']],
            mode='markers+text', marker=dict(color=COLOR_ACTUAL, size=14),
            text=[f"{row['Actual_Presion_Fiscal']:.0%}"], textposition='middle left',
            textfont=dict(color=COLOR_ACTUAL, weight='bold'),
            name='Legislación Actual' if i == 0 else "", showlegend=(i==0)
        ))
        # Punto PL (Rojo Óxido)
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
        yaxis=dict(showgrid=False, tickfont=dict(color=COLOR_ACTUAL, size=13, weight='bold')),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_presion, use_container_width=True)
    st.markdown("<hr style='border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)

    # --- GRÁFICO 2: TOTAL IMPUESTOS ---
    st.markdown(f"<h3 style='color: {COLOR_ACTUAL};'>💰 2. Total de Impuestos por Botella</h3>", unsafe_allow_html=True)
    col_graf, col_cards = st.columns([3, 1])
    
    with col_graf:
        fig_impuestos = go.Figure()
        fig_impuestos.add_trace(go.Bar(
            x=df['Categoría'], y=df['Actual_Total_Impuestos'],
            name='Legislación Actual', marker_color=COLOR_ACTUAL,
            text=[f"${x:,.0f}".replace(',', '.') for x in df['Actual_Total_Impuestos']],
            textposition='outside', textfont=dict(size=12, color=COLOR_ACTUAL)
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
            yaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False),
            xaxis=dict(tickfont=dict(color=COLOR_ACTUAL, weight='bold'))
        )
        st.plotly_chart(fig_impuestos, use_container_width=True)
        
    with col_cards:
        st.markdown("<br>", unsafe_allow_html=True)
        for i, row in df.iterrows():
            incremento = row['PL_Total_Impuestos'] - row['Actual_Total_Impuestos']
            # Tarjetas emulando el estilo limpio con borde y colores específicos
            st.markdown(f"""
            <div style="border: 1px solid #e5e5e5; border-radius: 8px; padding: 10px; margin-bottom: 10px; background-color: white;">
                <div style="color: {COLOR_ACTUAL}; font-weight: bold; font-size: 14px;">
                    <span style="background-color: {COLOR_ACENTO}; color: white; border-radius: 50%; padding: 2px 8px; margin-right: 5px;">{i+1}</span>
                    {row['Categoría']}
                </div>
                <div style="color: {COLOR_PL}; font-weight: bold; font-size: 15px; margin-top: 5px; text-align: right;">
                    +${incremento:,.0f}
                </div>
            </div>
            """.replace(',', '.'), unsafe_allow_html=True)
            
    st.markdown("<hr style='border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)

    # --- GRÁFICO 3: PRECIO DE VENTA FINAL ---
    st.markdown(f"<h3 style='color: {COLOR_ACTUAL};'>🏷️ 3. Precio de Venta Final al Consumidor</h3>", unsafe_allow_html=True)
    fig_precio = go.Figure()
    fig_precio.add_trace(go.Bar(
        y=df['Categoría'], x=df['Actual_Precio_Final'],
        name='Legislación Actual', orientation='h', marker_color=COLOR_ACTUAL,
        text=[f"${x:,.0f}".replace(',', '.') for x in df['Actual_Precio_Final']],
        textposition='inside', insidetextanchor='end', textfont=dict(color='white')
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
        xaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False),
        yaxis=dict(tickfont=dict(color=COLOR_ACTUAL, weight='bold'))
    )
    st.plotly_chart(fig_precio, use_container_width=True)

# ==========================================
# VISTA: PRODUCTO INDIVIDUAL
# ==========================================
else:
    prod_data = df[df['Categoría'] == seleccion].iloc[0]
    st.markdown(f"<h3 style='color: {COLOR_ACTUAL};'>DETALLE INTERACTIVO: {prod_data['Producto'].upper()}</h3>", unsafe_allow_html=True)
    
    delta_imp = prod_data['PL_Total_Impuestos'] - prod_data['Actual_Total_Impuestos']
    delta_pre = prod_data['PL_Precio_Final'] - prod_data['Actual_Precio_Final']
    delta_fis = prod_data['PL_Presion_Fiscal'] - prod_data['Actual_Presion_Fiscal']
    
    st.markdown(f"""
    <div style="display: flex; gap: 20px; margin-bottom: 20px;">
        <div style="flex: 1; border: 1px solid #e5e5e5; border-radius: 8px; padding: 20px; background-color: white;">
            <div style="color: {COLOR_ACTUAL}; font-size: 14px;">Total Impuestos (PL)</div>
            <div style="color: {COLOR_PL}; font-size: 24px; font-weight: bold;">${prod_data['PL_Total_Impuestos']:,.0f}</div>
            <div style="color: {COLOR_ACENTO}; font-size: 14px;">(+${delta_imp:,.0f})</div>
        </div>
        <div style="flex: 1; border: 1px solid #e5e5e5; border-radius: 8px; padding: 20px; background-color: white;">
            <div style="color: {COLOR_ACTUAL}; font-size: 14px;">Precio Final (PL)</div>
            <div style="color: {COLOR_PL}; font-size: 24px; font-weight: bold;">${prod_data['PL_Precio_Final']:,.0f}</div>
            <div style="color: {COLOR_ACENTO}; font-size: 14px;">(+${delta_pre:,.0f})</div>
        </div>
        <div style="flex: 1; border: 1px solid #e5e5e5; border-radius: 8px; padding: 20px; background-color: white;">
            <div style="color: {COLOR_ACTUAL}; font-size: 14px;">Presión Fiscal (PL)</div>
            <div style="color: {COLOR_PL}; font-size: 24px; font-weight: bold;">{prod_data['PL_Presion_Fiscal']:.0%}</div>
            <div style="color: {COLOR_ACENTO}; font-size: 14px;">(+{delta_fis:.0%} pt)</div>
        </div>
    </div>
    """.replace(',', '.'), unsafe_allow_html=True)

    fig_wf = go.Figure()
    fig_wf.add_trace(go.Waterfall(
        name="Actual", orientation="v", measure=["relative"]*4 + ["total"],
        x=["Base", "Ad Valorem", "Específico", "IVA", "Precio Final"],
        y=[prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']],
        textposition="outside", text=[f"${x:,.0f}".replace(',','.') for x in [prod_data['Precio_Base_2027'], prod_data['Actual_AdValorem_Valor'], prod_data['Actual_Especifico_Valor'], prod_data['Actual_IVA_Valor'], prod_data['Actual_Precio_Final']]],
        connector={"line": {"color": "#e0e0e0"}}, decreasing={"marker": {"color": COLOR_ACTUAL}}, increasing={"marker": {"color": COLOR_ACTUAL}}, totals={"marker": {"color": COLOR_PL}}
    ))
    fig_wf.update_layout(title=dict(text="Composición bajo Legislación Actual", font=dict(color=COLOR_ACTUAL)), plot_bgcolor='rgba(0,0,0,0)', height=350)
    st.plotly_chart(fig_wf, use_container_width=True)

# ==========================================
# TABLA DE TARIFAS ESTÁTICA
# ==========================================
st.markdown("<hr style='border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
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
      <th rowspan="2" style="background-color:white; color:{COLOR_ACTUAL}; border: none;">Origen</th>
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
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Licores y aperitivos</td><td style="color: {COLOR_ACTUAL};">Nacional</td>
      <td class="bg-blue">$360 por grado</td><td class="bg-blue">25%</td>
      <td class="bg-grey">$378 por grado</td><td class="bg-grey">25%</td>
      <td class="text-red">$750 por grado</td><td class="text-red">35%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Licores y aperitivos</td><td style="color: {COLOR_ACTUAL};">Extranjero</td>
      <td class="bg-blue">$360 por grado</td><td class="bg-blue">25%</td>
      <td class="bg-grey">$378 por grado</td><td class="bg-grey">25%</td>
      <td class="text-red">$750 por grado</td><td class="text-red">35%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Vinos y aperitivos vínicos</td><td style="color: {COLOR_ACTUAL};">Nacional</td>
      <td class="bg-blue">$243 por grado</td><td class="bg-blue">20%</td>
      <td class="bg-grey">$255 por grado</td><td class="bg-grey">20%</td>
      <td class="text-red">$750 por grado</td><td class="text-red">35%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Vinos y aperitivos vínicos</td><td style="color: {COLOR_ACTUAL};">Extranjero</td>
      <td class="bg-blue">$243 por grado</td><td class="bg-blue">20%</td>
      <td class="bg-grey">$255 por grado</td><td class="bg-grey">20%</td>
      <td class="text-red">$750 por grado</td><td class="text-red">35%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Cervezas y sifones</td><td style="color: {COLOR_ACTUAL};">Nacional</td>
      <td class="bg-blue">No existe</td><td class="bg-blue">48%*</td>
      <td class="bg-grey">No existe</td><td class="bg-grey">48%*</td>
      <td class="text-red">$330 por grado</td><td class="text-red">10%</td>
    </tr>
    <tr>
      <td style="color: {COLOR_ACTUAL}; font-weight: bold;">Cervezas y sifones</td><td style="color: {COLOR_ACTUAL};">Extranjero</td>
      <td class="bg-blue">No existe</td><td class="bg-blue">48%*</td>
      <td class="bg-grey">No existe</td><td class="bg-grey">48%*</td>
      <td class="text-red">$330 por grado</td><td class="text-red">10%</td>
    </tr>
  </tbody>
</table>
"""
st.markdown(html_tabla, unsafe_allow_html=True)
st.caption("En licores y vinos, el componente específico se calcula por grado alcoholimétrico en 750 ml o su equivalente. *En cervezas y refajos, la nueva tarifa específica se calcula por grado alcoholimétrico en 330 ml o su equivalente.")
