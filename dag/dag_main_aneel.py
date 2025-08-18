from datetime import datetime

from src.airflow.dag.base_controller import BaseController as _BaseController
from src.airflow.factory import DAGFactory as _DAGFactory

from dag.stage.aneel.stg_aneel_tasks import StageAneelTasks as _StageAneelTasks
from dag.dw.dw_tasks import DWTasks as _DWTasks

tasks = [_DWTasks, _StageAneelTasks]

controller = _BaseController(
    tasks,
    dag_id='dag_main_aneel',
)

dag = _DAGFactory(
    start_date=datetime(2025, 8, 18),
    schedule='0 0 * * *',
    catchup=False,
    **controller.params()
).create_dag()
