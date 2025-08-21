from src.airflow.dag.base_controller import BaseController as _BaseController
from src.airflow.factory import DAGFactory as _DAGFactory

from dag.dw.dw_tasks import DWTasks as _DWTasks

controller = _BaseController(
    _DWTasks,
    dag_id='dag_dw_controller',
)

dag = _DAGFactory(**controller.params()).create_dag()
