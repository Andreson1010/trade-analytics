# Módulo Especial de Consultoria na Área de Dados com Agentes de IA

## Projeto Prático Para Consultoria na Área de Dados com Agentes de IA

**Deploy de App Para Day Trade Analytics em Tempo Real com Agentes de IA, Groq, DeepSeek e AWS Para Monetização**

---

## 📁 Estrutura do Projeto

```
proj_9/
├── avk_app.py                    # Aplicação Streamlit principal
├── avk_agents.py                 # Módulo de agentes de IA
├── avk_analytics.py              # Módulo de analytics e visualizações
├── avk_data_provider.py          # Módulo de provedores de dados
├── assets/                       # Recursos estáticos (ícones)
│   ├── avk_icon_16x16.png
│   ├── avk_icon_32x32.png
│   ├── avk_icon_64x64.png
│   ├── avk_icon.ico
│   └── avk_icon.jpg
├── scripts/                      # Scripts auxiliares
│   └── gerar_icones_avk.py      # Script para gerar ícones
├── docs/                         # Documentação completa
│   ├── GUIA_DEPLOY_AWS.md        # Guia de deploy na AWS
│   ├── ALTERNATIVAS_YAHOO_FINANCE.md  # Guia de alternativas ao Yahoo Finance
│   └── guia_uv.md               # Guia do UV
├── requirements.txt              # Dependências Python
├── config.env.example            # Exemplo de variáveis de ambiente
├── .gitignore                    # Arquivos ignorados pelo Git
├── LICENSE                       # Licença MIT
├── README.md                     # Este arquivo
└── PRD.md                        # Product Requirements Document
```

---

## Execução Local

### Instalação do UV

O UV é um gerenciador de pacotes Python rápido e moderno. Instale-o seguindo as instruções abaixo:

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/MacOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Ou usando pip:
```bash
pip install uv
```

### Configuração do Ambiente

1. Abra o terminal ou prompt de comando e navegue até a pasta com os arquivos do projeto.

2. **Configure as variáveis de ambiente:**
   ```bash
   # Copie o arquivo de exemplo
   cp config.env.example .env
   
   # Edite o arquivo .env e adicione suas chaves API
   # GROQ_API_KEY=sua_chave_aqui
   ```

3. Crie um ambiente virtual com Python 3.12:
```bash
uv venv dsadeployai
```

3. Ative o ambiente virtual:

   **Windows (PowerShell):**
   ```powershell
   .\dsadeployai\Scripts\Activate.ps1
   ```

   **Windows (CMD):**
   ```cmd
   dsadeployai\Scripts\activate.bat
   ```

   **Linux/MacOS:**
   ```bash
   source dsadeployai/bin/activate
   ```

4. Instale as dependências:
```bash
uv pip install -r requirements.txt
```

### Execução da Aplicação

Execute o comando abaixo e acesse a app pelo navegador:
```bash
streamlit run avk_app.py
```

### Limpeza do Ambiente (Opcional)

Para desativar o ambiente virtual:
```bash
deactivate
```

Para remover o ambiente virtual, simplesmente delete a pasta `dsadeployai`:
```bash
# Windows
rmdir /s dsadeployai

# Linux/MacOS
rm -rf dsadeployai
```

---

## Execução na AWS

### Pré-requisitos

1. Crie sua conta gratuita na AWS.
2. Crie uma instância EC2 da camada gratuita AWS.
3. Acesse a instância pelo terminal conforme mostrado nas aulas.

### Instalação do UV na EC2

Instale o UV na instância EC2 com o comando abaixo:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Ou usando pip:
```bash
pip install uv
```

### Configuração do Projeto

1. Crie a pasta `app` e copie os arquivos do projeto para ela.

2. Navegue até a pasta do projeto:
```bash
cd app
```

3. Crie o ambiente virtual:
```bash
uv venv dsadeployai
```

4. Ative o ambiente virtual:
```bash
source dsadeployai/bin/activate
```

5. Instale as dependências:
```bash
uv pip install -r requirements.txt
```

### Execução da Aplicação

Inicie a app com um dos comandos abaixo:

**Execução normal:**
```bash
streamlit run avk_app.py
```

**Execução em background (recomendado para produção):**
```bash
nohup streamlit run avk_app.py --server.port=8501 --server.address=0.0.0.0 &
```

### Acesso à Aplicação

1. Acesse a app pelo navegador usando o endereço IP público da sua instância EC2 na porta 8501.
2. Resolva problemas de acesso conforme mostrado nas aulas (configuração de Security Groups, etc.).
3. Inicie a monetização da app com seus clientes.

### Nota Importante

⚠️ **Quando terminar seus testes, desligue a instância EC2 conforme mostrado nas aulas para evitar custos desnecessários.**

---

## Vantagens do UV

- ⚡ **Velocidade**: Instalação de pacotes muito mais rápida que pip/conda
- 🔒 **Confiabilidade**: Resolução de dependências mais robusta
- 📦 **Compatibilidade**: Compatível com pip e requirements.txt
- 🚀 **Moderno**: Ferramenta desenvolvida pela Astral (criadores do Ruff)

