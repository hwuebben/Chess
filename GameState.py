import numpy as np
import math
class GameState:
    """
    1 - Pawn
    2 - Horse
    3 - Bishop
    4 - Rook
    5 - Queen
    6 - King

    1 - Black
    2 - White
    """
    def __init__(self):
        self.pieces = {
            "W":{"P": [], "B": ["b1", "g1"], "H": [], "R": [], "Q": [], "K": []},
            "B":{"P": [], "B": ["b7", "g7"], "H": [], "R": [], "Q": [], "K": []}
        }
        board = np.zeros((8,8))
        board[1,:] = np.ones(8) * 11
        board[6,:] = np.ones(8) * 21
        board[0,:] = [14,12,13,15,16,13,12,14]
        board[7,:] = [24, 22, 23, 25, 26, 23, 22, 24]
        self.board = board
        self.moves = self.getMoves()
        self.lastBoard = None
        self.lastMoves = None
        # W (weiss) ist in schach bzw B ist in Schach:
        self.checkW = False
        self.checkB = False
        # W bzw B kann noch lang (L) oder kurz (S) rochieren
        self.castleWS = True
        self.castleWL = True
        self.castleBS = True
        self.castleBL = True

        self.lastTake = 0
    def getMoves(self):
        #TODO: nur moves fuer den Spieler an der Reihe
        self.possibleMoves = []
        #wo stehen die Figuren
        for posx,coloumn in enumerate(self.board):
            for posy,entry in enumerate(coloumn):
                if entry == 0:
                    continue
                pos = np.array([posx,posy])
                piece = int(entry % 10)
                color = math.floor(entry / 10)
                if piece == 1:
                    if color == 1:
                        for jp in np.array([[1, 0],[2,0]]):
                            blocked = self.considerMove(piece,color,pos,pos+jp)
                            if blocked:
                                break
                        for jp in np.array([[1, 1], [1, -1]]):
                            self.considerMove(piece, color, pos, pos + jp)
                    else:
                        for jp in np.array([[-1, 0],[-2,0]]):
                            blocked = self.considerMove(piece,color,pos,pos+jp)
                            if blocked:
                                break
                        for jp in np.array([[-1, -1], [-1, 1]]):
                            self.considerMove(piece, color, pos, pos + jp)
                elif piece == 2:
                    for jh in np.array([[-2, 0], [2, 0], [0, -2], [0, 2]]):
                        jhc = np.copy(jh)
                        for j in [-1, 1]:
                            jh[jhc == 0] = j
                            # print("horse:")
                            # print(jh)
                            # print(pos)
                            # print(pos + jh)
                            self.considerMove(piece, color, pos, pos + jh)
                elif piece == 3 or piece == 5:
                    for jd in np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]]):
                        for i in np.arange(1,8,1):
                            blocked = self.considerMove(piece, color, pos, pos + i * jd)
                            if blocked:
                                break
                if piece == 4 or piece == 5:
                    for jv in np.array([[-1, 0], [0, -1], [1, 0], [0, 1]]):
                        for i in np.arange(1,8,1):
                            blocked = self.considerMove(piece, color, pos, pos + i * jv)
                            if blocked:
                                break
                elif piece == 6:
                    for jk in np.array([[-1, 0], [0, -1], [1, 0], [0, 1],[1,1],[-1,-1],[-1,1],[1,-1]]):
                        self.considerMove(piece, color, pos, pos + jk)

    def considerMove(self,piece,color,start,dest,ret = False):
        #dest am Ende des Feldes?
        if (dest < 0).any() or (dest > 7).any():
            return True
        emptDest = self.board[dest[0],dest[1]] == 0
        #Zielfeld ist leer
        if emptDest:
            #bauern duerfen nur schraeg gehen wenn ein Gegner da ist:
            if piece == 1:
                if not start[1] == dest[1]:
                    return False
            move = str(start[0])+str(start[1])+"-"+str(dest[0])+str(dest[1])
            self.makeMove(move,test=True)
            if not self.isInCheck(color):
                if ret:
                    return move
                else:
                    self.possibleMoves.append(move)
            self.board = self.lastBoard
            return False
        #Zielfeld von eigener Figur blockiert
        ownDest = math.floor(self.board[dest[0],dest[1]] / 10) == color
        if ownDest:
            return True
        #sonst Zielfeld von gegnerischer Figur bestetzt:
        #beim bauern:  darf nur schlagen wenn gegner quer steht:
        if piece == 1:
            if start[1] == dest[1]:
                return True
        move = str(start[0]) + str(start[1]) + "x" + str(dest[0]) + str(dest[1])
        self.makeMove(move,test=True)
        if not self.isInCheck(color):
            if ret:
                return move
            else:
                self.possibleMoves.append(move)
        self.board = self.lastBoard
        return False


    """
    color: 1 or 2
    square: int[]
    """
    def squareAttackedby(self,square,color):
        #Horses?
        for jh in np.array([[-2,0],[2,0],[0,-2],[0,2]]):
            jhc = np.copy(jh)
            for j in [-1,1]:
                jh[jhc==0] = j
                hsquare = square + jh
                if (hsquare < 0).any() or (hsquare > 7).any():
                    continue
                if (self.board[hsquare[0], hsquare[1]] == 10*color+2):
                    return True

        #Diagonal: Pawns, Bishops Queen, King?
        baq = [color*10+3,color*10+5]
        for j,jd in enumerate(np.array([[-1,-1],[-1,1],[1,-1],[1,1]])):
            for i in np.arange(7)+1:
                dsquare = square + jd*i
                if (dsquare < 0).any() or (dsquare > 7).any():
                    break
                #King or pawn:
                if i == 1:
                    if color == 1:
                        #check for king
                        if self.board[dsquare[0],dsquare[1]] == 16:
                            return True
                        # check for pawn
                        if j > 1:
                            if self.board[dsquare[0],dsquare[1]] == 11:
                                return True
                    elif color == 2:
                        if self.board[dsquare[0],dsquare[1]] == 26:
                            return True
                        if j < 2:
                            if self.board[dsquare[0],dsquare[1]] == 21:
                                return True

                if (self.board[dsquare[0],dsquare[1]] == baq).any():
                    return True
                if not self.board[dsquare[0], dsquare[1]] == 0:
                    break

        #vertical: Rooks, Queen, King?
        raq = [color*10+4,color*10+5]
        for jv in np.array([[-1,0],[0,-1],[1,0],[0,1]]):
            for i in np.arange(7)+1:
                vsquare = square + jv*i
                if (vsquare < 0).any() or (vsquare > 7).any():
                    break
                #King?
                if i == 1:
                    if color == 1:
                        if self.board[vsquare[0], vsquare[1]] == 16:
                            return True
                    elif color == 2:
                        if self.board[vsquare[0], vsquare[1]] == 26:
                            return True
                #wenn eine Figur aus raq steht: Schach!
                if (self.board[vsquare[0],vsquare[1]] == raq).any():
                    return True
                #wenn eine andere Figur im wegsteht: break
                if not self.board[vsquare[0], vsquare[1]] == 0:
                    break
        return False

    def isInCheck(self,color):
        colorOpp = [2,1][color-1]
        # print(self.board)
        # print(10*color + 6)
        # print(np.argwhere(self.board == 10*color + 6))
        locKing = np.argwhere(self.board == 10*color + 6)
        if locKing.size == 0:
            return True
        square = locKing[0]
        return self.squareAttackedby(square, colorOpp)

    """
    Zuege werden in algebraischer NOtation angegeben
    e2-e4 (von e2 nach e4)
    e2xe4 (e2 schlaegt auf e4)
    e5epf6 (e5 schlaegt en passant f5 und geht zu f6)
    e7xpSf8 (e7 schlaegt auf f8 und verwandelt sich in S (Springer)
    e7-pSe8 (e7 geht zu e8 und verwandelt sich in S (Springer)
    e1rof1 (kurze Rochade)
    """
    def makeMove(self,move,test=False):
        if not test:
            self.getMoves()
            print("legal moves: ",self.possibleMoves)
            isLegal = False
            for m in self.possibleMoves:
                if m == move:
                    isLegal = True
            if not isLegal:
                return

        self.lastBoard = np.copy(self.board)
        # self.lastMoves = self.moves
        #source field
        sf = move[0:2]
        #target field
        tf = move[-2::]
        #move piece
        self.movePiece(sf,tf)

        #operation
        op = move[2:-2]
        #additional changes:
        if op == "ro":
            if tf[1] == "6":
                sfry = "7"
            elif tf[1] == "2":
                sfry = "0"
            #rook pos:
            sfr = [sf[0],sfry]
            #new pos for rook:
            tfr = [sf[0], (int(sf[1]) + int(tf[1])) / 2]
            self.movePiece(sfr,tfr)
        # print(self.isInCheck(1))
        # print(self.isInCheck(2))
        # print(self.board)

    def movePiece(self,sf,tf):
        self.board[int(tf[0]),int(tf[1])] = self.board[int(sf[0]),int(sf[1])]
        self.board[int(sf[0]),int(sf[1])] = 0

if __name__ == "__main__":
    gs = GameState()
    gs.getMoves()
    print(gs.board)
    print(gs.possibleMoves)
    gs.makeMove("06-53")
    #gs.makeMove("25-44")
    #gs.makeMove("05-14")
    #gs.makeMove("04ro06")






