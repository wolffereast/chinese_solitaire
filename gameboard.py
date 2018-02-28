'''
Created on Feb 10, 2018

@author: stephen
'''

import Tkinter
from random import randrange
from time import sleep

class Gameboard(Tkinter.Frame):
    
    # Board layouts must be an array of equal length arrays, one per column,
    # and they must only contain 0, -1, and 1. 
    def verifyGameboard(self, boardLayout):
        length = -1
        self.boardWidth = len(boardLayout)
        if not self.boardWidth:
            print 'invalid board layout: empty layout'
            return False
        for row in boardLayout:
            # Catch the type error, this will verify that the row is iterable. 
            try:
                self.boardHeight = len(row)
                if not self.boardHeight:
                    print 'invalid board layout: empty column'
                    return False
            except TypeError: # catch when for loop fails
                print 'invalid board layout: column is not a list'
                return False
                
            if -1 == length:
                length = len(row)
                continue
            
            if length != len(row):
                print 'invalid board layout: column lengths must be consistent'
                return False
            
            for i in row:
                try:
                    if i < -1 or i > 1:
                        print 'invalid board layout: column may only contain -1, 0, and 1'
                        return False
                except TypeError:
                    print 'invalid board layout: column may only contain -1, 0, and 1'
                    return False
                                 
        return True
    
    def createWidgets(self):
        self.quitButton = Tkinter.Button(self, fg = 'red', text = 'QUIT', command = self.quit)
        self.quitButton.pack({"side": "left"})
        
        self.showMovesButton = Tkinter.Button(self, fg = 'black', text = 'Show Moves', command = lambda: self.showAvailableMoves(self.boardLayout))
        self.showMovesButton.pack({"side": "left"})
        
        self.removeMovesButton = Tkinter.Button(self, fg = 'black', text = 'Remove Moves', command = lambda: self.removeAvailableMoveLines())
        self.removeMovesButton.pack({"side": "left"})
        
        self.randomMove = Tkinter.Button(self, fg = 'black', text = 'Random Move', command = lambda: self.makeMove())
        self.randomMove.pack({"side": "left"})
        
        self.solve = Tkinter.Button(self, fg = 'black', text = 'Solve', command = lambda: self.solveBoard())
        self.solve.pack({"side": "left"})
        
        # Need to create a marble for each item in the row
        self.canvas = Tkinter.Canvas(width = len(self.boardLayout[0]) * 20, height = len(self.boardLayout) * 20, bg = 'white')
        self.canvas.pack()
        
        self.canvasItems = [];
        for i, row in enumerate(self.boardLayout):
            self.canvasItems.append([])
            for j, item in enumerate(row):
                # skip empty squares.
                if -1 == item:
                    self.canvasItems[i].append('')
                    continue
                
                oval = self.createOval(i, j, 'black' if 1 == item else 'white')
                self.canvasItems[i].append(oval)
                
    def createOval(self, x, y, color):
        x1 = x * 20 + 5
        y1 = y * 20 + 5
        return self.canvas.create_oval(x1, y1, x1 + 15, y1 + 15, fill = color)
                
    def updateStatus(self, x, y, color):
        marble = self.canvasItems[x][y]
        self.canvas.itemconfig(marble, fill = color)
        
    # Given the current board layout, return a list of available moves as a
    # triplet with the first index as the item to move, the second as the item
    # to be removed, and the third as the target.
    def getAvailableMoves(self, boardLayout):
        availableMoves = []
        # Go through and find empty spots. Any empty spot with two marbles
        # in a row adjacent is a potential move.
        for i, row in enumerate(boardLayout):
            for j, item in enumerate(row):
                if item != 0:
                    continue
                # We need to check all four directions around an empty spot
                # to see if it has potential moves.
                # Jump Down.
                if j > 1 and 1 == boardLayout[i][j - 2] and 1 == boardLayout[i][j - 1]:
                    availableMove = []
                    availableMove.append([i, j - 2])
                    availableMove.append([i, j - 1])
                    availableMove.append([i, j])
                    availableMove.append(0)
                    availableMoves.append(availableMove);
                # Jump Left.
                if i < self.boardWidth - 2 and 1 == boardLayout[i + 1][j] and 1 == boardLayout[i + 2][j]:
                    availableMove = []
                    availableMove.append([i + 2, j])
                    availableMove.append([i + 1, j])
                    availableMove.append([i, j])
                    availableMove.append(1)
                    availableMoves.append(availableMove);
                # Jump Up.
                if j < self.boardHeight - 2 and 1 == boardLayout[i][j + 1] and 1 == boardLayout[i][j + 2]:
                    availableMove = []
                    availableMove.append([i, j + 2])
                    availableMove.append([i, j + 1])
                    availableMove.append([i, j])
                    availableMove.append(2)
                    availableMoves.append(availableMove);
                # Jump Right.
                if i > 1 and 1 == boardLayout[i - 1][j] and 1 == boardLayout[i - 2][j]:
                    availableMove = []
                    availableMove.append([i - 2, j])
                    availableMove.append([i - 1, j])
                    availableMove.append([i, j])
                    availableMove.append(3)
                    availableMoves.append(availableMove);
                
        return availableMoves
    
    def showAvailableMoves(self, boardLayout):
        # Wipe the board.
        self.removeAvailableMoveLines()
        
        availableMoves = self.getAvailableMoves(boardLayout)

        if not len(availableMoves):
            return
        
        # now print them all! We need to overlay the arrow on the middle item
        # in the quad. 
        for move in availableMoves:
            # The arrow points a different direction based on the fourth item.
            # Up.
            x1 = move[1][0] * 20 + 5
            y1 = move[1][1] * 20 + 5
            if 0 == move[3]:
                line = self.canvas.create_line(x1 + 8, y1, x1 + 8, y1 + 15)
        
                self.canvas.itemconfig(line, arrow = 'last', fill = 'green')
                self.availableMoveLines.append(line)
            elif 1 == move[3]:
                line = self.canvas.create_line(x1 + 15, y1 + 8, x1, y1 + 8)
                
                self.canvas.itemconfig(line, arrow = 'last', fill = 'green')
                self.availableMoveLines.append(line)
            elif 2 == move[3]:
                line = self.canvas.create_line(x1 + 8, y1 + 15, x1 + 8, y1)
        
                self.canvas.itemconfig(line, arrow = 'last', fill = 'green')
                self.availableMoveLines.append(line)
            elif 3 == move[3]:
                line = self.canvas.create_line(x1, y1 + 8, x1 + 15, y1 + 8)
                
                self.canvas.itemconfig(line, arrow = 'last', fill = 'green')
                self.availableMoveLines.append(line)
                
    def removeAvailableMoveLines(self):
        for item in self.availableMoveLines:
            self.canvas.delete(item)
    
    def getStateAfterMove(self, boardLayout, move):
        boardLayout[move[0][0]][move[0][1]] = 0;
        boardLayout[move[1][0]][move[1][1]] = 0;
        boardLayout[move[2][0]][move[2][1]] = 1;
        return boardLayout
        
    def makeMove(self):
        # Make sure we get rid of the available lines first.
        self.removeAvailableMoveLines()
        
        availableMoves = self.getAvailableMoves(self.boardLayout);
        if not len(availableMoves):
            print 'Game Over!'
            return
                  
        # make this random for now.
        move = randrange(0, len(availableMoves))
        
        # Need to remove the item being moved over and the item moving, then
        # add the item moved to.
        self.canvas.itemconfig(self.canvasItems[availableMoves[move][0][0]][availableMoves[move][0][1]], fill = 'green')
        # The update call is required, or it will queue all the updates and
        # wait until after both sleeps.
        self.canvas.update()
        sleep(.25)
        
        self.canvas.itemconfig(self.canvasItems[availableMoves[move][0][0]][availableMoves[move][0][1]], fill = 'white')
        self.canvas.itemconfig(self.canvasItems[availableMoves[move][1][0]][availableMoves[move][1][1]], fill = 'red')
        self.canvas.itemconfig(self.canvasItems[availableMoves[move][2][0]][availableMoves[move][2][1]], fill = 'green')
        self.canvas.update()
        sleep(.25)
        
        self.canvas.itemconfig(self.canvasItems[availableMoves[move][1][0]][availableMoves[move][1][1]], fill = 'white')
        self.canvas.itemconfig(self.canvasItems[availableMoves[move][2][0]][availableMoves[move][2][1]], fill = 'black')
        
        # Then update the self.boardLayout to reflect the same changes.
        self.boardLayout = self.getStateAfterMove(self.boardLayout, availableMoves[move])
                
    def solveBoard(self):
        availableMoves = self.getAvailableMoves(self.boardLayout);
        if not len(availableMoves):
            print 'Game Over!'
            print 'Score: %i' % self.getScore(self.boardLayout)
            return
        
        self.makeMove()
        self.solveBoard()
        
    def resetBoard(self):
        self.removeAvailableMoveLines()
        self.boardLayout = self.originalBoardLayout
        
        # Remove and recreate the marbles.
        
    # Determines the final score of a board layout based on the number of
    # marbles remaining.
    def getScore(self, boardLayout):
        score = 0
        for column in boardLayout:
            for j in column:
                if j == 1:
                    score += 1
                    
        return score

    def __init__(self, boardLayout=[], master=None):
        self.boardLayout = boardLayout
        self.originalBoardLayout = boardLayout
        
        # verify the boardLayout first.
        if not self.verifyGameboard(self.boardLayout):
            return
                
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
        self.availableMoveLines = []
        