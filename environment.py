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
    Scenariusz cykliczny (np. pory roku) dla dwuwymiarowego optimum,
    z możliwością wystąpienia nagłych, losowych zmian (szoków środowiskowych) wykraczających poza zwykłe limity sezonowe.

        alpha(t) = (alpha_h(t), alpha_r(t))
                 = (h0 + Ah * sin(2πt / T),
                    r0 + Ar * sin(2πt / T))
        Raz na jakiś czas pojawia się randomowy "szok" czyli skokowe przesunięcie optimum.

    gdzie:
        h0, r0 – średnie wartości cech (wzrost i głębokość korzenia)
        Ah, Ar – amplitudy wahań (kolejno dla wzrostu i głębokości korzenia)
        T      – okres cyklu (w pokoleniach)
    
    Parametry dodatkowe:
      - shock_prob: Prawdopodobieństwo nagłego skoku w każdym pokoleniu (np. 0.01)
      - shock_magnitude: Odchylenie std rysowania losowego wektora skoku (np. 2.0)
      - random_seed: Opcjonalnie seed dla powtarzalności
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
        shock_prob: float = 0.1,
        shock_magnitude: float = 1.0,
        random_seed: int = None,
    ):
        """
        :param h0: średni optymalny wzrost (składowa h)
        :param Ah: amplituda sezonowych zmian wzrostu
        :param r0: średnia optymalna głębokość korzenia (składowa r)
        :param Ar: amplituda sezonowych zmian głębokości korzenia
        :param T: okres cyklu (liczba pokoleń na pełen obrót)
        :param t0: początkowy czas (pokolenie), domyślnie 0
        :param theta: faza początkowa, domyślnie 0
        :param shock_prob: prawdopodobieństwo randomowego skoku
        :param shock_magnitude: skala amplitudy randomowego skoku
        :param random_seed: seed RNG
        """
        self.h0 = float(h0)
        self.Ah = float(Ah)
        self.r0 = float(r0)
        self.Ar = float(Ar)
        self.T = float(T)
        self.t = int(t0)
        self.theta = float(theta)
        self.shock_prob = float(shock_prob)
        self.shock_magnitude = float(shock_magnitude)
        self.rng = np.random.default_rng(random_seed)
        # Ustaw początkowy wektor optimum
        self._update_alpha()

    def _update_alpha(self) -> None:
        """Pomocniczo przelicza alpha(t) na podstawie bieżącego t."""
        phase = 2.0 * np.pi * self.t / self.T + self.theta
        alpha_h = self.h0 + self.Ah * np.sin(phase)
        alpha_r = self.r0 + self.Ar * np.sin(phase)
        self.alpha = np.array([alpha_h, alpha_r], dtype=float)

    def update(self) -> None:
        """Przejście do kolejnego pokolenia t -> t+1 i aktualizacja alpha(t).
        Często (wg shock_prob) rzuca losowy skok środowiskowy (duża zmiana)."""
        self.t += 1
        self._update_alpha()
        if self.shock_prob > 0 and self.rng.uniform() < self.shock_prob:
            # Dodaj nagłą, losową zmianę do optimum wykraczającą poza sezonowe granice!
            shock = self.rng.normal(loc=0.0, scale=self.shock_magnitude, size=2)
            self.alpha += shock

    def get_optimal_phenotype(self) -> np.ndarray:
        """Zwraca aktualny wektor [alpha_h(t), alpha_r(t)] (wraz z ewentualnym szokiem)."""
        return self.alpha.copy()


# Alias dla kompatybilności wstecznej
Environment = SeasonalCyclicEnvironment
