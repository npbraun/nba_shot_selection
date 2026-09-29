import json
import math
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FormatStrFormatter
from winprobcalc import pooledsequential
from dateutil import parser
import requests
import espn_scraper as espn

ESPN_HEADERS = {
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8,"
        "application/signed-exchange;v=b3;q=0.7"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Sec-CH-UA": '"Chromium";v="154", "Google Chrome";v="154", "Not A(Brand";v="99"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    ),
}


# Method adapted from @andr3w321 via https://github.com/andr3w321/espn_scraper
# Made adjustments to request headers, site url, fixed_get_season_start_end_datetimes_helper, and get_nba_playbyplay
# to fix errors with the original code

def my_retry_request(url, headers=None):
    print("REQUESTING:", url)

    response = requests.get(
        url,
        headers=ESPN_HEADERS
    )

    return response

espn.retry_request = my_retry_request


espn.API_v2_BASE_URL = "https://site.web.api.espn.com/apis/site/v2/sports"

def fixed_get_season_start_end_datetimes_helper(url):
    scoreboard = espn.get_url(url)

    return (
        parser.parse(scoreboard['leagues'][0]['calendarStartDate']),
        parser.parse(scoreboard['leagues'][0]['calendarEndDate'])
    )

def get_nba_playbyplay(game_id):
    url = (
        f"{espn.API_v2_BASE_URL}/basketball/nba/"
        f"summary?event={game_id}"
    )

    return espn.get_url(url, cached_path="cached_json")

espn.get_season_start_end_datetimes_helper = fixed_get_season_start_end_datetimes_helper

test_url = espn.get_date_scoreboard_url("nba", "20241101")

data = espn.get_url(test_url)

print(data.keys())

''' Pretty print json helper '''

def ppjson(data):
    print(json.dumps(data, indent=2, sort_keys=True))


def creatematrix(matrix, numposs, score, value = 0):
    for i in range(numposs + 1):
        row = []
        for j in range((score + 1) * 2):
            if i == 0:
                if j == 0:
                    row.append("Poss, Score")
                elif j == 1:
                    row.append(-score)
                else:
                    row.append(row[j - 1] + 1)
            elif j == 0:
                row.append(i)
            else:
                if value == [0, 0, 0, 0]:
                    row.append([0, 0, 0, 0])
                else:
                    row.append(value)
        matrix.append(row)


def trim(matrix, scorelimit):
    delete_each_side = (len(matrix[0]) - 2 * (scorelimit + 1)) // 2

    for row in matrix:
        del row[1:1 + delete_each_side]
        del row[-delete_each_side:]


def compare(observed, optimal, comparison, game_max_lead, p2, p3, ft):
    # offset by 3 because the optimal matrix must have valid references if the team were to extend their lead
    offset = 3
    for i in range(1, len(observed)):
        for j in range(1, len(observed[0])):
            dist_to_zero = j - (game_max_lead + 1) # correct
            if observed[i][j] == 2:
                newprob = p2 * (1 - optimal[i - 1][j + offset - 2 * dist_to_zero - 2]) + (1 - p2) * (1 - optimal[i - 1][j + offset - 2 * dist_to_zero])
                if optimal[i][j + offset] > 0:
                    grade = newprob - optimal[i][j + offset]
                    comparison[i][j] = grade
            elif observed[i][j] == 3:
                newprob = p3 * (1 - optimal[i - 1][j + offset - 2 * dist_to_zero - 3]) + (1 - p3) * (1 - optimal[i - 1][j + offset - 2 * dist_to_zero])
                if optimal[i][j + offset] > 0:
                    grade = newprob - optimal[i][j + offset] # correct
                    comparison[i][j] = grade
            elif observed[i][j] == 'Foul':
                continue
            # else:
            #     comparison[i][j] = ''


def updatecount(observed, optimal, tracker):
    for i in range(1, len(observed)):
        for j in range(1, len(observed[0])):
            if observed[i][j] == 2 or observed[i][j] == 3:
                if optimal[i][j + 3] == 'Any shot':
                    tracker[i][j] += 1
                elif str(observed[i][j]) in optimal[i][j + 3]:
                    tracker[i][j] += 1
            # else:
            #     tracker[i][j] = 'N/A'


def shotdist(observed, cum):
    adjustment = int((len(cum[0]) - len(observed[0])) / 2)
    for poss in range(1, len(observed)):
        for j in range(1, len(observed[0])):
            if observed[poss][j] == 'Quick 2':
                cum[poss][j + adjustment][0] += 1
            elif observed[poss][j] == 'Quick 3':
                cum[poss][j + adjustment][1] += 1
            elif observed[poss][j] == 'Slow 2':
                cum[poss][j + adjustment][2] += 1
            elif observed[poss][j] == 'Slow 3':
                cum[poss][j + adjustment][3] += 1
            elif observed[poss][j] == 2:
                cum[poss][j + adjustment][0] += 1
            elif observed[poss][j] == 3:
                cum[poss][j + adjustment][1] += 1


def normalize(cum):
    for i in range(1, len(cum)):
        for j in range(1, len(cum[0])):
            total = 0
            for k in range(len(cum[0][0])):
                total += cum[i][j][k]
            for k in range(len(cum[0][0])):
                if total != 0:
                    cum[i][j][k] /= total


# leagues = espn.get_leagues()
# print(leagues)
# for league in leagues:
#     teams = espn.get_teams(league)
#     print(league, len(teams))

# # print nfl 2016 postseason scores
# scoreboard_urls = espn.get_all_scoreboard_urls("nfl", 2016)
# for scoreboard_url in scoreboard_urls:
#     data = espn.get_url(scoreboard_url, cached_path="cached_json")
#     for event in data['events']:
#         if event['season']['type'] == 3:
#             print(event['season']['type'],
#                   event['season']['year'],
#                   event['competitions'][0]['competitors'][0]['team']['abbreviation'],
#                   event['competitions'][0]['competitors'][0]['score'],
#                   event['competitions'][0]['competitors'][1]['team']['abbreviation'],
#                   event['competitions'][0]['competitors'][1]['score'])

# NBA box score example
# url = espn.get_game_url("boxscore", "nba", 400900498)
# json_data = espn.get_url(url)
# # ppjson(json_data) # print full long json
#
# print(json_data['page']['content']['gamepackage']['bxscr'][0]['tm']['dspNm'])
# ppjson(json_data['page']['content']['gamepackage']['bxscr'][0]['stats'][0])

# Recent NBA game - OKC @ DET, DET W 124-116, print play-by-play
# url = espn.get_game_url("playbyplay", "nba", 401810697)

cumulativeshotmatrix = []
creatematrix(cumulativeshotmatrix, 420, 80, [0, 0, 0, 0])

regressiondata = []
gamecount = 1
scoreboard_urls = espn.get_all_scoreboard_urls("nba", 2025)
global_max_lead = 0
for scoreboard_url in scoreboard_urls:
    data = espn.get_url(scoreboard_url, cached_path="cached_json")
    for event in data['events']:
        if event['season']['type'] == 2:
            url = espn.get_game_url("playbyplay", "nba", event['id'])
            json_data = espn.get_url(url, cached_path="cached_json")
            # loop over ['events'] and get id, get playbyplay with espn.get_game_url
            # ppjson(json_data['page']['content']['gamepackage']['pbp'])
            shotcount = 0
            game_max_lead = 0
            for i in range(len(json_data['page']['content']['gamepackage']['pbp']['plays'])):
                if json_data['page']['content']['gamepackage']['pbp']['plays'][i]['title'] in (
                        'Missed FG', 'Missed 3PT', 'Missed FT', '+2 Points', '+3 Points', '+1 Point', 'Blocked Shot'):
                    # printing to understand how pbp system works, not functionally necessary
                    # print("Possession: ", end="")
                    # ppjson(json_data['page']['content']['gamepackage']['pbp']['plays'][i]['homeAway'])
                    # print("Shot selection: ", end="")
                    # ppjson(json_data['page']['content']['gamepackage']['pbp']['plays'][i]['pointsAttempted'])
                    # ppjson(json_data['page']['content']['gamepackage']['pbp']['plays'][i]['title'])
                    # print("Quarter: ", end="")
                    # ppjson(json_data['page']['content']['gamepackage']['pbp']['plays'][i]['period']['number'])
                    # print("Seconds remaining: ", end="")
                    # ppjson(json_data['page']['content']['gamepackage']['pbp']['plays'][i]['clock']['value'])
                    # print("Away score: ", end="")
                    # ppjson(json_data['page']['content']['gamepackage']['pbp']['plays'][i]['awScr'])
                    # print("Home score: ", end="")
                    # ppjson(json_data['page']['content']['gamepackage']['pbp']['plays'][i]['hmScr'])
                    # print()

                    # functionally necessary
                    game_max_lead = max(abs(json_data['page']['content']['gamepackage']['pbp']['plays'][i]['awScr'] -
                                      json_data['page']['content']['gamepackage']['pbp']['plays'][i]['hmScr']), game_max_lead)
                    global_max_lead = max(global_max_lead, game_max_lead)
                    if json_data['page']['content']['gamepackage']['pbp']['plays'][i]['title'] not in ('Missed FT', '+1 Point') or (
                            'free throw 1 of 2' in json_data['page']['content']['gamepackage']['pbp']['plays'][i][
                        'text'] or 'free throw 1 of 3' in json_data['page']['content']['gamepackage']['pbp']['plays'][i]['text']):
                        shotcount += 1

            print("Number of shots taken (excluding and-ones, multiple FT): ", shotcount)
            print("Maximum lead: ", game_max_lead)




            # TODO: How to compare observed to theoretical optimum?
            # Run model with observed shots of one team vs the theoretically optimal shots from the other team
            # TODO: Then aggregate all games to get stochastic %
            # TODO: Early vs late shots

            # Commented out to speed up program for regression-formatted data
            homematrix = []
            awaymatrix = []
            creatematrix(homematrix, shotcount, game_max_lead)
            creatematrix(awaymatrix, shotcount, game_max_lead)
            numposs = shotcount
            scorediff = 0

            print("Game ", gamecount, ", updating regression file")
            for i in range(len(json_data['page']['content']['gamepackage']['pbp']['plays'])):
                if json_data['page']['content']['gamepackage']['pbp']['plays'][i]['title'] in (
                        'Missed FG', 'Missed 3PT', 'Missed FT', '+2 Points', '+3 Points', '+1 Point', 'Blocked Shot'):
                    if json_data['page']['content']['gamepackage']['pbp']['plays'][i]['title'] not in ('Missed FT', '+1 Point'):
                        shottype = json_data['page']['content']['gamepackage']['pbp']['plays'][i]['pointsAttempted']
                        if json_data['page']['content']['gamepackage']['pbp']['plays'][i]['homeAway'] == 'home':
                            homematrix[numposs][game_max_lead + 1 + scorediff] = \
                                json_data['page']['content']['gamepackage']['pbp']['plays'][i]['pointsAttempted']
                            regressiondata.append([shottype, numposs, scorediff])
                        else:
                            awaymatrix[numposs][game_max_lead + 1 - scorediff] = \
                                json_data['page']['content']['gamepackage']['pbp']['plays'][i]['pointsAttempted']
                            regressiondata.append([shottype, numposs, -scorediff])
                        numposs -= 1
                    elif 'free throw 1 of 2' in json_data['page']['content']['gamepackage']['pbp']['plays'][i][
                            'text'] or 'free throw 1 of 3' in json_data['page']['content']['gamepackage']['pbp']['plays'][i]['text']:
                        # Commented out for regression which focuses only on 2/3
                        # if json_data['page']['content']['gamepackage']['pbp']['plays'][i]['homeAway'] == 'home':
                        #     # homematrix[numposs][game_max_lead + 1 + scorediff] = 'Foul'
                        # else:
                        #     # awaymatrix[numposs][game_max_lead + 1 - scorediff] = 'Foul'
                        numposs -= 1
                    scorediff = (json_data['page']['content']['gamepackage']['pbp']['plays'][i]['hmScr'] -
                                 json_data['page']['content']['gamepackage']['pbp']['plays'][i]['awScr'])
                    # scorediff = home - away -> away team matrix flips scorediff
            gamecount += 1
            shotdist(homematrix, cumulativeshotmatrix)
            shotdist(awaymatrix, cumulativeshotmatrix)

            homeshotfile = "./homeshot.csv"
            homematrix_df = pd.DataFrame(homematrix)
            homematrix_df.to_csv(homeshotfile, header=False, index=False)

            awayshotfile = "./awayshot.csv"
            awaymatrix_df = pd.DataFrame(awaymatrix)
            awaymatrix_df.to_csv(awayshotfile, header=False, index=False)

            regressionfile = "./regression.csv"
            regression_df = pd.DataFrame(regressiondata)
            regression_df.to_csv(regressionfile, header=False, index=False)

            shottotalfile = "./shottotal.csv"
            cumulativeshotmatrix_df = pd.DataFrame(cumulativeshotmatrix)
            cumulativeshotmatrix_df.to_csv(shottotalfile, header=False, index=False)

            shottype = []
            winprob = []
            creatematrix(shottype, shotcount, 3 * math.ceil(shotcount / 2))
            creatematrix(winprob, shotcount, 3 * math.ceil(shotcount / 2))
            pooledsequential(0.55, 0.36, 0.78, shotcount, 0, shottype, winprob)
            trim(winprob, game_max_lead + 3)
            trimmedshotfile = "./trimmed.csv"
            winprob_trimmed = pd.DataFrame(winprob)
            winprob_trimmed.to_csv(trimmedshotfile, header=False, index=False)

            # TODO: Commented out for regression
            # homecomparison = []
            # creatematrix(homecomparison, shotcount, game_max_lead)
            # compare(homematrix, winprob, homecomparison, game_max_lead, 0.55, 0.36, 0.78)
            # homecompfile = "./homecomparison.csv"
            # homecomparison_df = pd.DataFrame(homecomparison)
            # homecomparison_df.to_csv(homecompfile, header=False, index=False)
            #
            # awaycomparison = []
            # creatematrix(awaycomparison, shotcount, game_max_lead)
            # compare(awaymatrix, winprob, awaycomparison, game_max_lead, 0.55, 0.36, 0.78)
            # awaycompfile = "./awaycomparison.csv"
            # awaycomparison_df = pd.DataFrame(awaycomparison)
            # awaycomparison_df.to_csv(awaycompfile, header=False, index=False)
            #
            # trim(shottype, game_max_lead + 3)
            # count = []
            # creatematrix(count, shotcount, game_max_lead)
            # updatecount(homematrix, shottype, count)
            # countfile = "./count.csv"
            # count_df = pd.DataFrame(count)
            # count_df.to_csv(countfile, header=False, index=False)
            # optshotfile = "./optshottype.csv"
            # shottype_df = pd.DataFrame(shottype)
            # shottype_df.to_csv(optshotfile, header=False, index=False)

print(f"Max lead across all games: {global_max_lead}")

trim(cumulativeshotmatrix, global_max_lead)

for i in range(1, len(cumulativeshotmatrix)):
    for j in range(1, len(cumulativeshotmatrix[0])):
        if cumulativeshotmatrix[i][j] == [0, 0, 0, 0]:
            cumulativeshotmatrix[i][j] = -999
        else:
            twos = cumulativeshotmatrix[i][j][0]
            threes = cumulativeshotmatrix[i][j][1]
            cumulativeshotmatrix[i][j] = threes / (twos + threes)

while cumulativeshotmatrix and sum(x != -999 for x in cumulativeshotmatrix[-1]) < 2:
    cumulativeshotmatrix.pop()

nbashot = pd.DataFrame(cumulativeshotmatrix)
nbashot.to_csv(trimmedshotfile, header=False, index=False)




