import json
from pathlib import Path
import numpy as np

# Setup
experiment_dir = Path("experiments")

# zakres wartosci jaki ma byc symulowany
periods = [10, 20, 50, 100, 200, 500, 1000]
amplitudes = [0.1, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0]

# Parameters for shocks
shock_prob = 0.0001         # Example value: probability of shock per generation
shock_magnitude = 1.5     # Example value: std dev for shock vector

# ______________________________dla zmiany T______________________________
base_cfg = {
    "n": 2, "N": 100, "sigma": 0.1, "xi": 0.05, "mu": 0.1, "mu_c": 0.5,

    "h0": 0.0, "Ah": 0.05, "r0": 0.0, "Ar": 0.05, "theta": 0.0,
    
    "threshold": 0.05, "init_scale": 0.1, "max_generations": 1000, 
    "n_replicates": 20, "seeds": list(range(20)),
    # Używane do grupowania pozniejszzego wyniku
    "group": "dlugosc_cyklu",
    # SHOCKS
    "shock_prob": shock_prob,
    "shock_magnitude": shock_magnitude
}

for ZMIENNE in periods:
# w zaleznosci od tego co chcesz zmienic, to tez nazwy plikow bedzie trzeba zmodyfikowac odpowiednio
    cfg = base_cfg.copy()
    cfg["name"] = f"seasonal_T{ZMIENNE}_shock"
    cfg["T"] = ZMIENNE
    cfg["description"] = (
        f"Seasonal cycle with period T={ZMIENNE}, with environmental shocks. Testing adaptation speed."
    )
    file_path = experiment_dir / f"{cfg['name']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

print(f"Generated {len(periods)} experiments in {experiment_dir}/")

# ______________________________dla zmiany A______________________________
base_cfg = {
    "n": 2, "N": 100, "sigma": 0.1, "xi": 0.05, "mu": 0.1, "mu_c": 0.5,
    "h0": 0.0, "r0": 0.0, "T": 100, "theta": 0.0, 
    "threshold": 0.05, "init_scale": 0.1, "max_generations": 1000,
    "n_replicates": 20, "seeds": list(range(20)),
    "group": "wyczulenie_na_amplitude(oba)",
    # SHOCKS
    "shock_prob": shock_prob,
    "shock_magnitude": shock_magnitude
}

for A in amplitudes:
    cfg = base_cfg.copy()
    cfg["name"] = f"seasonal_A{str(A).replace('.', '_')}_shock"
    cfg["Ah"] = A
    cfg["Ar"] = A
    cfg["description"] = (
        f"Seasonal cycle with Amplitude A={A}, with environmental shocks. Testing survival limits."
    )
    file_path = experiment_dir / f"{cfg['name']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

print(f"Generated {len(amplitudes)} experiments in {experiment_dir}/")

# ______________________________dla zmiany theta______________________________
thetas = [0.0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi]

base_cfg = {
    "n": 2, "N": 100, "sigma": 0.2, "xi": 0.05, "mu": 0.1, "mu_c": 0.5,

    "h0": 0.0, "Ah": 0.1, "r0": 0.0, "Ar": 0.1, "T": 100,

    "threshold": 0.01, "init_scale": 0.1, "max_generations": 1000, 
    "n_replicates": 20, "seeds": list(range(20)),
    "group": "zmiennosc_przesuniecia_theta",
    # SHOCKS
    "shock_prob": shock_prob,
    "shock_magnitude": shock_magnitude
}

for T_val in thetas:
    cfg = base_cfg.copy()
    cfg["theta"] = float(T_val)
    name_suffix = str(round(T_val, 2)).replace('.', '_')
    cfg["name"] = f"seasonal_theta_{name_suffix}_shock"
    cfg["description"] = f"Testing phase shift theta={round(T_val, 2)} rad, with environmental shocks."
    file_path = experiment_dir / f"{cfg['name']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

print(f"Generated {len(thetas)} experiments in {experiment_dir}/")