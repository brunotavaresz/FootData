# ⚽ Football Manager Pro

Sistema avançado de gestão e análise de plantéis de futebol desenvolvido em Python com Streamlit.

## 🚀 Funcionalidades

### 🏟️ Campo Tático
- Visualização interativa dos jogadores no campo
- Formação 4-3-3 com posicionamento realista
- Campo de futebol com design profissional
- Clique nos jogadores para ver estatísticas

### 📊 Comparação de Clubes
- Métricas comparativas detalhadas
- Gráficos de distribuição de Overall e idades
- Análise de força por posição
- Estatísticas de valor de mercado

### 👤 Análise de Jogadores
- Gráficos radar de habilidades
- Comparação direta entre jogadores
- Informações detalhadas (foto, clube, posição, etc.)
- Métricas de potencial e crescimento

### 🎯 Sistema de Scouting
- Filtros avançados por Overall, idade e posição
- Busca de jogadores fora dos clubes selecionados
- Análise de potencial de crescimento
- Lista de prospects organizados

### 📈 Analytics Avançados
- Top 5 jogadores por clube
- Distribuições estatísticas
- Análise de química do time
- Tendências de valor de mercado

## 📋 Requisitos

```bash
pip install streamlit pandas plotly requests Pillow
```

## 🗂️ Estrutura do Projeto

```
football-manager-pro/
│
├── data/
│   └── players.csv          # Dataset dos jogadores
├── assets/
│   └── campo.png           # Imagem do campo (opcional)
├── app.py                  # Aplicação principal
├── gestao_plantel.py       # Sistema de gestão melhorado
├── utils.py                # Utilitários
├── styles.css              # Estilos personalizados
└── README.md              # Este arquivo
```

## 🚀 Como Executar

1. **Clone ou baixe os arquivos**

2. **Instale as dependências**
   ```bash
   pip install streamlit pandas plotly requests Pillow
   ```

3. **Coloque seu dataset CSV na pasta `data/`**
   - O arquivo deve se chamar `players.csv`
   - Certifique-se de que tem as colunas necessárias

4. **Execute a aplicação**
   ```bash
   streamlit run app.py
   ```

5. **Acesse no navegador**
   - Geralmente em `http://localhost:8501`

## 📊 Formato do Dataset

O CSV deve conter as seguintes colunas principais:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| ID | int | Identificador único |
| Name | str | Nome do jogador |
| Age | int | Idade |
| Photo | str | URL da foto |
| Nationality | str | Nacionalidade |
| Overall | int | Rating geral (0-99) |
| Potential | int | Potencial (0-99) |
| Club | str | Nome do clube |
| Club Logo | str | URL do logo |
| Value | str | Valor de mercado (€Xm) |
| Wage | str | Salário |
| Position | str | Posição (HTML) |
| Preferred Foot | str | Pé preferido |

## 🎨 Customização

### Cores e Temas
- Edite as variáveis CSS no arquivo `app.py`
- Modifique as cores dos gráficos nas funções plotly

### Formações
- Altere as posições no array `positions` da função `create_football_field()`
- Adicione novas formações modificando as coordenadas

### Estatísticas
- Customize as métricas na função `show_player_stats_radar()`
- Adicione novos cálculos de química e valor

## 🔧 Funcionalidades Avançadas

### Sistema de Estados
- A aplicação usa `st.session_state` para navegação
- Estados persistem durante a sessão
- Navegação fluida entre páginas

### Cache de Dados
- `@st.cache_data` otimiza carregamento
- Dados são processados uma vez por sessão
- Performance melhorada

### Interface Responsiva
- Layout adaptativo com colunas
- Design otimizado para desktop e mobile
- Componentes interativos

## 🐛 Solução de Problemas

### Erro de CSV
- Verifique se o arquivo está em `data/players.csv`
- Confirme a codificação (UTF-8 recomendado)
- Teste com um subset menor de dados

### Imagens não carregam
- URLs das fotos podem estar quebradas
- Implemente fallback para imagens locais
- Verifique conexão com internet

### Performance lenta
- Reduza o dataset para testes
- Use `st.cache_data` em mais funções
- Otimize gráficos plotly

## 🌟 Melhorias Futuras

- [ ] Sistema de login/usuários
- [ ] Banco de dados SQL
- [ ] Exportação de relatórios PDF
- [ ] Integração com APIs de futebol
- [ ] Sistema de transferências
- [ ] Análise preditiva com ML
- [ ] Dashboard executivo
- [ ] Modo dark/light

## 📱 Screenshots

### Seleção de Clubes
Interface moderna para escolha dos clubes com visualização de logos e estatísticas.

### Campo Tático
Campo interativo 3D com jogadores posicionados em formação 4-3-3.

### Comparação
Gráficos comparativos detalhados entre clubes.

### Scouting
Sistema avançado de descoberta de talentos.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ para entusiastas de futebol e análise de dados.

---

**Divirta-se explorando os dados do seu clube favorito! ⚽**