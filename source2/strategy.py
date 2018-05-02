
import random
import decimal
import numpy

width = 7
height = 6
numInRow = 4

class strategy:
    def __init__(self,board):
        b = [-1]*width
        board.append(b)
        board.append(b)
        self.board = board
    

    def placePiece(self,player, index):
        if not(self.indexIsFull(index)):
            i = 1
            while ((self.board[i][index] == -1) and (i < height)):
                i += 1
            self.board[i-1][index] = player
            #print(self.board)
            #self.displayBoard()
            #displayBoard1()
            return index

    def displayBoard(self):
        #print("  | 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
        for i in range(0,height):
            print("%d " % (i+1),end="", flush = True)
            for j in range(0,width):
                if j<width-1:
                    print("%s %s %s" % ('|', self.board[i][j], ''), end="", flush = True)
                else:
                    print("%s %s %s" % ('|', self.board[i][j], '|'), end="", flush = True)
            print(end="\n")

        print("\n" * 2)

    def indexIsFull(self,index):
        if self.board[0][index] != -1:
            return True
        else:
            return False


    def boardIsFull(self):
        for i in range(0, width):
            if self.indexIsFull(i) == False:
                return False
        return True


    def checkPoint(self,height_, width_, player):
        #Testing up and down
        i = 1
        #tracks from initial point down until it find a non player piece
        while (height_ - i >= 0) and (i < numInRow):
            if self.board[height_-i][width_] != player:
                break
            i += 1
        #if it tracks the length of win condition then that player wins
        if i == numInRow:
            return True
        j = numInRow-i
        #left over distance tracking down is moved to the top to check if
        #the rest of pieces needed are at the top
        while (height_+j < height) and (j > 0):
            if(self.board[height_+j][width_] != player):
                break
            j -= 1
        #if no more distance is needed than that player wins
        if j == 0:
            return True
        #Testing left and right in same fashion as first check
        i = 1
        while (width_ - i >= 0) and (i < numInRow):
            if self.board[height_][width_-i] != player:
                break
            i += 1
        if i == numInRow:
            return True
        j = numInRow-i
        while (width_+j < width) and (j > 0):
            if(self.board[height_][width_+j] != player):
                break
            j -= 1
        if j == 0:
            return True
        #Testing diagonals from top left to bottom right in same fashion as first check
        i = 1
        while (width_ - i >= 0) and (height_ - i >= 0) and (i < numInRow):
            if self.board[height_-i][width_-i] != player:
                break
            i += 1
        if i == numInRow:
            return True
        j = numInRow-i
        while (width_+j < width) and (height_ + i < height) and (j > 0):
            if(self.board[height_+j][width_+j] != player):
                break
            j -= 1
        if j == 0:
            return True
        #Testing diagonalsfrom bottom left to top right in same fashion as first check
        i = 1
        while (width_ - i >= 0) and (height_ + i < height) and (i < numInRow):
            if self.board[height_+i][width_-i] != player:
                break
            i += 1
        if i == numInRow:
            return True
        j = numInRow-i
        while (width_+j < width) and (height_ - i >= 0) and (j > 0):
            if(self.board[height_-j][width_+j] != player):
                break
            j -= 1
        if j == 0:
            return True
        else:
            return False

    def smartTurn0(self):
        noUse = []
        for i in range(0,width):
            if(self.indexIsFull(i)):
                noUse.append(i)
        #print("not usable: ", noUse)
        #checks if there is any location that would generate victory
        for i in range(0, width):
            if not(self.ifInList(i, noUse)):
                if(self.checkPoint(self.getTopOfIndex(i), i, 0)):
                    #self.placePiece(0, i)
                    return i
        #checks if there is any location that would generate victory for opponent
        #so that it can be blocked
        for i in range(0, width):
            if not(self.ifInList(i, noUse)):
                if(self.checkPoint(self.getTopOfIndex(i), i , 1)):
                    #self.placePiece(0, i)
                    return i
        #find all locations that would place opponent in a position to win and places
        #them on a list of unusable locations
        for i in range(0, width):
            if (self.getTopOfIndex(i)-1) >= 0 and (self.checkPoint(self.getTopOfIndex(i)-1, i , 1)):
                noUse.append(i)

        #self.placePiece(0, self.getLongestChain(noUse, 0))
        return self.getLongestChain(noUse, 0)

    def smartTurn1(self):
        noUse = []
        for i in range(0,width):
            if(self.indexIsFull(i)):
                noUse.append(i)
        print("not usable: ", noUse)
        for i in range(0, width):
            if not(self.ifInList(i, noUse)):
                if(self.checkPoint(self.getTopOfIndex(i), i, 1)):
                    return i
                    #return self.placePiece(1, i)
        for i in range(0, width):
            if not(self.ifInList(i, noUse)):
                if(self.checkPoint(self.getTopOfIndex(i), i , 0)):
                    return i
                    #return self.placePiece(1, i)
                   
        for i in range(0, width):
            if (self.getTopOfIndex(i)-1) >= 0 and (self.checkPoint(self.getTopOfIndex(i)-1, i , 0)):
                noUse.append(i)

        x = self.getLongestChain(noUse, 1)
        print("move ",x)
        return x

    def getTopOfIndex(self,index):
        i = 1
        while ((self.board[i][index] == -1) and (i < height)):
            i += 1
        return i-1

    def getLongestChain(self,notUsable, player):
        if len(notUsable) == width:
            print("returning first")
            return random.randint(0, height)
        if(self.board[3][height] == ""):
            print("second")
            index = 3
        """
        if len(notUsable) == width-1 and 6 not in notUsable:
            index = 6
            return index
        else:
            index = random.randint(0,height)
        """
        maxVal = 0
        lis = []
        temp=0
        for k in range(0, width):
            if not(self.ifInList(k, notUsable)):
                i = 1
                while (self.getTopOfIndex(k) - i >= 0) and (i < numInRow):	
                    if self.board[self.getTopOfIndex(k)-i][k] != player:
                        break
                    i += 1
                j = 1
                while (self.getTopOfIndex(k)+j < height) and (j < numInRow):
                    if(self.board[self.getTopOfIndex(k)+j][k] != player):
                        break
                    j += 1
                if(i+j-2 >= maxVal):
                    rand = random.randint(0,1)
                    if(rand == 1):
                        maxVal = i+j-2
                        index = k
                        if temp == maxVal:
                            lis.append(index)
                        else:
                            lis = []
                            lis.append(index)
                            temp = maxVal
                i = 1

                while (k - i >= 0) and (i < numInRow):
                    if self.board[self.getTopOfIndex(k)][k-i] != player:
                        break
                    i += 1
                j = 1
                while (k+j < width) and (j < numInRow):
                    if(self.board[self.getTopOfIndex(k)][k+j] != player):
                        break
                    j += 1
                if(i+j-2 >= maxVal):
                    rand = random.randint(0,1)
                    if(rand == 1):
                        maxVal = i+j-2
                        index = k
                        if temp == maxVal:
                            lis.append(index)
                        else:
                            lis = []
                            lis.append(index)
                            temp = maxVal
                        
                i = 1

                while (k - i >= 0) and (self.getTopOfIndex(k) - i >= 0) and (i < numInRow):
                    if self.board[self.getTopOfIndex(k)-i][k-i] != player:
                        break
                    i += 1
                j = 1
                while (k+j < width) and (self.getTopOfIndex(k) + i < height) and (j < numInRow):
                    if(self.board[self.getTopOfIndex(k)+j][k+j] != player):
                        break
                    j += 1
                if(i+j-2 >= maxVal):
                    rand = random.randint(0,1)
                    if(rand == 1):
                        maxVal = i+j-2
                        index = k
                        if temp == maxVal:
                            lis.append(index)
                        else:
                            lis = []
                            lis.append(index)
                            temp = maxVal
                i = 1
                while (k - i >= 0) and (self.getTopOfIndex(k) + i < height) and (i < numInRow):
                    if self.board[self.getTopOfIndex(k)+i][k-i] != player:
                        break
                    i += 1
                j = 1
                while (k+j < width) and (self.getTopOfIndex(k) - i >= 0) and (j < numInRow):
                    if(self.board[self.getTopOfIndex(k)-j][k+j] != player):
                        break
                    j += 1
                if(i+j-2 >= maxVal):
                    rand = random.randint(0,1)
                    if(rand == 1):
                        maxVal = i+j-2
                        index = k
                        if temp == maxVal:
                            lis.append(index)
                        else:
                            lis = []
                            lis.append(index)
                            temp = maxVal
        r = 0
        if len(lis)>1:
            r = random.randint(0,len(lis)-1)
        try:
            return lis[r]
        except:
            return 0
    

    def ifInList(self,num, list):
        for i in range(0, len(list)):
            if(list[i] == num):
                return True
        return False
