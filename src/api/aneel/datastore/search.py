import requests as _requests
import time as _time
import warnings as _warnings
import re as _re

from .resource import Resource as _Resource


class Search:
    """
    Classe para interagir com a API de dados abertos da ANEEL,
    especificamente o endpoint `datastore_search`.

    Esta classe facilita a busca e paginação de dados através da API,
    implementando lógica de retentativa para requisições em caso de falha.

    Attributes:
        URI (str): URL base para o endpoint de busca de dados da API da ANEEL.
        RETRY (int): Número máximo de tentativas de requisição antes de falhar
                     definitivamente.
        WAIT_TIME (int): Tempo de espera em segundos entre tentativas consecutivas
                         de requisição.
    """
    URI = 'https://dadosabertos.aneel.gov.br/api/3/action/datastore_search'
    RETRY: int = 3
    WAIT_TIME: int = 120

    def __init__(
        self,
        resource: type[_Resource],
        limit: int | None = None,
        next: int | None = None
    ) -> None:
        """
        Inicializa uma nova instância da classe Search.

        Args:
            resource (type[_Resource]): O tipo de recurso a ser consultado.
                                        Este objeto deve possuir um atributo 'ID'
                                        que representa o ID do recurso na API.
            limit (int | None, optional): O número máximo de registros a serem
                                          retornados por página. Se None, o limite
                                          padrão da API será usado. Defaults to None.
            next (int | None, optional): O offset inicial para a paginação,
                                         indicando o primeiro registro a ser retornado.
                                         Se None, a busca começará do primeiro registro.
                                         Defaults to None.
        """
        self.resource = resource
        self.limit = limit
        self.next = next

    @staticmethod
    def _decorator_retry(func):
        """
        Decorador estático para adicionar lógica de retentativa a uma função.

        Este decorador executa a função decorada e, em caso de exceção,
        tenta novamente por um número máximo de vezes (definido por `Search.RETRY`),
        esperando um tempo (definido por `Search.WAIT_TIME`) entre as tentativas.
        Emite avisos (`warnings`) sobre as tentativas e falhas.

        Raises:
            Exception: A exceção original que causou a falha, após esgotar
                       o número máximo de tentativas.

        Args:
            func (callable): A função a ser decorada com a lógica de retentativa.

        Returns:
            callable: A função 'wrapper' que encapsula a lógica de retentativa.
        """
        def wrapper(*args, **kwargs):
            retry_count = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    _warnings.warn(f"Tentativa {retry_count+1}/{Search.RETRY}: {e}")
                    retry_count += 1

                    if Search.RETRY < retry_count:
                        _warnings.warn("Número máximo de tentativas atingido. Falha ao executar o job.")
                        raise e
                _time.sleep(Search.WAIT_TIME)
        return wrapper

    @_decorator_retry
    def get(self, params: dict):
        """
        Realiza uma requisição GET para a URI da API da ANEEL.

        Esta função utiliza o decorador de retentativa (`_decorator_retry`)
        para garantir que a requisição seja tentada múltiplas vezes em caso de falha.

        Args:
            params (dict): Um dicionário de parâmetros de consulta a serem
                           enviados na requisição GET.

        Returns:
            _requests.Response: O objeto de resposta da requisição HTTP.

        Raises:
            requests.exceptions.RequestException: Em caso de falha na requisição
                                                  (por exemplo, problema de conexão,
                                                  tempo limite).
            requests.exceptions.HTTPError: Para respostas de status HTTP ruins (4xx ou 5xx),
                                           levantado por `response.raise_for_status()`.
        """
        response = _requests.get(self.URI, params=params)
        response.raise_for_status()
        return response

    def _get_dict(self, dict, key):
        """
        Método auxiliar para obter um valor de um dicionário de forma segura.

        Se a chave não for encontrada ou o valor associado for falso (ex: None, 0, ""),
        um aviso será emitido.

        Args:
            dict (dict): O dicionário do qual o valor será extraído.
            key (str): A chave a ser procurada no dicionário.

        Returns:
            Any | None: O valor associado à chave, ou None se a chave não for
                        encontrada ou o valor for avaliado como falso.
        """
        __value = dict.get(key)
        if __value:
            return __value

        _warnings.warn('Próxima pagina não encontrada.')
        return None # Explicitly return None if no value found/is falsy

    def _get_offset(self, response: _requests.Response):
        """
        Extrai o valor do offset da próxima página a partir de um objeto de
        resposta da API da ANEEL.

        Esta função navega pela estrutura JSON da resposta (result -> _links -> next)
        para encontrar o URL do próximo link de paginação e, em seguida,
        usa expressão regular para extrair o valor numérico do parâmetro 'offset'
        desse URL.

        Args:
            response (_requests.Response): O objeto de resposta HTTP da API.

        Returns:
            int | None: O valor do offset para a próxima página como um inteiro,
                        ou None se o link do próximo offset não for encontrado
                        ou o offset não puder ser extraído.
        """
        if result := self._get_dict(response.json(), 'result'):
            if links := self._get_dict(result, '_links'):
                if next_link := self._get_dict(links, 'next'): # Renomeado 'next' para 'next_link' para evitar conflito com built-in
                    if match:= _re.search(r'offset=(\d+)', next_link):
                        return int(match.group(1))
        return None # Explicitly return None if no offset found

    def page(self) -> _requests.Response:
        """
        Prepara e executa uma requisição GET para obter uma única página
        de dados do recurso especificado na API da ANEEL.

        Os parâmetros de busca (`resource_id`, `offset`, `limit`) são
        construídos com base nos atributos da instância (`self.resource.ID`,
        `self.next`, `self.limit`). Parâmetros com valor None são ignorados
        na requisição final.

        Returns:
            _requests.Response: O objeto de resposta da requisição HTTP,
                                contendo os dados da página.
        """
        params = {
            'resource_id': self.resource.ID,
            'offset': self.next,
            'limit': self.limit,
        }

        # Filtra parâmetros que são None
        params = {
            k: v
            for k, v in params.items()
            if v is not None # Changed from `if v` to `if v is not None` to be more precise.
        }

        return self.get(params)

    def iterpage(self):
        """
        Gera um iterador que percorre todas as páginas de resultados da API.

        Este método faz requisições sucessivas (`self.page()`), yieldindo
        cada resposta da página. Ele atualiza automaticamente o `self.next`
        com o offset da próxima página, conforme extraído da resposta da API.
        A iteração continua enquanto um novo offset para a próxima página
        for encontrado e for diferente do offset atual.

        Yields:
            _requests.Response: O objeto de resposta da requisição HTTP
                                para cada página de dados.
        """
        while True:
            response = self.page()
            new_offset = self._get_offset(response)
            self.next = new_offset

            if not response.json().get('result', {'records': []}).get('records'):
                break

            yield response
