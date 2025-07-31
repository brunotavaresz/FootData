import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils import *

def show_team_management(df):
    """Interface principal de gestão de plantéis"""
    club_left = st.session_state.club_left
    club_right = st.session_state.club_right
    
    # Header da gestão
    st.markdown(f"""
    <div class="app-header">
        <h2>⚽ Gestão de Plantéis</h2>
        <h3>{club_left} 🆚 {club_right}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão para voltar
    if st.button("← Voltar à Seleção"):
        st.session_state.page = 'selection'
        st.rerun()
    
    # Tabs principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏟️ Campo Tático", 
        "📊 Comparação", 
        "👤 Jogadores", 
        "📈 Análises", 
        "🎯 Scout"
    ])
    
    with tab1:
        show_tactical_field(df, club_left, club_right)
    
    with tab2:
        show_club_comparison(df, club_left, club_right)
    
    with tab3:
        show_player_analysis(df, club_left, club_right)
    
    with tab4:
        show_advanced_analytics(df, club_left, club_right)
    
    with tab5:
        show_scouting_system(df, club_left, club_right)

def show_tactical_field(df, club_left, club_right):
    """Exibe os campos táticos dos dois clubes"""
    st.markdown("### 🏟️ Visualização Tática dos Plantéis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {club_left}")
        field_left = create_football_field(df, club_left, "left")
        st.plotly_chart(field_left, use_container_width=True, key="field_left")
        
        # Formação e estatísticas
        players_left = df[df["Club"] == club_left].nlargest(11, 'Overall')
        st.markdown(f"""
        <div class="formation-display">
            Formação: 4-3-3 | Overall Médio: {players_left['Overall'].mean():.1f}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"#### {club_right}")
        field_right = create_football_field(df, club_right, "right")
        st.plotly_chart(field_right, use_container_width=True, key="field_right")
        
        # Formação e estatísticas
        players_right = df[df["Club"] == club_right].nlargest(11, 'Overall')
        st.markdown(f"""
        <div class="formation-display">
            Formação: 4-3-3 | Overall Médio: {players_right['Overall'].mean():.1f}
        </div>
        """, unsafe_allow_html=True)
    
    # Lista de jogadores titulares
    st.markdown("---")
    st.markdown("### 👥 Plantéis Titulares")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {club_left} - Starting XI")
        for i, player in enumerate(players_left.itertuples(), 1):
            position = extract_position(player.Position)
            rating_color = get_player_rating_color(player.Overall)
            
            st.markdown(f"""
            <div class="player-card">
                <div style="display: flex; align-items: center;">
                    <div style="background: {rating_color}; color: black; font-weight: bold; 
                                padding: 0.3rem 0.6rem; border-radius: 8px; margin-right: 1rem; 
                                min-width: 40px; text-align: center;">
                        {player.Overall}
                    </div>
                    <div style="flex: 1; color: black;">
                        <strong>{player.Name}</strong><br>
                        <small>{position} | {player.Age} anos | {player.Value}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📊 Ver Stats", key=f"stats_left_{i}"):
                show_player_detailed_stats(player)
    
    with col2:
        st.markdown(f"#### {club_right} - Starting XI")
        for i, player in enumerate(players_right.itertuples(), 1):
            position = extract_position(player.Position)
            rating_color = get_player_rating_color(player.Overall)
            
            st.markdown(f"""
            <div class="player-card">
                <div style="display: flex; align-items: center;">
                    <div style="background: {rating_color}; color: black; font-weight: bold; 
                                padding: 0.3rem 0.6rem; border-radius: 8px; margin-right: 1rem; 
                                min-width: 40px; text-align: center;">
                        {player.Overall}
                    </div>
                    <div style="flex: 1; color: black;">
                        <strong>{player.Name}</strong><br>
                        <small>{position} | {player.Age} anos | {player.Value}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📊 Ver Stats", key=f"stats_right_{i}"):
                show_player_detailed_stats(player)

def show_player_detailed_stats(player):
    """Mostra estatísticas detalhadas do jogador com dados reais"""
    st.markdown("---")
    st.markdown(f"### 📊 Análise Completa - {player.Name}")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Foto e info básica
        if hasattr(player, 'Photo') and pd.notna(player.Photo):
            try:
                st.image(player.Photo, width=150)
            except:
                st.markdown("📷 Foto não disponível")
        else:
            st.markdown("📷 Foto não disponível")
        
        st.markdown(f"""
        **Clube:** {player.Club}  
        **Posição:** {extract_position(player.Position)}  
        **Idade:** {player.Age} anos  
        **Nacionalidade:** {getattr(player, 'Nationality', 'N/A')}  
        **Valor:** {player.Value}  
        **Salário:** {getattr(player, 'Wage', 'N/A')}
        """)
    
    with col2:
        # Gráfico radar apenas se houver dados reais
        radar_fig = create_player_stats_radar(player)
        if radar_fig:
            st.plotly_chart(radar_fig, use_container_width=True)
        else:
            st.info("Estatísticas específicas não disponíveis no dataset")
    
    with col3:
        # Métricas principais apenas com dados reais
        st.metric("Overall", player.Overall)
        st.metric("Potencial", player.Potential)
        
        if hasattr(player, 'Preferred_Foot') and pd.notna(player.Preferred_Foot):
            st.metric("Pé Preferido", player.Preferred_Foot)
        
        if hasattr(player, 'International_Reputation') and pd.notna(player.International_Reputation):
            st.metric("Reputação", f"{player.International_Reputation}/5 ⭐")

def show_club_comparison(df, club_left, club_right):
    """Comparação detalhada entre clubes"""
    st.markdown("### 📊 Comparação Detalhada")
    
    data_left = df[df["Club"] == club_left]
    data_right = df[df["Club"] == club_right]
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_left = data_left['Overall'].mean()
        avg_right = data_right['Overall'].mean()
        st.metric(
            "Overall Médio",
            f"{avg_left:.1f}",
            f"{avg_left - avg_right:.1f}",
            delta_color="normal"
        )
    
    with col2:
        age_left = data_left['Age'].mean()
        age_right = data_right['Age'].mean()
        st.metric(
            "Idade Média",
            f"{age_left:.1f}",
            f"{age_left - age_right:.1f}",
            delta_color="inverse"
        )
    
    with col3:
        pot_left = data_left['Potential'].mean()
        pot_right = data_right['Potential'].mean()
        st.metric(
            "Potencial Médio",
            f"{pot_left:.1f}",
            f"{pot_left - pot_right:.1f}",
            delta_color="normal"
        )
    
    with col4:
        count_left = len(data_left)
        count_right = len(data_right)
        st.metric(
            "Total Jogadores",
            count_left,
            count_left - count_right
        )
    
    # Gráficos comparativos
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição de Overall
        fig_overall = go.Figure()
        fig_overall.add_trace(go.Histogram(
            x=data_left['Overall'],
            name=club_left,
            opacity=0.7,
            nbinsx=20,
            marker_color='rgba(30, 60, 114, 0.7)'
        ))
        fig_overall.add_trace(go.Histogram(
            x=data_right['Overall'],
            name=club_right,
            opacity=0.7,
            nbinsx=20,
            marker_color='rgba(220, 20, 60, 0.7)'
        ))
        fig_overall.update_layout(
            title="Distribuição de Overall",
            xaxis_title="Overall",
            yaxis_title="Número de Jogadores",
            barmode='overlay'
        )
        st.plotly_chart(fig_overall, use_container_width=True)
    
    with col2:
        # Distribuição de Idades
        fig_age = go.Figure()
        fig_age.add_trace(go.Histogram(
            x=data_left['Age'],
            name=club_left,
            opacity=0.7,
            nbinsx=15,
            marker_color='rgba(30, 60, 114, 0.7)'
        ))
        fig_age.add_trace(go.Histogram(
            x=data_right['Age'],
            name=club_right,
            opacity=0.7,
            nbinsx=15,
            marker_color='rgba(220, 20, 60, 0.7)'
        ))
        fig_age.update_layout(
            title="Distribuição de Idades",
            xaxis_title="Idade",
            yaxis_title="Número de Jogadores",
            barmode='overlay'
        )
        st.plotly_chart(fig_age, use_container_width=True)

def show_player_analysis(df, club_left, club_right):
    """Análise individual de jogadores"""
    st.markdown("### 👤 Análise Individual de Jogadores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {club_left}")
        players_left = df[df["Club"] == club_left]['Name'].tolist()
        selected_left = st.selectbox("Escolha um jogador:", players_left, key="player_left")
    
    with col2:
        st.markdown(f"#### {club_right}")
        players_right = df[df["Club"] == club_right]['Name'].tolist()
        selected_right = st.selectbox("Escolha um jogador:", players_right, key="player_right")
    
    if selected_left and selected_right:
        player_left = df[df['Name'] == selected_left].iloc[0]
        player_right = df[df['Name'] == selected_right].iloc[0]
        
        st.markdown("---")
        st.markdown("### ⚖️ Comparação Direta")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if hasattr(player_left, 'Photo') and pd.notna(player_left.Photo):
                try:
                    st.image(player_left.Photo, width=120)
                except:
                    st.markdown("📷")
            else:
                st.markdown("📷")
            st.markdown(f"**{player_left.Name}**")
            st.caption(f"{club_left} | {extract_position(player_left.Position)}")
        
        with col3:
            if hasattr(player_right, 'Photo') and pd.notna(player_right.Photo):
                try:
                    st.image(player_right.Photo, width=120)
                except:
                    st.markdown("📷")
            else:
                st.markdown("📷")
            st.markdown(f"**{player_right.Name}**")
            st.caption(f"{club_right} | {extract_position(player_right.Position)}")
        
        with col2:
            # Comparação de stats
            comparison_data = pd.DataFrame({
                player_left.Name: [player_left.Overall, player_left.Potential, player_left.Age],
                player_right.Name: [player_right.Overall, player_right.Potential, player_right.Age]
            }, index=['Overall', 'Potencial', 'Idade'])
            
            st.bar_chart(comparison_data)

def show_advanced_analytics(df, club_left, club_right):
    """Análises avançadas dos clubes"""
    st.markdown("### 📈 Análises Avançadas")
    
    data_left = df[df["Club"] == club_left]
    data_right = df[df["Club"] == club_right]
    
    # Top jogadores
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### 🌟 Top 5 Jogadores - {club_left}")
        top_left = data_left.nlargest(5, 'Overall')[['Name', 'Overall', 'Age', 'Position', 'Value']]
        for _, player in top_left.iterrows():
            position = extract_position(player.Position)
            rating_color = get_player_rating_color(player.Overall)
            st.markdown(f"""
            <div class="player-card">
                <div style="display: flex; align-items: center;">
                    <div style="background: {rating_color}; color: black; font-weight: bold; 
                                padding: 0.3rem 0.6rem; border-radius: 8px; margin-right: 1rem; 
                                min-width: 40px; text-align: center;">
                        {player.Overall}
                    </div>
                    <div style="flex: 1; color: black;">
                        <strong>{player.Name}</strong><br>
                        <small>{position} | {player.Age} anos | {player.Value}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"#### 🌟 Top 5 Jogadores - {club_right}")
        top_right = data_right.nlargest(5, 'Overall')[['Name', 'Overall', 'Age', 'Position', 'Value']]
        for _, player in top_right.iterrows():
            position = extract_position(player.Position)
            rating_color = get_player_rating_color(player.Overall)
            st.markdown(f"""
            <div class="player-card">
                <div style="display: flex; align-items: center;">
                    <div style="background: {rating_color}; color: black; font-weight: bold; 
                                padding: 0.3rem 0.6rem; border-radius: 8px; margin-right: 1rem; 
                                min-width: 40px; text-align: center;">
                        {player.Overall}
                    </div>
                    <div style="flex: 1; color: black;">
                        <strong>{player.Name}</strong><br>
                        <small>{position} | {player.Age} anos | {player.Value}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Análise por posição
    st.markdown("---")
    st.markdown("#### 📍 Força por Posição")
    
    pos_left = data_left.groupby(data_left['Position'].apply(extract_position))['Overall'].mean()
    pos_right = data_right.groupby(data_right['Position'].apply(extract_position))['Overall'].mean()
    
    df_positions = pd.DataFrame({
        club_left: pos_left,
        club_right: pos_right
    }).fillna(0)
    
    st.bar_chart(df_positions)

def show_scouting_system(df, club_left, club_right):
    """Sistema de scouting para encontrar jogadores"""
    st.markdown("### 🎯 Sistema de Scouting")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_overall = st.slider("Overall Mínimo", 60, 99, 75)
    
    with col2:
        max_age = st.slider("Idade Máxima", 16, 40, 28)
    
    with col3:
        position_filter = st.selectbox(
            "Posição",
            ["Todas"] + sorted(df['Position'].apply(extract_position).unique())
        )
    
    # Filtrar jogadores
    filtered_df = df[
        (df['Overall'] >= min_overall) & 
        (df['Age'] <= max_age) &
        (~df['Club'].isin([club_left, club_right]))
    ]
    
    if position_filter != "Todas":
        filtered_df = filtered_df[filtered_df['Position'].apply(extract_position) == position_filter]
    
    # Mostrar resultados
    st.markdown(f"#### 🔍 Jogadores Encontrados ({len(filtered_df)})")
    
    if len(filtered_df) > 0:
        # Top 10 jogadores
        top_prospects = filtered_df.nlargest(10, 'Overall')
        
        for _, player in top_prospects.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 2])
            
            with col1:
                if hasattr(player, 'Photo') and pd.notna(player.Photo):
                    try:
                        st.image(player.Photo, width=50)
                    except:
                        st.markdown("📷")
                else:
                    st.markdown("📷")
            
            with col2:
                st.markdown(f"**{player.Name}**")
                st.caption(f"{player.Club} | {extract_position(player.Position)}")
            
            with col3:
                st.metric("Overall", player.Overall)
            
            with col4:
                st.metric("Idade", player.Age)
            
            with col5:
                st.markdown(f"**Valor:** {player.Value}")
                potential_growth = player.Potential - player.Overall
                if potential_growth > 0:
                    st.success(f"Potencial: +{potential_growth}")
                else:
                    st.info("Jogador experiente")
    else:
        st.info("Nenhum jogador encontrado com os critérios selecionados.")