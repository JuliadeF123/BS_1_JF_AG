import pandas as pd
import os
import glob
from scipy.stats import fisher_exact

# --- KONFIGURACJA ---
base_path = 'results/' 
periods = [1, 10, 50, 150, 200, 500, 1000]
# Słownik: Klucz to nazwa w tabeli, Wartość to wzorzec folderu
amplitudes = {
    "A=0.1": "A0_1", # BAZA do porównań
    "A=0.5": "A0_5",
    "A=1.2": "A1_2",
    "A=3.0": "A3_0",
    "A=6.0": "A6_0"
}
target_theta = "th0_0"
n_replicates = 20

# Dodanie p-value do nagłówka tabeli
header_amplitudes = " | ".join([
    f"{a:>10} (p-value)" for a in list(amplitudes.keys())[1:]
])
print(f"{'T':>5} | {'Base (0.1)':>10} | {header_amplitudes}")
print("-" * 120)


def format_p_value(p):
    # Notacja wykładnicza dla bardzo małych p-value
    if p < 1e-4:
        return f"{p:.1e}"
    else:
        return f"{p:.4f}"

for t in periods:
    def get_ext(pattern):
        search = os.path.join(base_path, f"*_{pattern}_T{t}_{target_theta}*")
        f = glob.glob(search)
        if f and os.path.exists(os.path.join(f[0], 'summary.csv')):
            return int(pd.read_csv(os.path.join(f[0], 'summary.csv'))['extinct_count'].iloc[-1])
        return None

    ext_base = get_ext(amplitudes["A=0.1"])
    base_frac = ext_base/n_replicates if ext_base is not None else None
    row_str = f"{t:5d} | {base_frac if base_frac is not None else 'N/A':>10} | "
    
    for a_name in list(amplitudes.keys())[1:]:
        ext_comp = get_ext(amplitudes[a_name])
        
        if ext_base is not None and ext_comp is not None:
            frac_comp = ext_comp / n_replicates
            # Macierz 2x2: [[Ext_Base, Sur_Base], [Ext_Comp, Sur_Comp]]
            table = [[ext_base, n_replicates - ext_base], 
                     [ext_comp, n_replicates - ext_comp]]
            _, p_val = fisher_exact(table)
            
            # Oznaczenie gwiazdką (*) jeśli p < 0.05 / 4 (korekta Bonferroniego dla 4 testów)
            sig = "*" if p_val < (0.05 / 4) else " "
            row_str += f"{frac_comp:>6} {sig:1} ({format_p_value(p_val)}) | "
        else:
            row_str += f"{'N/A':>10} ( N/A ) | "
            
    print(row_str)