from PyQt5 import QtWidgets, QtCore, QtGui
import sys, random
from PyQt5.QtWidgets import QApplication
from Shape import Shape
from PyQt5.QtCore import Qt

class BoardUI(QtWidgets.QWidget):
    """游戏主要界面绘制，方块的绘制"""

    squareWidth = 30
    squareHeight = 30
    boardWidth = 10
    boardHeight = 20
    dropSpeed = 300 # 300ms
    pixWidth = squareWidth * boardWidth
    pixHeight = squareHeight * boardHeight

    msg2statusBar = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Game")
        self.resize(BoardUI.pixWidth, BoardUI.pixHeight)
        self.squares = []  # [x, y, color]
        self.X = 0
        self.Y = 0
        self.SQ = None
        self.removedLineNum = 0
        self.status = False # True is start 
        self.pause = False # True is pause
        
        self.timer = QtCore.QBasicTimer()
        
        # self.setFocusPolicy(Qt.StrongFocus) # 因为Tetris将keyEvent直接传递给BoardUI, 所以不需要获得当前的Focus


    def getPix(self, x, y): # 将相对的坐标转化为图上绝对的像素点坐标
        return [x*BoardUI.squareWidth, y*BoardUI.squareHeight]

    def RelPoints2AbsPoints(self, points): # 将相对的坐标转化为图上相对的坐标
        return [ [x+self.X, y+self.Y] for x, y in points ]

    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)


        for x, y, color in self.squares:
            pixPoint = self.getPix(x, y)
            self.drawSquare(pixPoint, paint, event, color) # 绘制矩形

        try:
            for x, y in self.SQ.vertex:
                pixPoint = self.getPix(x+self.X, y+self.Y)
                self.drawSquare(pixPoint, paint, event, self.SQ.color)
        except AttributeError as e:
            print(e)
        
        paint.end()

    def drawSquare(self, point, paint, event, color):
        QCol = QtGui.QColor()
        QCol.setNamedColor(color)
        paint.setBrush(QtGui.QBrush(QCol))
        # paint.setPen(QCol)
        paint.drawRect(*point, BoardUI.squareWidth, BoardUI.squareHeight)

    def putShape(self):
        shape = Shape()
        shape.getRandomShape()
        self.SQ = shape
        self.X = BoardUI.boardWidth // 2  - 1 # 放到中间
        self.Y = abs(shape.yRange()[0])  # 最小的y值的绝对值

        if not self.canPut(self.SQ)[0]: # 一开始就放不了了 ， 那就是结束了
            self.timer.stop()
            self.status = False
            self.msg2statusBar.emit('Game Over, your score is ' + str(self.removedLineNum))


    def start(self):
        self.initBoard()
        self.status = True
        self.pause = False
        self.putShape()
        self.timer.start(BoardUI.dropSpeed, self)

    def initBoard(self): # 初始化面板
        self.squares.clear()
        self.X = 0
        self.Y = 0
        self.SQ = None
        self.removedLineNum = 0
        self.status = False
        self.pause = False
        self.msg2statusBar.emit('0')

    def timerEvent(self, event):
        self.Y = self.Y+1
        msg = self.canPut(self.SQ)

        # print(msg)

        if msg[1] == 'out of buttom' or msg[1] == 'overlap': # 到达底部或出现重叠就说明不能放了
            self.Y -= 1
            self.pushSquare(self.SQ)


        if not msg[0]:
            self.putShape()

        print('time is over')
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        print('Put Key:', key, self.status)


        if key == Qt.Key_S:
            self.start()          
        elif self.status == False:
            pass # if it's not start ,just ignore the key as the following
        elif key == Qt.Key_P:
            self.PauseOrRestart()
        elif self.status == True and self.pause == True:
            pass
        elif key == Qt.Key_Left:  # 尝试向右移动，若可以就移动
            self.X -= 1
            if not self.canPut(self.SQ)[0]:
                self.X += 1
        elif key == Qt.Key_Right: # 尝试向右移动，若可以就移动
            self.X += 1
            if not self.canPut(self.SQ)[0]:
                self.X -= 1
        elif key == Qt.Key_Down:
            self.SQ.rotate('Clockwise')
            if not self.canPut(self.SQ)[0]:
                self.SQ.rotate('AntiClockwise')
        elif key == Qt.Key_Up:
            self.SQ.rotate('AntiClockwise')
            if not self.canPut(self.SQ)[0]:
                self.SQ.rotate('Clockwise')
        elif key == Qt.Key_Space:
            while self.canPut(self.SQ)[0]:
                self.Y += 1
            self.Y -= 1
        else:
            super().keyPressEvent(event) # 没有我们想要的就调用父类额

        self.update()

    def canPut(self, shape):  # 检查是否可以放
        points = shape.vertex
        minX = shape.xRange()[0] + self.X
        maxX = shape.xRange()[1] + self.X
        minY = shape.yRange()[0] + self.Y
        maxY = shape.yRange()[1] + self.Y

        if minX>=0 and maxX<BoardUI.boardWidth:
            pass
        else:
            return False, 'out of X'

        if minY>=0: 
            pass
        else:  
            return False, 'out of top'

        if maxY<BoardUI.boardHeight:
            pass
        else:
            return False, 'out of buttom'

        for *p,color in self.squares:
            if p in self.RelPoints2AbsPoints(shape.vertex):
                return False, 'overlap'

        return True, ''

    def readyRemoveLine(self):
        
        cnt = [0] * 20
        for x, y, c in self.squares:
            cnt[y] += 1
        
        self.removedLineNum += cnt.count(BoardUI.boardWidth) # 更新removedLineNum
        self.msg2statusBar.emit(str(self.removedLineNum))


        nSquare = []
        for x, y, c in self.squares:
            dy = 0
            for r in range(y, 20):
                if cnt[r] == BoardUI.boardWidth:
                    if y == r: # 该点要消除
                        break
                    else:  # r>y 该点要向下移一格
                        dy += 1

            else: # 无break就执行
                nSquare += [[x, y+dy, c]]

        self.squares = nSquare
        self.update() # 重新绘制


    def PauseOrRestart(self):
        if not self.pause:
            self.pause = True
            self.timer.stop()
            self.msg2statusBar.emit('Pause')
        else:
            self.pause = False
            self.timer.start(BoardUI.dropSpeed, self)
            self.msg2statusBar.emit(str(self.removedLineNum))

    def pushSquare(self, shape):
        AbsPoints = self.RelPoints2AbsPoints(shape.vertex)
        
        self.squares += [  [x, y, shape.color] for x, y in AbsPoints]

        self.readyRemoveLine() # 检查是否删除
       

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = BoardUI(None)
    game.show()
    sys.exit(app.exec_())
