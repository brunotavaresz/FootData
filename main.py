import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO
from utils import *
from management import show_team_management

# Configuração da página
st.set_page_config(
    page_title="Football Manager Pro ⚽",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_custom_css():
    with open('styles.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Interface principal
def main():
    load_custom_css()
    
    # Carregar dados
    df = load_data()
    
    # Header
    st.markdown("""
    <div class="app-header">
        <h1>⚽ Football Manager Pro</h1>
        <p>Sistema Avançado de Gestão e Análise de Plantéis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado da aplicação
    if 'page' not in st.session_state:
        st.session_state.page = 'selection'
    
    if st.session_state.page == 'selection':
        show_club_selection(df)
    elif st.session_state.page == 'management':
        show_team_management(df)

def show_club_selection(df):
    """Interface de seleção de clubes"""
    st.markdown("## 🏆 Escolha os Clubes para Comparar")
    
    # Estatísticas dos clubes
    club_stats = df.groupby("Club").agg({
        'Overall': 'mean',
        'Value': lambda x: x.apply(convert_value_to_float).sum(),
        'Club Logo': 'first'
    }).sort_values('Overall', ascending=False)
    
    clubs = club_stats.index.tolist()
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown("""
        <div class="club-selection-container">
            <h3>🏆 Clube A</h3>
        </div>
        """, unsafe_allow_html=True)
        
        club_left = st.selectbox(
            "Selecione o primeiro clube",
            clubs,
            key="left_club",
            format_func=lambda x: f"{x} (Overall: {club_stats.loc[x, 'Overall']:.1f})"
        )
        
        if club_left:
            logo_left = get_club_logo(df, club_left)
            st.image(logo_left, width=150)
            
            # Estatísticas do clube
            club_data = df[df["Club"] == club_left]
            col_stat1, col_stat2 = st.columns(2)
            
            with col_stat1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Overall Médio</h4>
                    <h2>{club_data['Overall'].mean():.1f}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col_stat2:
                total_value = club_data['Value'].apply(convert_value_to_float).sum()
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Valor Total</h4>
                    <h2>€{total_value:.1f}M</h2>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="vs-divider">⚡ VS ⚡</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="club-selection-container">
            <h3>🏆 Clube B</h3>
        </div>
        """, unsafe_allow_html=True)
        
        club_right = st.selectbox(
            "Selecione o segundo clube",
            clubs,
            key="right_club",
            format_func=lambda x: f"{x} (Overall: {club_stats.loc[x, 'Overall']:.1f})"
        )
        
        if club_right:
            logo_right = get_club_logo(df, club_right)
            st.image(logo_right, width=150)
            
            # Estatísticas do clube
            club_data = df[df["Club"] == club_right]
            col_stat1, col_stat2 = st.columns(2)
            
            with col_stat1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Overall Médio</h4>
                    <h2>{club_data['Overall'].mean():.1f}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col_stat2:
                total_value = club_data['Value'].apply(convert_value_to_float).sum()
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Valor Total</h4>
                    <h2>€{total_value:.1f}M</h2>
                </div>
                """, unsafe_allow_html=True)
    
    # Botão para continuar
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Iniciar Gestão de Plantéis", type="primary", use_container_width=True):
            if club_left and club_right:
                st.session_state.club_left = club_left
                st.session_state.club_right = club_right
                st.session_state.page = 'management'
                st.rerun()
            else:
                st.error("⚠️ Por favor, selecione ambos os clubes!")

# Executar aplicação
if __name__ == "__main__":
    main()