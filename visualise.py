import pandas as pd
import os
import glob
from scipy.stats import fisher_exact

# --- KONFIGURACJA ---
base_path = 'results/' 
periods = [1, 10, 50, 150, 200, 500, 1000]
target_theta = "th0_0"  # Stałe przesunięcie fazowe dla porównania amplitud

# Definiujemy wzorce dla porównywanych Amplitud (A)
label_a, pattern_a = "A=0.5", "A0_5"
label_b, pattern_b = "A=3.0", "A3_0"
n_replicates = 20

results = []

print(f"{'T':>5} | {'Rate A (0.5)':>12} | {'Rate B (3.0)':>12} | {'p-value':>10} | {'Significant'}")
print("-" * 65)

for t in periods:
    def get_extinction_count(a_pattern):
        # Szukamy folderu pasującego do Amplitudy, T i stałej Theta
        search = os.path.join(base_path, f"*_{a_pattern}_T{t}_{target_theta}*")
        folders = glob.glob(search)
        
        if folders and os.path.exists(os.path.join(folders[0], 'summary.csv')):
            df = pd.read_csv(os.path.join(folders[0], 'summary.csv'))
            return int(df['extinct_count'].iloc[-1])
        return None

    ext_a = get_extinction_count(pattern_a)
    ext_b = get_extinction_count(pattern_b)

    if ext_a is not None and ext_b is not None:
        # Test Fishera dla różnicy w wymieralności
        table = [[ext_a, n_replicates - ext_a], 
                 [ext_b, n_replicates - ext_b]]
        
        _, p_value = fisher_exact(table)
        rate_a = ext_a / n_replicates
        rate_b = ext_b / n_replicates
        sig = p_value < 0.05
        
        results.append({
            'T': t,
            'Rate_A': rate_a,
            'Rate_B': rate_b,
            'p_value': p_value,
            'Significant': sig
        })
        
        # Printowanie wiersza tabeli na bieżąco
        print(f"{t:5d} | {rate_a:12.2f} | {rate_b:12.2f} | {p_value:10.4e} | {sig}")

if not results:
    print("\n[BŁĄD] Nie znaleziono danych dla podanych wzorców amplitud (A0_1, A1_0).")