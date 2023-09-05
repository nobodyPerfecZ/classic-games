import unittest

from classic_games.tictactoe.model.metadata import Metadata


class TestMetadata(unittest.TestCase):
    """
    Tests the class Metadata.
    """

    def setUp(self):
        self.empty_rule_settings = Metadata()
        self.rule_settings = Metadata(
            board_shape=(4, 4),
            tiles_to_win=4,
            your_symbol=2,
            enemy_symbol=-2,
            render_modes=["human"],
            render_fps=40,
        )

    def test_to_dict(self):
        """
        Tests the method to_dict().
        """
        empty_rule_settings = self.empty_rule_settings.to_dict()
        rule_settings = self.rule_settings.to_dict()

        self.assertEqual((3, 3), empty_rule_settings["board_shape"])
        self.assertEqual(3, empty_rule_settings["tiles_to_win"])
        self.assertEqual(1, empty_rule_settings["your_symbol"])
        self.assertEqual(-1, empty_rule_settings["enemy_symbol"])
        self.assertEqual(["human", "rgb_array"], empty_rule_settings["render_modes"])
        self.assertEqual(30, empty_rule_settings["render_fps"])

        self.assertEqual(self.rule_settings.board_shape, rule_settings["board_shape"])
        self.assertEqual(self.rule_settings.tiles_to_win, rule_settings["tiles_to_win"])
        self.assertEqual(self.rule_settings.your_symbol, rule_settings["your_symbol"])
        self.assertEqual(self.rule_settings.enemy_symbol, rule_settings["enemy_symbol"])
        self.assertEqual(self.rule_settings.render_modes, rule_settings["render_modes"])
        self.assertEqual(self.rule_settings.render_fps, rule_settings["render_fps"])


if __name__ == '__main__':
    unittest.main()
