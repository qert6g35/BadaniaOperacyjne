
from FordFulkerson import Graph
from Odciencia import Greed1MinCut, Greed2MinCut
from generator import generate_random_max_flow_instance
from DataManagment import loadData

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
import time

show_mistakes_prints = False
n_probs = 1000
n_instances = [5,10,20,30,40,50,60,70,80,90,100]
g1_mistakes = 0
g2_mistakes = 0
times_0_was_answer = 0

avg_times_Greed1MinCut = []
avg_times_Greed2MinCut = []
avg_times_bellman = []

for n_instance in n_instances:
       #instance = loadData("/Examples/"+str(n_instance))
       #print(instance)
       times_Greed1MinCut = []
       times_Greed2MinCut = []
       times_bellman = []

       for _ in range(n_probs):
              instance = generate_random_max_flow_instance(n_instance)
              graph1 = instance.copy()
              graph2 = instance.copy()
              graphFF = instance.copy()
              source_vertex = 0
              sink_vortex = len(graph1)-1
              # Mierzenie czasu działania algorytmu GreedyMinCuts1 (wybór pkt do odcięcia po min nastemptym przekroju)
              start_time = time.time()
              greed1_value = Greed1MinCut(graph1, source_vertex,sink_vortex,False)
              elapsed_time = time.time() - start_time
              times_Greed1MinCut.append(elapsed_time)

              # Mierzenie czasu działania algorytmu GreedyMinCuts2 (wybór pkt do odcięcia po największym dopływie do już odciętych pkt)
              start_time = time.time()
              greed2_value = Greed2MinCut(graph2, source_vertex,sink_vortex,False)
              elapsed_time = time.time() - start_time
              times_Greed2MinCut.append(elapsed_time)

              # Mierzenie czasu działania algorytmu FordaFolkersonma
              start_time = time.time()
              fordFulkerson_value = Graph(graphFF).FordFulkerson(source_vertex,sink_vortex)
              elapsed_time = time.time() - start_time
              times_bellman.append(elapsed_time)
              
              if fordFulkerson_value == 0:
                times_0_was_answer += 1
              if fordFulkerson_value - greed1_value != 0 :
                if show_mistakes_prints:
                    print("we have dissagreement !! n:"+str(n_instance))
                    print("Greeds1Cuts:"+str(greed1_value))
                    print("fordFolkerson:"+str(fordFulkerson_value))
                g1_mistakes += 1

            
              if  fordFulkerson_value - greed2_value != 0 :
                if show_mistakes_prints:
                    print("we have dissagreement !! n:"+str(n_instance))
                    print("Greeds2Cuts:"+str(greed2_value))
                    print("fordFolkerson:"+str(fordFulkerson_value))
                g2_mistakes += 1
       
       avg_times_Greed1MinCut.append(np.mean(times_Greed1MinCut))
       avg_times_Greed2MinCut.append(np.mean(times_Greed2MinCut))
       avg_times_bellman.append(np.mean(times_bellman))

print("g1_błędy:", g1_mistakes)
print("g2_błędy:", g2_mistakes)
print("generator wypluł coś bez maksymalnego przepływu:", times_0_was_answer)
plt.figure(figsize=(10, 6))
plt.plot(n_instances, avg_times_Greed1MinCut, label='Algorytm GreedCuts1', marker='o')
plt.plot(n_instances, avg_times_Greed2MinCut, label='Algorytm GreedCuts2', marker='o')
plt.plot(n_instances, avg_times_bellman, label='Algorytm FordaFolkersona', marker='o')
plt.xlabel('Liczba wierzchołków w instancji')
plt.ylabel('Średni czas działania (s)')
plt.title('Porównanie średniego czasu działania algorytmów')
plt.legend()
plt.grid(True)
plt.show()