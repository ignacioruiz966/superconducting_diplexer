import numpy as np
from pathlib import Path
import skrf as rf
import matplotlib.pyplot as plt

class SonnetResults:
    def __init__(self, s2p_path: str | Path):
        self.s2p_path = s2p_path

        self.network = rf.Network(str(self.s2p_path))

        self.frequencies: np.ndarray = self.network.f
        self.s11: np.ndarray = self.network.s[:, 0, 0]
        self.s21: np.ndarray = self.network.s[:, 1, 0]


    def extract_resonant_frequency(self) -> float:

        min_idx = np.argmax(np.abs(self.s21))
        return float(self.frequencies[min_idx])



    def calculate_q_factor(self) -> float:

        s21_db = self.network.s_db[:, 1, 0]
        max_idx = np.argmax(s21_db)
        f_res = self.frequencies[max_idx]

        target_db = s21_db[max_idx] - 3.0

        freq_left = self.frequencies[:max_idx]
        freq_right = self.frequencies[max_idx:]

        left_side = s21_db[:max_idx]
        right_side = s21_db[max_idx:]


        f_left = np.interp(target_db, left_side, freq_left)
        f_right = np.interp(target_db, right_side[::-1], freq_right[::-1])

        bandwidth = abs(f_right - f_left)
        if bandwidth == 0:
            return 0.0

        return float(f_res / bandwidth)


    def plot_s_parameters(self, save_path: str | Path | None = None) -> None:

        plt.figure(figsize = (8, 5))
        self.network.plot_s_db(m=0, n=0, label="$S_{11}$")
        self.network.plot_s_db(m=1, n=0, label="$S_{21}$")

        f_res = self.extract_resonant_frequency()
        plt.axvline(f_res, color="red", linestyle="dashed", label=f'Resonance ({f_res/1e9:.3f} GHz)')
        plt.axvline(8e9, color="red", linestyle="dashed")
        plt.axvline(10.5e9, color="red", linestyle="dashed")

        plt.axhline(-3, color="blue", linestyle="dashed")
        plt.axhline(-20, color="blue", linestyle="dashed")


        plt.title("Sonnet Simulation Results")
        plt.grid(True)

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()


