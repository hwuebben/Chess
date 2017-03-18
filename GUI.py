from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import pylab
import numpy as np
import math
import GameState

class GUI:


    def __init__(self):
        self.gs = GameState.GameState()
        # board image:
        board = mpimg.imread('img/chessboard.png')
        # pieces images
        bid = mpimg.imread('img/Chess_bdt60.png')
        bil = mpimg.imread('img/Chess_blt60.png')
        knd = mpimg.imread('img/Chess_ndt60.png')
        knl = mpimg.imread('img/Chess_nlt60.png')
        pad = mpimg.imread('img/Chess_pdt60.png')
        pal = mpimg.imread('img/Chess_plt60.png')
        rod = mpimg.imread('img/Chess_rdt60.png')
        rol = mpimg.imread('img/Chess_rlt60.png')
        qud = mpimg.imread('img/Chess_qdt60.png')
        qul = mpimg.imread('img/Chess_qlt60.png')
        kid = mpimg.imread('img/Chess_kdt60.png')
        kil = mpimg.imread('img/Chess_klt60.png')

        self.pieces = np.array([
            [pal, knl, bil, rol, qul, kil],
            [pad, knd, bid, rod, qud, kid]
        ])
        fig = plt.figure("Board")
        ax = fig.add_subplot()
        cid = fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.imshow(board)
        self.squares = np.empty((8, 8), dtype=object)

        for i in range(8):
            for j in range(8):
                offsetx = 131.5
                offsety = 132.5
                dummy = plt.imshow([[],[],[]],extent=[73.5+offsetx*i, 200+offsetx*i, 73.5+offsety*j, 200+offsety*j])
                self.squares[i,j] = dummy

        self.isClicked = False
        self.moveSquares = np.empty((2,2),dtype=int)
        self.drawBoard(init = True)

    def onclick(self,event):
        # print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        #       (event.button, event.x, event.y, event.xdata, event.ydata))
        coord = np.array([event.xdata,event.ydata])
        if (coord >= 73.5).all() and (coord <= 1126.5).all():

            if self.isClicked:
                self.moveSquares[1,:] = self.coordToSquare(coord)
                move = self.generateMove()
                if move:
                    self.gs.makeMove(move)
                    self.drawBoard()
            else:
                self.moveSquares[0,:] = self.coordToSquare(coord)
            self.isClicked = not self.isClicked

    def generateMove(self):
        square1 = self.moveSquares[0,:][::-1]
        square2 = self.moveSquares[1,:][::-1]
        piece = self.gs.board[square1[0],square1[1]]
        color = math.floor(piece / 10)
        print(self.gs.possibleMoves)
        move = self.gs.considerMove(piece,color,square1,square2,ret=True)
        print(move)
        if isinstance(move,str):
            return move
        else:
            return False

        # if self.gs.board[square2[1],square2[0]] == 0:
        #     move = str(square1[1])+str(square1[0])+"-"+str(square2[1])+str(square2[0])
        # else:
        #     move = str(square1[1]) + str(square1[0]) + "x" + str(square2[1]) + str(square2[0])
        # return move

    def coordToSquare(self,coord):
        xs = int(math.floor((coord[0] - 73.5) / 131.5))
        ys = int(math.floor((coord[1] - 73.5) / 131.5))
        return [xs,ys]


    def drawBoard(self,init=False):
        for i in range(8):
            for j in range(8):
                if self.gs.board[j,i] > 0:
                    p0 = int(str(self.gs.board[j,i])[0])-1
                    p1 = int(str(self.gs.board[j,i])[1])-1
                    self.squares[i,j].set_data(self.pieces[p0,p1])
                else:
                    self.squares[i, j].set_data([[],[],[]])
        pylab.ylim([0, 1200])
        pylab.xlim([0, 1200])
        if init:
            plt.show()
        else:
            plt.draw()
if __name__ == "__main__":
    myGUI = GUI()
