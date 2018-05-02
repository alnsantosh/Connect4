
# coding: utf-8

# In[1]:

import time
import numpy as np
import random
from Board import Board
from RandomPlayer import RandomPlayer
from RLPlayer import RLPlayer
import RLModel
import math
from strategyPlayer import strategyPlayer
from keras.models import load_model

# In[12]:


class Game():
	def __init__(self, player1, player2, play=True):
		
		self.winner=None
		self.completed=False
		self.win_direction=None
		self.win_point=None
		self.p=[None,None]
		self.board=Board()
		player1.move=1
		player2.move=2
		self.p[0]=player1
		self.p[1]=player2


	def reset(self):
		self.winner=None
		self.completed=False
		self.win_direction=None
		self.win_point=None
		self.board=Board()
		
		
	
	def verticalCheck(self,r,c):
		win=False
		if 6-r>=4:
			win=True
			for i in range(4):
				if self.board.board[r][c]!=self.board.board[r+i][c]:
					win=False
					break
		if win:
			self.win_direction='v'
		return win
	
	def horizontalCheck(self,r,c):
		win=False
		if 7-c>=4:
			win=True
			for i in range(4):
				if self.board.board[r][c]!=self.board.board[r][c+i]:
					win=False
					break
		if win:
			self.win_direction='h'
		return win
	
	def positiveDiagonalCheck(self,r,c):
		win=False
		if 6-r>=4 and 7-c>=4:
			win=True
			for i in range(4):
				if self.board.board[r][c]!=self.board.board[r+i][c+i]:
					win=False
					break
		if win:
			self.win_direction='pD'
		return win
	
	def negativeDiagonalCheck(self,r,c):
		win=False
		if 6-r>=4 and 7-c<=4:
			win=True
			for i in range(4):
				if self.board.board[r][c]!=self.board.board[r+i][c-i]:
					win=False
					break
		if win:
			self.win_direction='nD'
		return win


	
	def findWinner(self):
		for r in range(6):
			for c in range(7):
				if self.board.board[r][c]!=0:
					win= self.verticalCheck(r,c) or self.horizontalCheck(r,c) or self.positiveDiagonalCheck(r,c) or self.negativeDiagonalCheck(r,c)
					if win:
						self.winner=self.board.board[r][c]
						self.completed=True
						self.win_point=(r,c)
						return
	
	def run(self,debug=False):
		move=0
		while not self.completed and not self.board.checkFilled():
			flatten_board=self.board.board.flatten()
			possible=self.board.nextPossibleMove()
			if len(self.board.nextPossibleMove())==0:
					print("draw")
					self.completed=1
			else:
				p=self.p[move].playMove(flatten_board,possible)
				if not self.board.checkValidMove(p):
					print("Invalid Move")
					print("Game ends")
					return
				self.board.makeMove(p,move+1)
				self.findWinner()
				if move:
					move=0
				else:
					move=1
				if debug:
					print(self.board.board)
					print("")
					print("")
					time.sleep(2)
		if debug:
			print(self.winner)
			print(self.board.board)
			print(self.win_direction)
			print(self.win_point)

	def learn_game(self,episodes=5000):
		# Iterate the game
		overall=0
		verwinplot=np.zeros((6,7))
		horwinplot=np.zeros((6,7))
		pdwinplot=np.zeros((6,7))
		ndwinplot=np.zeros((6,7))
		for e in range(episodes):

			if(e%200==0):
				x=0
				for i in range(200):
					b=Game(self.p[0],self.p[1])
					b.run()
					if b.winner==1:
						x=x+1
				print("Model won " ,x," games out of 200")
				overall=overall+x
				model.save('structured_NN.h5')  # creates a HDF5 file 'my_model.h5'

			self.reset()
			move=0
			while not self.completed:
				curr_move=self.board.board.flatten()
				if len(self.board.nextPossibleMove())==0:
					print("draw")
					self.completed=1
				else:
					c = self.p[move].playMove(curr_move,self.board.nextPossibleMove())
					if not self.board.checkValidMove(c):
						print("Invalid Move")
						print("Game ends")
						break
					curr_move=self.board.board.flatten()
				
					self.board.makeMove(c,move+1)
					if move==0:
						self.p[0].remember(curr_move,c)
				
					self.findWinner()
					if self.completed:
						if self.winner==1:
							if self.win_direction=='v':
								verwinplot[self.win_point[0]][self.win_point[1]]+=1
								self.p[0].remember(curr_move,c)
								overwinpenalty=1-math.sqrt((verwinplot[self.win_point[0]][self.win_point[1]]/e))
								self.p[0].replay(1*overwinpenalty )

							if self.win_direction=='h':
								horwinplot[self.win_point[0]][self.win_point[1]]+=1
								self.p[0].remember(curr_move,c)
								self.p[0].replay(1* (1-(horwinplot[self.win_point[0]][self.win_point[1]]/e)))

							if self.win_direction=='nD':
								ndwinplot[self.win_point[0]][self.win_point[1]]+=1
								self.p[0].remember(curr_move,c)
								self.p[0].replay(1* (1-(ndwinplot[self.win_point[0]][self.win_point[1]]/e)))

							if self.win_direction=='pD':
								pdwinplot[self.win_point[0]][self.win_point[1]]+=1
								self.p[0].remember(curr_move,c)
								self.p[0].replay(1* (1-(pdwinplot[self.win_point[0]][self.win_point[1]]/e)))
						else:
							self.p[0].remember(curr_move,-1)
							self.p[0].replay(-1)
							
					
				if self.completed:
					break
				else:
					if move:
						move=0
					else:
						move=1
			

		print(verwinplot)
		print(horwinplot)
		print(pdwinplot)
		print(ndwinplot)
		print(overall)
	


# In[14]:

# a=Game(RandomPlayer(1),RandomPlayer(2))
# a.run()

model=RLModel.get_model()
a=Game(RLPlayer(168,42,model),strategyPlayer(2))
a.learn_game()
#a.run()

