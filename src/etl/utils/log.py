import logging
import time
import functools
from datetime import datetime

def setup_log():
    """Configura e retorna um logger customizado."""
    logger = logging.getLogger("AppLogger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Handler para o arquivo
        file_handler = logging.FileHandler("execution_details.log")
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # Handler para o console
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
        stream_handler.setFormatter(stream_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        
    return logger

logger = setup_log()

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp_inicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        params = ", ".join(args_repr + kwargs_repr)
        
        logger.info(f"Iniciando '{func.__name__}' em {timestamp_inicio}")
        logger.info(f"Parâmetros informados: {params}")

        start_time = time.perf_counter()
        
        try:
            resultado = func(*args, **kwargs)

            end_time = time.perf_counter()
            tempo_execucao = end_time - start_time

            logger.info(f"'{func.__name__}' retornou: {resultado!r}")
            logger.info(f"Execução de '{func.__name__}' finalizada. Tempo de execução: {tempo_execucao:.4f} segundos.")
            
            return resultado
            
        except Exception as e:
            end_time = time.perf_counter()
            tempo_execucao = end_time - start_time
            
            logger.exception(f"Erro em '{func.__name__}' após {tempo_execucao:.4f} segundos. Exceção: {e}")
            raise

    return wrapper
