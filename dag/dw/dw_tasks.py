from .task_factory import (
    TaskFactory as _TaskFactory,
    ConfigTask as _ConfigTask,
)

from src.airflow.factory.tasks import Tasks as _Tasks
from src.airflow.config.pool import Pool as _Pool

from etl.dw import (
    DimensionCidade,
    DimensionCompetencia,
    DimensionEmpresaDistribuidora,
    DimensionGeracao,
    DimensionGrupoTarifario,
    DimensionTipoConsumidor,
    DimensionData,
    FactGeracaoDistribuida,
    FactHistoricoGeracaoDistribuida,
)


class ConfigDefault(_ConfigTask):
    POOL = _Pool.LEVE
    CONN = _ConfigTask.DEFAULT


class ConfigMongo(_ConfigTask):
    POOL = _Pool.LEVE
    CONN = _ConfigTask.MONGO


class DWTasks(_Tasks):
    ALL_TASKS = {
        ConfigMongo: [
            DimensionCidade,
            DimensionEmpresaDistribuidora,
            DimensionGeracao,
            DimensionGrupoTarifario,
            DimensionTipoConsumidor,
            FactGeracaoDistribuida,
            FactHistoricoGeracaoDistribuida,
        ],
        ConfigDefault: [
            DimensionCompetencia,
            DimensionData,
        ],
    }

    TASKS = [
        _TaskFactory(s, k).get_task
        for k, v in ALL_TASKS.items()
        for s in v
    ]

    DEPENDENCIES = {
        'f_geracao_distribuida': [
            'd_cidade',
            'd_competencia',
            'd_empresa_distribuidora',
            'd_geracao',
            'd_grupo_tarifario',
            'd_tipo_consumidor',
            'stg_aneel_egd_informacoes_tecnicas',
        ],
        'f_historico_geracao_distribuida': [
            'd_cidade',
            'd_data',
            'd_empresa_distribuidora',
            'd_geracao',
            'd_grupo_tarifario',
            'd_tipo_consumidor',
            'stg_aneel_egd_informacoes_tecnicas',
        ],
        'd_cidade': ['stg_aneel_empreendimento_geracao_distribuida'],
        'd_empresa_distribuidora': ['stg_aneel_empreendimento_geracao_distribuida'],
        'd_geracao': ['stg_aneel_empreendimento_geracao_distribuida'],
        'd_grupo_tarifario': ['stg_aneel_empreendimento_geracao_distribuida'],
        'd_tipo_consumidor': ['stg_aneel_empreendimento_geracao_distribuida'],
    }
