# Módulo de Agentes de IA
# Configuração e gerenciamento dos agentes de IA

# Imports
import re
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools

# Carrega o arquivo de variáveis de ambiente
load_dotenv()

########## Agentes de IA ##########

# Agentes de IA 
# Agente financeiro: análise de dados financeiros e notícias via YFinanceTools
avk_agente_financeiro = Agent(name="AVK Agente Financeiro",
                              model=Groq(id="llama-3.3-70b-versatile"),
                              description="Fazer análise financeira de ações e buscar notícias relevantes",
                              tools=[YFinanceTools(stock_price=True,
                                                   analyst_recommendations=True,
                                                   stock_fundamentals=True,
                                                   company_news=True)],
                              instructions=[
                                  "Use tabelas para mostrar os dados",
                                  "Sempre inclua as fontes das notícias",
                                  "Busque notícias recentes sobre a empresa para complementar a análise",
                                  "Foque em usar stock_price, stock_fundamentals e company_news para análise",
                                  "Se uma ferramenta falhar, continue com as outras disponíveis"
                              ],
                              show_tool_calls=True, markdown=True)

# Multi-agente: usa apenas o agente financeiro (que já tem acesso a notícias via YFinanceTools)
# Nota: Removemos o agente de busca web devido a problemas com tipos de parâmetros no phidata
multi_ai_agent = Agent(team=[avk_agente_financeiro],
                       model=Groq(id="llama-3.3-70b-versatile"),
                       instructions=[
                           "Sempre inclua as fontes",
                           "Use tabelas para mostrar os dados",
                           "Combine dados financeiros com notícias recentes para uma análise completa",
                           "Se uma ferramenta não estiver disponível ou falhar, continue com outras ferramentas",
                           "Foque em fornecer análise útil mesmo se algumas ferramentas não funcionarem"
                       ],
                       show_tool_calls=True, markdown=True)

def limpar_resposta_ia(ai_response_content):
    """
    Remove linhas indesejadas da resposta do agente de IA.
    
    Args:
        ai_response_content: Conteúdo da resposta do agente de IA
    
    Returns:
        String com a resposta limpa
    """
    # Remove linhas que começam com "Running:" ou "Running "
    # Remove o bloco "Running:" e também linhas "transfer_task_to_finance_ai_agent"
    # Remove também linhas que contenham "Running avk_extrai_dados"
    clean_response = ai_response_content
    # Remove blocos "Running:" com múltiplas linhas
    clean_response = re.sub(r"Running:[\s\S]*?\n\n", "", clean_response, flags=re.MULTILINE)
    # Processa linha por linha para remover linhas indesejadas
    lines = clean_response.split('\n')
    filtered_lines = []
    for line in lines:
        # Remove linhas que começam com "Running" ou contêm "Running avk_extrai_dados"
        if line.strip().startswith('Running') or ('Running' in line and 'avk_extrai_dados' in line):
            continue
        # Remove linhas "transfer_task_to_finance_ai_agent"
        if 'transfer_task_to_finance_ai_agent' in line:
            continue
        filtered_lines.append(line)
    clean_response = '\n'.join(filtered_lines).strip()
    return clean_response

