import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# Ścieżka bazowa, gdzie znajdują się foldery z wynikami
base_path = 'results/' 

# Lista wartości T, które chcemy wyplotować
target_T = [1, 50, 200, 1000]

plt.figure(figsize=(12, 7))

# Słownik do przechowywania ścieżek (zakładamy, że nazwa folderu zawiera T1, T100 itd.)
# Używamy dopasowania wzorca, aby znaleźć foldery dla konkretnych T
for t_val in target_T:
    # Szukamy folderów, które mają w nazwie T{t_val}_ (np. T100_)
    # Wzorzec dopasowuje np. "grid_A0_1_T100_th1_57_..."
    pattern = os.path.join(base_path, f"grid_A0_1_T{t_val}_th3_14*")
    folders = glob.glob(pattern)
    
    if not folders:
        print(f"Nie znaleziono folderu dla T={t_val}")
        continue
    
    # Bierzemy pierwszy znaleziony folder dla danej wartości T
    folder_path = folders[0]
    file_path = os.path.join(folder_path, 'summary.csv') # upewnij się co do nazwy pliku
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        # Rysowanie linii średniej
        line, = plt.plot(df['generation'], df['mean_fitness_mean'], label=f'T = {t_val}')
        
        # Opcjonalnie: Dodanie obszaru błędu (± standard deviation)
        plt.fill_between(
            df['generation'], 
            df['mean_fitness_mean'] - df['mean_fitness_std'], 
            df['mean_fitness_mean'] + df['mean_fitness_std'], 
            color=line.get_color(), 
            alpha=0.1
        )
    else:
        print(f"Nie znaleziono pliku CSV w {folder_path}")

# Formatowanie wykresu
plt.title('Ewolucja Mean Fitness w zależności od okresu T dla A=0.1, theta=3.14', fontsize=14)
plt.xlabel('Pokolenie (Generation)', fontsize=12)
plt.ylabel('Mean Fitness', fontsize=12)
plt.legend(title="Okres (T)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.ylim(0, 1.05) # Fitness zazwyczaj jest w zakresie 0-1

plt.tight_layout()
plt.show()