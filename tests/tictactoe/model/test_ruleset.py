import unittest

from classic_games.tictactoe.model.ruleset import RuleSettings


class TestRuleSettings(unittest.TestCase):
    """
    Tests the class RuleSettings.
    """

    def setUp(self):
        self.rule = RuleSettings(
            board_shape=(3, 3),
            tiles_to_win=3,
            your_symbol=1,
            enemy_symbol=-1,
        )

    def test_export(self):
        """
        Tests the method export().
        """
        dictionary = self.rule.export()

        self.assertEqual(self.rule.board_shape, dictionary["board_shape"])
        self.assertEqual(self.rule.tiles_to_win, dictionary["tiles_to_win"])
        self.assertEqual(self.rule.your_symbol, dictionary["your_symbol"])
        self.assertEqual(self.rule.enemy_symbol, dictionary["enemy_symbol"])


if __name__ == '__main__':
    unittest.main()
