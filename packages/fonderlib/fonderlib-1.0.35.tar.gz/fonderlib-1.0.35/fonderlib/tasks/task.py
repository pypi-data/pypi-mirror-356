import time
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


from .task_result import TaskResult
from ..common.logger import get_logger


class Task(ABC):
    """Base class for a task execution"""

    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f"Task-{name}", level="DEBUG")

    def run(self, context: Dict[str, Any]) -> TaskResult:
        """Ejecuta la tarea y devuelve el resultado"""
        start_time = time.time()
        try:
            self.logger.info(f"Initiating task: {self.name}")

            result_data, processed_count = self.execute(context)

            elapsed = time.time() - start_time
            self.logger.info(
                f"Task {self.name} completed in {elapsed:.2f}. Processed: {processed_count}"
            )

            return TaskResult(
                success=True,
                data=result_data,
                elapsed_time=elapsed,
                processed_count=processed_count,
            )
        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.error(f"Error in task {self.name}: {str(e)}")
            import traceback

            self.logger.error(traceback.format_exc())

            return TaskResult(success=False, error=e, elapsed_time=elapsed)

    @abstractmethod
    def execute(self, context: Optional[Dict[str, Any]]) -> tuple[Any, int]:
        """Implementación específica de la tarea"""
        raise NotImplementedError("Las subclases deben implementar execute()")
