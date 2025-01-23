import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_name = "tsp_benchmarak_results.csv"
data = pd.read_csv(file_name)

# Flags to control which plots to show
show_basic = True
show_twoOpt = True
show_TabuSearch = True

show_random = False
show_Fi = True
show_NN = True

To_FI = [ (data['scoreTOFI'][i] - data['scoreFI'][i])/data['scoreFI'][i] for i in range(0,data['scoreFI'].size) ]
Ts_FI = [ (data['scoreTSFI'][i] - data['scoreFI'][i])/data['scoreFI'][i] for i in range(0,data['scoreFI'].size) ]

To_NN = [ (data['scoreTONN'][i] - data['scoreNN'][i])/data['scoreNN'][i] for i in range(0,data['scoreNN'].size) ]
Ts_NN = [ (data['scoreTSNN'][i] - data['scoreNN'][i])/data['scoreNN'][i] for i in range(0,data['scoreNN'].size) ]

# Display the DataFrame
print(data)

# Plot the data
plt.figure(figsize=(10, 6))

if show_basic:
    # Plot basic scores
    if show_NN:
        plt.plot(data['size'], data['scoreNN'], label='Score NN', marker='o',color = "purple")
    if show_Fi:
        plt.plot(data['size'], data['scoreFI'], label='Score FI', marker='o',color = "purple")

if show_twoOpt:
    # Plot TwoOpt scores
    if show_random:
        plt.plot(data['size'], data['scoreTORP'], label='Score TORP', marker='o', color="lightgreen")
    if show_NN:
        plt.plot(data['size'], data['scoreTONN'], label='Score TONN', marker='o', color="green")
    if show_Fi:
        plt.plot(data['size'], data['scoreTOFI'], label='Score TOFI', marker='o', color="darkgreen")

if show_TabuSearch:
    # Plot TabuSearch scores
    if show_random:
        plt.plot(data['size'], data['scoreTSRP'], label='Score TSRP', marker='o', color="lightblue")
    if show_NN:
        plt.plot(data['size'], data['scoreTSNN'], label='Score TSNN', marker='o', color="blue")
    if show_Fi:
        plt.plot(data['size'], data['scoreTSFI'], label='Score TSFI', marker='o', color="darkblue")


# Customize the plot
plt.title("TSP Benchmark Results")
plt.xlabel("Size")
plt.ylabel("Scores")
plt.legend()
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()
