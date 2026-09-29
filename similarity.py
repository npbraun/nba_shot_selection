import math
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import winprobcalc as wpc

if __name__ == "__main__":
    # This file will calculate the similarity between the NBA team's strategy and the optimal strategy.
    # Begin by comparing the 2pt frequency in each cell.
    # Use subtraction for an absolute measure
    # The y-axis value to be plotted is the frequency that an NBA team shoots a 2 pointer - optimal 2pt frequency
    # Value of 20% means an NBA team shoots 2 pointers 20 percentage points too frequently in that situation

    # Later, use division for a relative measure to calculate how much WPA is added in the situation by a
    # constant amount of strategy improvement

    # Get user inputs
    print("Simulate games between team using optimal strategy and one using NBA strategy:")
    print("League average values for 2pt and 3pt% are: 55% and 36%")
    print("Recommended number of possessions: 200")
    team1twopt = float(input("Enter two-point shot percentage for team 1 as a decimal: "))
    team1threept = float(input("Enter three-point shot percentage for team 1 as a decimal: "))
    # team1ft = float(input("Enter free throw shot percentage for team 1 as a decimal: "))
    team1ft = 0
    team2twopt = team1twopt
    # float(input("Enter two-point shot percentage for team 2 as a decimal: "))
    team2threept = team1threept
    # float(input("Enter three-point shot percentage for team 2 as a decimal: "))
    team2ft = team1ft
    # float(input("Enter free throw shot percentage for team 2 as a decimal: "))
    numposs = int(input("Enter number of total possessions: "))
    # shootingteam = int(input("Enter which team is shooting first, 1 or 2: "))
    # oreb = float(input("Enter Offensive Rebounding Percentage as a decimal: "))
    # TO = float(input("Enter turnover Percentage as a decimal: "))
    # tempo = input("Allow for quick/slow shots?: ")
    oreb = 0
    TO = 0
    tempo = 'n'

    rows = numposs + 1
    cols = 3 * numposs + 2

    probmatrix = []
    shotmatrix = []
    teamshot = []
    teamprob = []

    # CREATE THE SHOT SELECTION TABLE FOR THE TEAM USING RESULT FROM R REGRESSION OUTPUT:
    # Use csv.reader to parse the file, then convert the iterator directly to a list
    with open('/Users/nathanbraun/Downloads/nbashotmatrix.csv', mode='r', newline='', encoding='utf-8') as f:
        nbashotmatrix = list(csv.reader(f))

    # Convert nbashotmatrix values to float from string
    for i in range(len(nbashotmatrix)):
        for j in range(len(nbashotmatrix[1])):
            if i != 0 or j != 0:
                nbashotmatrix[i][j] = float(nbashotmatrix[i][j])

    # Create teamshotmatrix which uses values directly from nbashotmatrix where available and regression otherwise
    maxdiff = -nbashotmatrix[0][1]
    print(f"maxdiff : {maxdiff}")
    maxposs = len(nbashotmatrix) - 1
    print(f"maxposs: {maxposs}")
    numcols = int(6 * math.ceil(numposs / 2) + 2)
    print(f"numcols: {numcols}")
    for i in range(numposs + 1):
        # print(f"col: {i}")
        row = []
        # for j in range(min(6 * math.ceil(numposs / 2) + 2, 64)):
        for j in range(numcols):
            nbacol = int(j + maxdiff - (3 * math.ceil(numposs / 2)))
            # print(f"nbacol: {nbacol}")
            if i == 0:
                if j == 0:
                    row.append("Poss, Score")
                elif j == 1:
                    row.append(3 * -math.ceil(numposs / 2))
                else:
                    row.append(row[j - 1] + 1)
            elif j == 0:
                row.append(i)
            else:
                if nbacol > 0 and nbacol < 2 * (maxdiff + 1):
                    prob3 = nbashotmatrix[i][nbacol]

                    if nbashotmatrix[i][nbacol] == -999:
                        # Calculate odds from R logistic regression (which outputs log-odds)
                        x = math.exp(-0.3 - 1.6 * (10 ** -4) * i)
                        # Convert log odds to probability
                        prob2 = x / (1 + x)
                        row.append([prob2, 1 - prob2, 0, 0])
                    else:
                        row.append([1 - prob3, prob3, 0, 0])
                else:
                    x = math.exp(-0.3 - 1.6 * (10 ** -4) * i)
                    # Convert log odds to probability
                    prob2 = x / (1 + x)
                    row.append([prob2, 1 - prob2, 0, 0])
        teamshot.append(row)

    wpc.creatematrix(probmatrix, numposs, numcols)
    wpc.creatematrix(shotmatrix, numposs, numcols)
    wpc.creatematrix(teamprob, numposs, numcols)

    # Calculate matchup between CPU and NBA team
    wpc.strategy(team1twopt, team1threept, team1ft, oreb, tempo, teamshot, shotmatrix, teamprob, probmatrix)

    stratdist = []
    wpc.creatematrix(stratdist, numposs, numcols)

    # Calculate the difference in strategies.
    # This code computes an absolute measure of distance: if stratdist[i][j] = 0.20, then nba teams shoot 2-pointers
    # with a frequency 20 percentage points greater than the optimal frequency
    for i in range(len(shotmatrix)):
        for j in range(len(shotmatrix[1])):
            if i != 0 and j != 0:
                if shotmatrix[i][j] == "Quick 2":
                    stratdist[i][j] = teamshot[i][j][0] - 1
                elif shotmatrix[i][j] == "Quick 3":
                    stratdist[i][j] = teamshot[i][j][0]
                else:

                    stratdist[i][j] = 0

    stratdist_df = pd.DataFrame(stratdist)

    # GRAPH THE RESULTS
    adjustment = (3 * math.ceil(numposs / 2)) + 1
    # Plot with fixed possessions
    score = stratdist_df.iloc[0, 1:]

    # Extract y-values: all rows excluding row 0 and column 0
    winprob = stratdist_df.iloc[numposs - 10:, 1:]

    # Extract labels from column 0 (excluding row 0)
    possessions = stratdist_df.iloc[numposs - 10:, 0].values

    plt.figure(figsize=(10, 6))

    # Loop through each row and plot
    for i, idx in enumerate(winprob.index):
        plt.plot(
            score,  # X-axis from row 0
            winprob.loc[idx],  # Y-values for this row
            label=str(possessions[i])
        )

    plt.xlabel("Score")
    plt.ylabel("2pt Frequency Relative to Optimal")
    plt.title("Strategy Similarity against Score with Fixed Number of Possessions")

    # Y-axis formatting
    plt.ylim(-1, 1)
    plt.xlim(-30, 30)
    ax = plt.gca()
    ax.yaxis.set_major_locator(MultipleLocator(0.25))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))

    # X-axis formatting: only integer major ticks if applicable
    ax.xaxis.set_major_locator(MultipleLocator(10))

    # Gridlines
    ax.grid(which='major', axis='both', linestyle='-', linewidth=0.8)
    ax.grid(which='minor', axis='y', linestyle='--', linewidth=0.5, alpha=0.6)

    # ax.invert_xaxis()

    # Legend on right with title
    plt.legend(
        title="Poss",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )
    plt.axhline(0, color="black", linestyle="-", linewidth=1.5)
    plt.tight_layout()
    plt.show()

    # Alternative methods would be: What % of the time does the NBA team make the correct shot?
