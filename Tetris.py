from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from BoardUI import BoardUI

class Tetris(QtWidgets.QMainWindow):
    def __init__(self, title):
        super(Tetris, self).__init__()

        self.setWindowTitle(title)
        self.resize(BoardUI.pixWidth, BoardUI.pixHeight+30)
# 
        initWidget = QtWidgets.QWidget(self)
        startButton = QtWidgets.QPushButton('开始(S)')
        startButton.clicked.connect(self.gameStart)
        startButton.setShortcut('S') #设置快捷方式
        msgLabel = QtWidgets.QLabel('         按S键可以开始\n         按P键可以暂停/继续')

        hbox = QtWidgets.QHBoxLayout()  # 设置水平垂直居中
        hbox.addStretch(1)
        hbox.addWidget(startButton)
        hbox.addStretch(1)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addWidget(msgLabel)
        vbox.addStretch(1)
        initWidget.setLayout(vbox)
        startButton.resize(100, 30)
        self.setCentralWidget(initWidget)


        self.center()

    def center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, \
            (screen.height()-size.height())/2)

    def gameStart(self):
     
        self.UI = BoardUI(self)
        self.resize(BoardUI.pixWidth, BoardUI.pixHeight+30)

        self.sBar = self.statusBar()
        self.UI.msg2statusBar[str].connect(self.sBar.showMessage)

        self.setCentralWidget(self.UI)
        print(self.centralWidget())
        # self.UI.setFocus() # 不知道为什么无法使 BoardUI 获得 Focus
        # print(self.focusWidget()) # 还是 QPushButton
        self.UI.start()


    def keyPressEvent(self, event): # 通过这种方法绕过Focus, 将keyEvent一直给centralWidget()
        self.centralWidget().keyPressEvent(event) # 传递给centralWidget

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = Tetris('Tetris')
    game.show()
    sys.exit(app.exec_())