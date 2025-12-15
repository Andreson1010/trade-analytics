# Módulo Especial de Consultoria na Área de Dados com Agentes de IA
# Projeto Prático Para Consultoria na Área de Dados com Agentes de IA
# Deploy de App Para Day Trade Analytics em Tempo Real com Agentes de IA, Groq, DeepSeek e AWS Para Monetização

# Import do Streamlit deve ser o primeiro
import streamlit as st

# Configuração da página do Streamlit DEVE ser a primeira chamada
st.set_page_config(page_title="Aivoraq_Agência de IA", page_icon="assets/avk_icon_32x32.png", layout="wide")

# Imports restantes após st.set_page_config
from yfinance.exceptions import YFRateLimitError
from avk_data_provider import avk_extrai_dados
from avk_analytics import (
    avk_plot_stock_price,
    avk_plot_candlestick,
    avk_plot_media_movel,
    avk_plot_volume
)
from avk_agents import multi_ai_agent, limpar_resposta_ia

########## App Web ##########

# Barra Lateral com instruções
st.sidebar.title("Instruções")
st.sidebar.markdown("""
### Como Utilizar a App:

- Insira o símbolo do ticker da ação desejada no campo central.
- Clique no botão **Analisar** para obter a análise em tempo real com visualizações e insights gerados por IA.

### Exemplos de tickers válidos:
- MSFT (Microsoft)
- TSLA (Tesla)
- AMZN (Amazon)
- GOOG (Alphabet)

Mais tickers podem ser encontrados aqui: https://stockanalysis.com/list/nasdaq-stocks/

### Finalidade da App:
Este aplicativo realiza análises avançadas de preços de ações da Nasdaq em tempo real utilizando Agentes de IA com modelo DeepSeek através do Groq e infraestrutura AWS para apoio a estratégias de Day Trade para monetização. Uma app completa de exemplo para quem deseja iniciar em Consultoria na Área de Dados e IA.

### ⚠️ Sobre Rate Limits:
O Yahoo Finance limita o número de requisições. Se você receber um erro de rate limit, aguarde 2-3 minutos antes de tentar novamente. Os dados são armazenados em cache por 5 minutos para otimizar o uso.
""")

# Botão de suporte na barra lateral
if st.sidebar.button("Suporte"):
    st.sidebar.write("No caso de dúvidas envie e-mail para: suporte@aivoraq.com.br")

# Título principal
st.title("Aivoraq - Agência de IA")

# Interface principal
st.header("Day Trade Analytics em Tempo Real com Agentes de IA")

# Caixa de texto para input do usuário
ticker = st.text_input("Digite o Código (símbolo do ticker):").upper()

# Se o usuário pressionar o botão, entramos neste bloco
if st.button("Analisar"):

    # Se temos o código da ação (ticker)
    if ticker:

        # Inicia o processamento
        try:
            with st.spinner("Buscando os Dados em Tempo Real. Aguarde..."):
                
                # Obtém os dados com tratamento de erro
                try:
                    hist = avk_extrai_dados(ticker)
                except YFRateLimitError as e:
                    st.error("⚠️ **Rate Limit do Yahoo Finance**")
                    st.warning(
                        "Muitas requisições foram feitas ao Yahoo Finance. Por favor, aguarde alguns minutos antes de tentar novamente.\n\n"
                        "**Dicas:**\n"
                        "- O cache está ativo por 5 minutos, então dados recentes podem ser reutilizados\n"
                        "- Tente novamente em 2-3 minutos\n"
                        "- Evite fazer múltiplas requisições em sequência"
                    )
                    st.stop()
                except ValueError as e:
                    st.error(f"❌ Erro: {str(e)}")
                    st.info("Verifique se o ticker está correto e tente novamente.")
                    st.stop()
                except Exception as e:
                    st.error(f"❌ Erro ao buscar dados: {str(e)}")
                    st.info("Por favor, tente novamente mais tarde.")
                    st.stop()
                
                # Renderiza um subtítulo
                st.subheader("Análise Gerada Por IA")
                
                # Executa o time de Agentes de IA
                try:
                    ai_response = multi_ai_agent.run(f"Resumir a recomendação do analista e compartilhar as últimas notícias para {ticker}")

                    # Limpa a resposta removendo linhas indesejadas
                    clean_response = limpar_resposta_ia(ai_response.content)

                    # Imprime a resposta
                    st.markdown(clean_response)
                except Exception as e:
                    st.warning(f"⚠️ Erro ao gerar análise por IA: {str(e)}")
                    st.info("Os gráficos ainda estão disponíveis abaixo.")

                # Renderiza os gráficos
                st.subheader("Visualização dos Dados")
                avk_plot_stock_price(hist, ticker)
                avk_plot_candlestick(hist, ticker)
                avk_plot_media_movel(hist, ticker)
                avk_plot_volume(hist, ticker)
                
        except Exception as e:
            st.error(f"❌ Erro inesperado: {str(e)}")
            st.info("Por favor, tente novamente ou entre em contato com o suporte.")
    else:
        st.error("Ticker inválido. Insira um símbolo de ação válido.")


# Fim
# Obrigado Aivorak - Agência de IA!
