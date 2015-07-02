# File: xlo365.py
# Author(s) names AND netid's: Xiaolin Li (xlo365), Zijiang Yang (zyz293)
# Date: Apr. 20th, 2015
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm (done)
# You will also define the score function in the MancalaPlayer class (done)
# a subclass of the Player class. (done)



from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400


class Player:
	""" A basic AI (or human) player """
	HUMAN = 0
	RANDOM = 1
	MINIMAX = 2
	ABPRUNE = 3
	CUSTOM = 4

	def __init__(self, playerNum, playerType, ply=0):
		"""Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
		self.num = playerNum
		self.opp = 2 - playerNum + 1
		self.type = playerType
		self.ply = ply

	def __repr__(self):
		"""Returns a string representation of the Player."""
		return str(self.num)

	def minimaxMove(self, board, ply):
		""" Choose the best minimax move.  Returns (score, move) """
		move = -1
		score = -INFINITY
		turn = self
		for m in board.legalMoves(self):
			# for each legal move
			if ply == 0:
				# if we're at ply 0, we need to call our eval function & return
				return (self.score(board), m)
			if board.gameOver():
				return (-1, -1)  # Can't make a move, the game is over
			nb = deepcopy(board)
			# make a new board
			nb.makeMove(self, m)
			# try the move
			opp = Player(self.opp, self.type, self.ply)
			s = opp.minValue(nb, ply - 1, turn)
			#and see what the opponent would do next
			if s > score:
				#if the result is better than our best score so far, save that move,score
				move = m
				score = s
		# return the best score and move so far
		return score, move

	def maxValue(self, board, ply, turn):
		""" Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
		if board.gameOver():
			return turn.score(board)
		score = -INFINITY
		for m in board.legalMoves(self):
			if ply == 0:
				# print "turn.score(board) in max value is: " + str(turn.score(board))
				return turn.score(board)
			# make a new player to play the other side
			opponent = Player(self.opp, self.type, self.ply)
			# Copy the board so that we don't ruin it
			nextBoard = deepcopy(board)
			nextBoard.makeMove(self, m)
			s = opponent.minValue(nextBoard, ply - 1, turn)
			# print "s in maxValue is: " + str(s)
			if s > score:
				score = s
		return score

	def minValue(self, board, ply, turn):
		""" Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
		if board.gameOver():
			return turn.score(board)
		score = INFINITY
		for m in board.legalMoves(self):
			if ply == 0:
				# print "turn.score(board) in min Value is: " + str(turn.score(board))
				return turn.score(board)
			# make a new player to play the other side
			opponent = Player(self.opp, self.type, self.ply)
			# Copy the board so that we don't ruin it
			nextBoard = deepcopy(board)
			nextBoard.makeMove(self, m)
			s = opponent.maxValue(nextBoard, ply - 1, turn)
			# print "s in minValue is: " + str(s)
			if s < score:
				score = s
		return score


	# The default player defines a very simple score function
	# You will write the score function in the MancalaPlayer below
	# to improve on this function.
	def score(self, board):
		""" Returns the score for this player given the state of the board """
		if board.hasWon(self.num):
			return 100.0
		elif board.hasWon(self.opp):
			return 0.0
		else:
			return 50.0








		# You should not modify anything before this point.
		# The code you will add to this file appears below this line.

		# You will write this function (and any helpers you need)
		# You should write the function here in its simplest form:
		# 1. Use ply to determine when to stop (when ply == 0)
		# 2. Search the moves in the order they are returned from the board's
		# legalMoves function.
		# However, for your custom player, you may copy this function
		# and modify it so that it uses a different termination condition
		# and/or a different move search order.

	def alphaBetaMove(self, board, ply):
		""" Choose a move with alpha beta pruning.  Returns (score, move) """
		# returns the score adn the associated moved
		move = -1
		score = -INFINITY
		turn = self
		alpha = -INFINITY
		beta = INFINITY
		for m in board.legalMoves(self):
			# for each legal move
			if ply == 0:
				# if we're at ply 0, we need to call our eval function & return
				return (self.score(board), m)
			if board.gameOver():
				return (-1, -1)  # Can't make a move, the game is over
			nb = deepcopy(board)
			# make a new board
			nb.makeMove(self, m)
			#try the move
			opp = Player(self.opp, self.type, self.ply)
			s = opp.minValue1(nb, ply - 1, turn, alpha, beta)
			#and see what the opponent would do next
			if s > score:
				#if the result is better than our best score so far, save that move,score
				move = m
				score = s
		# return the best score and move so far
		return score, move

	def maxValue1(self, board, ply, turn, alpha, beta):
		""" Find the minimax value for the next move for this player
        at a given board configuation. Returns score. Take alpha and beta into consideration"""
		if board.gameOver():
			return turn.score(board)
		score = -INFINITY
		for m in board.legalMoves(self):
			if ply == 0:
				# print "turn.score(board) in max value is: " + str(turn.score(board))
				return turn.score(board)
			# make a new player to play the other side
			opponent = Player(self.opp, self.type, self.ply)
			# Copy the board so that we don't ruin it
			nextBoard = deepcopy(board)
			nextBoard.makeMove(self, m)
			s = opponent.minValue1(nextBoard, ply - 1, turn, alpha, beta)
			# print "s in maxValue is: " + str(s)
			if s > score:
				score = s
			if score >= beta:
				return score
			if score > alpha:
				alpha = score

		return score

	def minValue1(self, board, ply, turn, alpha, beta):
		""" Find the minimax value for the next move for this player
	            at a given board configuation. Returns score."""
		if board.gameOver():
			return turn.score(board)
		score = INFINITY
		for m in board.legalMoves(self):
			if ply == 0:
				# print "turn.score(board) in min Value is: " + str(turn.score(board))
				return turn.score(board)
			# make a new player to play the other side
			opponent = Player(self.opp, self.type, self.ply)
			# Copy the board so that we don't ruin it
			nextBoard = deepcopy(board)
			nextBoard.makeMove(self, m)
			s = opponent.maxValue1(nextBoard, ply - 1, turn, alpha, beta)
			# print "s in minValue is: " + str(s)
			if s < score:
				score = s
			if score <= alpha:
				return score
			if score < beta:
				beta = score
		return score


	def chooseMove(self, board):
		""" Returns the next move that this player wants to make """
		if self.type == self.HUMAN:
			move = input("Please enter your move:")
			while not board.legalMove(self, move):
				print move, "is not valid"
				move = input("Please enter your move")
			return move
		elif self.type == self.RANDOM:
			move = choice(board.legalMoves(self))
			print "chose move", move
			return move
		elif self.type == self.MINIMAX:
			val, move = self.minimaxMove(board, self.ply)
			print "chose move", move, " with value", val
			return move
		elif self.type == self.ABPRUNE:
			val, move = self.alphaBetaMove(board, self.ply)
			#print board
			print "chose move", move, " with value", val
			return move
		elif self.type == self.CUSTOM:
			# if get CUSTOM, start the CUSTOM function
			val, move = self.customMove(board, 7)
			return move
		else:
			print "Unknown player type"
			return -1

	def customMove(self, board, ply):
		#print ply
		#tic = time.time()
		"""define the custom move"""
		move = -1
		score = -INFINITY
		turn = self
		for m in board.legalMoves(self):
			if ply == 0:
				return (self.score(board), m)
			if board.gameOver():
				return (-1, 1)
			nb = deepcopy(board)
			nb.makeMove(self, m)
			opp = Player(self.opp, self.type, self.ply)
			s = opp.minCustom(nb, ply-1, turn)
			if s > score:
				move = m
				score = s
		#toc = time.time()
		#print tic - toc
		return score, move

	def minCustom(self, board, ply, turn):
		if board.gameOver():
			return turn.score(board)
		# initiate the accumulator
		score = 0
		acc = 0
		for m in board.legalMoves(self):
			if ply == 0:
				return turn.score(board)
			opponent = Player(self.opp, self.type, self.ply)
			nextBoard = deepcopy(board)
			nextBoard.makeMove(self, m)
			s = opponent.maxCustom(nextBoard, ply-1, turn)
			# counter to compute the number of legal moves
			acc += 1
			# sum on score
			score += s
		# assuming equal probability, calculate the expectation value
		score = score / acc
		return score

	def maxCustom(self, board, ply, turn):
		if board.gameOver():
			return turn.score(board)
		# initiate the accumulator "score"
		score = 0
		acc = 0
		for m in board.legalMoves(self):
			if ply == 0:
				return turn.score(board)
			opponent = Player(self.opp, self.type, self.ply)
			nextBoard = deepcopy(board)
			nextBoard.makeMove(self, m)
			s = opponent.minCustom(nextBoard, ply-1, turn)
			# counter to compute the number of legal moves
			acc += 1
			# sum on score
			score += s
		# assuming equal probability, calculate the expectation value
		score = score / acc
		return score


# Note, you should change the name of this player to be your netid
class xlo365(Player):
	""" Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """
	"""def customMove(self, board, ply):
		#define the custom move
		move = -1
		score = -INFINITY
		turn = self
		for m in board.legalMoves(self):
			if ply == 0:
				return (self.score(board), m)
			if board.gameOver():
				return (-1, 1)
			nb = deepcopy(board)
			nb.makeMove(self, m)
			opp = Player(self.opp, self.type, self.ply)
			s = opp.minCustom(nb, ply-1, turn)
			if s > score:
				move = m
				score = s
		return score, move

	def minCustom(self, board, ply, turn):
		print "min"
		if board.gameOver():
			return turn.score(board)
		score = 0
		acc = 0
		for m in board.legalMoves(self):
			if ply == 0:
				return turn.score(board)
			opponent = Player(self.opp, self.type, self.ply)
			nextBoard = deepcopy(board)
			nextBoard.makeMove(self, m)
			s = opponent.maxCustom(nextBoard, ply-1, turn)
			acc += 1
			score += s
		score /= float(acc)
		return score

	def maxCustom(self, board, ply, turn):
		if board.gameOver():
			return turn.score(board)
		score = 0
		acc = 0
		for m in board.legalMoves(self):
			if ply == 0:
				return turn.score(board)
			opponent = Player(self.opp, self.type, self.ply)
			nextBoard = deepcopy(board)
			nextBoard.makeMove(self, m)
			s = opponent.minCustom(nextBoard, ply-1, turn)
			acc += 1
			score += s
		score /= float(acc)
		return score"""

	def score(self, board):
		if board.hasWon(self.num):
			return 100
		elif board.hasWon(self.opp):
			return -100
		else:
			# copy the current board
			if self.num == 1:
				mycups = board.P1Cups[:]
				myscore = board.scoreCups[0]
				oppcups = board.P2Cups[:]
				oppscore = board.scoreCups[1]
			else:
				mycups = board.P2Cups[:]
				myscore = board.scoreCups[1]
				oppcups = board.P1Cups[:]
				oppscore = board.scoreCups[0]
			# discuss some special cases leading to win or lose
			if myscore > 24 and oppscore < 24:
				return 100
			if myscore < 24 and oppscore > 24:
				return -100
			if myscore == 24 and oppscore == 24:
				return 0
			mytoget = 25 - myscore
			opptoget = 25 - oppscore
			if myscore == 24: # when mancala = 24, add 1 to win
				for i in range(len(mycups)):
					if mycups[i] + i >= 6:
						return 100
			else:
				for i in range(len(mycups)): # capture to win
					if i + mycups[i] <= 5:
						if mycups[i] != 0 and mycups[i+mycups[i]] == 0:
							#if oppcups[5-i-mycups[i]] != 0:
								earn = 1 + oppcups[5-i-mycups[i]]
								if earn >= mytoget:
									return 100
					elif mycups[i] < 13 and mycups[i] >= 13 - i:
						uppos = mycups[i] - 13 + i
						if mycups[i] != 0 and mycups[uppos] == 0: #and oppcups[5-uppos] !=0:

							earn = 1 + oppcups[5-uppos]
							if earn >= mytoget:
								return 100
					elif mycups[i] == 13:
						earn = 2 + oppcups[5-i]
						if earn >= mytoget:
							return 100
			# score evaluation
			mycounter = 0
			oppcounter = 0
			for i in range(len(mycups)): # general
				if mycups[i] != 0: #my side eval
					if mycups[i] % 13 == 6 - i:
						mycounter += 5
					elif mycups[i] + i > 6:
						mycounter += mycups[i] / 13 + 1
					elif i + mycups[i] <= 5:
						if mycups[i+mycups[i]] == 0:
							#if oppcups[5-i-mycups[i]] != 0:
								mycounter += 1 + oppcups[5-i-mycups[i]]

					elif mycups[i] < 13 and mycups[i] >= 13 - i:
						uppos = mycups[i] - 13 + i
						if mycups[uppos] == 0: #and oppcups[5-uppos] != 0:
							mycounter += 1 + oppcups[5-uppos]
					elif mycups[i] == 13:
						mycounter += 2 + oppcups[5-i]

			for i in range(len(oppcups)):
				if oppcups[i] != 0: #opp side eval
					if oppcups[i] % 13 == 6 - i:
						oppcounter += 1
					elif i + oppcups[i] <= 5:
						if oppcups[i+oppcups[i]] == 0:
							#if mycups[5-i-oppcups[i]] != 0:
								oppcounter += 1 + mycups[5-i-oppcups[i]]

					elif oppcups[i] < 13 and oppcups[i] >= 13 - i:
						uppos = oppcups[i] - 13 + i
						if oppcups[uppos] == 0: #and mycups[5-uppos] != 0:
							oppcounter += 1 + mycups[5-uppos]
					elif oppcups[i] == 13:
						oppcounter += 2 + mycups[5-i]
			continu = 0 # deduce points if my move enable opp's free turn move
			for i in range(len(mycups)):
				newcups = oppcups[:]
				if mycups[i] + i > 6:

					if i + mycups[i] <= 12: # less than 1 lap
						opppos = i + mycups[i] - 7
						for j in range(opppos + 1):
							newcups[j] += 1
							if newcups[j] + j == 6:
								continu += 1
					elif i + mycups[i] > 19 and i + mycups[i] < 26: # more than or equal to 1 lap
						for j in range(len(newcups)):
							newcups[j] += 1
						opppos = i + (mycups[i] % 13) - 7

						for j in range(opppos + 1):
							newcups[j] += 1
							if newcups[j] + j == 6:
								continu += 1
					#return the final score based on the previous 3 aspects
			return 2*mycounter - oppcounter - continu









        
