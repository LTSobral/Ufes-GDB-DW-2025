class Pool:
    """
    Define e agrupa constantes relacionadas a níveis de consumo de energia
    e entidades reguladoras.

    Esta classe atua como um repositório centralizado para valores
    string pré-definidos que representam categorias ou agências
    relevantes no contexto de sistemas elétricos ou de energia.
    """

    ANEEL = 'ANEEL'
    """
    Representa a Agência Nacional de Energia Elétrica (ANEEL).
    
    É o órgão regulador do setor elétrico brasileiro.
    """

    LEVE = "leve"
    """
    Define o nível de consumo 'leve'.
    
    Frequentemente utilizado para classificar demandas ou cargas de baixa intensidade.
    """

    MEDIA = "media"
    """
    Define o nível de consumo 'médio'.
    
    Usado para classificar demandas ou cargas de intensidade intermediária.
    """

    PESADA = "pesada"
    """
    Define o nível de consumo 'pesado'.
    
    Aplicado para classificar demandas ou cargas de alta intensidade.
    """
