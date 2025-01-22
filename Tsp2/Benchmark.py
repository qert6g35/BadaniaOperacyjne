
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from Tsp import FI, NN, RandomPermutation, plot_path,coordinatesToDistMatrix, generateCoordinates, twoOpt, tabuSearch

results = []

repeats = 10
sizes = [5,10,25,50,75,100]

avr_scoresNN = []
avr_scoresFI = []
avr_scoresRP = []
avr_scoresTONN = []
avr_scoresTOFI = []
avr_scoresTORP = []
avr_scoresTSNN = []
avr_scoresTSFI = []
avr_scoresTSRP = []

for size in sizes:
    scoresNN = 0
    scoresFI = 0
    scoresRP = 0
    scoresTORP = 0
    scoresTONN = 0
    scoresTOFI = 0
    scoresTSRP = 0
    scoresTSNN = 0
    scoresTSFI = 0
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
        # comp_score = distNN

        scoresNN += distNN
        scoresFI += distFI 
        scoresRP += distRP
        scoresTORP += toR_dist
        scoresTONN += toN_dist
        scoresTOFI += toF_dist
        scoresTSRP += tsR_dist
        scoresTSNN += tsN_dist
        scoresTSFI += tsF_dist
    # 1 - 2 / 2


    avr_scoreNN = scoresNN / repeats
    avr_scoreFI = scoresFI / repeats
    avr_scoreRP = scoresRP / repeats

    avr_scoreTORP = scoresTORP / repeats
    avr_scoreTONN = scoresTONN / repeats
    avr_scoreTOFI = scoresTOFI / repeats

    avr_scoreTSRP = scoresTSRP / repeats
    avr_scoreTSNN = scoresTSNN / repeats
    avr_scoreTSFI = scoresTSFI / repeats


    avr_scoresNN.append(avr_scoreNN)
    avr_scoresFI.append(avr_scoreFI)
    avr_scoresRP.append(avr_scoreRP)

    avr_scoresTSRP.append(avr_scoreTSRP)
    avr_scoresTSNN.append(avr_scoreTSNN)
    avr_scoresTSFI.append(avr_scoreTSFI)

    avr_scoresTORP.append(avr_scoreTORP)
    avr_scoresTONN.append(avr_scoreTONN)
    avr_scoresTOFI.append(avr_scoreTOFI)

    results.append({
        'size': size,
        'scoreNN': avr_scoreNN,
        'scoreFI': avr_scoreFI,
        'scoreTORP': avr_scoreTORP,
        'scoreTONN': avr_scoreTONN,
        'scoreTOFI': avr_scoreTOFI,
        'scoreTSRP': avr_scoreTSRP,
        'scoreTSNN': avr_scoreTSNN,
        'scoreTSFI': avr_scoreTSFI
    })

df = pd.DataFrame(results)
df.to_csv("tsp_benchmarak_results.csv", index=False)
print("Wyniki zapisane do pliku tsp_results.csv")

# plt.figure(figsize=(10, 6))
# plt.plot(sizes, avr_scoresNN, label='NN', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresFI, label='FI', marker='o',alpha=0.7)
# # plt.plot(sizes, avr_scoresRP, label='RP', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresTONN, label='TONN', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresTOFI, label='TOFI', marker='o',alpha=0.7)
# # plt.plot(sizes, avr_scoresSARP, label='SARP', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresTSNN, label='TSNN', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresTSFI, label='TSFI', marker='o',alpha=0.7)

# plt.xlabel('Liczba wierzchołków w instancji')
# plt.ylabel('(A-A*)/A*[%]')
# plt.title('Porównanie różnych kombinacji algorytmów dla problemu TSP')
# plt.legend()
# plt.grid(True)
# plt.show()

plt.figure(figsize=(10, 6))
plt.plot(sizes, avr_scoresNN, label='NN', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresFI, label='FI', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresRP, label='RP', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresTONN, label='TONN', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresTOFI, label='TOFI', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresTORP, label='TORP', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresTSNN, label='TSNN', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresTSFI, label='TSFI', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresTSRP, label='TSRP', marker='o',alpha=0.7)
plt.xlabel('Liczba wierzchołków w instancji')
plt.ylabel('(A-A*)/A*[%]')
plt.title('Porównanie różnych kombinacji algorytmów dla problemu TSP')
plt.legend()
plt.grid(True)
plt.show()

# plt.figure(figsize=(10, 6))
# # plt.plot(sizes, avr_scoresNN, label='NN', marker='o',alpha=0.7)
# # plt.plot(sizes, avr_scoresFI, label='FI', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresRP, label='RP', marker='o',alpha=0.7)
# # plt.plot(sizes, avr_scoresSANN, label='SANN', marker='o',alpha=0.7)
# # plt.plot(sizes, avr_scoresSAFI, label='SAFI', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresTORP, label='TORP', marker='o',alpha=0.7)
# plt.plot(sizes, avr_scoresTSRP, label='TSRP', marker='o',alpha=0.7)

# plt.xlabel('Liczba wierzchołków w instancji')
# plt.ylabel('(A-A*)/A*[%]')
# plt.title('Porównanie różnych kombinacji algorytmów dla problemu TSP')
# plt.legend()
# plt.grid(True)
# plt.show()