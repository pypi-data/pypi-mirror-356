'''Examples of usage.'''

from dans.endpoints.playerlogs import PlayerLogs
from dans.endpoints.playerstats import PlayerStats
from dans.endpoints.teams import Teams
from dans.library.arguments import DataFormat, SeasonType

# logs_df = PlayerLogs('LeBron James', [2012, 2014], season_type=SeasonType.playoffs).bball_ref()
# print(logs_df)

# stats_list = PlayerStats('Kawhi Leonard', [2019, 2021], [100, 110], \
#                             season_type=SeasonType.playoffs).nba_stats()
# print(stats_list)

# stats_list = PlayerStats('Kevin Durant', [2017, 2019], [105, 110], data_format=\
#                          DataFormat.opp_pace_adj, season_type=SeasonType.playoffs).nba_stats()
# print(stats_list)

# teams_df = Teams([2010, 2020], [105, 110]).bball_ref()
# print(teams_df)
# s2 = PlayerStats('Nikola Jokić', [2023, 2023], [80, 130], data_format=DataFormat.opp_pace_adj, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats("Larry Bird", [1982, 1987], [80, 130], data_format=DataFormat.opp_pace_adj, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Nikola Jokić', [2021, 2025], [80, 130], data_format=DataFormat.opp_pace_adj, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [1999, 1999], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2000, 2000], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2001, 2001], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2002, 2002], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2003, 2003], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2004, 2004], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2006, 2006], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2007, 2007], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2008, 2008], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2009, 2009], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2010, 2010], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)

# s2 = PlayerStats('Stephen Curry', [2022, 2022], [80, 107], data_format=DataFormat.opp_pace_adj, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Reggie Miller', [1992, 2001], [80, 130], data_format=DataFormat.opp_pace_adj, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
names = [
    # ["Kobe Bryant", [2001, 2010]],
    # ["LeBron James", [2009, 2018]],
    # ["Shaquille O'Neal", [1996, 2005]],
    # ["Michael Jordan", [1989, 1998]],
    # ["Magic Johnson", [1982, 1991]],
    # ["Larry Bird", [1980, 1989]],
    # ["Stephen Curry", [2015, 2024]],
    # ["Kevin Durant", [2012, 2021]],
    # ["Giannis Antetokounmpo", [2019, 2025]],
    # ["James Harden", [2013, 2022]],
    # ["Steve Nash", [2002, 2011]],
    # ["Kevin Garnett", [1999, 2008]],
    # ["Tim Duncan", [1998, 2007]],
    # ["Dirk Nowitzki", [2002, 2011]],
    # ["Hakeem Olajuwon", [1986, 1995]],
    # ["Shai Gilgeous-Alexander", [2025, 2025]]
    ["Nikola Jokić", [2021, 2025]],
]

import pandas as pd

# for name in names:
#     logs = PlayerLogs(name[0], name[1], season_type=SeasonType.playoffs).bball_ref()
#     s2 = PlayerStats(logs, [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
#     print(name[0])
#     print(logs)
#     print(s2)

# t1 = PlayerLogs("Kobe Bryant", [2001, 2003], season_type=SeasonType.playoffs).nba_stats()
# s1 = PlayerStats(t1, [80, 130], data_format=DataFormat.opp_pace_adj).nba_stats()
# print(s1)
# s1 = PlayerStats(t1, [80, 130], data_format=DataFormat.opp_pace_adj).nba_stats(adj_drtg=True)
# print(s1)
t1 = PlayerLogs("LeBron James", [2014, 2014], season_type=SeasonType.playoffs).nba_stats()
s1 = PlayerStats(t1, [80, 99.0], data_format=DataFormat.opp_pace_adj).nba_stats()
print(s1)
s1 = PlayerStats(t1, [80, 99.6], data_format=DataFormat.opp_pace_adj).nba_stats(adj_drtg=True)
print(s1)
# t2 = PlayerLogs("Kobe Bryant", [2002, 2002], season_type=SeasonType.playoffs).bball_ref()
# t2 = t2[t2["MATCHUP"] == "POR"]
# t3 = PlayerLogs("Kobe Bryant", [2003, 2003], season_type=SeasonType.playoffs).bball_ref()
# t3 = t3[t3["MATCHUP"] == "MIN"]
# t6 = PlayerLogs("Kobe Bryant", [2006, 2006], season_type=SeasonType.playoffs).bball_ref()
# t7 = PlayerLogs("Kobe Bryant", [2007, 2007], season_type=SeasonType.playoffs).bball_ref()
# t8 = PlayerLogs("Kobe Bryant", [2008, 2008], season_type=SeasonType.playoffs).bball_ref()
# t8 = t8[(t8["MATCHUP"] == "DEN") | (t8["MATCHUP"] == "UTA")]
# t9 = PlayerLogs("Kobe Bryant", [2009, 2009], season_type=SeasonType.playoffs).bball_ref()
# t9 = t9[(t9["MATCHUP"] == "UTA") | (t9["MATCHUP"] == "DEN")]
# t10 = PlayerLogs("Kobe Bryant", [2010, 2010], season_type=SeasonType.playoffs).bball_ref()
# t10 = t10[(t10["MATCHUP"] == "PHO") | (t10["MATCHUP"] == "UTA") | (t10["MATCHUP"] == "OKC")]

# df = pd.concat([t1, t2, t3, t6, t7, t8, t9, t10])
# print(df)
# s = PlayerStats(df, [80, 130], data_format=DataFormat.default).bball_ref()
# print(s)

# s2 = PlayerStats('Kobe Bryant', [2001, 2010], [100, 102], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2001, 2010], [102, 104], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2001, 2010], [104, 106], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2001, 2010], [106, 108], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2000, 2010], [108, 110], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2001, 2010], [110, 120], data_format=DataFormat.per_game, season_type=SeasonType.playoffs).bball_ref()
# print(s2)
# s2 = PlayerStats('Kobe Bryant', [2009, 2009], [80, 130], data_format=DataFormat.per_game, season_type=SeasonType.regular_season).bball_ref()
# print(s2)
player = "Kevin Durant"

players = [
    # ["Michael Jordan", 1988, 1998],
    # ["Kobe Bryant", 2001, 2012],
    # ["LeBron James", 2009, 2018],
    # ["Tim Duncan", 1999, 2007],
    # ["Shaquille O'Neal", 1994, 2005],
    # ["Hakeem Olajuwon", 1985, 1997],
    ["Kevin Garnett", 2000, 2008]
    # ["Kevin Durant", 2011, 2021],
    # ["Stephen Curry", 2015, 2022],
    # ["Magic Johnson", 1980, 1990],
    # ["Larry Bird", 1980, 1988],
    # ["Giannis Antetokuonmpo", 2019, 2024],
    # ["Luka Dončić", 2021, 2024],
    # ["Nikola Jokić", 2020, 2024]
]

player_data = []

# for player in players:

#     for year in range(player[1], player[2] + 1):

#         s1 = PlayerStats(player[0], [year, year], [80, 130], season_type=SeasonType.playoffs, data_format=DataFormat.opp_pace_adj).bball_ref()
#         if s1.empty:
#             continue
        
#         pts = s1["PTS"].loc[0]
#         rts = s1["rTS%"].loc[0]
#         player_data.append([player[0], year, pts, rts])

# print(player_data)
    # if s1.empty or s2.empty:
    #     continue
    
    # point_change = s2["PTS"].loc[0] - s1["PTS"].loc[0]
    # eff_change = s2["rTS%"].loc[0] - s1["rTS%"].loc[0]
    # drtg_change = s2["DRTG"].loc[0] - s1["DRTG"].loc[0]

    # print(f"Year: {year}")
    # print(f"Point Change: {point_change}")
    # print(f"rTS% Change: {eff_change}")
    # print(f"DRTG Change: {drtg_change}\n")

