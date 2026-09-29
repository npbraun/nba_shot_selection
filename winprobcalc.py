import math
from tabulate import tabulate
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FormatStrFormatter
import numpy as np


def calcwinprobmatrix(t1twopt, t1threept, numposs, oreb, TO, prob, shot):
    adjustment = 3 * math.ceil(numposs / 2) + 1
    max_index = 6 * math.ceil(numposs / 2) + 2
    for poss in range(1, numposs + 1):
        for scorediff in range(-adjustment + 1, adjustment):
            # Calculate values for the final possession
            if poss == 1:
                if scorediff > 0:
                    winp2 = 1
                elif scorediff == 0:
                    winp2 = t1twopt + 0.5 * (1 - t1twopt)
                elif (scorediff + 2) > 0:
                    winp2 = t1twopt
                elif (scorediff + 2) == 0:
                    winp2 = (0.5 * t1twopt)
                else:
                    winp2 = 0
                if scorediff > 0:
                    winp3 = 1
                elif scorediff == 0:
                    winp3 = (t1threept + 0.5 * (1 - t1threept))
                elif (scorediff + 3) > 0:
                    winp3 = t1threept
                elif (scorediff + 3) == 0:
                    winp3 = (0.5 * t1threept)
                else:
                    winp3 = 0
                prob[poss][scorediff + adjustment] = max(winp2, winp3)
                if winp2 > winp3:
                    shot[poss][scorediff + adjustment] = "2pt"
                elif winp3 > winp2:
                    shot[poss][scorediff + adjustment] = "3pt"
                else:
                    shot[poss][scorediff + adjustment] = "2 or 3"
            # Win% and lead are always the % for the shooting team
            else:
                if scorediff + adjustment + 2 >= max_index:
                    winp2 = ((1 - TO) * t1twopt + (1 - TO) * (1 - t1twopt) *
                             (1 - oreb) * (1 - prob[poss - 1][-1 * (scorediff + adjustment)]))
                    (+ (1 - TO) * (1 - t1twopt) * oreb * prob[poss - 1][scorediff + adjustment] +
                     TO * (1 - prob[poss - 1][-1 * (scorediff + adjustment)]))
                    winp3 = ((1 - TO) * t1threept + (1 - TO) * (1 - t1threept) *
                             (1 - oreb) * (1 - prob[poss - 1][-1 * (scorediff + adjustment)]))
                    (+ (1 - TO) * (1 - t1threept) * oreb * prob[poss - 1][scorediff + adjustment] +
                     TO * (1 - prob[poss - 1][-1 * (scorediff + adjustment)]))
                elif scorediff + adjustment + 3 >= max_index:
                    winp3 = ((1 - TO) * t1threept + (1 - TO) * (1 - t1threept) *
                             (1 - oreb) * (1 - prob[poss - 1][-1 * (scorediff + adjustment)]))
                    (+ (1 - TO) * (1 - t1threept) * oreb * prob[poss - 1][scorediff + adjustment] +
                     TO * (1 - prob[poss - 1][-1 * (scorediff + adjustment)]))
                    winp2 = (1 - TO) * (t1twopt * (1 - prob[poss - 1][-1 * (scorediff + adjustment + 2)])
                                        + (1 - TO) * (1 - t1twopt) * (1 - oreb) * (
                                                1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                        + (1 - TO) * (1 - t1twopt) * oreb * prob[poss - 1][scorediff + adjustment]
                                        + TO * (1 - prob[poss - 1][-1 * (scorediff + adjustment)]))
                else:
                    winp2 = (1 - TO) * (t1twopt * (1 - prob[poss - 1][-1 * (scorediff + adjustment + 2)])
                                        + (1 - TO) * (1 - t1twopt) * (1 - oreb) * (
                                                1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                        + (1 - TO) * (1 - t1twopt) * oreb * prob[poss - 1][scorediff + adjustment]
                                        + TO * (1 - prob[poss - 1][-1 * (scorediff + adjustment)]))
                    winp3 = (1 - TO) * (t1threept * (1 - prob[poss - 1][-1 * (scorediff + adjustment + 3)])
                                        + (1 - TO) * (1 - t1threept) * (1 - oreb) * (
                                                1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                        + (1 - TO) * (1 - t1threept) * oreb * prob[poss - 1][scorediff + adjustment]
                                        + TO * (1 - prob[poss - 1][-1 * (scorediff + adjustment)]))
                prob[poss][scorediff + adjustment] = max(winp2, winp3)
                if winp2 > winp3:
                    shot[poss][scorediff + adjustment] = "2pt"
                elif winp3 > winp2:
                    shot[poss][scorediff + adjustment] = "3pt"
                else:
                    shot[poss][scorediff + adjustment] = "2 or 3"


def timematrix(t1twopt, t1threept, t2twopt, t2threept, numposs, oreb, TO, prob, shot):
    adjustment = 1 * (3 * math.ceil(numposs / 2) + 1)
    max_index = 1 * (6 * math.ceil(numposs / 2) + 2)
    for poss in range(1, numposs + 1):
        for scorediff in range(-adjustment + 1, adjustment):
            # Calculate values for the final possession
            if poss == 1:
                winquick2 = 0
                winquick3 = 0
                winslow2 = 0
                winslow3 = 0
                if scorediff > 0:
                    winquick2 = 1
                    winquick3 = 1
                    winslow2 = 1
                    winslow3 = 1
                elif scorediff == 0:
                    winquick2 = t1twopt + 0.5 * (1 - t1twopt)
                    winquick3 = t1threept + 0.5 * (1 - t1threept)
                    winslow2 = 0.5
                    winslow3 = 0.5
                elif scorediff == -1:
                    winquick2 = t1twopt
                    winquick3 = t1threept
                elif scorediff == -2:
                    winquick2 = 0.5 * t1twopt
                    winquick3 = t1threept
                elif scorediff == -3:
                    winquick3 = 0.5 * t1threept
            elif poss == 2:
                winquick2 = 0
                winquick3 = 0
                winslow2 = 0
                winslow3 = 0
                if scorediff > 0:
                    winslow2 = 1
                    winslow3 = 1
                elif scorediff == 0:
                    winslow2 = t1twopt + 0.5 * (1 - t1twopt)
                    winslow3 = t1threept + 0.5 * (1 - t1threept)
                elif scorediff == -1:
                    winslow2 = t1twopt
                    winslow3 = t1threept
                elif scorediff == -2:
                    winslow2 = 0.5 * t1twopt
                    winslow3 = t1threept
                elif scorediff == -3:
                    winslow3 = 0.5 * t1threept
                if scorediff + adjustment + 2 >= max_index:
                    winquick2 = t1twopt + (1 - t1twopt) * ((1 - oreb) *
                                                           (1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                                           + oreb * prob[poss - 1][scorediff + adjustment])
                    winquick3 = t1threept + (1 - t1threept) * ((1 - oreb) * (
                            1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                                               + oreb * prob[poss - 1][scorediff + adjustment])
                elif scorediff + adjustment + 3 >= max_index:
                    winquick2 = (t1twopt * (1 - prob[poss - 1][-1 * (scorediff + adjustment + 2)]) + (1 - t1twopt) *
                                 ((1 - oreb) * (1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                  + oreb * prob[poss - 1][scorediff + adjustment]))
                    winquick3 = (t1threept + (1 - t1threept) *
                                 ((1 - oreb) * (1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                  + oreb * prob[poss - 1][scorediff + adjustment]))
                else:
                    winquick2 = (t1twopt * (1 - prob[poss - 1][-1 * (scorediff + adjustment + 2)] + (1 - t1twopt)) *
                                 ((1 - oreb) * (1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                  + oreb * prob[poss - 1][scorediff + adjustment]))
                    winquick3 = (t1threept * (1 - prob[poss - 1][-1 * (scorediff + adjustment + 3)]) + (1 - t1threept) *
                                 ((1 - oreb) * (1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                  + oreb * prob[poss - 1][scorediff + adjustment]))
            else:
                if scorediff + adjustment + 2 >= max_index:
                    winquick2 = t1twopt + (1 - t1twopt) * ((1 - oreb) *
                                                           (1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                                           + oreb * prob[poss - 1][scorediff + adjustment])
                    winquick3 = t1threept + (1 - t1threept) * ((1 - oreb) * (
                            1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                                               + oreb * prob[poss - 1][scorediff + adjustment])
                    winslow2 = (t1twopt + (1 - t1twopt) *
                                ((1 - oreb) * (1 - prob[poss - 2][-1 * (scorediff + adjustment)])
                                 + oreb * prob[poss - 2][scorediff + adjustment]))
                    winslow3 = t1threept + (1 - t1threept) * ((1 - oreb) *
                                                              (1 - prob[poss - 2][-1 * scorediff + adjustment]) +
                                                              oreb * prob[poss - 2][scorediff + adjustment])
                elif scorediff + adjustment + 3 >= max_index:
                    winquick2 = (t1twopt * (1 - prob[poss - 1][-1 * (scorediff + adjustment + 2)]) + (1 - t1twopt) *
                                 ((1 - oreb) * (1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                  + oreb * prob[poss - 1][scorediff + adjustment]))
                    winquick3 = (t1threept + (1 - t1threept) *
                                 ((1 - oreb) * (1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                  + oreb * prob[poss - 1][scorediff + adjustment]))
                    winslow2 = (t1twopt * (1 - prob[poss - 2][-1 * (scorediff + adjustment + 2)]) + (1 - t1twopt) *
                                ((1 - oreb) * (1 - prob[poss - 2][-1 * (scorediff + adjustment)])
                                 + oreb * prob[poss - 2][scorediff + adjustment]))
                    winslow3 = (t1threept + (1 - t1threept) *
                                ((1 - oreb) * (1 - prob[poss - 2][-1 * (scorediff + adjustment)])
                                 + oreb * prob[poss - 2][scorediff + adjustment]))
                else:
                    winquick2 = (t1twopt * (1 - prob[poss - 1][-1 * (scorediff + adjustment + 2)]) + (1 - t1twopt) *
                                 ((1 - oreb) * (1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                  + oreb * prob[poss - 1][scorediff + adjustment]))
                    winquick3 = (t1threept * (1 - prob[poss - 1][-1 * (scorediff + adjustment + 3)]) + (1 - t1threept) *
                                 ((1 - oreb) * (1 - prob[poss - 1][-1 * (scorediff + adjustment)])
                                  + oreb * prob[poss - 1][scorediff + adjustment]))
                    winslow2 = (t1twopt * (1 - prob[poss - 2][-1 * (scorediff + adjustment + 2)]) + (1 - t1twopt) *
                                ((1 - oreb) * (1 - prob[poss - 2][-1 * (scorediff + adjustment)])
                                 + oreb * prob[poss - 2][scorediff + adjustment]))
                    winslow3 = (t1threept * (1 - prob[poss - 2][-1 * (scorediff + adjustment + 3)]) + (1 - t1threept) *
                                ((1 - oreb) * (1 - prob[poss - 2][-1 * (scorediff + adjustment)])
                                 + oreb * prob[poss - 2][scorediff + adjustment]))
            winprobmaxquick = max(winquick2, winquick3)
            winprobmaxslow = max(winslow2, winslow3)
            winprobmax = max(winprobmaxquick, winprobmaxslow)
            prob[poss][scorediff + adjustment] = winprobmax
            if winprobmaxquick > winprobmaxslow:
                if winquick2 > winquick3:
                    shot[poss][scorediff + adjustment] = "Quick 2"
                elif winquick3 > winquick2:
                    shot[poss][scorediff + adjustment] = "Quick 3"
                else:
                    shot[poss][scorediff + adjustment] = "Quick 2 or 3"
            elif winprobmaxslow > winprobmaxquick:
                if winslow2 > winslow3:
                    shot[poss][scorediff + adjustment] = "Slow 2"
                elif winslow3 > winslow2:
                    shot[poss][scorediff + adjustment] = "Slow 3"
                else:
                    shot[poss][scorediff + adjustment] = "Slow 2 or 3"
            else:  # winprobmaxquick = winprobmaxslow
                if winquick2 > winquick3:
                    if winslow2 > winslow3:
                        shot[poss][scorediff + adjustment] = "Quick or Slow 2"
                    elif winslow3 > winslow2:
                        shot[poss][scorediff + adjustment] = "Quick 2 or Slow 3"
                    else:
                        shot[poss][scorediff + adjustment] = "Quick 2 or Slow 2 or 3"
                elif winquick3 > winquick2:
                    if winslow2 > winslow3:
                        shot[poss][scorediff + adjustment] = "Quick 3 or Slow 2"
                    elif winslow3 > winslow2:
                        shot[poss][scorediff + adjustment] = "Quick or Slow 3"
                    else:
                        shot[poss][scorediff + adjustment] = "Quick 3 or Slow 2 or 3"
                else:
                    shot[poss][scorediff + adjustment] = "Any"
        # Win% and lead are always the % for the shooting team


def format_floats(x, skip=False):
    if skip:
        return x
    if isinstance(x, float):
        return f"{x:.4f}"
    elif isinstance(x, list):
        return [format_floats(item) for item in x]
    return x


def chooseshottype(winquick2, winquick3, winslow2, winslow3):
    winprobmaxquick = max(winquick2, winquick3)
    winprobmaxslow = max(winslow2, winslow3)
    winprobmax = max(winprobmaxquick, winprobmaxslow)
    if winquick2 == 1 and winquick3 == 1 and winslow2 == 1 and winslow3 == 1:
        return "Any shot"
    if winprobmaxquick > winprobmaxslow:
        if winquick2 > winquick3:
            return "Quick 2"
        elif winquick3 > winquick2:
            return "Quick 3"
        else:
            return "Quick 2 or 3"
    elif winprobmaxslow > winprobmaxquick:
        if winslow2 > winslow3:
            return "Slow 2"
        elif winslow3 > winslow2:
            return "Slow 3"
        else:
            return "Slow 2 or 3"
    else:  # winprobmaxquick = winprobmaxslow
        if winquick2 > winquick3:
            if winslow2 > winslow3:
                return "Quick or Slow 2"
            elif winslow3 > winslow2:
                return "Quick 2 or Slow 3"
            else:
                return "Quick 2 or Slow 2 or 3"
        elif winquick3 > winquick2:
            if winslow2 > winslow3:
                return "Quick 3 or Slow 2"
            elif winslow3 > winslow2:
                return "Quick 3 or Slow 3"
            else:
                return "Quick 3 or Slow 2 or 3"
        else:
            return "Any shot"


def fouldecision(ft, numposs, prob, foul, defensematrix, defense2):
    adjustment = 1 * (3 * math.ceil(numposs / 2) + 1)
    max_index = 1 * (6 * math.ceil(numposs / 2) + 2)
    quickfoul = 0
    slowfoul = 0
    for i in range(numposs + 1):
        for j in range(6 * math.ceil(numposs / 2) + 2):
            if i != 0 and j != 0:
                defensematrix[i][j] = 1.0 - prob[i][j]
    for poss in range(1, numposs + 1):
        for scorediff in range(-adjustment + 1, adjustment):
            if poss == 1:
                quickfoul = 0
                # if scorediff == 0:
                #     quickfoul = 0.5 * (1 - ft) ** 2
                # elif scorediff == -1:
                #     quickfoul = ((1 - ft) ** 2) + (0.5 * 2 * ft * (1 - ft))
                # elif scorediff == -2:
                #     quickfoul = ((1 - ft) ** 2) + (2 * ft * (1 - ft)) + (0.5 * (ft ** 2))
                # elif scorediff == -3:
                #     quickfoul = 1:
            elif poss == 2:
                if scorediff + adjustment + 1 >= max_index:
                    quickfoul = (1 - ft) ** 2 * prob[poss - 1][-1 * (scorediff + adjustment)]
                elif scorediff + adjustment + 2 >= max_index:
                    quickfoul = 2 * ft * (1 - ft) * prob[poss - 1][-1 * (scorediff + adjustment + 1)] + (1 - ft) ** 2 * \
                                prob[poss - 1][-1 * (scorediff + adjustment)]
                else:
                    quickfoul = ft ** 2 * prob[poss - 1][-1 * (scorediff + adjustment + 2)]
                    + 2 * ft * (1 - ft) * prob[poss - 1][-1 * (scorediff + adjustment + 1)] + (1 - ft) ** 2 * \
                    prob[poss - 1][-1 * (scorediff + adjustment)]
            else:
                if scorediff + adjustment + 1 >= max_index:
                    quickfoul = (1 - ft) ** 2 * prob[poss - 1][-1 * (scorediff + adjustment)]
                    slowfoul = (1 - ft) ** 2 * prob[poss - 2][-1 * (scorediff + adjustment)]
                elif scorediff + adjustment + 2 >= max_index:
                    quickfoul = 2 * ft * (1 - ft) * prob[poss - 1][-1 * (scorediff + adjustment + 1)] + (1 - ft) ** 2 * \
                                prob[poss - 1][-1 * (scorediff + adjustment)]
                    slowfoul = 2 * ft * (1 - ft) * prob[poss - 2][-1 * (scorediff + adjustment + 1)] + (1 - ft) ** 2 * \
                               prob[poss - 2][-1 * (scorediff + adjustment)]
                else:
                    quickfoul = ft ** 2 * prob[poss - 1][-1 * (scorediff + adjustment + 2)]
                    + 2 * ft * (1 - ft) * prob[poss - 1][-1 * (scorediff + adjustment + 1)] + (1 - ft) ** 2 * \
                    prob[poss - 1][-1 * (scorediff + adjustment)]
                    slowfoul = ft ** 2 * prob[poss - 2][-1 * (scorediff + adjustment + 2)]
                    + 2 * ft * (1 - ft) * prob[poss - 2][-1 * (scorediff + adjustment + 1)] + (1 - ft) ** 2 * \
                    prob[poss - 2][-1 * (scorediff + adjustment)]
            defense2[poss][scorediff + adjustment] = max(defensematrix[poss][scorediff + adjustment], quickfoul,
                                                         slowfoul)
            if defensematrix[poss][scorediff + adjustment] <= max(defensematrix[poss][scorediff + adjustment],
                                                                  quickfoul, slowfoul):
                if quickfoul == slowfoul:
                    if quickfoul == defensematrix[poss][scorediff + adjustment]:
                        foul[poss][scorediff + adjustment] = "Any"
                    elif quickfoul > defensematrix[poss][scorediff + adjustment]:
                        foul[poss][scorediff + adjustment] = "Quick or Slow Foul"
                elif quickfoul > slowfoul:
                    if quickfoul == defensematrix[poss][scorediff + adjustment]:
                        foul[poss][scorediff + adjustment] = "Quick foul or none"
                    else:
                        foul[poss][scorediff + adjustment] = "Quick foul"
                else:
                    if slowfoul == defensematrix[poss][scorediff + adjustment]:
                        foul[poss][scorediff + adjustment] = "Slow foul or none"
                    else:
                        foul[poss][scorediff + adjustment] = "Slow foul"
            else:
                foul[poss][scorediff + adjustment] = "No foul"


def pooledsequential(two, three, ft, numposs, oreb, shot, oprob):
    adjustment = (3 * math.ceil(numposs / 2)) + 1
    out_of_bounds = (6 * math.ceil(numposs / 2)) + 2
    for poss in range(1, numposs + 1):
        for scorediff in range(-adjustment + 1, adjustment):
            # Calculate values for the final possession
            if poss == 1:
                winquick2 = 0
                winquick3 = 0
                winslow2 = 0
                winslow3 = 0
                quickfoul = 0
                slowfoul = 0
                if scorediff > 0:
                    winquick2 = 1
                    winquick3 = 1
                    winslow2 = 1
                    winslow3 = 1
                elif scorediff == 0:
                    winquick2 = two + 0.5 * (1 - two)
                    winquick3 = three + 0.5 * (1 - three)
                    winslow2 = 0.5
                    winslow3 = 0.5
                elif scorediff == -1:
                    winquick2 = two
                    winquick3 = three
                elif scorediff == -2:
                    winquick2 = 0.5 * two
                    winquick3 = three
                elif scorediff == -3:
                    winquick3 = 0.5 * three
            elif poss == 2:
                slowfoul = 0
                # Calculate defensive win probability
                if scorediff + adjustment + 1 >= out_of_bounds:
                    quickfoul = (1 - ft) ** 2 * oprob[poss - 1][adjustment - scorediff]
                elif scorediff + adjustment + 2 >= out_of_bounds:
                    quickfoul = (2 * ft * (1 - ft) * oprob[poss - 1][adjustment - (scorediff + 1)] +
                                 (1 - ft) ** 2 * oprob[poss - 1][adjustment - scorediff])
                else:
                    quickfoul = (ft ** 2 * oprob[poss - 1][adjustment - (scorediff + 2)] +
                                 2 * ft * (1 - ft) * oprob[poss - 1][adjustment - (scorediff + 1)] +
                                 (1 - ft) ** 2 * oprob[poss - 1][adjustment - scorediff])
                # Calculate offensive win probability
                if scorediff > 3:
                    winquick2 = 1
                    winquick3 = 1
                    winslow2 = 1
                    winslow3 = 1
                elif scorediff > 0:
                    winslow2 = 1
                    winslow3 = 1
                elif scorediff == 0:
                    winslow2 = two + 0.5 * (1 - two)
                    winslow3 = three + 0.5 * (1 - three)
                elif scorediff == -1:
                    winslow2 = two
                    winslow3 = three
                elif scorediff == -2:
                    winslow2 = 0.5 * two
                    winslow3 = three
                elif scorediff == -3:
                    winslow3 = 0.5 * three
                    winslow2 = 0
                else:
                    winslow3 = 0
                    winslow2 = 0
                if scorediff + adjustment + 2 >= out_of_bounds:
                    winquick2 = two + (1 - two) * ((1 - oreb) *
                                                   (1 - oprob[poss - 1][adjustment - scorediff])
                                                   + oreb * oprob[poss - 1][scorediff + adjustment])
                    winquick3 = three + (1 - three) * ((1 - oreb) * (
                            1 - oprob[poss - 1][adjustment - scorediff])
                                                       + oreb * oprob[poss - 1][scorediff + adjustment])
                elif scorediff + adjustment + 3 >= out_of_bounds:
                    winquick2 = (two * (1 - oprob[poss - 1][adjustment - (scorediff + 2)]) + (1 - two) *
                                 ((1 - oreb) * (1 - oprob[poss - 1][adjustment - scorediff])
                                  + oreb * oprob[poss - 1][scorediff + adjustment]))
                    winquick3 = (three + (1 - three) *
                                 ((1 - oreb) * (1 - oprob[poss - 1][adjustment - scorediff])
                                  + oreb * oprob[poss - 1][scorediff + adjustment]))
                else:
                    winquick2 = (two * (1 - oprob[poss - 1][adjustment - (scorediff + 2)]) + (1 - two) *
                                 ((1 - oreb) * (1 - oprob[poss - 1][adjustment - scorediff])
                                  + oreb * oprob[poss - 1][scorediff + adjustment]))
                    winquick3 = (three * (1 - oprob[poss - 1][-1 * (scorediff + adjustment + 3)]) + (
                            1 - three) *
                                 ((1 - oreb) * (1 - oprob[poss - 1][adjustment - scorediff])
                                  + oreb * oprob[poss - 1][scorediff + adjustment]))
            else:
                # Calculate defensive win probability
                if scorediff + adjustment + 1 >= out_of_bounds:
                    quickfoul = (1 - ft) ** 2 * oprob[poss - 1][adjustment - scorediff]
                    slowfoul = (1 - ft) ** 2 * oprob[poss - 2][adjustment - scorediff]
                elif scorediff + adjustment + 2 >= out_of_bounds:
                    quickfoul = (2 * ft * (1 - ft) * oprob[poss - 1][adjustment - (scorediff + 1)] +
                                 (1 - ft) ** 2 * oprob[poss - 1][adjustment - scorediff])
                    slowfoul = (2 * ft * (1 - ft) * oprob[poss - 2][adjustment - (scorediff + 1)] +
                                (1 - ft) ** 2 * oprob[poss - 2][adjustment - scorediff])
                else:
                    quickfoul = (ft ** 2 * oprob[poss - 1][adjustment - (scorediff + 2)] +
                                 2 * ft * (1 - ft) * oprob[poss - 1][adjustment - (scorediff + 1)] +
                                 (1 - ft) ** 2) * oprob[poss - 1][adjustment - scorediff]
                    slowfoul = (ft ** 2 * oprob[poss - 2][adjustment - (scorediff + 2)] +
                                (2 * ft * (1 - ft) * oprob[poss - 2][adjustment - (scorediff + 1)] +
                                 (1 - ft) ** 2 * oprob[poss - 2][adjustment - scorediff]))
                # Calculate offensive win probability
                if scorediff + adjustment + 2 >= out_of_bounds:
                    winquick2 = two + (1 - two) * ((1 - oreb) *
                                                   (1 - oprob[poss - 1][adjustment - scorediff])
                                                   + oreb * oprob[poss - 1][adjustment + scorediff])
                    winquick3 = three + (1 - three) * ((1 - oreb) * (
                            1 - oprob[poss - 1][adjustment - scorediff])
                                                       + oreb * oprob[poss - 1][adjustment + scorediff])
                    winslow2 = (two + (1 - two) *
                                ((1 - oreb) * (1 - oprob[poss - 2][adjustment - scorediff])
                                 + oreb * oprob[poss - 2][adjustment + scorediff]))
                    winslow3 = three + (1 - three) * ((1 - oreb) *
                                                      (1 - oprob[poss - 2][adjustment - scorediff]) +
                                                      oreb * oprob[poss - 2][adjustment + scorediff])
                elif scorediff + adjustment + 3 >= out_of_bounds:
                    winquick2 = (two * (1 - oprob[poss - 1][adjustment - (scorediff + 2)]) + (1 - two) *
                                 ((1 - oreb) * (1 - oprob[poss - 1][adjustment - scorediff])
                                  + oreb * oprob[poss - 1][adjustment + scorediff]))
                    winquick3 = (three + (1 - three) *
                                 ((1 - oreb) * (1 - oprob[poss - 1][adjustment - scorediff])
                                  + oreb * oprob[poss - 1][adjustment + scorediff]))
                    winslow2 = (two * (1 - oprob[poss - 2][adjustment - (scorediff + 2)]) + (1 - two) *
                                ((1 - oreb) * (1 - oprob[poss - 2][adjustment - scorediff])
                                 + oreb * oprob[poss - 2][adjustment + scorediff]))
                    winslow3 = (three + (1 - three) *
                                ((1 - oreb) * (1 - oprob[poss - 2][adjustment - scorediff])
                                 + oreb * oprob[poss - 2][adjustment + scorediff]))
                else:
                    winquick2 = (two * (1 - oprob[poss - 1][adjustment - (scorediff + 2)]) + (1 - two) *
                                 ((1 - oreb) * (1 - oprob[poss - 1][adjustment - scorediff])
                                  + oreb * oprob[poss - 1][adjustment + scorediff]))
                    winquick3 = (three * (1 - oprob[poss - 1][adjustment - (scorediff + 3)]) + (
                            1 - three) *
                                 ((1 - oreb) * (1 - oprob[poss - 1][adjustment - scorediff])
                                  + oreb * oprob[poss - 1][adjustment + scorediff]))
                    winslow2 = (two * (1 - oprob[poss - 2][adjustment - (scorediff + 2)]) + (1 - two) *
                                ((1 - oreb) * (1 - oprob[poss - 2][adjustment - scorediff])
                                 + oreb * oprob[poss - 2][adjustment + scorediff]))
                    winslow3 = (three * (1 - oprob[poss - 2][adjustment - (scorediff + 3)]) + (1 - three) *
                                ((1 - oreb) * (1 - oprob[poss - 2][adjustment - scorediff])
                                 + oreb * oprob[poss - 2][adjustment + scorediff]))

            # print("Game state: ", numposs, ", ", scorediff, ". Winquick2: ", winquick2)
            # print("Game state: ", numposs, ", ", scorediff, ". Winquick3: ", winquick3)
            # print("Game state: ", numposs, ", ", scorediff, ". Winslow2: ", winslow2)
            # print("Game state: ", numposs, ", ", scorediff, ". Winslow3: ", winslow3)

            winoprobmaxquick = max(winquick2, winquick3)
            winoprobmaxslow = max(winslow2, winslow3)
            winoprobmax = max(winoprobmaxquick, winoprobmaxslow)

            # Use strictly greater than because teams would prefer not to foul if it doesnt affect their win %
            if quickfoul > slowfoul and quickfoul > (1 - winoprobmax):
                oprob[poss][scorediff + adjustment] = 1 - quickfoul
                shot[poss][scorediff + adjustment] = "Early Foul"
            elif slowfoul > quickfoul and slowfoul > (1 - winoprobmax):
                if (1 - slowfoul) >= winoprobmaxquick:  # Offense chooses to get fouled late instead of shooting early
                    oprob[poss][scorediff + adjustment] = 1 - slowfoul
                    shot[poss][scorediff + adjustment] = "Late Foul"
                else:  # Offense chooses early shot over late foul
                    if (1 - winoprobmaxquick) >= quickfoul:  # Defense chooses not to foul early
                        oprob[poss][scorediff + adjustment] = winoprobmax
                        shot[poss][scorediff + adjustment] = chooseshottype(winquick2, winquick3, winslow2, winslow3)
                    else:  # Defense chooses to foul early instead of letting early shot
                        oprob[poss][scorediff + adjustment] = 1 - quickfoul
                        shot[poss][scorediff + adjustment] = "Early Foul"
            elif quickfoul == slowfoul and quickfoul > (1 - winoprobmax):
                oprob[poss][scorediff + adjustment] = 1 - quickfoul
                shot[poss][scorediff + adjustment] = "Early or Late Foul"
            else:  # No Foul
                oprob[poss][scorediff + adjustment] = winoprobmax
                shot[poss][scorediff + adjustment] = chooseshottype(winquick2, winquick3, winslow2, winslow3)
        # Win% and lead are always the % for the shooting team


def creatematrix(matrix, numposs, numcols):
    for i in range(numposs + 1):
        row = []
        for j in range(numcols):
            if i == 0:
                if j == 0:
                    row.append("Poss, Score")
                elif j == 1:
                    row.append(int(-numcols/2 + 1))
                else:
                    row.append(row[j - 1] + 1)
            elif j == 0:
                row.append(i)
            else:
                row.append(0)
        matrix.append(row)


def shotwinprob(i, j, p2, p3, oreb, teamwin, cpuwin, tempo):
    adjustment = int(len(teamwin[0]) / 2)
    scorediff = j - adjustment
    if i == 1:
        winquick2 = 0
        winquick3 = 0
        winslow2 = 0
        winslow3 = 0
        quickfoul = 0
        slowfoul = 0
        if scorediff > 0:
            winquick2 = 1
            winquick3 = 1
            winslow2 = 1
            winslow3 = 1
        elif scorediff == 0:
            winquick2 = p2 + 0.5 * (1 - p2)
            winquick3 = p3 + 0.5 * (1 - p3)
            winslow2 = 0.5
            winslow3 = 0.5
        elif scorediff == -1:
            winquick2 = p2
            winquick3 = p3
        elif scorediff == -2:
            winquick2 = 0.5 * p2
            winquick3 = p3
        elif scorediff == -3:
            winquick3 = 0.5 * p3

    elif i == 2:
        slowfoul = 0
        # if j + 1 >= len(cpuwin[0]):
        #     quickfoul = (1 - ft) ** 2 * cpuwin[i - 1][adjustment - scorediff]
        # elif j + 2 >= len(cpuwin[0]):
        #     quickfoul = (2 * ft * (1 - ft) * cpuwin[i - 1][j - 2 * adjustment] +
        #                  (1 - ft) ** 2 * cpuwin[i - 1][adjustment - scorediff])
        # else:
        #     quickfoul = (ft ** 2 * cpuwin[i - 1][adjustment - (scorediff + 2)] +
        #                  2 * ft * (1 - ft) * cpuwin[i - 1][adjustment - (scorediff + 1)] +
        #                  (1 - ft) ** 2 * cpuwin[i - 1][adjustment - scorediff])
        # Calculate offensive win probability
        if scorediff > 3:
            winquick2 = 1
            winquick3 = 1
            winslow2 = 1
            winslow3 = 1
        elif scorediff > 0:
            winslow2 = 1
            winslow3 = 1
        elif scorediff == 0:
            winslow2 = p2 + 0.5 * (1 - p2)
            winslow3 = p3 + 0.5 * (1 - p3)
        elif scorediff == -1:
            winslow2 = p2
            winslow3 = p3
        elif scorediff == -2:
            winslow2 = 0.5 * p2
            winslow3 = p3
        elif scorediff == -3:
            winslow3 = 0.5 * p3
            winslow2 = 0
        else:
            winslow3 = 0
            winslow2 = 0
        if j + 2 >= len(cpuwin[0]):
            winquick2 = p2 + (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j])
            winquick3 = p3 + (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j])

        elif j + 3 >= len(cpuwin[0]):
            winquick2 = (p2 * (1 - teamwin[i - 1][j - 2 * scorediff - 2])
                         + (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j]))
            winquick3 = p3 + (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j])

        else:
            winquick2 = (p2 * (1 - teamwin[i - 1][j - 2 * scorediff - 2]) +
                         (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j]))
            winquick3 = (p3 * (1 - teamwin[i - 1][j - 2 * scorediff - 3]) +
                         (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j]))

    else:  # 3 or more possessions remaining
        if j + 2 >= len(cpuwin[0]):
            winquick2 = p2 + (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j])
            winquick3 = p3 + (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j])
            winslow2 = p2 + (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 2][j - 2 * scorediff]) + oreb * cpuwin[i - 2][j])
            winslow3 = p3 + (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 2][j - 2 * scorediff]) + oreb * cpuwin[i - 2][j])

        elif j + 3 >= len(cpuwin[0]):
            winquick2 = (p2 * (1 - teamwin[i - 1][j - 2 * scorediff - 2])
                         + (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j]))
            winquick3 = p3 + (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j])
            winslow2 = (p2 * (1 - teamwin[i - 2][j - 2 * scorediff - 2])
                        + (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 2][j - 2 * scorediff]) + oreb * cpuwin[i - 2][j]))
            winslow3 = p3 + (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 2][j - 2 * scorediff]) + oreb * cpuwin[i - 2][j])

        else:
            winquick2 = (p2 * (1 - teamwin[i - 1][j - 2 * scorediff - 2]) +
                         (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j]))
            winquick3 = (p3 * (1 - teamwin[i - 1][j - 2 * scorediff - 3]) +
                         (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j]))
            winslow2 = (p2 * (1 - teamwin[i - 2][j - 2 * scorediff - 2]) +
                        (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 2][j - 2 * scorediff]) + oreb * cpuwin[i - 2][j]))
            winslow3 = (p3 * (1 - teamwin[i - 2][j - 2 * scorediff - 3]) +
                        (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 2][j - 2 * scorediff]) + oreb * cpuwin[i - 2][j]))
    if tempo == "N" or tempo =="n":
        winslow2 = 0
        winslow3 = 0
    return [winquick2, winquick3, winslow2, winslow3]


def teamwincalc(teamwin, teamchoice, cpuwin, i, j, p2, p3, oreb, tempo):
    adjustment = int(len(teamchoice[0]) / 2)
    scorediff = j - adjustment
    shotprob = shotwinprob(i, j, p2, p3, oreb, teamwin, cpuwin, tempo)

    if i == 1:
        teamwin[i][j] = (teamchoice[i][j][0] * shotprob[0] + teamchoice[i][j][1] * shotprob[1] +
                         teamchoice[i][j][2] * shotprob[2] + teamchoice[i][j][3] * shotprob[3])
    elif i == 2:
        if j + 2 >= len(cpuwin[0]):
            shotprob[0] = p2 + (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j])
            shotprob[1] = p3 + (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j])

            teamwin[i][j] = (teamchoice[i][j][0] * (p2 + (1 - p2) * (1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][1] * (p3 + (1 - p3) * (1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][2] * shotprob[2] + teamchoice[i][j][3] * shotprob[3])
        elif j + 3 >= len(cpuwin[0]):
            shotprob[0] = (p2 * (1 - teamwin[i - 1][j - 2 * scorediff - 2])
                         + (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j]))
            shotprob[1] = p3 + (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j])
            teamwin[i][j] = (teamchoice[i][j][0] * (p2 * (1 - cpuwin[i - 1][j - 2 * scorediff - 2]) + (1 - p2) * (
                        1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][1] * (p3 + (1 - p3) * (1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][2] * shotprob[2] + teamchoice[i][j][3] * shotprob[3])
        else:
            shotprob[0] = (p2 * (1 - teamwin[i - 1][j - 2 * scorediff - 2]) +
                         (1 - p2) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j]))

            shotprob[1] = (p3 * (1 - teamwin[i - 1][j - 2 * scorediff - 3]) +
                         (1 - p3) * ((1 - oreb) * (1 - teamwin[i - 1][j - 2 * scorediff]) + oreb * cpuwin[i - 1][j]))

            teamwin[i][j] = (teamchoice[i][j][0] * (p2 * (1 - cpuwin[i - 1][j - 2 * scorediff - 2]) +
                                                    (1 - p2) * (1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][1] * (p3 * (1 - cpuwin[i - 1][j - 2 * scorediff - 3])
                                                      + (1 - p3) * (1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][2] * shotprob[2] + teamchoice[i][j][3] * shotprob[3])
    else:  # 3 or more possessions remaining
        if j + 2 >= len(cpuwin[0]):
            teamwin[i][j] = (teamchoice[i][j][0] * (p2 + (1 - p2) * (1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][1] * (p3 + (1 - p3) * (1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][2] * (p2 + (1 - p2) * (1 - cpuwin[i - 2][j - 2 * scorediff]))
                             + teamchoice[i][j][3] * (p3 + (1 - p3) * (1 - cpuwin[i - 2][j - 2 * scorediff])))
        elif j + 3 >= len(cpuwin[0]):
            teamwin[i][j] = (teamchoice[i][j][0] * (p2 * (1 - cpuwin[i - 1][j - 2 * scorediff - 2]) + (1 - p2) * (
                        1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][1] * (p3 + (1 - p3) * (1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][2] * (p2 * (1 - cpuwin[i - 2][j - 2 * scorediff - 2]) + (1 - p2) * (
                                1 - cpuwin[i - 2][j - 2 * scorediff]))
                             + teamchoice[i][j][3] * (p3 + (1 - p3) * (1 - cpuwin[i - 2][j - 2 * scorediff])))
        else:
            teamwin[i][j] = (teamchoice[i][j][0] * (
                        p2 * (1 - cpuwin[i - 1][j - 2 * scorediff - 2]) + (1 - p2) * (1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][1] * (p3 * (1 - cpuwin[i - 1][j - 2 * scorediff - 3]) + (1 - p3) * (
                                1 - cpuwin[i - 1][j - 2 * scorediff]))
                             + teamchoice[i][j][2] * (p2 * (1 - cpuwin[i - 2][j - 2 * scorediff - 2]) + (1 - p2) * (
                                1 - cpuwin[i - 2][j - 2 * scorediff]))
                             + teamchoice[i][j][3] * (p3 * (1 - cpuwin[i - 2][j - 2 * scorediff - 3]) + (1 - p3) * (
                                1 - cpuwin[i - 2][j - 2 * scorediff])))


def cpuwincalc(cpuwin, cpuchoice, teamwin, i, j, p2, p3, oreb, tempo):
    shotprob = shotwinprob(i, j, p2, p3, oreb, teamwin, cpuwin, tempo)
    winoprobmaxquick = max(shotprob[0], shotprob[1])
    winoprobmaxslow = max(shotprob[2], shotprob[3])
    winoprobmax = max(winoprobmaxquick, winoprobmaxslow)

    # Use strictly greater than because teams would prefer not to foul if it doesnt affect their win %
    # if quickfoul > slowfoul and quickfoul > (1 - winoprobmax):
    #     cpuwin[i][j] = 1 - quickfoul
    #     cpuchoice[i][j] = "Early Foul"
    # elif slowfoul > quickfoul and slowfoul > (1 - winoprobmax):
    #     if (1 - slowfoul) >= winoprobmaxquick:  # Offense chooses to get fouled late instead of shooting early
    #         cpuwin[i][j] = 1 - slowfoul
    #         cpuchoice[i][j] = "Late Foul"
    #     else:  # Offense chooses early shot over late foul
    #         if (1 - winoprobmaxquick) >= quickfoul:  # Defense chooses not to foul early
    #             cpuwin[i][j] = winoprobmax
    #             cpuchoice[i][j] = chooseshottype(winquick2, winquick3, winslow2,
    #                                              winslow3)
    #         else:  # Defense chooses to foul early instead of letting early shot
    #             cpuwin[i][j] = 1 - quickfoul
    #             cpuchoice[i][j] = "Early Foul"
    # elif quickfoul == slowfoul and quickfoul > (1 - winoprobmax):
    #     cpuwin[i][j] = 1 - quickfoul
    #     cpuchoice[i][j] = "Early or Late Foul"
    # else:  # No Foul
    cpuwin[i][j] = winoprobmax
    cpuchoice[i][j] = chooseshottype(shotprob[0], shotprob[1], shotprob[2], shotprob[3])


# THE strategy METHOD CALCULATES THE RESULT OF A COMPUTER (CPU) TEAM PLAYING AN NBA TEAM (TEAM)
def strategy(p2, p3, ft, oreb, tempo, teamchoice, cpuchoice, teamwin, cpuwin):
    # Let both matrices be the same size. Assume that any reference to a cell out-of-bounds will return probability 0/1.
    # Each cell of teamchoice will have a matrix representing the shot selection. The shots will be ordered
    # Quick 2, Quick 3, Slow 2, Slow 3. The reference [1][adjustment][0], for example,
    # will represent the team's propensity to shoot a quick two-pointer with the last shot of a tied game.
    # adjustment = int(len(teamchoice[0]) / 2)
    for i in range(1, len(teamchoice)):
        for j in range(1, len(teamchoice[0])):
            teamwincalc(teamwin, teamchoice, cpuwin, i, j, p2, p3, oreb, tempo)
            cpuwincalc(cpuwin, cpuchoice, teamwin, i, j, p2, p3, oreb, tempo)


def nbamirror(p2, p3, ft, oreb, tempo, choice1, choice2, win1, win2):
    for i in range(1, len(choice1)):
        for j in range(1, len(choice1[0])):
            teamwincalc(win1, choice1, win2, i, j, p2, p3, oreb, tempo)
            teamwincalc(win2, choice2, win1, i, j, p2, p3, oreb, tempo)


def gamesim(p2, p3, ft, oreb, tempo, t1choice, t2choice, team1, team2):

    i = int(len(t2choice)) - 1
    j = int(len(t2choice[0]) / 2)
    print("[i, j]: [%d,%d]" %(i, j))
    cpuscore = 0
    teamscore = 0
    # cpu and team sim functions return [points scored, possessions remaining, j index]

    while i >= 1:
        if team1.casefold() == "cpu":
            state = cpusim(p2, p3, ft, i, j, oreb, tempo, t1choice, t2choice)
            cpuscore += state[0]
            i = state[1]
            j = state[2]
            print("Computer: %d points, %d possessions left, %d index" %(state[0], state[1], state[2]))
        else:
            state = teamsim(p2, p3, ft, i, j, oreb, tempo, t1choice, t2choice)
            cpuscore += state[0]
            i = state[1]
            j = state[2]
            print("Team: %d points, %d possessions left, %d index" % (state[0], state[1], state[2]))
        # Team 2 is always NBA
        state = teamsim(p2, p3, ft, i, j, oreb, tempo, t1choice, t2choice)
        teamscore += state[0]
        i = state[1]
        j = state[2]
        print("Team: %d points, %d possessions left, %d index" %(state[0], state[1], state[2]))
    # while i >= 1:
    #
    #     state = cpusim(p2, p3, ft, i, j, oreb, tempo, t1choice, t2choice)
    #     cpuscore += state[0]
    #     i = state[1]
    #     j = state[2]
    #     print("Computer: %d points, %d possessions left, %d index" %(state[0], state[1], state[2]))

    print("Final score: %d : %d" % (cpuscore, teamscore))
    return [cpuscore, teamscore]


def cpusim(p2, p3, ft, poss, j, oreb, tempo, cpuchoice, teamchoice):
    rng = np.random.default_rng()
    midpoint = int(len(teamchoice[0]) / 2)
    if tempo == "N" or tempo == "n":
        if poss >= 1:
            if cpuchoice[poss][j] == 'Quick 3':
                print("Quick 3")
                points = 3 * rng.binomial(n = 1, p = p3)
            elif cpuchoice [poss][j] == 'Quick 2':
                print("Quick 2")
                points = 2 * rng.binomial(n = 1, p = p2)
            else:
                print("Not quick 2 or quick 3")
                shottype = rng.binomial(n = 1, p = 0.5)
                if shottype == 0:
                    points = 2 * rng.binomial(n = 1, p = p2)
                else:
                    points = 3 * rng.binomial(n = 1, p = p3)
            # Update and flip the score, pass to team's turn
            j += points
            j += 2 * (midpoint - j)
            poss -= 1
            return [points, poss, j]
        else: return [0,0,0]


def teamsim(p2, p3, ft, poss, j, oreb, tempo, oppchoice, teamchoice):
    rng = np.random.default_rng()
    midpoint = int(len(teamchoice[0]) / 2)
    if tempo == "N" or tempo == "n":
        if poss >= 1:
            shottype = rng.binomial(n = 1, p = teamchoice[poss][j][1])
            if shottype == 0:
                points = 2 * rng.binomial(n=1, p=p2)
            else:
                points = 3 * rng.binomial(n=1, p=p3)
            # Update and flip the score, pass to team's turn
            j += points
            j += 2 * (midpoint - j)
            poss -= 1
            return[points, poss, j]
        else: return [0,0,0]


if __name__ == "__main__":
    # Get user inputs
    print("Calculate optimal shot selection to maximize Win % for Team 1 at a given score with fixed shooting %s and "
          "known number of possessions:")
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
    # team1lead = int(input("Enter team 1's lead (positive for team1 winning, negative for team1 losing): "))
    # calcwinprob(team1twopt, team1threept, team2twopt, team2threept, team1poss, team2poss, shootingteam, oreb, TO,
    #            team1lead)
    team1 = input("Team 1: NBA or CPU? ")
    team2 = input("Team 2: NBA or CPU? ")
    matchup = ''.join([team1, team2])

    rows = numposs + 1
    cols = 3 * numposs + 2


    probmatrix = []
    shotmatrix = []
    teamshot = []
    teamprob = []

    # CREATE THE SHOT SELECTION TABLE FOR THE TEAM USING RESULT FROM R REGRESSION OUTPUT:

    with open('trimmed.csv', mode='r', newline='', encoding='utf-8') as f:
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

    creatematrix(probmatrix, numposs, numcols)
    creatematrix(shotmatrix, numposs, numcols)
    creatematrix(teamprob, numposs, numcols)

    # # For simple team strategies
    # for i in range(numposs + 1):
    #     row = []
    #     for j in range(6 * math.ceil(numposs / 2) + 2):
    #         if i == 0:
    #             if j == 0:
    #                 row.append("Poss, Score")
    #             elif j == 1:
    #                 row.append(3 * - math.ceil(numposs / 2))
    #             else:
    #                 row.append(row[j - 1] + 1)
    #         elif j == 0:
    #             row.append(i)
    #         else:
    #             row.append([1, 0, 0, 0])
    #     teamshot.append(row)

    # calcwinprobmatrix(team1twopt, team1threept, numposs, oreb, TO, probmatrix, shotmatrix)
    # timematrix(team1twopt, team1threept, team2twopt, team2threept,numposs, oreb, TO, probmatrix, shotmatrix)
    # pooledsequential(team1twopt, team1threept, team1ft, numposs, oreb, shotmatrix, probmatrix)

    # RUN
    if matchup.casefold() == "CPUNBA".casefold() or matchup.casefold() == "NBACPU".casefold():
        strategy(team1twopt, team1threept, team1ft, oreb, tempo, teamshot, shotmatrix, teamprob, probmatrix)
    elif matchup.casefold() == "nbanba".casefold():
        team2shot = teamshot.copy()
        team2prob = teamprob.copy()
        nbamirror(team1twopt, team1threept, team1ft, oreb, tempo, teamshot, team2shot, teamprob, team2prob)

    # PRINT OUTPUT
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
    #         teamshot_formatted[i][j] = format_floats(teamshot_formatted[i][j])
    #
    # print(tabulate(teamshot_formatted, floatfmt=".4f", headers="firstrow", numalign="center", stralign="center",
    #                tablefmt="fancy_grid"))
    # print('\nWinning Probability Table (Team): ')
    # print(tabulate(teamprob, floatfmt=".4f", headers="firstrow", numalign="center", stralign="center",
    #                tablefmt="fancy_grid"))

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

    # Graphs

    # adjustment = (3 * math.ceil(numposs / 2)) + 1
    # # Plot with fixed possessions
    # score = probmatrix_df.iloc[0, 1:]
    #
    # # Extract y-values: all rows excluding row 0 and column 0
    # winprob = probmatrix_df.iloc[numposs - 10:, 1:]
    #
    # # Extract labels from column 0 (excluding row 0)
    # possessions = probmatrix_df.iloc[numposs - 10:, 0].values
    #
    # plt.figure(figsize=(10, 6))
    #
    # # Loop through each row and plot
    # for i, idx in enumerate(winprob.index):
    #     plt.plot(
    #         score,  # X-axis from row 0
    #         winprob.loc[idx],  # Y-values for this row
    #         label=str(possessions[i])
    #     )
    #
    # plt.xlabel("Score")
    # plt.ylabel("Win%")
    # plt.title("Win% against Score with Fixed Number of Possessions")
    #
    # # Y-axis formatting
    # plt.ylim(0, 1)
    # ax = plt.gca()
    # ax.yaxis.set_major_locator(MultipleLocator(0.25))
    # ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    #
    # # X-axis formatting: only integer major ticks if applicable
    # ax.xaxis.set_major_locator(MultipleLocator(1))
    #
    # # Gridlines
    # ax.grid(which='major', axis='both', linestyle='-', linewidth=0.8)
    # ax.grid(which='minor', axis='y', linestyle='--', linewidth=0.5, alpha=0.6)
    #
    # # ax.invert_xaxis()
    #
    # # Legend on right with title
    # plt.legend(
    #     title="Poss",
    #     loc="center left",
    #     bbox_to_anchor=(1, 0.5)
    # )
    #
    # plt.tight_layout()
    # plt.show()
    #
    # legend_labels = probmatrix_df.iloc[0, adjustment - 5:adjustment + 5].values
    # x_values = probmatrix_df.iloc[1:, 0].values
    # filtered = probmatrix_df.iloc[1:, adjustment - 5:adjustment + 5]
    #
    # plt.figure(figsize=(10, 6))
    # # Plot each column using column 0 as x-axis
    # for i, col in enumerate(filtered.columns):
    #     plt.plot(
    #         x_values,  # x-axis
    #         filtered[col].values,  # y-axis (one column at a time)
    #         label=str(legend_labels[i])
    #     )
    # plt.xlabel("Time")
    # plt.ylabel("Win %")
    # plt.title("Win % Against Time with Fixed Score")
    #
    # # Set y-axis limits
    # plt.ylim(0, 1)
    #
    # # Configure major and minor ticks
    # ax = plt.gca()
    # ax.yaxis.set_major_locator(MultipleLocator(0.25))
    # ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    # ax.xaxis.set_major_locator(MultipleLocator(1))
    # # Gridlines for major and minor ticks
    # ax.grid(which='major', linestyle='-', linewidth=0.8)
    # ax.grid(which='minor', axis='y', linestyle='--', linewidth=0.5, alpha=0.6)
    #
    # ax.invert_xaxis()
    # # Legend on right with title
    # plt.legend(
    #     title="Score",
    #     loc="center left",
    #     bbox_to_anchor=(1, 0.5)
    # )
    #
    # plt.tight_layout()
    # plt.show()
    print("Shot selection strategy is displayed in shottype.csv")
    print("Win probabilities are displayed in winprob.csv")
