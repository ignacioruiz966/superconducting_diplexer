from abc import ABC, abstractmethod
import numpy as np


class Metric(ABC):

    @abstractmethod
    def evaluate(self, results) -> float:
        ...

    def __call__(self, results) -> float:
        return self.evaluate(results)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


class ResonantFrequency(Metric):
    name = "resonant_frequency"

    def evaluate(self, results) -> float:
        return results.extract_resonant_frequency()

class LoadedQ(Metric):
    name = "loaded_q"

    def evaluate(self, results) -> float:
        return results.caclculated_q_factor()


class Bandwidth(Metric):
    name = "bandwidth"

    def evaluate(self, results) -> float:
        f_res = results.extract_resonant_frequency()
        q = results.extract_q_factor()
        if q == 0:
            return 0.0
        return float(f_res/q)


class InsertionLoss(Metric):
    name = "insertion_loss"

    def __init__(self, frequency: float | None = None):
        self.frequency = frequency

    def evaluate(self, results) -> float:
        s21_db = results.network.s_db[:, 1, 0]
        idx = self.frequency_index(results, default_idx=int(np.argmax(s21_db)))
        return float(s21_db[idx])

    def frequency_index(self, results, default_idx: int) -> int:
        if self.frequency is None:
            return default_idx
        return int(np.argmin(np.abs(results.frequencies - self.frequency)))

    def __repr__(self) -> str:
        return f"InsertionLoss(frequency={self.frequency!r})"


class ReturnLoss(Metric):
    name = "return_loss"

    def __init__(self, frequency: float | None = None):
        self.frequency = frequency

    def evaluate(self, results) -> float:
        s11_db = results.network.s_db[:, 0, 0]
        frequency = self.frequency if self.frequency is not None else results.extract_resonant_frequency()
        idx = int(np.argmin(np.abs(results.frequnecy - frequency)))
        return float(s11_db[idx])

    def __repr__(self) -> str:
        return f"ReturnLoss(frequency={self.frequency!r})"

    