#!/usr/bin/env python
import struct, string, math, copy


class SudokuBoard:
	"""This will be the sudoku board game object your player will manipulate."""

	def __init__(self, size, board):
		"""the constructor for the SudokuBoard"""
		self.BoardSize = size  # the size of the board
		self.CurrentGameBoard = board  # the current state of the game board

	def set_value(self, row, col, value):
		"""This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

		# add the value to the appropriate position on the board
		self.CurrentGameBoard[row][col] = value
		#return a new board of the same size with the value added
		return SudokuBoard(self.BoardSize, self.CurrentGameBoard)


	def print_board(self):
		"""Prints the current game board. Leaves unassigned spots blank."""
		div = int(math.sqrt(self.BoardSize))
		dash = ""
		space = ""
		line = "+"
		sep = "|"
		for i in range(div):
			dash += "----"
			space += "    "
		for i in range(div):
			line += dash + "+"
			sep += space + "|"
		for i in range(-1, self.BoardSize):
			if i != -1:
				print "|",
				for j in range(self.BoardSize):
					if self.CurrentGameBoard[i][j] > 9:
						print self.CurrentGameBoard[i][j],
					elif self.CurrentGameBoard[i][j] > 0:
						print "", self.CurrentGameBoard[i][j],
					else:
						print "  ",
					if (j + 1 != self.BoardSize):
						if ((j + 1) // div != j / div):
							print "|",
						else:
							print "",
					else:
						print "|"
			if ((i + 1) // div != i / div):
				print line
			else:
				print sep


def parse_file(filename):
	"""Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

	f = open(filename, 'r')
	BoardSize = int(f.readline())
	NumVals = int(f.readline())

	# initialize a blank board
	board = [[0 for i in range(BoardSize)] for j in range(BoardSize)]

	#populate the board with initial values
	for i in range(NumVals):
		line = f.readline()
		chars = line.split()
		row = int(chars[0])
		col = int(chars[1])
		val = int(chars[2])
		board[row - 1][col - 1] = val

	return board


def is_complete(sudoku_board):
	"""Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
	BoardArray = sudoku_board.CurrentGameBoard
	size = len(BoardArray)
	subsquare = int(math.sqrt(size))

	# check each cell on the board for a 0, or if the value of the cell
	#is present elsewhere within the same row, column, or square
	for row in range(size):
		for col in range(size):
			if BoardArray[row][col] == 0:
				return False
			for i in range(size):
				if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
					return False
				if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
					return False
			#determine which square the cell is in
			SquareRow = row // subsquare
			SquareCol = col // subsquare
			for i in range(subsquare):
				for j in range(subsquare):
					if ((BoardArray[SquareRow * subsquare + i][SquareCol * subsquare + j]
						     == BoardArray[row][col])
					    and (SquareRow * subsquare + i != row)
					    and (SquareCol * subsquare + j != col)):
						return False
	return True

def does_complete(BoardArray):
	"""
	Test whether the given board is complete
	:param BoardArray: 2 dimensional array of board
	:return: True --> complete; False --> not yet
	"""

	size = len(BoardArray)
	subsquare = int(math.sqrt(size))

	# check each cell on the board for a 0, or if the value of the cell
	#is present elsewhere within the same row, column, or square
	for row in range(size):
		for col in range(size):
			if isinstance(BoardArray[row][col], list):
				return False
			for i in range(size):
				if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
					return False
				if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
					return False
			#determine which square the cell is in
			SquareRow = row // subsquare
			SquareCol = col // subsquare
			for i in range(subsquare):
				for j in range(subsquare):
					if ((BoardArray[SquareRow * subsquare + i][SquareCol * subsquare + j]
						     == BoardArray[row][col])
					    and (SquareRow * subsquare + i != row)
					    and (SquareCol * subsquare + j != col)):
						return False
	return True
def init_board(file_name):
	"""Creates a SudokuBoard object initialized with values from a text file"""
	board = parse_file(file_name)
	return SudokuBoard(len(board), board)


def solve(initial_board, forward_checking=False, MRV=False, MCV=False, LCV=False):
	open = []
	BoardArray1 = initial_board.CurrentGameBoard
	BoardArray = init_domain(BoardArray1)
	size = len(BoardArray)
	open.append(BoardArray)
	count = 0
	while len(open) > 0:
		print count
		count += 1
		cur = open.pop()
		if does_complete(cur):
			initial_board.CurrentGameBoard = cur
			return initial_board
		else:
			#print "cur is:", cur
			[i, j] = next_legal_update(cur)
			print i,j
			if len(BoardArray[i][j]) != 0:
				for m in BoardArray[i][j]:
					if elm_consistency(cur, i, j, m):
						cur[i][j] = m
						if forward_checking:
							cur1 = forward_update(cur, i, j, m)
							if forward_test(cur1):
								open.append(copy.deepcopy(cur1))
						else:
							open.append(copy.deepcopy(cur))
	print "haha"
	return initial_board


def forward_update(board1, i, j, m):
	board = copy.deepcopy(board1)
	size = len(board)
	for col in range(size):
		if isinstance(board[i][col], list):
			if m in board[i][col]:
				board[i][col].remove(m)
	for raw in range(size):
		if isinstance(board[raw][j], list):
			if m in board[raw][j]:
				board[raw][j].remove(m)
	b_size = int(size**0.5)
	b_x = int(i // b_size)
	b_y = int(j // b_size)
	for raw in range(b_x*b_size, b_size*(b_x+1)):
		for col in range(b_y*b_size, b_size*(b_y+1)):
			if isinstance(board[raw][col], list):
				if m in board[raw][col]:
					board[raw][col].remove(m)
	return board

def forward_test(board):
	size = len(board)
	for raw in range(size):
		for col in range(size):
			if isinstance(board[raw][col],list):
				if len(board[raw][col]) == 0:
					return False
	return True



def init_domain(BoardArray):
	size = len(BoardArray)
	for i in range(size):
		for j in range(size):
			if BoardArray[i][j] == 0:
				BoardArray[i][j] = range(1, 10)
	for i in range(size):
		for j in range(size):
			if isinstance(BoardArray[i][j], int):
				BoardArray = forward_update(BoardArray, i, j, BoardArray[i][j])
	return BoardArray

def next_legal_update(BoardArray):
	size = len(BoardArray)
	for i in range(size):
		for j in range(size):
			if isinstance(BoardArray[i][j], list):
				return [i, j]

def elm_consistency(BoardArray,i,j,m):
	"""
	Check the consistency of the added element
	:param BoardArray: the board
	:param i: raw number
	:param j: col number
	:param m: value plugged in
	:return: True --> consistent, False --> not consistent
	"""
	size = int(len(BoardArray))
	for col in range(size):
		# examine the column
		if BoardArray[i][col] == m and col != j:
			return False
	for raw in range(size):
		# examine the raw
		if BoardArray[raw][j] == m and raw != i:
			return False
	#print size**0.5
	block_raw = int(i // (size**0.5))
	block_col = int(j // (size**0.5))
	#print block_raw
	#print block_col
	for raw in range(int(size**0.5)*block_raw, int(size**0.5)*(block_raw+1)):
		for col in range(int(size**0.5)*block_col, int(size**0.5)*(block_col+1)):
			if BoardArray[raw][col] == m and raw != i and col != j:
				return False
	return True
