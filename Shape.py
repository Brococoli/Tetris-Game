import random

class BlockType(): # 设置 方块的类型
    NoShape = 0
    ZShape = 1
    LShape = 2
    TShape = 3
    OShape = 4
    IShape = 5
    SShape = 6
    _IShape = 7

    init_shape = ( # 方块的相对坐标
        (), # None
        ((-1, 0), (0, 0), ( 0, -1), (1, -1)), # Z
        (( 0, 1), (0, 0), ( 0, -1), (1, -1)), # L
        ((-1, 0), (0, 0), ( 1,  0), (0, -1)), # T
        ((-1, 0), (0, 0), (-1, -1), (0, -1)), # 口
        (( 0, 1), (0, 0), ( 0, -1), (0, -2)), # I
        (( 1, 0), (0, 0), ( 0, -1), (-1, -1)), # S (Z 的镜像)
        (( 0, 1), (0, 0), ( 0, -1), (-1, -1)), # _/ (L 的镜像)
    )

class Shape():
    def __init__(self):
        self.vertex = [] # 方块的点
        self.type = 0 # 方块的类型
        self.color = '#000000' # 方块的颜色

    def getRandomShape(self):
        self.type = random.randint(1,7) # 1 <= N <=7
        self.vertex = [ list(v) for v in BlockType.init_shape[self.type] ] # 所有tuple 转化为list
        self.color = hex(random.randint(0,0xffffff)).replace('0x', '#').upper() # '0xf2f5ab' 转化为 '#F2F5AB'

    def rotate(self, str): # 旋转
        if not self.vertex or self.type == 4:
            return

        nVertex = []
        if str == 'Clockwise':
            for x, y in self.vertex: # 没个点变为（y, -x) 可根据极坐标得出: x = rcos(θ-π/2) = rsin(θ) = y
                nVertex.append([y, -x])

        else:
            for x, y in self.vertex:
                nVertex.append([-y, x])

        self.vertex = nVertex

    def xRange(self): # x的范围
        xList = [v[0] for v in self.vertex]
        minX = min(xList)
        maxX = max(xList)
        return (minX, maxX)

    def yRange(self): # y的范围
        yList = [v[1] for v in self.vertex]
        minY = min(yList)
        maxY = max(yList)
        return (minY, maxY)

        

if __name__ == '__main__':
    shape = Shape()
    print(shape.vertex)
    shape.getRandomShape()
    print(shape.vertex)
    shape.rotate('Clockwise')
    print(shape.vertex)
    shape.rotate("Anticlockwise")
    print(shape.vertex)