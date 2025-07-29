"""Task implementations for LLMThinkBench."""

from .base_task import BaseTask
from .sorting_task import SortingTask
from .comparison_task import ComparisonTask
from .sum_task import SumTask
from .multiplication_task import MultiplicationTask
from .odd_count_task import OddCountTask
from .even_count_task import EvenCountTask
from .absolute_difference_task import AbsoluteDifferenceTask
from .division_task import DivisionTask
from .find_maximum_task import FindMaximumTask
from .find_minimum_task import FindMinimumTask
from .mean_task import MeanTask
from .median_task import MedianTask
from .mode_task import ModeTask
from .subtraction_task import SubtractionTask

# Dict mapping task names to task classes
AVAILABLE_TASKS = {
    "sorting": SortingTask,
    "comparison": ComparisonTask,
    "sum": SumTask,
    "multiplication": MultiplicationTask,
    "odd_count": OddCountTask,
    "even_count": EvenCountTask,
    "absolute_difference": AbsoluteDifferenceTask,
    "division": DivisionTask,
    "find_maximum": FindMaximumTask,
    "find_minimum": FindMinimumTask,
    "mean": MeanTask,
    "median": MedianTask,
    "mode": ModeTask,
    "subtraction": SubtractionTask
}

def get_task_class(task_name):
    """Get task class by name."""
    if task_name not in AVAILABLE_TASKS:
        raise ValueError(f"Unknown task: {task_name}. Available tasks: {list(AVAILABLE_TASKS.keys())}")
    return AVAILABLE_TASKS[task_name]

__all__ = ["BaseTask", "SortingTask", "ComparisonTask", "SumTask", "MultiplicationTask", 
           "OddCountTask", "EvenCountTask", "AbsoluteDifferenceTask", "DivisionTask", 
           "FindMaximumTask", "FindMinimumTask", "MeanTask", "MedianTask", "ModeTask", "SubtractionTask", 
           "get_task_class", "AVAILABLE_TASKS"]