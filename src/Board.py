from src.Block import BlockType, Block


class Board:
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

    def place_block(self):
        pass
