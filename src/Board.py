from src.Block import BlockType, Block


class Board():
    def __init__(self):
        self.width = 10
        self.height = 20
        self.board = []
        self.active_block = Block()
        self.hold = BlockType.I

    def update(self):
        # 消行
        # 生成方塊
        pass


'''施工中請稍後'''

class Board:
   def __init__(self):
        self.width = 10
        self.height = 20
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.active_block = Block()
        self.hold = BlockType.I

   def update(self):
        #檢查有沒有行可以消
        self.clear_complete_rows()
       
        #更新方塊
        self.active_block.move_down()
       
        #檢查碰撞
        if self.check_collision():
        
           '''
           self.lock_block()
           self.spawn_new_block()
           '''

   def clear_complete_rows(self):
       # Iterate through the rows, clearing any that are full
       for row in range(self.height):
           if all(self.board[row]):
               self.board.pop(row)
               self.board.insert(0, [0] * self.width)

   def check_collision(self):
       # Check for collisions between the active block and the board
       for x, y in self.active_block.get_block_positions():
           if x < 0 or x >= self.width or y < 0 or y >= self.height or self.board[y][x] != 0:
               return True
       return False

   def lock_block(self):
       # Lock the active block into the board
       for x, y in self.active_block.get_block_positions():
           self.board[y][x] = self.active_block.block_type.value

   def spawn_new_block(self):
       # Create a new active block
       self.active_block = Block(self.hold)
       self.hold = BlockType((self.hold.value + 1) % len(BlockType))