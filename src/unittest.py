import unittest
from unittest.mock import patch, MagicMock
from src import GameManager, Block, BlockType, Direction, Board

class TestGameManager(unittest.TestCase):
    def setUp(self):
        self.width = 10
        self.height = 20
        self.game_manager = GameManager(self.width, self.height)

    @patch('src.Block')
    def test_next_block(self, MockBlock):
        MockBlock.side_effect = lambda *args, **kwargs: MagicMock()
        block = self.game_manager.next_block()
        self.assertIsNotNone(block)
        self.assertEqual(len(self.game_manager.blocks_queue), 7 + self.game_manager.preview_count - 1)

    def test_move_right_valid(self):
        self.game_manager.current_block.pos = [5, 5]
        self.game_manager.move_right()
        self.assertEqual(self.game_manager.current_block.pos, [6, 5])

    def test_move_right_invalid(self):
        self.game_manager.current_block.pos = [self.width - 1, 5]
        self.game_manager.move_right()
        self.assertEqual(self.game_manager.current_block.pos, [self.width - 1, 5])

    def test_rotate_right_valid(self):
        initial_direction = self.game_manager.current_block.direction
        self.game_manager.rotate_right()
        self.assertNotEqual(self.game_manager.current_block.direction, initial_direction)

    def test_rotate_left_valid(self):
        initial_direction = self.game_manager.current_block.direction
        self.game_manager.rotate_left()
        self.assertNotEqual(self.game_manager.current_block.direction, initial_direction)

    def test_hold_block_first_time(self):
        self.game_manager.hold_block()
        self.assertIsNotNone(self.game_manager.hold)
        self.assertNotEqual(self.game_manager.hold, self.game_manager.current_block)

    def test_hold_block_swap(self):
        self.game_manager.hold_block()  # First hold
        first_hold = self.game_manager.hold
        self.game_manager.hold_block()  # Swap hold
        self.assertEqual(self.game_manager.current_block, first_hold)

    def test_place_block_and_score_update(self):
        initial_score = self.game_manager.score
        initial_line_cleared = self.game_manager.line_cleared
        with patch.object(self.game_manager.board, 'place_block', return_value=1):  # Mock one line cleared
            self.game_manager.place_block()
        self.assertGreater(self.game_manager.score, initial_score)
        self.assertEqual(self.game_manager.line_cleared, initial_line_cleared + 1)

    def test_check_gameover(self):
        self.game_manager.board.board[self.height - 1] = [1] * self.width  # Simulate filled row
        self.assertTrue(self.game_manager.check_gameover())
        self.assertEqual(self.game_manager.game_state, GameState.GameOver)

    @patch('json.dump')
    @patch('os.path.exists', return_value=False)
    def test_record_score_new_file(self, mock_exists, mock_dump):
        self.game_manager.record_score()
        mock_dump.assert_called()

    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[])
    def test_record_score_update(self, mock_load, mock_exists, mock_dump):
        self.game_manager.score = 500
        self.game_manager.record_score()
        mock_dump.assert_called()

if __name__ == "__main__":
    unittest.main()
