from abc import ABC
import csv
from pathlib import Path
from typing import Dict, Iterable, Optional

from parameter_set import ParameterSet


class Callback(ABC):

    def on_start(self, **kwargs) -> None:
        pass

    def on_iteration(
            self,
            iteration: int,
            parameters: ParameterSet,
            score: float,
            metrics: Optional[Dict[str, float]] = None,
    ) -> None:
        pass

    def on_end(self, **kwargs) -> None:
        pass

class CallbackList(Callback):

    def __init__(self, callbacks: Iterable[Callback]) -> None:
        self.callbacks = callbacks

    def on_start(self, **kwargs) -> None:
        for callback in self.callbacks:
            callback.on_start(**kwargs)

    def on_iteration(self, iteration, parameters, score, metrics=None) -> None:
        for callback in self.callbacks:
            callback.on_iteration(iteration, parameters, score, metrics)

    @property
    def should_stop(self) -> bool:
        return any(getattr(cb, "should_stop", False) for cb in self.callbacks)


class ConsoleLogger(Callback):

    def on_iteration(self, iteration, parameters, score, metrics=None) -> None:
        print(f"[iter {iteration:04d}] score = {score:.6g}")


class CSVLogger(Callback):

    def __init__(self, path: "str | Path"):
        self.path = path
        self.file = None
        self.writer = None

    def on_start(self, **kwargs) -> None:
        self.file = open(self.path, "w", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["iteration", "score", "parameters"])

    def on_iteration(self, iteration, parameters, score, metrics=None) -> None:
        if self.writer is None:
            self.on_start()
            self.writer.writerow([iteration, score, dict(parameters.design_values)])
            self.file.flush()

    def on_end(self, **kwargs) -> None:
        if self.file is not None:
            self.file.close()
            self.file = None
            self.writer = None

class BestDesignSaver(Callback):

    def __init__(self):
        self.best_score: float = float("inf")
        self.best_parameters: Optional[ParameterSet] = None

    def on_iteration(self, iteration, parameters, score, metrics=None) -> None:
        if score < self.best_score:
            self.best_score = score
            self.best_parameters = parameters.copy()


class EarlyStopping(Callback):

    def __init__(self, patience: int = 20, min_delta: float = 1e-6) -> None:
        self.patience = patience
        self.min_delta = min_delta
        self.best_score: float = float("inf")
        self.wait: int = 0
        self.should_stop: bool = False

    def on_iteration(self, iteration, parameters, score, metrics=None) -> None:
        if score < self.best_score - self.min_delta:
            self.best_score = score
            self.wait = 0
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.should_stop = True