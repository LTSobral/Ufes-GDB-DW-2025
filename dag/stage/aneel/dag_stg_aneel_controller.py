from src.airflow.dag.base_controller import BaseController as _BaseController
from src.airflow.factory import DAGFactory as _DAGFactory

from dag.stage.aneel.stg_aneel_tasks import StageAneelTasks as _StageAneelTasks

controller = _BaseController(
    _StageAneelTasks,
    dag_id='dag_stg_aneel_controller',
)

dag = _DAGFactory(**controller.params()).create_dag()
