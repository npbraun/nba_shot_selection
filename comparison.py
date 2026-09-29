import math
from tabulate import tabulate
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import winprobcalc as wpc

if __name__ == "__main__":
    # This file will compare the win probability between optimal and NBA strategy
    # Results in a plot of optimal win probability - theoretical NBA win probability
    # Numerical values are stored in comparison.csv

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

    # Reset values of teamprob back to 0
    for i in range(len(teamprob)):
        for j in range(len(teamprob[0])):
            if i != 0 and j != 0:
                teamprob[i][j] = 0

    # PRINT OUTPUT (Check that teamprob reset correctly)
    # for j in range(numcols):
    #     shotmatrix[0][j] = str(f"{shotmatrix[0][j]:^4}")
    #     probmatrix[0][j] = str(f"{shotmatrix[0][j]:^4}")
    # print("Winning Probability Table (Computer): ")
    # print(tabulate(probmatrix, floatfmt=".4f", headers="firstrow", numalign="center", stralign="center",
    #                tablefmt="fancy_grid"))
    # print("\nShot Selection Table (Computer): ")
    # print(tabulate(shotmatrix, floatfmt=".4f", headers="firstrow", numalign="center", stralign="center",
    #                tablefmt="fancy_grid"))
    # print('\nShot Selection Table (Team): ')
    #
    # teamshot_formatted = teamshot.copy()
    # teamshot_formatted[0][0] = teamshot[0][0]
    # for i in range(len(teamshot_formatted)):
    #     for j in range(len(teamshot_formatted[i])):
    #         if i == 0 and j == 0:
    #             continue
    #         teamshot_formatted[i][j] = wpc.format_floats(teamshot_formatted[i][j])
    #
    # print(tabulate(teamshot_formatted, floatfmt=".4f", headers="firstrow", numalign="center", stralign="center",
    #                tablefmt="fancy_grid"))
    # print('\nWinning Probability Table (Team): ')
    # print(tabulate(teamprob, floatfmt=".4f", headers="firstrow", numalign="center", stralign="center",
    #                tablefmt="fancy_grid"))

    # Calculate NBA v NBA mirror matchup
    team2shot = teamshot.copy()
    team2prob = teamprob.copy()
    wpc.nbamirror(team1twopt, team1threept, team1ft, oreb, tempo, teamshot, team2shot, teamprob, team2prob)

    # Print results for NBA team in mirror match (Check only)
    teamshot_formatted = teamshot.copy()
    teamshot_formatted[0][0] = teamshot[0][0]
    for i in range(len(teamshot_formatted)):
        for j in range(len(teamshot_formatted[i])):
            if i == 0 and j == 0:
                continue
            teamshot_formatted[i][j] = wpc.format_floats(teamshot_formatted[i][j])

    print(tabulate(teamshot_formatted, floatfmt=".4f", headers="firstrow", numalign="center", stralign="center",
                   tablefmt="fancy_grid"))
    print('\nWinning Probability Table (Team): ')
    print(tabulate(teamprob, floatfmt=".4f", headers="firstrow", numalign="center", stralign="center",
                   tablefmt="fancy_grid"))

    # Compare Win % against a team using NBA strategy for team 1 when team 1 uses game theory and when team 1 uses NBA
    comparison = []

    wpc.creatematrix(comparison, numposs, numcols)
    for i in range(len(comparison)):
        for j in range(len(comparison[0])):
            if i != 0 and j != 0:
                comparison[i][j] = probmatrix[i][j] - teamprob[i][j]

    axis = min(int((len(comparison) - 1) / 2), maxdiff)

    print("Winning Probability Comparison Table (Game Theory - NBA): ")
    print(tabulate(comparison, floatfmt=".4f", headers="firstrow", numalign="center", stralign="center",
                   tablefmt="fancy_grid"))

    comparison_df = pd.DataFrame(comparison)
    # Graph results of comparison_df
    adjustment = int(numcols / 2)
    # Set posslimit to only graph the last n possessions
    posslimit = numposs - 1

    # PLOT GRAPH OF COMPARISON USING FIXED POSSESSIONS, VARIABLE SCORE

    score = comparison_df.iloc[0, 1:]

    possessions = comparison_df.iloc[15::15, 0].values
    winprob = comparison_df.iloc[15::15, 1:]

    plt.figure(figsize=(10, 6))

    # Loop through each row and plot
    for i, idx in enumerate(winprob.index):
        plt.plot(
            score,  # X-axis from row 0
            winprob.loc[idx],  # Y-values for this row
            label=str(possessions[i])
        )

    plt.xlabel("Score Differential")
    plt.ylabel("Win Percentage Added")
    plt.title("Win Percentage Added by Optimal Strategy")

    # Y-axis formatting
    plt.ylim(0, 0.075)
    ax = plt.gca()
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
    ax.yaxis.set_minor_locator(MultipleLocator(0.01))

    # X-axis formatting: only integer major ticks if applicable
    ax.xaxis.set_major_locator(MultipleLocator(6))
    plt.xlim(-axis, axis)

    # Gridlines
    ax.grid(which='major', axis='both', linestyle='-', linewidth=0.8)
    ax.grid(which='minor', axis='y', linestyle='--', linewidth=0.5, alpha=0.6)
    plt.axvline(0, color="black", linestyle="--", alpha=0.7)

    # ax.invert_xaxis()

    # Legend on right with title
    plt.legend(
        title="Possessions remaining",
        loc="upper right"
    )

    plt.tight_layout()
    plt.show()

    legend_labels = comparison_df.iloc[0, adjustment - 5:adjustment + 5].values
    x_values = comparison_df.iloc[1:, 0].values
    filtered = comparison_df.iloc[1:, adjustment - 5:adjustment + 5]

    plt.figure(figsize=(10, 6))
    # Plot each column using column 0 as x-axis
    for i, col in enumerate(filtered.columns):
        plt.plot(
            x_values,  # x-axis
            filtered[col].values,  # y-axis (one column at a time)
            label=str(legend_labels[i])
        )
    plt.xlabel("Time")
    plt.ylabel("Win %")
    plt.title("Win % Against Time with Fixed Score")

    # Set y-axis limits
    plt.ylim(0, 0.10)

    # Configure major and minor ticks
    ax = plt.gca()
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax.xaxis.set_major_locator(MultipleLocator(10))
    # Gridlines for major and minor ticks
    ax.grid(which='major', linestyle='-', linewidth=0.8)
    ax.grid(which='minor', axis='y', linestyle='--', linewidth=0.5, alpha=0.6)

    ax.invert_xaxis()
    # Legend on right with title
    plt.legend(
        title="Score",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    plt.tight_layout()
    plt.show()

    # DOWNLOAD OUTPUT AS CSV FILES
    csvfile1 = "./teamprob.csv"
    teamprob_df = pd.DataFrame(teamprob)
    teamprob_df.to_csv(csvfile1, header=False, index=False)
    csvfile1 = "./teamshot.csv"
    teamshot_df = pd.DataFrame(teamshot)
    teamshot_df.to_csv(csvfile1, header=False, index=False)
    csvfile1 = "./winprob.csv"
    csvfile2 = "./shottype.csv"
    probmatrix_df = pd.DataFrame(probmatrix)
    probmatrix_df.to_csv(csvfile1, header=False, index=False)
    shotmatrix_df = pd.DataFrame(shotmatrix)
    shotmatrix_df.to_csv(csvfile2, header=False, index=False)
    csvfile1 = "./comparison.csv"
    comparison_df.to_csv(csvfile1, header=False, index=False)


