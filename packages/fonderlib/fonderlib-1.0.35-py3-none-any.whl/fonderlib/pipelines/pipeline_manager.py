import logging
import time
from typing import Dict, List, Optional, Any
from ..tasks.task import Task
from ..tasks.task_result import TaskResult
from ..common.logger import get_logger
from abc import ABC


class PipelineManager(ABC):
    logger: logging.Logger = get_logger("PipelineManager", level="DEBUG")

    def __init__(self, limit: int = 100, days: int = 60):
        self.limit = limit
        self.days = days

        self.tasks: Dict[str, Task] = {}
        self.task_dependencies: Dict[str, List[str]] = {}
        self.task_results: Dict[str, TaskResult] = {}
        self.context: Dict[str, Any] = {}

    def register_task(self, task: Task, dependencies: Optional[List[str]] = None):
        """Register a task in the pipeline"""
        self.tasks[task.name] = task
        self.task_dependencies[task.name] = dependencies or []
        self.logger.debug(f"Task registered: {task.name}")

    def _can_run_task(self, task_name: str) -> bool:
        """Verifica si una tarea puede ejecutarse"""
        dependencies = self.task_dependencies.get(task_name, [])
        for dep in dependencies:
            if dep not in self.task_results:
                return False
            if not self.task_results[dep].success:
                return False
        return True

    def run(self) -> Dict[str, TaskResult]:
        """Ejecuta todas las tareas registradas en el pipeline"""
        self.logger.info("Initiating pipeline...")
        start_time = time.time()

        # Inicializar contexto con la configuración del pipeline
        self.context = {
            "pipeline_config": {
                "limit": self.limit,
                "days": self.days,
            }
        }

        self.task_results = {}

        # Determinar orden de ejecución respetando dependencias
        remaining_tasks = set(self.tasks.keys())

        while remaining_tasks:
            # Encontrar tareas que pueden ejecutarse
            runnable = [t for t in remaining_tasks if self._can_run_task(t)]

            if not runnable:
                self.logger.error(
                    "No hay tareas ejecutables y aún quedan tareas pendientes. Posible ciclo de dependencias."
                )
                break

            # Ejecutar cada tarea
            for task_name in runnable:
                task = self.tasks[task_name]
                result = task.run(self.context)
                self.task_results[task_name] = result

                # Añadir resultado al contexto
                self.context[task_name] = result.data

                # Remover de pendientes
                remaining_tasks.remove(task_name)

        elapsed = time.time() - start_time
        success = all(result.success for result in self.task_results.values())

        if success:
            self.logger.info(
                f"Pipeline completado exitosamente en {elapsed:.2f} segundos"
            )
        else:
            self.logger.error(
                f"Pipeline completado con errores en {elapsed:.2f} segundos"
            )

        return self.task_results
