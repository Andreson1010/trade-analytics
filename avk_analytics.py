# Módulo de Analytics
# Funções para extração de dados e visualização de ações

# Imports
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

########## Analytics ##########

# Nota: A função avk_extrai_dados está em avk_data_provider.py
# e é importada diretamente em avk_app.py quando necessário

# Define a função para plotar o preço das ações com base no histórico fornecido
def avk_plot_stock_price(hist, ticker):
    # Cria um gráfico de linha interativo usando Plotly Express
    # O eixo X representa a data e o eixo Y representa o preço de fechamento das ações
    # O título do gráfico inclui o ticker da ação e o período de análise
    fig = px.line(hist, x="Date", y="Close", title=f"{ticker} Preços das Ações (Últimos 6 Meses)", markers=True)
    
    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

# Define a função para plotar um gráfico de candlestick com base no histórico fornecido
def avk_plot_candlestick(hist, ticker):

    # Cria um objeto Figure do Plotly para armazenar o gráfico
    fig = go.Figure(

        # Adiciona um gráfico de candlestick com os dados do histórico da ação
        data=[go.Candlestick(x=hist['Date'],        # Define as datas no eixo X
                             open=hist['Open'],     # Define os preços de abertura
                             high=hist['High'],     # Define os preços mais altos
                             low=hist['Low'],       # Define os preços mais baixos
                             close=hist['Close'])]  # Define os preços de fechamento
    )
    
    # Atualiza o layout do gráfico, incluindo um título dinâmico com o ticker da ação
    fig.update_layout(title=f"{ticker} Candlestick Chart (Últimos 6 Meses)")
    
    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

# Define a função para plotar médias móveis com base no histórico fornecido
def avk_plot_media_movel(hist, ticker):

    # Calcula a Média Móvel Simples (SMA) de 20 períodos e adiciona ao DataFrame
    hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
    
    # Calcula a Média Móvel Exponencial (EMA) de 20 períodos e adiciona ao DataFrame
    hist['EMA_20'] = hist['Close'].ewm(span=20, adjust=False).mean()
    
    # Cria um gráfico de linha interativo usando Plotly Express
    # Plota os preços de fechamento, a SMA de 20 períodos e a EMA de 20 períodos
    fig = px.line(hist, 
                  x='Date', 
                  y=['Close', 'SMA_20', 'EMA_20'],
                  title=f"{ticker} Médias Móveis (Últimos 6 Meses)",  # Define o título do gráfico
                  labels={'value': 'Price (USD)', 'Date': 'Date'})    # Define os rótulos dos eixos
    
    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

# Define a função para plotar o volume de negociação da ação com base no histórico fornecido
def avk_plot_volume(hist, ticker):

    # Cria um gráfico de barras interativo usando Plotly Express
    # O eixo X representa a data e o eixo Y representa o volume negociado
    fig = px.bar(hist, 
                 x='Date', 
                 y='Volume', 
                 title=f"{ticker} Trading Volume (Últimos 6 Meses)")  # Define o título do gráfico
    
    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

