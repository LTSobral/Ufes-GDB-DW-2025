import re as _re
from unicodedata import normalize as _normalize


_TASK_ID_SUB_COMPILE = (
    (_re.compile(r"\W").sub, "_"),
    (_re.compile(r"_{2,}").sub, "_"),
)


def task_id(id: str) -> str:
    """Gera um ID de tarefa padronizado a partir de uma string de entrada.

    Esta função processa uma string para criar um identificador limpo e consistente.
    Ela remove caracteres não alfanuméricos, padroniza múltiplos underscores para um
    único, remove underscores iniciais ou finais, e converte o resultado para
    maiúsculas.

    Args:
        id (str): A string de entrada a ser convertida em um ID de tarefa.

    Returns:
        str: O ID de tarefa padronizado, em maiúsculas e sem caracteres especiais
             ou underscores redundantes.

    Exemplo:
        >>> task_id("Minha Nova Tarefa!")
        'MINHA_NOVA_TAREFA'
        >>> task_id("projeto-x___versao_1.0")
        'PROJETO_X_VERSAO_1_0'
    """
    for sub, char in _TASK_ID_SUB_COMPILE:
        id = sub(char, id)

    return id.strip("_").upper()


def pascal_case_to_snake_case(text: str) -> str:
    """Converte uma string de PascalCase (ou CamelCase) para um formato snake_case.

    Esta função aplica uma série de transformações para converter nomes de variáveis
    ou textos formatados em PascalCase/CamelCase para um formato snake_case.
    Ela lida com múltiplos padrões de capitalização, substitui pontos, caracteres
    não-alfanuméricos e consolida underscores. Adicionalmente, normaliza caracteres
    Unicode (removendo acentos) e converte a string final para minúsculas.

    Args:
        text (str): A string de entrada a ser convertida.

    Returns:
        str: A string convertida para o formato snake_case, normalizada (sem acentos)
             e em minúsculas.

    Exemplos:
        >>> pascal_case_to_snake_case("MinhaVariavelPascalCase")
        'minha_variavel_pascal_case'
        >>> pascal_case_to_snake_case("camelCaseExample")
        'camel_case_example'
        >>> pascal_case_to_snake_case("HTTPResponseCode")
        'http_response_code'
        >>> pascal_case_to_snake_case("String.Com.Pontos_e_Acentos_áéíóú")
        'string__com__pontos_e_acentos_aeiou'
        >>> pascal_case_to_snake_case("Texto Com Espaços e Símbolos!@#")
        'texto_com_espacos_e_simbolos_'
    """
    _text = _re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)

    _text = _re.sub(r"(?<=[a-z])(?=[A-Z])", r"_", _text)

    # Substitui pontos por underscores duplos (comportamento específico da função)
    _text = _re.sub(r"\.", r"__", _text)
    # Substitui caracteres não-palavra por underscores
    _text = _re.sub(r"\W", r"_", _text)
    # Consolida 3 ou mais underscores para 2 (comportamento específico da função)
    _text = _re.sub(r"_{3,}", r"__", _text)
    
    # Normaliza caracteres Unicode (remove acentos, etc.), converte para ASCII,
    # decodifica e transforma em minúsculas
    _text = (
        _normalize("NFD", _text)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .lower()
    )

    return _text

