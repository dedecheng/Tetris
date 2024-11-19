from src.Block import BlockType, Block

class Board:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.active_block = Block()
        self.hold = BlockType.I

    def update(self):        
        self.clear_complete_rows()
        #呼叫消行        
        self.active_block.move_down()
        #呼叫生成方塊
        
        if self.check_collision():
        #呼叫碰撞然後呼叫鎖住和生成新方塊
            self.lock_block()
            #生成方塊改到game裡
            self.spawn_new_block()

    def clear_complete_rows(self):
        #檢查每行然後消除
        for row in range(self.height):
            if all(self.board[row]):
                self.board.pop(row)
                self.board.insert(0, [0] * self.width)

    def check_collision(self):
        #檢查碰撞(外if判斷方塊位置，內for和if判斷停留時長)
        for x, y in self.active_block.pos:
            if x < 0 or x >= self.width or y < 0 or y >= self.height or self.board[y][x] != 0:
                '''
                for i in range(self.active_block.stayed_time):
                    if i > 1:
                    #停留時長可以再改
                        return True
                    '''
        return False

    def lock_block(self):
        #鎖住方塊
        for x, y in self.active_block.pos:
            self.board[y][x] = self.active_block.type

'''
    def spawn_new_block(self):
        #生成新方塊
        self.active_block = Block(self.hold)
        self.hold = BlockType((self.hold.value + 1) % len(BlockType))
'''