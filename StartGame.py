import sys
from PyQt5 import QtWidgets
from Tetris import Tetris

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = Tetris('Tetris Game')
    game.show()
    sys.exit(app.exec_())