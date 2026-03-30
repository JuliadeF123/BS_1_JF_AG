import pandas as pd
import os
import glob
from scipy.stats import fisher_exact

# --- KONFIGURACJA ---
base_path = 'results/' 
periods = [1, 10, 50, 150, 200, 500, 1000]  # Chcemy porównywać różne T
amplitudes = [
      "A0_1", "A0_3",  "A0_5", 'A1_0','A1_2','A1_5', 'A2_0','A3_0', 'A6_0'
]  # Przez wszystkie amplitudy - zgodnie z generacją albo wynikami
target_theta = "th0_0"
n_replicates = 20

# Robimy porównanie dla różnych T versus bazowego T (tu: pierwsze z periods)
base_T = periods[0]
header_periods = " | ".join([
    f"T={t:>5} (p-value)" for t in periods[1:]
])
print(f"{'Amplituda':>10} | {'Base_T ('+str(base_T)+')':>10} | {header_periods}")
print("-" * 120)

def format_p_value(p):
    # Notacja wykładnicza dla bardzo małych p-value
    if p < 1e-4:
        return f"{p:.1e}"
    else:
        return f"{p:.4f}"

def get_ext(amplitude, t):
    search = os.path.join(base_path, f"*_{amplitude}_T{t}_{target_theta}*")
    f = glob.glob(search)
    if f and os.path.exists(os.path.join(f[0], 'summary.csv')):
        return int(pd.read_csv(os.path.join(f[0], 'summary.csv'))['extinct_count'].iloc[-1])
    return None

for amplitude in amplitudes:
    # Podstawowa wartość extinct_count dla bazowego T
    ext_base = get_ext(amplitude, base_T)
    base_frac = ext_base / n_replicates if ext_base is not None else None
    row_str = f"{amplitude:>10} | {base_frac if base_frac is not None else 'N/A':>10} | "

    for t in periods[1:]:
        ext_comp = get_ext(amplitude, t)
        if ext_base is not None and ext_comp is not None:
            frac_comp = ext_comp / n_replicates
            # Macierz 2x2: [[Ext_Base, Sur_Base], [Ext_Comp, Sur_Comp]]
            table = [[ext_base, n_replicates - ext_base],
                     [ext_comp, n_replicates - ext_comp]]
            _, p_val = fisher_exact(table)
            # Korekta Bonferroniego na liczbę testów
            sig = "*" if p_val < (0.05 / (len(periods)-1)) else " "
            row_str += f"{frac_comp:>6} {sig:1} ({format_p_value(p_val)}) | "
        else:
            row_str += f"{'N/A':>10} ( N/A ) | "
    print(row_str)