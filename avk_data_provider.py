# Módulo de Provedores de Dados Financeiros
# Suporta múltiplas fontes de dados para evitar rate limits

# Imports
import os
import time
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import yfinance as yf
from yfinance.exceptions import YFRateLimitError

# Tente importar Streamlit (opcional, para uso em scripts não-Streamlit)
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    st = None

# Tente importar Alpha Vantage (opcional)
try:
    from alpha_vantage.timeseries import TimeSeries
    ALPHA_VANTAGE_AVAILABLE = True
except ImportError:
    ALPHA_VANTAGE_AVAILABLE = False

########## Configuração de Provedores ##########

# Configuração padrão - pode ser alterada via variável de ambiente
def _get_config(key: str, default: str = "") -> str:
    """Obtém configuração de st.secrets ou variável de ambiente (lazy evaluation)"""
    # Primeiro tenta variável de ambiente
    env_value = os.getenv(key, "")
    if env_value:
        return env_value
    
    # Depois tenta st.secrets (apenas se Streamlit estiver disponível e configurado)
    if STREAMLIT_AVAILABLE and st is not None:
        try:
            # Verifica se st.secrets está disponível (após set_page_config)
            if hasattr(st, 'secrets') and st.secrets is not None:
                secrets_value = st.secrets.get(key, "")
                if secrets_value:
                    return secrets_value
        except:
            pass
    
    return default

# Valores padrão - serão atualizados quando necessário
DATA_PROVIDER = os.getenv("DATA_PROVIDER", "yfinance")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")

########## Funções de Extração de Dados ##########

def _extrai_dados_yfinance(ticker: str, period: str = "6mo", max_retries: int = 3, retry_delay: int = 5) -> pd.DataFrame:
    """
    Extrai dados usando Yahoo Finance (método original).
    
    Args:
        ticker: Símbolo da ação
        period: Período dos dados
        max_retries: Número máximo de tentativas
        retry_delay: Tempo de espera entre tentativas
    
    Returns:
        DataFrame com dados históricos
    """
    for tentativa in range(max_retries):
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                raise ValueError(f"Nenhum dado encontrado para o ticker {ticker}")
            
            hist.reset_index(inplace=True)
            return hist
            
        except YFRateLimitError as e:
            if tentativa < max_retries - 1:
                time.sleep(retry_delay * (tentativa + 1))
                continue
            else:
                raise e
        except Exception as e:
            raise e

def _extrai_dados_alpha_vantage(ticker: str, period: str = "6mo", api_key: Optional[str] = None) -> pd.DataFrame:
    """
    Extrai dados usando Alpha Vantage API.
    
    Args:
        ticker: Símbolo da ação
        period: Período dos dados (convertido para intervalo da API)
        api_key: Chave da API Alpha Vantage
    
    Returns:
        DataFrame com dados históricos no mesmo formato do yfinance
    """
    if not ALPHA_VANTAGE_AVAILABLE:
        raise ImportError("Biblioteca alpha_vantage não está instalada. Instale com: pip install alpha-vantage")
    
    if not api_key:
        api_key = ALPHA_VANTAGE_API_KEY
        if not api_key:
            raise ValueError("Chave da API Alpha Vantage não fornecida. Configure ALPHA_VANTAGE_API_KEY")
    
    ts = TimeSeries(key=api_key, output_format='pandas')
    
    # Mapeia period para intervalo da API
    # Alpha Vantage suporta: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'
    interval = 'daily'
    
    # Calcula a data de início baseado no período
    period_days = {
        '1d': 1, '5d': 5, '1mo': 30, '3mo': 90, 
        '6mo': 180, '1y': 365, '2y': 730, '5y': 1825, '10y': 3650, 'ytd': 365, 'max': 3650
    }
    days = period_days.get(period, 180)
    
    try:
        # Obtém dados diários usando endpoint gratuito (get_daily)
        # get_daily_adjusted é premium, então usamos get_daily
        # outputsize='full' também é premium, então usamos apenas 'compact' (gratuito)
        # 'compact' retorna os últimos 100 pontos de dados, que é suficiente para análise de 6 meses
        data, meta_data = ts.get_daily(symbol=ticker, outputsize='compact')
        
        # Verifica se a resposta contém erro da API
        if isinstance(meta_data, dict):
            if 'Error Message' in meta_data:
                error_msg = meta_data['Error Message']
                if 'Invalid API call' in error_msg or 'API call frequency' in error_msg:
                    raise ValueError(f"Alpha Vantage API Error: {error_msg}")
                if 'Thank you for using Alpha Vantage' in error_msg:
                    raise ValueError("Alpha Vantage: Limite de chamadas excedido ou chave API inválida")
        
        # Verifica se data está vazio ou None
        if data is None or (isinstance(data, pd.DataFrame) and data.empty):
            raise ValueError(f"Nenhum dado encontrado para o ticker {ticker} no Alpha Vantage")
        
        # Verifica se data é um DataFrame válido
        if not isinstance(data, pd.DataFrame):
            raise ValueError(f"Resposta inválida do Alpha Vantage para {ticker}")
        
        # Converte índice para coluna Date
        data.reset_index(inplace=True)
        if 'date' in data.columns:
            data.rename(columns={'date': 'Date'}, inplace=True)
        
        # Verifica se temos a coluna Date
        if 'Date' not in data.columns and data.index.name != 'date':
            # Tenta encontrar coluna de data
            date_cols = [col for col in data.columns if 'date' in col.lower() or 'time' in col.lower()]
            if date_cols:
                data.rename(columns={date_cols[0]: 'Date'}, inplace=True)
            else:
                raise ValueError("Não foi possível encontrar coluna de data na resposta do Alpha Vantage")
        
        # Converte Date para datetime
        data['Date'] = pd.to_datetime(data['Date'])
        
        # Filtra pelos últimos N dias
        cutoff_date = datetime.now() - timedelta(days=days)
        data = data[data['Date'] >= cutoff_date].copy()
        
        if data.empty:
            raise ValueError(f"Nenhum dado encontrado para o período solicitado ({period})")
        
        # Mapeia colunas do Alpha Vantage para o formato esperado
        # get_daily retorna: '1. open', '2. high', '3. low', '4. close', '5. volume'
        # (sem adjusted close, que só está disponível no endpoint premium)
        column_mapping = {
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        }
        
        # Renomeia colunas
        for old_name, new_name in column_mapping.items():
            if old_name in data.columns:
                data.rename(columns={old_name: new_name}, inplace=True)
        
        # Seleciona apenas as colunas necessárias
        required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        available_cols = [col for col in required_cols if col in data.columns]
        
        if len(available_cols) < 2:  # Precisa pelo menos Date e uma coluna de preço
            raise ValueError(f"Colunas insuficientes na resposta do Alpha Vantage. Colunas encontradas: {list(data.columns)}")
        
        data = data[available_cols].copy()
        
        # Ordena por data (mais antiga primeiro)
        data = data.sort_values('Date').reset_index(drop=True)
        
        return data
        
    except ValueError as e:
        # Re-lança ValueError sem modificar
        raise e
    except KeyError as e:
        raise ValueError(f"Erro ao processar resposta do Alpha Vantage: estrutura de dados inesperada - {str(e)}")
    except Exception as e:
        error_msg = str(e)
        # Verifica se é erro de JSON parsing
        if "Expecting value" in error_msg or "JSON" in error_msg:
            raise ValueError(
                f"Alpha Vantage retornou resposta inválida para {ticker}. "
                f"Possíveis causas: chave API inválida, limite excedido, ou ticker não encontrado. "
                f"Erro: {error_msg}"
            )
        raise Exception(f"Erro ao obter dados do Alpha Vantage: {error_msg}")

def _avk_extrai_dados_impl(ticker: str, period: str = "6mo", max_retries: int = 3, retry_delay: int = 5, 
                           provider: Optional[str] = None, api_key: Optional[str] = None) -> pd.DataFrame:
    """
    Extrai dados históricos de uma ação usando o provedor configurado.
    
    Args:
        ticker: Símbolo da ação
        period: Período dos dados (padrão: 6 meses)
        max_retries: Número máximo de tentativas (apenas para yfinance)
        retry_delay: Tempo de espera entre tentativas (apenas para yfinance)
        provider: Provedor a usar ('yfinance' ou 'alpha_vantage'). Se None, usa DATA_PROVIDER
        api_key: Chave da API (necessária para Alpha Vantage)
    
    Returns:
        DataFrame com dados históricos no formato padrão (Date, Open, High, Low, Close, Volume)
    
    Raises:
        Exception: Se não conseguir obter os dados
    """
    if provider is None:
        # Tenta obter do config (pode usar st.secrets se disponível)
        provider = _get_config("DATA_PROVIDER", DATA_PROVIDER)
    
    if api_key is None and provider == "alpha_vantage":
        # Tenta obter do config (pode usar st.secrets se disponível)
        api_key = _get_config("ALPHA_VANTAGE_API_KEY", ALPHA_VANTAGE_API_KEY)
    
    # Tenta usar o provedor especificado, com fallback para yfinance
    if provider == "alpha_vantage":
        # Verifica se a chave API está configurada
        if not api_key or api_key.strip() == "":
            # Se não tem chave, usa yfinance diretamente sem tentar Alpha Vantage
            if STREAMLIT_AVAILABLE:
                st.info("ℹ️ Alpha Vantage não configurado. Usando Yahoo Finance.")
            return _extrai_dados_yfinance(ticker, period, max_retries, retry_delay)
        
        try:
            return _extrai_dados_alpha_vantage(ticker, period, api_key)
        except (ValueError, ImportError) as e:
            # Para erros conhecidos (chave inválida, limite excedido, etc), usa fallback silenciosamente
            if STREAMLIT_AVAILABLE:
                # Só mostra warning se for um erro inesperado
                if "chave API inválida" in str(e).lower() or "limite excedido" in str(e).lower():
                    st.info(f"ℹ️ Alpha Vantage indisponível. Usando Yahoo Finance como alternativa.")
                else:
                    st.warning(f"⚠️ Alpha Vantage: {str(e)}. Usando Yahoo Finance como alternativa.")
            return _extrai_dados_yfinance(ticker, period, max_retries, retry_delay)
        except Exception as e:
            # Para outros erros, tenta fallback
            if STREAMLIT_AVAILABLE:
                st.warning(f"⚠️ Erro com Alpha Vantage. Usando Yahoo Finance como alternativa.")
            return _extrai_dados_yfinance(ticker, period, max_retries, retry_delay)
    else:
        # Usa yfinance por padrão
        return _extrai_dados_yfinance(ticker, period, max_retries, retry_delay)

# Função pública com cache do Streamlit
if STREAMLIT_AVAILABLE:
    @st.cache_data(ttl=300, show_spinner=False)
    def avk_extrai_dados(ticker: str, period: str = "6mo", max_retries: int = 3, retry_delay: int = 5, 
                         provider: Optional[str] = None, api_key: Optional[str] = None) -> pd.DataFrame:
        """Wrapper com cache para uso no Streamlit"""
        return _avk_extrai_dados_impl(ticker, period, max_retries, retry_delay, provider, api_key)
else:
    # Sem cache se não estiver no Streamlit
    def avk_extrai_dados(ticker: str, period: str = "6mo", max_retries: int = 3, retry_delay: int = 5, 
                         provider: Optional[str] = None, api_key: Optional[str] = None) -> pd.DataFrame:
        """Wrapper sem cache para uso fora do Streamlit"""
        return _avk_extrai_dados_impl(ticker, period, max_retries, retry_delay, provider, api_key)

