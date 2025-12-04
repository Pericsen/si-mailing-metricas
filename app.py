import streamlit as st
import pandas as pd
import gspread
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib

# =====================================================
# Sistema de Autenticación
# =====================================================
def hash_password(password):
    """Crea hash de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_authentication():
    """Verifica si el usuario está autenticado"""
    # Usuarios autorizados (en producción, esto debería estar en secrets de Streamlit)
    # Para agregar un nuevo usuario: genera el hash de su contraseña y agrégalo aquí
    try:
        AUTHORIZED_USERS = st.secrets["authorized_users"]
    except:
        AUTHORIZED_USERS={
            "admin": hash_password("admin123")
        }
    
    # Verificar si ya está autenticado
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("Iniciar Sesión")
        st.markdown("### Dashboard de Campañas Email – MSI + RML")
        
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Iniciar Sesión")
            
            if submit:
                if username in AUTHORIZED_USERS:
                    if AUTHORIZED_USERS[username] == hash_password(password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("✅ Inicio de sesión exitoso")
                        st.rerun()
                    else:
                        st.error("❌ Contraseña incorrecta")
                else:
                    st.error("❌ Usuario no autorizado")
        return False
    
    return True

# Verificar autenticación antes de mostrar el dashboard
if not check_authentication():
    st.stop()

# Botón de cerrar sesión en la barra lateral
with st.sidebar:
    st.write(f"👤 Usuario: **{st.session_state.username}**")
    if st.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
    st.divider()

# =====================================================
# Carga Google Sheet
# =====================================================
load_dotenv()
try:
    SHEET_ID = st.secrets["SHEET_ID"]
    service_account_info = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(service_account_info)
except:
    # Fallback para desarrollo local con .env
    load_dotenv()
    SHEET_ID = os.getenv("SHEET_ID")
    SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH")
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_PATH)

sheet = gc.open_by_key(SHEET_ID).get_worksheet(2)
data = sheet.get_all_records()
df = pd.DataFrame(data)

# =====================================================
# Limpieza de datos
# =====================================================
df["Fecha"] = pd.to_datetime(df["Fecha"], format='%d/%m/%Y').dt.date
df["Enviados"] = pd.to_numeric(df["Enviados"], errors="coerce")
df["Abiertos"] = pd.to_numeric(df["Abiertos"], errors="coerce")
df["Clics"] = pd.to_numeric(df["Clics"], errors="coerce")
df["Desuscripción"] = pd.to_numeric(df["Desuscripción"], errors="coerce")

# Métricas numéricas
df["OR_pct"] = df["Abiertos"] / df["Enviados"]
df["CTR_pct"] = df["Clics"] / df["Enviados"]
df["CTOR_pct"] = df["Clics"] / df["Abiertos"]
df["Des_pct"] = df["Desuscripción"] / df["Enviados"]

# Versiones para tabla (% formateado)
df["OR"] = df["OR_pct"].map("{:.1%}".format)
df["CTR"] = df["CTR_pct"].map("{:.1%}".format)
df["CTOR"] = df["CTOR_pct"].map("{:.1%}".format)
df["% Des"] = df["Des_pct"].map("{:.2%}".format)

df["Email_ID"] = df["Campaña"].str.extract(r'Email\s*(\d+)')[0]
df["Email_ID"] = pd.to_numeric(df["Email_ID"], errors="coerce")

# Cálculo de OR Global
base_envios = (
    df[df["Base"].str.contains("Completa", case=False, na=False)]
    .groupby("Email_ID")["Enviados"]
    .max()
)

df["Envios_Base_Email"] = df["Email_ID"].map(base_envios)
df["OR_Global_pct"] = df["Abiertos"] / df["Envios_Base_Email"]
df.loc[df["Envios_Base_Email"].isna(), "OR_Global_pct"] = df["Abiertos"] / df["Enviados"]
df["OR Global"] = df["OR_Global_pct"].map('{:.1%}'.format)

# Filtrar nan
df = df[df['OR Global'] != 'nan%']
df = df.sort_values("Fecha", ascending=False)

# =====================================================
# UI
# =====================================================
st.set_page_config(page_title="Dashboard Mailing MSI + RML", layout="wide")
st.title("📩 Dashboard de Campañas Email – MSI + RML")

# =====================================================
# KPIs PRINCIPALES
# =====================================================
st.subheader("📊 Métricas Generales")
with st.container(border=True):
    col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

    total_enviados = df["Enviados"].sum()
    total_abiertos = df["Abiertos"].sum()
    total_clics = df["Clics"].sum()
    or_promedio = (total_abiertos / total_enviados) * 100
    ctr_promedio = (total_clics / total_enviados) * 100

    with col_kpi1:
        st.metric("📧 Total Enviados", f"{total_enviados:,.0f}")
    with col_kpi2:
        st.metric("👀 Total Abiertos", f"{total_abiertos:,.0f}")
    with col_kpi3:
        st.metric("🖱️ Total Clics", f"{total_clics:,.0f}")
    with col_kpi4:
        st.metric("📈 OR Promedio", f"{or_promedio:.1f}%")
    with col_kpi5:
        st.metric("🎯 CTR Promedio", f"{ctr_promedio:.2f}%")

st.divider()

# =====================================================
# GRÁFICOS PRINCIPALES
# =====================================================

# FILA 1: Evolución temporal + Top campañas
col1, col2 = st.columns([1, 1])

with col1, st.container(border=True):
    st.subheader("📈 Evolución de métricas en el tiempo")
    
    # Preparar datos para el gráfico
    time_df = df.sort_values("Fecha").copy()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # OR Global
    fig.add_trace(
        go.Scatter(x=time_df["Fecha"], y=time_df["OR_Global_pct"]*100, 
                   name="OR Global (%)", mode='lines+markers',
                   line=dict(color='#1f77b4', width=2)),
        secondary_y=False
    )
    
    # CTR
    fig.add_trace(
        go.Scatter(x=time_df["Fecha"], y=time_df["CTR_pct"]*100, 
                   name="CTR (%)", mode='lines+markers',
                   line=dict(color='#ff7f0e', width=2)),
        secondary_y=False
    )
    
    # Enviados
    fig.add_trace(
        go.Scatter(x=time_df["Fecha"], y=time_df["Enviados"], 
                   name="Enviados", mode='lines',
                   line=dict(color='#2ca02c', width=2)),
        secondary_y=True
    )
    
    fig.update_xaxes(title_text="Fecha")
    fig.update_yaxes(title_text="Tasa (%)", secondary_y=False)
    fig.update_yaxes(title_text="Cantidad Enviados", secondary_y=True)
    fig.update_layout(height=400, hovermode='x unified')
    
    st.plotly_chart(fig, use_container_width=True)

with col2, st.container(border=True):
    st.subheader("🏆 Top 10 Campañas por OR Global")
    
    top_campaigns = df.nlargest(10, 'OR_Global_pct')[['Campaña', 'OR_Global_pct']].copy()
    top_campaigns['Campaña_short'] = top_campaigns['Campaña'].str[:30] + '...'
    # Ordenar de mayor a menor para el gráfico
    top_campaigns = top_campaigns.sort_values('OR_Global_pct', ascending=True)
    
    fig = px.bar(top_campaigns, 
                 y='Campaña_short', 
                 x='OR_Global_pct',
                 orientation='h',
                 labels={'OR_Global_pct': 'OR Global (%)', 'Campaña_short': ''},
                 color='OR_Global_pct',
                 color_continuous_scale='Blues')
    
    fig.update_traces(texttemplate='%{x:.1%}', textposition='outside')
    fig.update_layout(height=400, showlegend=False, xaxis_tickformat='.0%')
    
    st.plotly_chart(fig, use_container_width=True)

# st.divider()

# FILA 2: Análisis de correlación + Distribución
col3, col4 = st.columns(2)

with col3, st.container(border=True):
    st.subheader("🎯 Tamaño de envío vs Rendimiento")
    
    # Crear bins para mejor visualización con orden específico
    df_copy = df.copy()
    df_copy['Tamaño'] = pd.cut(df_copy['Enviados'], 
                                bins=[0, 1000, 5000, 50000, 200000],
                                labels=['Pequeño (<1K)', 'Mediano (1K-5K)', 
                                       'Grande (5K-50K)', 'Muy Grande (>50K)'])
    
    # Definir el orden categórico
    order_categorias = ['Pequeño (<1K)', 'Mediano (1K-5K)', 'Grande (5K-50K)', 'Muy Grande (>50K)']
    
    fig = px.box(df_copy, 
                 x='Tamaño', 
                 y='OR_Global_pct',
                 color='Tamaño',
                 labels={'OR_Global_pct': 'OR Global (%)', 'Tamaño': 'Tamaño de envío'},
                 points='all',
                 category_orders={'Tamaño': order_categorias})
    
    fig.update_layout(height=400, showlegend=False, yaxis_tickformat='.0%')
    
    st.plotly_chart(fig, use_container_width=True)

with col4, st.container(border=True):
    st.subheader("📉 Distribución de OR Global")
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(x=df['OR_Global_pct']*100,
                               nbinsx=20,
                               marker_color='lightblue',
                               name='Frecuencia'))
    
    # Agregar línea de promedio
    mean_or = df['OR_Global_pct'].mean() * 100
    fig.add_vline(x=mean_or, line_dash="dash", line_color="red",
                  annotation_text=f"Promedio: {mean_or:.1f}%",
                  annotation_position="top right")
    
    fig.update_layout(height=400,
                     xaxis_title="OR Global (%)",
                     yaxis_title="Cantidad de campañas",
                     showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)

# st.divider()

# FILA 3: Análisis por Base + Asunto
col5, col6 = st.columns(2)

with col5, st.container(border=True):
    st.subheader("📊 Rendimiento por Tipo de Base")
    
    base_summary = df.groupby('Base').agg({
        'Enviados': 'sum',
        'Abiertos': 'sum',
        'Clics': 'sum',
        'Campaña': 'count'
    }).reset_index()
    
    base_summary['OR'] = (base_summary['Abiertos'] / base_summary['Enviados']) * 100
    base_summary['CTR'] = (base_summary['Clics'] / base_summary['Enviados']) * 100
    base_summary = base_summary.nlargest(10, 'Enviados')
    # Ordenar por OR de mayor a menor
    base_summary = base_summary.sort_values('OR', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='OR (%)',
        x=base_summary['Base'],
        y=base_summary['OR'],
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name='CTR (%)',
        x=base_summary['Base'],
        y=base_summary['CTR'],
        marker_color='lightcoral'
    ))
    
    fig.update_layout(height=400, barmode='group', xaxis_tickangle=-45)
    
    st.plotly_chart(fig, use_container_width=True)

with col6, st.container(border=True):
    st.subheader("⚡ Palabras clave en asuntos exitosos")
    
    # Identificar campañas exitosas (OR Global > promedio)
    threshold = df['OR_Global_pct'].median()
    exitosas = df[df['OR_Global_pct'] > threshold]['Asunto'].str.lower()
    
    # Extraer palabras clave
    from collections import Counter
    import re
    
    palabras = []
    for asunto in exitosas:
        palabras.extend(re.findall(r'\b\w{4,}\b', str(asunto)))
    
    top_palabras = Counter(palabras).most_common(10)
    
    if top_palabras:
        palabras_df = pd.DataFrame(top_palabras, columns=['Palabra', 'Frecuencia'])
        # Ordenar de mayor a menor (ascending=True para que el más alto quede arriba)
        palabras_df = palabras_df.sort_values('Frecuencia', ascending=True)
        
        fig = px.bar(palabras_df, 
                     x='Frecuencia', 
                     y='Palabra',
                     orientation='h',
                     color='Frecuencia',
                     color_continuous_scale='Reds')
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay suficientes datos para analizar palabras clave")

st.divider()

# =====================================================
# TABLA DETALLADA CON FILTROS
# =====================================================
st.subheader("Explorador de Campañas")

col_filter1, col_filter2, col_filter3 = st.columns(3)

with col_filter1:
    bases_disponibles = ['Todas'] + sorted(df['Base'].unique().tolist())
    base_seleccionada = st.selectbox('Filtrar por Base:', bases_disponibles)

with col_filter2:
    fecha_min = df['Fecha'].min()
    fecha_max = df['Fecha'].max()
    fecha_desde = st.date_input('Desde:', fecha_min, min_value=fecha_min, max_value=fecha_max)

with col_filter3:
    fecha_hasta = st.date_input('Hasta:', fecha_max, min_value=fecha_min, max_value=fecha_max)

# Aplicar filtros
df_filtrado = df.copy()

if base_seleccionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Base'] == base_seleccionada]

df_filtrado = df_filtrado[
    (df_filtrado['Fecha'] >= fecha_desde) & 
    (df_filtrado['Fecha'] <= fecha_hasta)
]

# Mostrar tabla
columnas_tabla = ['Fecha', 'Campaña', 'Base', 'Asunto', 'Enviados', 'Abiertos', 
                  'OR', 'Clics', 'CTR', 'CTOR', 'Desuscripción', '% Des', 'OR Global']

st.dataframe(
    df_filtrado[columnas_tabla].sort_values('Fecha', ascending=False),
    use_container_width=True,
    height=400
)

# Botón de descarga
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Descargar datos filtrados (CSV)",
    data=csv,
    file_name="campanas_email_filtradas.csv",
    mime="text/csv",
)