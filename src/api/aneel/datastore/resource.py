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
    ID = "b1bd71e7-d0ad-4214-9053-cbd58e9564a7"

class EGDInformacoesTecnicasFotovoltaica(Resource):
    ID = "49fa9ca0-f609-4ae3-a6f7-b97bd0945a3a"

class EGDInformacoesTecnicasEolica(Resource):
    ID = "5f903d78-25ae-4a3f-a2bd-9a93351c59fb"

class EGDInformacoesTecnicasHidreletrica(Resource):
    ID = "c189442a-18f0-44eb-9c89-3b48147a4d65"

class EGDInformacoesTecnicasTermeletrica(Resource):
    ID = "bd1d3783-b389-49d8-a828-a56e193d0671"