'''Testing player methods (NBA-Stats only).'''
import unittest
import pandas as pd

from dans.endpoints.playerstats import PlayerStats
from dans.endpoints.playerlogs import PlayerLogs
from dans.library.arguments import DataFormat, SeasonType

class TestNBAStats(unittest.TestCase):
    '''Tests for each dans player endpoint: NBA-Stats only'''
    def test_player_game_logs(self):
        logs = PlayerLogs(
            "Stephen Curry",
            year_range=[2015, 2017],
            season_type=SeasonType.playoffs
        ).nba_stats()

        expected_columns = ['SEASON', 'SEASON_TYPE', 'DATE', 'NAME', 'TEAM', 'HOME', 'MATCHUP',
                            'MIN', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%',
                            'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', '+/-']

        self.assertEqual(logs['PTS'].sum(), 1523)
        self.assertListEqual(list(logs.columns), expected_columns)

    def test_player_stats(self):
        
        logs = PlayerLogs(
            "Kobe Bryant",
            year_range=[2003, 2003],
            season_type=SeasonType.playoffs
        ).nba_stats()

        per_game_stats = PlayerStats(
            logs,
            drtg_range=[90, 100],
            data_format=DataFormat.default
        ).nba_stats()

        per_poss_stats = PlayerStats(
            logs,
            drtg_range=[90, 100],
            data_format=DataFormat.per_100_poss
        ).nba_stats()
        
        self.assertEqual(per_game_stats["PTS"].loc[0], 32.3)
        self.assertEqual(per_poss_stats["PTS"].loc[0], 38.7)

if __name__ == '__main__':
    unittest.main()
