from Dijkstra import dijkstra, matrix_to_graph, build_paths
from BellmanFiesta import BellMyFord
from DataManagment import loadData

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
import time

n_probs = 100
n_instances = [5,10,15,20,25]

avg_times_dijkstra = []
avg_times_bellman = []

for n_instance in n_instances:
       instance = loadData("/Paths/MinPaths_data"+str(n_instance))

       times_dijkstra = []
       times_bellman = []

       for _ in range(n_probs):
              graph = matrix_to_graph(instance)
              source_vertex = 0

              # Mierzenie czasu działania algorytmu Dijkstry
              start_time = time.time()
              dijkstra(graph, source_vertex)
              elapsed_time = time.time() - start_time
              times_dijkstra.append(elapsed_time)

              # Mierzenie czasu działania algorytmu Bellmana-Forda
              start_time = time.time()
              BellMyFord(instance)  
              elapsed_time = time.time() - start_time
              times_bellman.append(elapsed_time)
       
       avg_times_dijkstra.append(np.mean(times_dijkstra))
       avg_times_bellman.append(np.mean(times_bellman))

plt.figure(figsize=(10, 6))
plt.plot(n_instances, avg_times_dijkstra, label='Algorytm Dijkstry', marker='o')
plt.plot(n_instances, avg_times_bellman, label='Algorytm Bellmana-Forda', marker='o')
plt.xlabel('Liczba wierzchołków w instancji')
plt.ylabel('Średni czas działania (s)')
plt.title('Porównanie średniego czasu działania algorytmów Dijkstry i Bellmana-Forda')
plt.legend()
plt.grid(True)
plt.show()