class Task:
    """
    Representa a definição abstrata e as configurações de uma tarefa ou unidade de trabalho.

    Esta classe serve como um modelo base para definir propriedades e comportamentos
    comuns que várias tarefas podem compartilhar, como configurações de conexão,
    políticas de repetição e limites de tempo de execução.

    Atributos:
        CONN (str | None): O nome ou identificador da conexão a ser utilizada pela tarefa.
                           Pode ser `None` se nenhuma conexão específica for necessária,
                           implicando o uso de uma conexão padrão do sistema ou nenhuma.
        POOL (str | None): O nome ou identificador do pool de recursos (por exemplo, pool de conexões,
                           pool de threads, pool de processos) onde a tarefa deve ser executada
                           ou de onde deve obter recursos. `None` implica o uso de um pool padrão.
        RETRIES (int | None): O número máximo de vezes que a tarefa deve ser tentada novamente
                              em caso de falha. Se `None`, a política de repetição padrão do sistema
                              será aplicada (que pode ser zero, ilimitada ou um valor configurado).
        DEPLOY (bool): Indica se a tarefa é designada para implantação.
                       Se `True`, a tarefa é considerada implantável; se `False`, pode ser
                       uma tarefa local ou apenas uma definição abstrata não destinada à implantação.
                       Padrão é `True`.
        RETRY_DELAY: O atraso a ser aplicado entre as tentativas de repetição.
                     O tipo e a interpretação exata (por exemplo, segundos, `timedelta`)
                     dependem da implementação do sistema de execução da tarefa.
                     Se `None`, um atraso padrão do sistema será utilizado.
        EXECUTION_TIMEOUT: O tempo máximo permitido para a execução da tarefa antes que
                           ela seja terminada. O tipo e a interpretação exata (por exemplo,
                           segundos, `timedelta`) dependem da implementação do sistema de execução.
                           Se `None`, nenhum tempo limite explícito é definido ou um tempo limite
                           padrão do sistema é aplicado.
    """
    CONN: str | None = None
    POOL: str | None = None
    RETRIES: int | None = None
    DEPLOY: bool = True
    RETRY_DELAY = None
    EXECUTION_TIMEOUT = None
