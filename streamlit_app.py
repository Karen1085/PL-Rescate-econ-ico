import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Impacto Tributario Licores", layout="wide")

# Paleta de colores basada en la imagen de referencia
COLOR_ACTUAL = '#707070'  # Gris
COLOR_PL = '#8A1C30'      # Rojo Tinto / Burdeos

# 1. Carga de Datos
@st.cache_data
def load_data():
    return pd.read_excel("Base_Datos_Tributaria_Licores.xlsx")

df = load_data()

# Título y separador
st.title("🍷 Impacto del PL de Rescate Económico en Bebidas")
st.markdown("---")

# ==========================================
# SECCIÓN 1: TOTAL IMPUESTOS (Estilo Infografía)
# ==========================================
st.subheader("1. Total de Impuestos por Botella")

col_graf, col_cards = st.columns([3, 1])

with col_graf:
    fig_impuestos = go.Figure()
    
    # Barras Hoy
    fig_impuestos.add_trace(go.Bar(
        x=df['Categoría'], y=df['Actual_Total_Impuestos'],
        name='Hoy', marker_color=COLOR_ACTUAL,
        text=[f"${x:,.0f}".replace(',', '.') for x in df['Actual_Total_Impuestos']],
        textposition='outside', textfont=dict(size=12, color='black')
    ))
    
    # Barras Proyecto
    fig_impuestos.add_trace(go.Bar(
        x=df['Categoría'], y=df['PL_Total_Impuestos'],
        name='Proyecto', marker_color=COLOR_PL,
        text=[f"${x:,.0f}".replace(',', '.') for x in df['PL_Total_Impuestos']],
        textposition='outside', textfont=dict(size=12, color=COLOR_PL, weight='bold')
    ))
    
    fig_impuestos.update_layout(
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', 
        margin=dict(t=20, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False)
    )
    st.plotly_chart(fig_impuestos, use_container_width=True)

with col_cards:
    st.markdown("<br><br>", unsafe_allow_html=True)
    # Tarjetas de incrementos como en la imagen
    for _, row in df.iterrows():
        incremento = row['PL_Total_Impuestos'] - row['Actual_Total_Impuestos']
        st.info(f"**{row['Categoría']}**\n\n+${incremento:,.0f} por botella".replace(',', '.'))

st.markdown("---")

# ==========================================
# SECCIÓN 2: PRECIO DE VENTA FINAL (Barras Horizontales)
# ==========================================
st.subheader("2. Precio de Venta Final al Consumidor")

fig_precio = go.Figure()

fig_precio.add_trace(go.Bar(
    y=df['Categoría'], x=df['Actual_Precio_Final'],
    name='Hoy', orientation='h', marker_color=COLOR_ACTUAL,
    text=[f"${x:,.0f}".replace(',', '.') for x in df['Actual_Precio_Final']],
    textposition='inside', insidetextanchor='end'
))

fig_precio.add_trace(go.Bar(
    y=df['Categoría'], x=df['PL_Precio_Final'],
    name='Proyecto', orientation='h', marker_color=COLOR_PL,
    text=[f"${x:,.0f}".replace(',', '.') for x in df['PL_Precio_Final']],
    textposition='outside'
))

fig_precio.update_layout(
    barmode='group', plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=20, b=0, l=0, r=0), height=400,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(showgrid=True, gridcolor='#E5E5E5', showticklabels=False)
)
st.plotly_chart(fig_precio, use_container_width=True)

st.markdown("---")

# ==========================================
# SECCIÓN 3: PRESIÓN FISCAL (Gráfico Dumbbell / Mancuerna)
# ==========================================
st.subheader("3. Presión Fiscal (% del precio que son impuestos)")

fig_presion = go.Figure()

for i, row in df.iterrows():
    # Línea conectora
    fig_presion.add_trace(go.Scatter(
        x=[row['Actual_Presion_Fiscal'], row['PL_Presion_Fiscal']],
        y=[row['Categoría'], row['Categoría']],
        mode='lines', line=dict(color='gray', width=3), showlegend=False
    ))
    
    # Punto Actual
    fig_presion.add_trace(go.Scatter(
        x=[row['Actual_Presion_Fiscal']], y=[row['Categoría']],
        mode='markers+text', marker=dict(color=COLOR_ACTUAL, size=15),
        text=[f"{row['Actual_Presion_Fiscal']:.0%}"], textposition='middle left',
        name='Hoy' if i == 0 else "", showlegend=(i==0)
    ))
    
    # Punto PL
    fig_presion.add_trace(go.Scatter(
        x=[row['PL_Presion_Fiscal']], y=[row['Categoría']],
        mode='markers+text', marker=dict(color=COLOR_PL, size=15),
        text=[f"{row['PL_Presion_Fiscal']:.0%}"], textposition='middle right',
        textfont=dict(color=COLOR_PL, weight='bold'),
        name='Proyecto' if i == 0 else "", showlegend=(i==0)
    ))

fig_presion.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', height=400,
    margin=dict(t=20, b=40, l=0, r=0),
    xaxis=dict(showgrid=True, gridcolor='#E5E5E5', tickformat='.0%'),
    yaxis=dict(showgrid=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_presion, use_container_width=True)

# Nota metodológica al pie
st.caption("Nota: Simulación proyectada a 2027 suponiendo traslado completo de incrementos tributarios al consumidor final.")
