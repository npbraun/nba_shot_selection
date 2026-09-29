import math
import pandas as pd
import csv
import matplotlib.pyplot as plt
import winprobcalc as wpc
import numpy as np
import seaborn as sns
import statistics

if __name__ == "__main__":
    # CPU should be weakly better than NBA in all cases

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
    numrepeat = int(input("Enter number of games to simulate: "))
    # firstposs = input("Which team to shoot first? (CPU or NBA): ")

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
                if nbacol > 0 and nbacol < 2 * (maxdiff + 1) :
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

    # Initialize matrices with proper dimension
    wpc.creatematrix(probmatrix, numposs, numcols)
    wpc.creatematrix(shotmatrix, numposs, numcols)
    wpc.creatematrix(teamprob, numposs, numcols)

    # Fill shotmatrix with optimal shot types based on situation
    wpc.strategy(team1twopt, team1threept, team1ft, oreb, tempo, teamshot, shotmatrix, teamprob, probmatrix)

    cpuscore = []
    teamscore = []
    cpumargin = []

    csvfile1 = "./nbashot.csv"
    nbashot_df = pd.DataFrame(teamshot)
    nbashot_df.to_csv(csvfile1, header=False, index=False)

    csvfile1 = "./cpushot.csv"
    shotmatrix_df = pd.DataFrame(shotmatrix)
    shotmatrix_df.to_csv(csvfile1, header=False, index=False)


    # Simulate numrepeat games of numposs possessions and keep track of score in matrices
    for i in range(numrepeat):
        score = wpc.gamesim(team1twopt, team1threept, team1ft, oreb, tempo, shotmatrix, teamshot, "cpu", "nba")
        cpuscore.append(score[0])
        teamscore.append(score[1])
        cpumargin.append(score[0] - score[1])

    cpuavg = 0
    cpuwins = 0
    teamavg = 0
    teamwins = 0
    ties = 0
    marginavg = 0

    # Simulate games again with two nba teams playing
    team1shot = teamshot.copy()

    team1score = []
    team2score = []
    team1margin = []

    # Simulate numrepeat games of numposs possessions and keep track of score in matrices
    for i in range(numrepeat):
        score = wpc.gamesim(team1twopt, team1threept, team1ft, oreb, tempo, team1shot, teamshot, "nba", "nba")
        team1score.append(score[0])
        team2score.append(score[1])
        team1margin.append(score[0] - score[1])

    # Report summary data from simulated games (CPU v NBA)
    for i in range(len(cpuscore)):
        cpuavg += cpuscore[i]
        teamavg += teamscore[i]
        if cpuscore[i] > teamscore[i]:
            cpuwins += 1
            marginavg += cpumargin[i]
        elif teamscore[i] > cpuscore[i]:
            teamwins += 1
        else:
            ties += 1

    cpuavg /= len(cpuscore)
    teamavg /= len(teamscore)
    marginavg /= cpuwins

    print("Computer record: %d W, %d L, %d T" % (cpuwins, teamwins, ties))
    print(f"Average score: {cpuavg} : {teamavg}")
    print(f"Average win margin for CPU:  {marginavg}")
    print(f"Variance of cpumargin: {statistics.variance(cpumargin)}")

    # Print summary data about team 1's performance:
    t1avg = 0
    t1wins = 0
    t2avg = 0
    t2wins = 0
    nbaties = 0
    t1marginavg = 0

    for i in range(len(team1score)):
        t1avg += team1score[i]
        t2avg += team2score[i]
        if team1score[i] > team2score[i]:
            t1wins += 1
            t1marginavg += team1margin[i]
        elif team2score[i] > team1score[i]:
            t2wins += 1
        else:
            nbaties += 1

    t1avg /= len(team1score)
    t2avg /= len(team2score)
    if t1wins > 0:
        t1marginavg /= t1wins

    print("Team 1 record: %d W, %d L, %d T" %(t1wins, t2wins, nbaties))
    print(f"Average score: {t1avg} : {t2avg}")
    print(f"Average win margin for Team 1:  {t1marginavg}")
    print(f"Variance of team1margin : {statistics.variance(team1margin)}")

    # Maximum for plotting
    maxmargin = max(
        max(cpumargin),
        max(team1margin),
        abs(min(cpumargin)),
        abs(min(team1margin))
    )

    bound = maxmargin + maxmargin % 2
    alpha = 0.5

    integer_range = np.arange(-bound, bound + 1)
    bins = integer_range - 0.5
    bins = np.append(bins, bound + 0.5)

    # FIGURE 1: Two stacked histograms

    fig1, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    n1, _, _ = axes[0].hist(
        team1margin,
        bins=bins,
        color="red",
        edgecolor="black",
        alpha=alpha
    )

    axes[0].set_title("NBA Strategy")
    axes[0].axvline(0, color="black", linestyle="--")
    axes[0].plot([], [], label=f"{numrepeat:,}", color="red", alpha=alpha)
    axes[0].legend(title="Number of Simulations")

    n2, _, _ = axes[1].hist(
        cpumargin,
        bins=bins,
        color="blue",
        edgecolor="black",
        alpha=alpha
    )

    axes[1].set_title("Optimal Strategy")
    axes[1].axvline(0, color="black", linestyle="--", alpha=0.7)
    axes[1].plot([], [], label=f"{numrepeat:,}", color="blue", alpha=alpha)
    axes[1].legend(title="Number of Simulations")

    max_y = max(n1.max(), n2.max())

    axes[0].set_ylim(0, max_y * 1.05)
    axes[1].set_ylim(0, max_y * 1.05)

    fig1.suptitle("Distribution of Final Score Differentials")
    axes[1].set_xlabel("Score Difference")

    fig1.tight_layout()


    # FIGURE 2: Overlaid histogram
    fig2, ax2 = plt.subplots(figsize=(10, 6))

    ax2.hist(
        cpumargin,
        bins=bins,
        alpha=alpha,
        label="CPU",
        color="blue",
        edgecolor="black"
    )

    ax2.hist(
        team1margin,
        bins=bins,
        alpha=alpha,
        label="NBA",
        color="red",
        edgecolor="black"
    )

    ax2.set_title("Distribution of Final Score Differential")
    ax2.legend(loc="upper right")
    ax2.axvline(0, color="black", linestyle="--")

    plt.show()

    # # Plot difference between histograms (Optimal - NBA)
    # nba_freq, bin_edges = np.histogram(team1margin, bins=bins)
    # optimal_freq, _ = np.histogram(cpumargin, bins=bins)
    # diff_freq = optimal_freq - nba_freq
    # plt.figure(figsize=(10, 6))
    #
    # bar_colors = ["blue" if x > 0 else "red" for x in diff_freq]
    # plt.bar(
    #     integer_range,
    #     diff_freq,
    #     width=1,
    #     edgecolor="black",
    #     color=bar_colors,
    #     alpha=alpha
    # )
    #
    # plt.axhline(0, color="black", linestyle="-", linewidth=1.5)
    # plt.grid(axis="y", linestyle="--", alpha=0.7)
    # plt.title(
    #     "Difference in Frequency of Final Scores (CPU - NBA)",
    #     fontsize=14,
    # )
    # plt.xlabel("Score", fontsize=12)
    # plt.ylabel("Difference in Frequency", fontsize=12)
    #
    # plt.show()
    #
    # # Plot cumulative difference in frequency
    # cumulative_diff = np.cumsum(diff_freq)
    #
    # plt.figure(figsize=(10, 6))
    #
    # plt.step(
    #     integer_range,
    #     cumulative_diff,
    #     where="mid",
    #     color="purple",
    #     linewidth=2.5,
    #     label="Cumulative Difference",
    # )
    #
    # plt.fill_between(
    #     integer_range, cumulative_diff, step="mid", color="purple", alpha=0.15
    # )
    # plt.axhline(0, color="black", linestyle="-", linewidth=1.5)
    #
    # plt.grid(True, linestyle="--", alpha=0.5)
    #
    # plt.title(
    #     "Cumulative Difference in Score Frequency (CPU vs. NBA)",
    #     fontsize=14,
    # )
    # plt.xlabel("Score Margin", fontsize=12)
    # plt.ylabel("Cumulative Difference", fontsize=12)
    #
    # plt.show()
    #
    # # Plot the survival function
    # # Convert counts into probabilities (percentages between 0 and 1)
    # nba_prob = nba_freq / np.sum(nba_freq)
    # optimal_prob = optimal_freq / np.sum(optimal_freq)
    #
    # # Calculate P(X > x)
    # cpu_survival = [np.sum(optimal_prob[integer_range > x]) for x in integer_range]
    # nba_survival = [np.sum(nba_prob[integer_range > x]) for x in integer_range]
    #
    # plt.figure(figsize=(10, 6))
    #
    # # Plot the lines
    # plt.step(
    #     integer_range,
    #     cpu_survival,
    #     where="mid",
    #     color="blue",
    #     linewidth=2.5,
    #     label="CPU",
    #     alpha = alpha
    # )
    # plt.step(
    #     integer_range,
    #     nba_survival,
    #     where="mid",
    #     color="red",
    #     linewidth=2.5,
    #     label="NBA",
    #     alpha = alpha
    # )
    #
    # # Set Y-axis to show percentages cleanly (0% to 100%)
    # plt.ylim(0, 1.05)
    # plt.gca().yaxis.set_major_formatter(
    #     plt.FuncFormatter(lambda y, _: f"{y * 100:.0f}%")
    # )
    #
    # plt.axvline(0, color="black", linestyle="--", alpha=0.7)
    # plt.grid(True, linestyle="--", alpha=0.5)
    # plt.title(
    #     "Probability of Winning by More Than 'X' Points (Survival Function)",
    #     fontsize=14,
    # )
    # plt.xlabel("Score Margin (X)", fontsize=12)
    # plt.ylabel("Probability P(Margin > X)", fontsize=12)
    # plt.legend(loc="upper right", fontsize=12)
    #
    # plt.show()
    #
    # # Now plot difference in survival functions
    # diff_survival = np.array(cpu_survival) - np.array(nba_survival)
    #
    # plt.step(
    #     integer_range,
    #     diff_survival,
    #     where="mid",
    #     color="purple",
    #     linewidth=2.5,
    #     label="Difference (CPU - NBA)",
    #     alpha=alpha
    # )
    #
    # # Set Y-axis to show percentages cleanly (0% to 100%)
    # plt.ylim(-0.25, 0.25)
    # plt.gca().yaxis.set_major_formatter(
    #     plt.FuncFormatter(lambda y, _: f"{y * 100:.0f}%")
    # )
    #
    # plt.axvline(0, color="black", linestyle="--", alpha=0.7)
    # plt.axhline(0, color="black",linestyle="-", linewidth=1.5)
    # plt.grid(True, linestyle="--", alpha=0.5)
    # plt.title(
    #     "Difference in Survival Functions (CPU - NBA)",
    #     fontsize=14,
    # )
    # plt.xlabel("Score Margin (X)", fontsize=12)
    # plt.ylabel("P(CPU > X) - P(NBA > X)", fontsize=12)
    # plt.legend(loc="upper right", fontsize=12)
    #
    # plt.show()

