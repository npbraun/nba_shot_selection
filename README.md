This is a project using game theory to derive the optimal shot selection strategy for an NBA team as a function of the score and number
of possessions remaining. 
The program also scrapes ESPN for play-by-play shot data (currently defaulted to 2024-25 NBA regular season).
Finally, the program compares the derived optimal strategy to the observed NBA strategy with a variety of plots.

The file `scrape.py` scrapes the observed data from ESPN. Run this file first, as it is referenced in all of the other files.

The file `winprobcalc.py` derives the optimal strategy for a team playing against an NBA team. It also computes the win
probability for the team. The results are stored in `shottype.csv` and `winprob.csv`. The file also defines several key functions.

The file `comparison.py` calculates and the plots the difference in win probability for a team using optimal strategy and one using NBA strategy.

The file `similarity.py` calculates and plots how similar the two strategies are. 

The file `simulate.py` simulates games multiple times. The first matchup simulated is one where team A uses the optimal strategy against team B,
which uses NBA strategy.  The simulation is repeated for the case where team A and team B both use the NBA strategy. The program compares
the final score differential for team A under both strategies and shows that the optimal strategy is superior in win probability, and 
reduces the variance of the final score differential.

My work draws upon the `espn_scraper` repository by `andr3w321` to obtain NBA data. 
The repository can be found at https://github.com/andr3w321/espn_scraper
