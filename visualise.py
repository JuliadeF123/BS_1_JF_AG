import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Path to results directory
base_path = 'results/'

def get_params(folder_name):
    """Extract T and A from a folder name."""
    t_match = re.search(r'_T(\d+)_', folder_name)
    A_match = re.search(r'_A([\d_]+)_', folder_name)
    t_val = int(t_match.group(1)) if t_match else None
    A_val = A_match.group(1) if A_match else None
    if A_val is not None:
        A_val = A_val.replace('_', '.')
    return t_val, A_val

# Only desired A values
wanted_A_values = {"0.1", "0.5", "1.0", "3.0"}

# Prompt user for which theta to include
user_theta = input("Enter desired value for theta (e.g. 0.5): ").strip()

if not user_theta:
    raise RuntimeError("You must specify a theta value, e.g. 0.5")

# Data storage: A_val -> {T: lag}
results = {}

found_theta_anywhere = False
for folder in os.listdir(base_path):
    full_path = os.path.join(base_path, folder)
    if os.path.isdir(full_path) and 'summary.csv' in os.listdir(full_path):
        # Check for theta value in folder name
        th_match = re.search(r'_th(\d+_\d+)_', folder)
        if not th_match:
            continue
        th_val = th_match.group(1).replace('_', '.')
        if th_val == user_theta:
            found_theta_anywhere = True

for folder in os.listdir(base_path):
    full_path = os.path.join(base_path, folder)
    if os.path.isdir(full_path) and 'summary.csv' in os.listdir(full_path):
        # Only include runs with the desired theta
        th_match = re.search(r'_th(\d+_\d+)_', folder)
        if not th_match:
            continue
        th_val = th_match.group(1).replace('_', '.')
        if th_val != user_theta:
            continue

        t_val, A_val = get_params(folder)
        if t_val is None or A_val is None:
            continue
        if A_val not in wanted_A_values:
            continue

        df = pd.read_csv(os.path.join(full_path, 'summary.csv'))
        # Average lag from the last generation (G=1000 or final before extinction)
        final_lag = df['distance_from_optimum_mean'].iloc[-1]

        if A_val not in results:
            results[A_val] = {}
        results[A_val][t_val] = final_lag

if not found_theta_anywhere:
    raise RuntimeError(f"No folder with a _th.*_ pattern found in results/. Cannot find theta={user_theta}.")

if not results:
    raise RuntimeError(f"No results found for theta={user_theta} with wanted A values {wanted_A_values}.")

# Plotting
plt.figure(figsize=(10, 6))

for A_label in sorted(results, key=lambda x: float(x)):
    points = results[A_label]
    sorted_t = sorted(points.keys())
    sorted_lags = [points[t] for t in sorted_t]

    plt.plot(sorted_t, sorted_lags, 'o-', label=f'Amplitude: {A_label}', markersize=7, lw=2)

plt.xscale('log')
plt.title(f'Final Evolutionary Lag vs. Period T (theta={user_theta})', fontsize=14)
plt.xlabel('Period T (Number of generations per cycle)', fontsize=12)
plt.ylabel('Mean distance from optimum (Final Generation)', fontsize=12)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend(title="Amplitude (A)")
plt.tight_layout()
plt.show()