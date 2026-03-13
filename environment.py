# environment.py

import numpy as np
from strategies import EnvironmentDynamics


class LinearShiftEnvironment(EnvironmentDynamics):
    """
    Scenariusz globalnego ocieplenia: optymalny fenotyp przesuwa się liniowo
    z opcjonalnymi losowymi fluktuacjami w każdym pokoleniu.

        alpha(t) = alpha(t-1) + N(c, delta^2 * I)

    Jeśli delta=0, przesunięcie jest czysto deterministyczne:
        alpha(t) = alpha(t-1) + c
    """

    def __init__(self, alpha_init: np.ndarray, c: np.ndarray, delta: float = 0.0):
        """
        :param alpha_init: początkowy optymalny fenotyp
        :param c: wektor kierunkowej zmiany (średnie przesunięcie na pokolenie)
        :param delta: odch. std. losowych fluktuacji wokół c (0 = brak szumu)
        """
        self.alpha = np.array(alpha_init, dtype=float)
        self.c = np.array(c, dtype=float)
        self.delta = float(delta)

    def update(self) -> None:
        """alpha(t) = alpha(t-1) + N(c, delta^2 * I)"""
        if self.delta > 0:
            shift = np.random.normal(loc=self.c, scale=self.delta, size=len(self.alpha))
        else:
            shift = self.c.copy()
        self.alpha = self.alpha + shift

    def get_optimal_phenotype(self) -> np.ndarray:
        return self.alpha.copy()


class SeasonalCyclicEnvironment(EnvironmentDynamics):
    """
    Scenariusz cykliczny (np. pory roku) dla dwuwymiarowego optimum:

        alpha(t) = (alpha_h(t), alpha_r(t))
                 = (h0 + Ah * sin(2πt / T),
                    r0 + Ar * sin(2πt / T))

    gdzie:
        h0, r0 – średnie wartości cech (wzrost i głębokość korzenia)
        Ah, Ar – amplitudy wahań (kolejno dla wzrostu i głębokości korzenia)
        T      – okres cyklu (w pokoleniach)
    """

    def __init__(
        self,
        h0: float,
        Ah: float,
        r0: float,
        Ar: float,
        T: float,
        t0: int = 0,
        theta: float = 0.0,
    ):
        """
        :param h0: średni optymalny wzrost (składowa h)
        :param Ah: amplituda sezonowych zmian wzrostu
        :param r0: średnia optymalna głębokość korzenia (składowa r)
        :param Ar: amplituda sezonowych zmian głębokości korzenia
        :param T: okres cyklu (liczba pokoleń na pełen obrót)
        :param t0: początkowy czas (pokolenie), domyślnie 0
        :param theta: faza początkowa, domyślnie 0
        """
        self.h0 = float(h0)
        self.Ah = float(Ah)
        self.r0 = float(r0)
        self.Ar = float(Ar)
        self.T = float(T)
        self.t = int(t0)
        self.theta = float(theta)
        # Ustaw początkowy wektor optimum
        self._update_alpha()

    def _update_alpha(self) -> None:
        """Pomocniczo przelicza alpha(t) na podstawie bieżącego t."""
        phase = 2.0 * np.pi * self.t / self.T + self.theta
        alpha_h = self.h0 + self.Ah * np.sin(phase)
        alpha_r = self.r0 + self.Ar * np.sin(phase)
        self.alpha = np.array([alpha_h, alpha_r], dtype=float)

    def update(self) -> None:
        """Przejście do kolejnego pokolenia t -> t+1 i aktualizacja alpha(t)."""
        self.t += 1
        self._update_alpha()

    def get_optimal_phenotype(self) -> np.ndarray:
        """Zwraca aktualny wektor [alpha_h(t), alpha_r(t)]."""
        return self.alpha.copy()


# Alias dla kompatybilności wstecznej
Environment = LinearShiftEnvironment
