
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from Tsp import FI, NN, RandomPermutation, plot_path,coordinatesToDistMatrix, generateCoordinates, twoOpt, tabuSearch

results = []

repeats = 1
sizes = [100, 200, 300, 400, 500]
sizes = [10,20,30,40,50,60,70,80,90] + sizes

avr_scoresNN = []
avr_scoresFI = []
avr_scoresRP = []
avr_scoresTONN = []
avr_scoresTOFI = []
avr_scoresTORP = []
avr_scoresTSNN = []
avr_scoresTSFI = []
avr_scoresTSRP = []

T0 = 74
alpha = 0.9524385825925
L = 55
T_min = 0.26818680277433227

for size in sizes:
    scoresNN = []
    scoresFI = []
    scoresRP = []
    scoresTORP = []
    scoresTONN = []
    scoresTOFI = []
    scoresTSRP = []
    scoresTSNN = []
    scoresTSFI = []
    for i in range(repeats):
        print("repeat:",i+1,"/",repeats,", size: ",size)
        coordinates = generateCoordinates(size)
        distMatrix = coordinatesToDistMatrix(coordinates)


        # podstawowe algorytmy
        pathNN, distNN = NN(distMatrix)
        pathFI, distFI = FI(distMatrix)
        pathRP, distRP = RandomPermutation(distMatrix)

        # wyrzażanie dla NN, FI oraz random
        saF_permutation, toF_dist = twoOpt(distMatrix,pathFI[:-1])
        saN_permutation, toN_dist = twoOpt(distMatrix,pathNN[:-1])
        saR_permutation, toR_dist = twoOpt(distMatrix,pathRP[:-1])

        # wyrzażanie dla NN, FI oraz random
        saF_permutation, tsF_dist = tabuSearch(distMatrix,pathFI[:-1])
        saN_permutation, tsN_dist = tabuSearch(distMatrix,pathNN[:-1])
        saR_permutation, tsR_dist = tabuSearch(distMatrix,pathRP[:-1])

        # przeliczenie wyników procentowa lepszość od randomowej prermutacji
        comp_score = distNN

        scoresNN.append(100*(distNN-comp_score)/comp_score)
        scoresFI.append(100*(distFI-comp_score)/comp_score)
        scoresRP.append(100*(distRP-comp_score)/comp_score)
        scoresSARP.append(100*(saR_dist-comp_score)/comp_score)
        scoresSANN.append(100*(saN_dist-comp_score)/comp_score)
        scoresSAFI.append(100*(saF_dist-comp_score)/comp_score)
        
    # 1 - 2 / 2


    avr_scoreNN=sum(scoresNN)/repeats
    avr_scoreFI=sum(scoresFI)/repeats
    avr_scoreRP=sum(scoresRP)/repeats
    avr_scoreSARP=sum(scoresSARP)/repeats
    avr_scoreSANN=sum(scoresSANN)/repeats
    avr_scoreSAFI=sum(scoresSAFI)/repeats


    avr_scoresNN.append(avr_scoreNN)
    avr_scoresFI.append(avr_scoreFI)
    avr_scoresRP.append(avr_scoreRP)
    avr_scoresSARP.append(avr_scoreSARP)
    avr_scoresSANN.append(avr_scoreSANN)
    avr_scoresSAFI.append(avr_scoreSAFI)

    results.append({
        'size': size,
        'scoreNN': avr_scoreNN,
        'scoreFI': avr_scoreFI,
        'scoreSARP': avr_scoreSARP,
        'scoreSANN': avr_scoreSANN,
        'scoreSAFI': avr_scoreSAFI
    })

plt.figure(figsize=(10, 6))
plt.plot(sizes, avr_scoresNN, label='NN', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresFI, label='FI', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresRP, label='RP', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresSANN, label='SANN', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresSAFI, label='SAFI', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresSARP, label='SARP', marker='o',alpha=0.7)

plt.xlabel('Liczba wierzchołków w instancji')
plt.ylabel('(A-A*)/A*[%]')
plt.title('Porównanie różnych kombinacji algorytmów dla problemu TSP')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(sizes, avr_scoresNN, label='NN', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresFI, label='FI', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresRP, label='RP', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresSANN, label='SANN', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresSAFI, label='SAFI', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresSARP, label='SARP', marker='o',alpha=0.7)

plt.xlabel('Liczba wierzchołków w instancji')
plt.ylabel('(A-A*)/A*[%]')
plt.title('Porównanie różnych kombinacji algorytmów dla problemu TSP')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
# plt.plot(sizes, avr_scoresNN, label='NN', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresFI, label='FI', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresRP, label='RP', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresSANN, label='SANN', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresSAFI, label='SAFI', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresSARP, label='SARP', marker='o',alpha=0.7)

plt.xlabel('Liczba wierzchołków w instancji')
plt.ylabel('(A-A*)/A*[%]')
plt.title('Porównanie różnych kombinacji algorytmów dla problemu TSP')
plt.legend()
plt.grid(True)
plt.show()

df = pd.DataFrame(results)
df.to_csv("tsp_benchmarak_results.csv", index=False)
print("Wyniki zapisane do pliku tsp_results.csv")