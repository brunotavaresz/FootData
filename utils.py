import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv("data/players.csv")
    return filter_valid_players(df)

def filter_valid_players(df):
    """Filtra e limpa os dados dos jogadores"""
    # Remove jogadores sem dados essenciais
    df = df.dropna(subset=['Name', 'Club'])
    df = df[df['Overall'] > 0]
    
    # Converte tipos de dados
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df['Overall'] = pd.to_numeric(df['Overall'], errors='coerce')
    df['Potential'] = pd.to_numeric(df['Potential'], errors='coerce')
    
    # Remove linhas com dados inválidos após conversão
    df = df.dropna(subset=['Age', 'Overall'])
    
    # Garante que Value não seja NaN
    df['Value'] = df['Value'].fillna('€0M')
    
    # Garante que Position não seja NaN
    df['Position'] = df['Position'].fillna('<span class="pos">N/A</span>')
    
    return df

def get_club_logo(df, club):
    try:
        logo_url = df[df['Club'] == club]['Club Logo'].iloc[0]
        if pd.notna(logo_url) and logo_url.startswith('http'):
            return logo_url
        else:
            return "https://via.placeholder.com/120x120/2a5298/white?text=FC"
    except:
        return "https://via.placeholder.com/120x120/2a5298/white?text=FC"

def convert_value_to_float(value_str):
    """Converte valores monetários para float (€91M, €575K, etc.)"""
    try:
        if pd.isna(value_str):
            return 0.0
        
        # Remove € e espaços
        clean_value = str(value_str).replace('€', '').strip()
        
        if 'M' in clean_value:
            # Milhões
            return float(clean_value.replace('M', ''))
        elif 'K' in clean_value:
            # Milhares - converte para milhões
            return float(clean_value.replace('K', '')) / 1000
        else:
            # Tenta converter diretamente
            try:
                return float(clean_value)
            except:
                return 0.0
    except:
        return 0.0

def extract_position(position_html):
    try:
        import re
        if pd.isna(position_html):
            return "N/A"
        match = re.search(r'>([A-Z]+)<', str(position_html))
        return match.group(1) if match else "N/A"
    except:
        return "N/A"

def create_football_field(df, club, side="left"):
    """Cria um campo de futebol interativo com jogadores"""
    players = df[df["Club"] == club].nlargest(11, 'Overall')
    
    # Formação 4-3-3
    positions = [
        (50, 5),   # GK
        (20, 25), (40, 25), (60, 25), (80, 25),  # Defense
        (30, 50), (50, 50), (70, 50),  # Midfield  
        (25, 75), (50, 85), (75, 75)   # Attack
    ]
    
    fig = go.Figure()
    
    # Campo base
    fig.add_shape(
        type="rect", x0=0, y0=0, x1=100, y1=90,
        line=dict(color="white", width=3),
        fillcolor="rgba(34, 139, 34, 0.9)"
    )
    
    # Linha do meio
    fig.add_shape(
        type="line", x0=0, y0=45, x1=100, y1=45,
        line=dict(color="white", width=2)
    )
    
    # Círculo central
    fig.add_shape(
        type="circle", x0=45, y0=40, x1=55, y1=50,
        line=dict(color="white", width=2)
    )
    
    # Áreas
    fig.add_shape(
        type="rect", x0=25, y0=0, x1=75, y1=18,
        line=dict(color="white", width=2), fillcolor="rgba(255,255,255,0.1)"
    )
    fig.add_shape(
        type="rect", x0=25, y0=72, x1=75, y1=90,
        line=dict(color="white", width=2), fillcolor="rgba(255,255,255,0.1)"
    )
    
    # Adicionar jogadores
    for i, (player, (x, y)) in enumerate(zip(players.itertuples(), positions)):
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            marker=dict(
                size=30,
                color="rgba(30, 60, 114, 0.9)",
                line=dict(color="white", width=3),
                symbol="circle"
            ),
            text=[player.Name.split()[-1][:6]],
            textposition="bottom center",
            textfont=dict(color="white", size=10, family="Arial Black"),
            hovertemplate=f"""
            <b>{player.Name}</b><br>
            Overall: {player.Overall}<br>
            Posição: {extract_position(player.Position)}<br>
            Idade: {player.Age}<br>
            Valor: {player.Value}<br>
            <extra></extra>
            """,
            name=f"{player.Name}",
            customdata=[player.ID] if hasattr(player, 'ID') else [i]
        ))
    
    fig.update_layout(
        width=500, height=600,
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[0, 100]),
        yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[0, 90]),
        plot_bgcolor="rgba(34, 139, 34, 0.9)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        title=dict(
            text=f"{club} - Formação 4-3-3",
            x=0.5,
            font=dict(color="white", size=16)
        )
    )
    
    return fig

def create_player_stats_radar(player):
    """Cria gráfico radar APENAS com dados reais do dataset"""
    # Verificar quais colunas de stats existem no dataset
    available_stats = {}
    
    # Lista de possíveis colunas de estatísticas no dataset FIFA
    stat_columns = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical']
    
    for stat in stat_columns:
        if hasattr(player, stat) and pd.notna(getattr(player, stat)):
            available_stats[stat] = getattr(player, stat)
    
    # Se não há estatísticas específicas, não criar gráfico radar
    if not available_stats:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=list(available_stats.values()),
        theta=list(available_stats.keys()),
        fill='toself',
        fillcolor='rgba(30, 60, 114, 0.3)',
        line=dict(color='rgba(30, 60, 114, 1)', width=3),
        name=player.Name
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            )
        ),
        showlegend=False,
        title=f"Habilidades - {player.Name}",
        width=400,
        height=400
    )
    
    return fig

def load_image_from_url(url, width=100):
    """Carrega imagem de uma URL"""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return image
    except:
        return None

def format_currency(value_str):
    """Formata valores monetários"""
    try:
        if pd.isna(value_str):
            return "N/A"
        
        # Remove símbolos e converte para float
        clean_value = str(value_str).replace('€', '').replace('M', '').replace('K', '')
        
        if 'M' in str(value_str):
            return f"€{float(clean_value):.1f}M"
        elif 'K' in str(value_str):
            return f"€{float(clean_value):.0f}K"
        else:
            return str(value_str)
    except:
        return "N/A"

def get_player_rating_color(overall):
    """Retorna cor baseada no rating do jogador"""
    if overall >= 85:
        return "#FFD700"  # Dourado
    elif overall >= 80:
        return "#C0C0C0"  # Prateado  
    elif overall >= 75:
        return "#CD7F32"  # Bronze
    else:
        return "#808080"  # Cinza