import requests as _requests
import time as _time
import warnings as _warnings
import re as _re

from .resource import Resource as _Resource


class Search:
    URI = 'https://dadosabertos.aneel.gov.br/api/3/action/datastore_search'
    RETRY: int = 3
    WAIT_TIME: int = 120

    def __init__(
        self,
        resource: type[_Resource],
        limit: int | None = None,
        next: int | None = None
    ) -> None:
        self.resource = resource
        self.limit = limit
        self.next = next

    @staticmethod
    def _decorator_retry(func):
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
        response = _requests.get(self.URI, params=params)
        response.raise_for_status()
        return response

    def _get_dict(self, dict, key):
        __value = dict.get(key)
        if __value:
            return __value

        _warnings.warn('Próxima pagina não encontrada.')

    def _get_offset(self, response: _requests.Response):
        if result := self._get_dict(response.json(), 'result'):
            if links := self._get_dict(result, '_links'):
                if next := self._get_dict(links, 'next'):
                    if match:= _re.search(r'offset=(\d+)', next):
                        return int(match.group(1))

    def page(self):
        params = {
            'resource_id': self.resource.ID,
            'offset': self.next,
            'limit': self.limit,
        }

        params = {
            k: v
            for k, v in params.items()
            if v
        }

        return self.get(params)

    def iterpage(self):
        while True:
            response = self.page()
            yield response
            new_offset = self._get_offset(response)

            if new_offset is None or new_offset == self.next:
                break
            self.next = new_offset
