
from matplotlib import pyplot as plt
from Tsp import FI, NN, RandomPermutation, plot_path,coordinatesToDistMatrix, generateCoordinates, SA

repeats = 10
sizes = [100,200,300,400,500,600,700,800,900,1000]
# sizes = [10,20,30,40,50,60,70,80,90,100]

avr_scoresNN = []
avr_scoresFI = []
avr_scoresSARP = []
avr_scoresSANN = []
avr_scoresSAFI = []

for size in sizes:
    scoresNN = []
    scoresFI = []
    scoresSARP = []
    scoresSANN = []
    scoresSAFI = []
    for i in range(repeats):
        print("repeat:",i,"/",repeats,", size: ",size)

        coordinates = generateCoordinates(size)
        distMatrix = coordinatesToDistMatrix(coordinates)

        # podstawowe algorytmy
        pathNN, distNN = NN(distMatrix)
        pathFI, distFI = FI(distMatrix)
        pathRP, distRP = RandomPermutation(distMatrix)

        # wyrzażanie dla NN, FI oraz random
        saF_permutation, Fpermutation_value_history = SA(distMatrix,pathFI[:-1], cf = 0.99)
        saN_permutation, Npermutation_value_history = SA(distMatrix,pathNN[:-1], cf = 0.99)
        saR_permutation, Rpermutation_value_history = SA(distMatrix,pathRP[:-1], cf = 0.99)

        # przeliczenie wyników procentowa lepszość od randomowej prermutacji
        comp_score = distRP

        scoresNN.append((distNN-comp_score)/comp_score)
        scoresFI.append((distFI-comp_score)/comp_score)
        scoresSARP.append(((Rpermutation_value_history)-comp_score)/comp_score)
        scoresSANN.append(((Npermutation_value_history)-comp_score)/comp_score)
        scoresSAFI.append(((Fpermutation_value_history)-comp_score)/comp_score)

    avr_scoresNN.append(sum(scoresNN)/repeats)
    avr_scoresFI.append(sum(scoresFI)/repeats)
    avr_scoresSARP.append(sum(scoresSARP)/repeats)
    avr_scoresSANN.append(sum(scoresSANN)/repeats)
    avr_scoresSAFI.append(sum(scoresSAFI)/repeats)

plt.figure(figsize=(10, 6))
plt.plot(sizes, avr_scoresNN, label='NN', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresFI, label='FI', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresSANN, label='SANN', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresSAFI, label='SAFI', marker='o',alpha=0.7)
plt.plot(sizes, avr_scoresSARP, label='SARP', marker='o',alpha=0.7)

plt.xlabel('Liczba wierzchołków w instancji')
plt.ylabel('Lepszość [%]')
plt.title('Porównanie różnych kombinacji algorytmów dla problemu TSP')
plt.legend()
plt.grid(True)
plt.show()

