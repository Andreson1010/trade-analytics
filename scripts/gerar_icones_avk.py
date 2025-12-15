"""
Script para gerar ícones AVK em múltiplos formatos
Execute: python gerar_icones_avk.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

def criar_icone_avk(tamanho, formato, nome_arquivo):
    """
    Cria um ícone com o texto "AVK"
    
    Args:
        tamanho: tupla (largura, altura)
        formato: formato da imagem ('PNG', 'ICO', 'JPEG')
        nome_arquivo: nome do arquivo de saída
    """
    # Cria uma imagem com fundo transparente (PNG) ou branco (JPG)
    if formato == 'JPEG':
        img = Image.new('RGB', tamanho, color='#1E3A8A')  # Azul escuro
    else:
        img = Image.new('RGBA', tamanho, color=(30, 58, 138, 255))  # Azul escuro com transparência
    
    draw = ImageDraw.Draw(img)
    
    # Tenta carregar uma fonte, se não encontrar usa a padrão
    try:
        # Tenta usar fonte do sistema (Windows)
        font_size = int(tamanho[0] * 0.5)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            # Tenta usar fonte do sistema (Linux/Mac)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            # Usa fonte padrão
            font = ImageFont.load_default()
            font_size = int(tamanho[0] * 0.3)
    
    # Texto "AVK"
    texto = "AVK"
    
    # Calcula a posição central do texto
    bbox = draw.textbbox((0, 0), texto, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (tamanho[0] - text_width) // 2
    y = (tamanho[1] - text_height) // 2 - bbox[1]
    
    # Desenha o texto em branco
    draw.text((x, y), texto, fill='white', font=font)
    
    # Salva a imagem
    if formato == 'ICO':
        # Para ICO, precisa de múltiplos tamanhos
        img.save(nome_arquivo, format='ICO', sizes=[(tamanho[0], tamanho[1])])
    else:
        img.save(nome_arquivo, format=formato)
    
    print(f"✓ Criado: {nome_arquivo} ({tamanho[0]}x{tamanho[1]})")

def main():
    """Gera todos os ícones AVK"""
    
    # Cria pasta assets se não existir
    os.makedirs('assets', exist_ok=True)
    
    print("Gerando ícones AVK...\n")
    
    # 1. PNG 16x16 (favicon pequeno)
    criar_icone_avk((16, 16), 'PNG', 'assets/avk_icon_16x16.png')
    
    # 2. PNG 32x32 (favicon HD)
    criar_icone_avk((32, 32), 'PNG', 'assets/avk_icon_32x32.png')
    
    # 3. PNG 64x64 (tamanho médio)
    criar_icone_avk((64, 64), 'PNG', 'assets/avk_icon_64x64.png')
    
    # 4. ICO (formato Windows, multi-resolução)
    criar_icone_avk((32, 32), 'ICO', 'assets/avk_icon.ico')
    
    # 5. JPG 32x32 (alternativa)
    criar_icone_avk((32, 32), 'JPEG', 'assets/avk_icon.jpg')
    
    print("\n✅ Todos os ícones foram gerados com sucesso!")
    print("📁 Arquivos salvos na pasta 'assets/'")
    print("\nPara usar no Streamlit, atualize a linha 129 do avk_app.py:")
    print('   st.set_page_config(page_icon="assets/avk_icon_32x32.png")')

if __name__ == "__main__":
    main()