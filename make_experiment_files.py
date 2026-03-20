import json
from pathlib import Path

# Setup
experiment_dir = Path("experiments")

# zakres wartosci jaki ma byc symulowany
periods = [10, 20, 50, 100, 200, 500, 1000]

# konfiguracja
base_cfg = {
    "n": 2, "N": 100, "sigma": 0.2, "xi": 0.05, "mu": 0.1, "mu_c": 0.5,

    "h0": 0.0, "Ah": 0.05, "r0": 0.0, "Ar": 0.05, "theta": 0.0,
    
    "threshold": 0.01, "init_scale": 0.1, "max_generations": 1000, 
    "n_replicates": 20, "seeds": list(range(20)),

    # uzywane do grupowania pozniejszzego wyniku, wiec dla kazdego parametru zmieniamy
    "group": "dlugosc cyklu"
}

for ZMIENNE in periods:
# w zaleznosci od tego co chcesz zmienic, to tez nazwy plikow bedzie trzeba zmodyfikowac odpowiednio
    cfg = base_cfg.copy()
    cfg["name"] = f"seasonal_T{ZMIENNE}"
    cfg["T"] = ZMIENNE
    cfg["description"] = f"Seasonal cycle with period T={ZMIENNE}. Testing adaptation speed."
    
    # zapisz do pliku
    file_path = experiment_dir / f"{cfg['name']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

print(f"Generated {len(periods)} experiments in {experiment_dir}/")