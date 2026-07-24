from dataclasses import dataclass, field
from time import perf_counter
from typing import Any, Dict, List, Optional

from parameter_set import ParameterSet

@dataclass
class HistoryEntry:
    iteration: int
    parameters: Dict[str, float]
    objective: float
    metrics: Dict[str, float] = field(default_factory=dict)
    runtime: float = 0.0

class OptimizationHistory:

    def __init__(self):
        self.entries: List[HistoryEntry] = []
        self.iteration_start: Optional[float] = None

    def start_iteration(self) -> None:
        self.iteration_start = perf_counter()

    def record(
            self,
            iteration: int,
            parameters: ParameterSet,
            objective: float,
            metrics: Optional[Dict[str, float]] = None,
    ) -> HistoryEntry:
        runtime = perf_counter() - self.iteration_start if self.iteration_start is not None else 0.0
        self.iteration_start = None

        entry = HistoryEntry(
            iteration = iteration,
            parameters = parameters,
            objective = objective,
            metrics = metrics,
            runtime = runtime,
        )
        self.entries.append(entry)
        return entry

    def __len__(self) -> int:
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries)

    @property
    def best_entry(self) -> Optional[HistoryEntry]:
        if not self.entries:
            return None
        return min(self.entries, key=lambda e: e.objective)

    def to_list(self) -> List[Dict[str, Any]]:
        return [vars(entry) for entry in self.entries]

    def to_dataframe(self):
        import pandas as pd
        return pd.DataFrame(self.to_list())

    def plot_convergence(self, save_path: "str | None" = None) -> None:
        import matplotlib.pyplot as plt

        objectives = [entry.objective for entry in self.entries]
        running_best: List[float] = []
        best = float("inf")
        for value in objectives:
            best = min(best, value)
            running_best.append(best)

        plt.figure(figsize=(7, 4))
        plt.plot(objectives, label="Objective", alpha=0.5)
        plt.plot(running_best, label="Best so far", linewidth=2)
        plt.xlabel("Iteration")
        plt.ylabel("Objective")
        plt.title("Optimization Convergence")
        plt.legend()
        plt.grid(True)

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
