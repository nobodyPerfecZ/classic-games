import unittest
import gymnasium as gym
import numpy as np

from classic_games.tictactoe.agent.min_max_player import MinMaxPlayer


class TestTicTacToeV0(unittest.TestCase):
    """
    Tests the class tictactoe.
    """

    @classmethod
    def setUpClass(cls) -> None:
        gym.register(id="TicTacToe-v0", entry_point="classic_games.tictactoe.game.env:TicTacToeEnv")

    def setUp(self):
        # Create the tictactoe environment
        self.env = gym.make("TicTacToe-v0", render_mode="human")

    def tearDown(self):
        # Close the tictactoe environment
        self.env.close()

    def test_reset(self):
        """
        Tests the method reset().
        """
        observation, info = self.env.reset(seed=10)

        self.assertEqual(8, self.env.action_space.n)
        self.assertEqual((3, 3), self.env.observation_space.shape)

        np.testing.assert_array_equal(np.array([[0, 0, 0], [0, -1, 0], [0, 0, 0]]), observation)
        self.assertEqual((3, 3), info["board_shape"])
        self.assertEqual(3, info["tiles_to_win"])
        self.assertEqual(1, info["your_symbol"])
        self.assertEqual(-1, info["enemy_symbol"])

    def test_step(self):
        """
        Tests the method step().
        """
        observation, info = self.env.reset(seed=10)
        your_player = MinMaxPlayer(
            your_symbol=1,
            enemy_symbol=-1,
            tiles_to_win=3,
            seed=10
        )

        # Take the first action
        action = your_player.act(observation)
        observation, reward, terminated, truncated, info = self.env.step(action)
        self.assertEqual(0.0, reward)
        self.assertFalse(terminated)
        self.assertFalse(truncated)
        self.assertEqual((3, 3), info["board_shape"])
        self.assertEqual(3, info["tiles_to_win"])
        self.assertEqual(1, info["your_symbol"])
        self.assertEqual(-1, info["enemy_symbol"])

        # Take the second action
        action = your_player.act(observation)
        observation, reward, terminated, truncated, info = self.env.step(action)
        self.assertEqual(0.0, reward)
        self.assertFalse(terminated)
        self.assertFalse(truncated)
        self.assertEqual((3, 3), info["board_shape"])
        self.assertEqual(3, info["tiles_to_win"])
        self.assertEqual(1, info["your_symbol"])
        self.assertEqual(-1, info["enemy_symbol"])

        # Take the third action
        action = your_player.act(observation)
        observation, reward, terminated, truncated, info = self.env.step(action)
        self.assertEqual(1.0, reward)
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertEqual((3, 3), info["board_shape"])
        self.assertEqual(3, info["tiles_to_win"])
        self.assertEqual(1, info["your_symbol"])
        self.assertEqual(-1, info["enemy_symbol"])

    def test_render(self):
        """
        Tests the method render().
        """
        # Perform actions and render frames
        observation, info = self.env.reset(seed=0)
        your_player = MinMaxPlayer(
            your_symbol=1,
            enemy_symbol=-1,
            tiles_to_win=3,
            seed=0
        )
        for _ in range(5):
            action = your_player.act(observation)
            observation, reward, terminated, truncated, info = self.env.step(action)
            self.env.render()

            if terminated or truncated:
                break

    def test_run_episode(self):
        """
        Tests to run one episode
        """
        observation, info = self.env.reset(seed=0)
        your_player = MinMaxPlayer(
            your_symbol=1,
            enemy_symbol=-1,
            tiles_to_win=3,
            seed=0
        )
        for _ in range(5):
            action = your_player.act(observation)
            observation, reward, terminated, truncated, info = self.env.step(action)
            self.env.render()

            if terminated or truncated:
                break

        self.assertEqual(1.0, reward)
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertEqual((3, 3), info["board_shape"])
        self.assertEqual(3, info["tiles_to_win"])
        self.assertEqual(1, info["your_symbol"])
        self.assertEqual(-1, info["enemy_symbol"])

    def test_run_gym_loop(self):
        """
        Tests to run a gym loop.
        """
        rewards = 0.0
        your_player = MinMaxPlayer(
            your_symbol=1,
            enemy_symbol=-1,
            tiles_to_win=3,
            seed=0
        )
        for i in range(10):
            observation, info = self.env.reset(seed=0)
            your_player.reset(seed=0)

            for _ in range(5):
                action = your_player.act(observation)
                observation, reward, terminated, truncated, info = self.env.step(action)

                if terminated or truncated:
                    break

            rewards += reward

        self.assertEqual(10.0, rewards)


if __name__ == '__main__':
    unittest.main()
