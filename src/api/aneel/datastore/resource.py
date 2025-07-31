class Resource:
    """
    Classe base abstrata para representar um recurso genérico dentro do sistema.

    Esta classe define a estrutura comum que todos os recursos devem seguir,
    especialmente a exigência de um identificador único.

    Atributos:
        ID (str): Um identificador único para o recurso. Subclasses são
                  esperadas para sobrescrever este atributo com um valor específico.
                  Idealmente, este ID deve ser um UUID para garantir unicidade global.
    """
    ID: str

class EmpreendimentoGeracaoDistribuida(Resource):
    """
    Representa um recurso de empreendimento de geração distribuída.

    Esta classe herda de `Resource` e define um tipo específico de empreendimento
    de geração distribuída com um identificador único e constante (UUID v4)
    associado a ele.

    Atributos:
        ID (str): O identificador UUID v4 constante para este tipo de recurso
                  de empreendimento de geração distribuída.
                  Valor: "b1bd71e7-d0ad-4214-9053-cbd58e9564a7"
    """
    ID = "b1bd71e7-d0ad-4214-9053-cbd58e9564a7"

