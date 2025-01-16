import optuna
import numpy as np
from Tsp import SA, loadDistanceMatrix

# Funkcja celu do optymalizacji
def objective(trial):
    # Hiperparametry do optymalizacji
    T0 = trial.suggest_float("T0", 10, 10000, log=True)
    alpha = trial.suggest_float("alpha", 0.85, 0.99)
    L = trial.suggest_int("L", 10, 500)
    T_min = trial.suggest_float("T_min", 0.001, 1.0, log=True)

    # Generowanie instancji TSP
    filename = "./datasets/gr96.tsp"
    distMatrix = loadDistanceMatrix(filename)

    # Uruchomienie SA
    _, score = SA(distMatrix, _permutation=None, _temp=T0, cooling_rate=alpha, L=L, min_temp=T_min)
    
    return score 

# Tworzenie obiektu optymalizacyjnego
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=1000)

# Wyświetlenie najlepszych parametrów
print("Najlepsze hiperparametry:", study.best_params)
print("Najlepsza wartość funkcji celu:", study.best_value)

# Wizualizacja wyników
optuna.visualization.plot_optimization_history(study).show()
optuna.visualization.plot_param_importances(study).show()
