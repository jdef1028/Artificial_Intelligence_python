# Name: Xiaolin Li & Zijiang Ynag
# NetID: xlo365, zyz293

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
	"""
	solving CSP problem of sudoku puzzle
	:param initial_board: Board
	:param forward_checking: use forward_checking or not
	:param MRV: use MRV or not
	:param MCV: use MCV or not
	:param LCV: use LCV or not
	:return: the solution to the board
	"""
	#create a stack named open
	open = []
	BoardArray1 = initial_board.CurrentGameBoard
	BoardArray = init_domain(BoardArray1)
	size = len(BoardArray)
	open.append(BoardArray)
	count = 0
	while len(open) > 0:
		#extract the last component in the stack to study the possible steps
		cur = open.pop()
		#print count
		if does_complete(cur):
			#examine if it is the solutino
			initial_board.CurrentGameBoard = cur
			#print count
			return initial_board
		else:
			#options cases
			#determine which variable is the next element to assign
			if MRV:
				[i, j] = MRV_next(cur)
			elif MCV:
				[i, j] = MCV_next(cur)
			else:
				[i, j] = next_legal_update(cur)
			#print i, j
			if len(BoardArray[i][j]) != 0:
				for m in value_domain(BoardArray, i, j, LCV):
					# if consistency, then assign
					count += 1
					if elm_consistency(cur, i, j, m):
						cur[i][j] = m
						if forward_checking:
							# constraints propagation if forward_checking is selected
							cur1 = forward_update(cur, i, j, m)
							if forward_test(cur1):
								#test if [] occurs on the board
								open.append(copy.deepcopy(cur1))
						else:
							open.append(copy.deepcopy(cur))
	print "Failure"
	return initial_board


def value_domain(BoardArray, i, j, LCV):
	"""
	:param BoardArray: board
	:param i: the studied position -- x component
	:param j: the studied position -- y component
	:param LCV: LCV option --> determine if we need to sort the available choices by their constraints
	:return: the optimal sequence of available values
	"""
	if not LCV:
		return BoardArray[i][j]
	else:
		size = len(BoardArray)
		b_size = int(size**0.5)
		candidate = {}
		for cd in BoardArray[i][j]:
			# reset the frequency counter
			counter = 0
			for col in range(size):
				#scan the raw
				if col != j and isinstance(BoardArray[i][col], list):
					if cd in BoardArray[i][col]:
						counter += 1
			for raw in range(size):
				#scan the column
				if raw != i and isinstance(BoardArray[raw][j], list):
					if cd in BoardArray[raw][j]:
						counter += 1
			bx = int(i // b_size)
			by = int(j // b_size)
			#scen the quadrant
			for raw in range(bx*b_size, (bx+1)*b_size):
				for col in range(by*b_size, (by+1)*b_size):
					if raw != i and col != j:
						if isinstance(BoardArray[raw][col], list):
							if cd in BoardArray[raw][col]:
								counter += 1
			candidate[cd] = counter
		# so far, keys of candidate is the available choice of values,
		# values are nums of constraints associated
		domain = []
		for key, value in sorted(candidate.iteritems(), key=lambda (k, v):(v, k)):
			domain.append(key)
		return domain



def forward_update(board1, i, j, m):
	# constrain propagation
	board = copy.deepcopy(board1)
	size = len(board)
	for col in range(size):
		#raw
		if isinstance(board[i][col], list):
			if m in board[i][col]:
				board[i][col].remove(m)
	for raw in range(size):
		#column
		if isinstance(board[raw][j], list):
			if m in board[raw][j]:
				board[raw][j].remove(m)
	b_size = int(size ** 0.5)
	b_x = int(i // b_size)
	b_y = int(j // b_size)
	# quadrant
	for raw in range(b_x * b_size, b_size * (b_x + 1)):
		for col in range(b_y * b_size, b_size * (b_y + 1)):
			if isinstance(board[raw][col], list):
				if m in board[raw][col]:
					board[raw][col].remove(m)
	# return the propagated board
	return board


def forward_test(board):
	"""
	:param board: board info
	:return: False: [] exists on the board, no choices for the next steps, else True
	"""
	size = len(board)
	for raw in range(size):
		for col in range(size):
			if isinstance(board[raw][col], list):
				if len(board[raw][col]) == 0:
					return False
	return True


def init_domain(BoardArray):
	"""
	initialize the board: 1) replace 0 with [1...size] 2) eliminate impossible choices
	:param BoardArray:  board
	:return: update board
	"""
	size = len(BoardArray)
	for i in range(size):
		for j in range(size):
			if BoardArray[i][j] == 0:
				BoardArray[i][j] = range(1, size + 1)
	for i in range(size):
		for j in range(size):
			if isinstance(BoardArray[i][j], int):
				BoardArray = forward_update(BoardArray, i, j, BoardArray[i][j])
	return BoardArray


def next_legal_update(BoardArray):
	"""
	find the next list(element to assign)
	:param BoardArray: board
	:return: i -- x component; j -- y component
	"""
	size = len(BoardArray)
	for i in range(size):
		for j in range(size):
			if isinstance(BoardArray[i][j], list):
				return [i, j]


def MRV_next(BoardArray):
	""" find the next element to assign using MRV
	:param BoardArray: board
	:return: position x,y
	"""
	size = len(BoardArray)
	xlabel = -1
	ylabel = -1
	L = size + 1
	for i in range(size):
		for j in range(size):
			if isinstance(BoardArray[i][j], list):
				if len(BoardArray[i][j]) < L:
					L = len(BoardArray[i][j])
					xlabel = i
					ylabel = j

	return xlabel, ylabel


def MCV_next(BoardArray):
	""" find the next element to assign using MCV
	:param BoardArray:  board
	:return: x component & y component
	"""
	size = len(BoardArray)
	b_s = int(size ** 0.5)
	xlabel = -1
	ylabel = -1
	current_most = -1
	for i in range(size):
		for j in range(size):
			if isinstance(BoardArray[i][j], list):
				counter = 0
				#scan the same raw as BoardArray[i][j]
				for col in range(size):
					if col != j and isinstance(BoardArray[i][col], list):
						counter += 1
				#scen the same column as BoardArray[i][j]
				for raw in range(size):
					if raw != i and isinstance(BoardArray[raw][j], list):
						counter += 1
				#scan the local quadrant
				bx = int(i // b_s)
				by = (j // b_s)
				for raw in range(b_s * bx, b_s * (bx + 1)):
					for col in range(b_s * by, b_s * (by + 1)):
						if raw != i and col != j:
							if isinstance(BoardArray[raw][col], list):
								counter += 1
				if counter > current_most:
					current_most = counter
					xlabel = i
					ylabel = j
	return xlabel, ylabel


def elm_consistency(BoardArray, i, j, m):
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
	block_raw = int(i // (size ** 0.5))
	block_col = int(j // (size ** 0.5))
	#print block_raw
	#print block_col
	for raw in range(int(size ** 0.5) * block_raw, int(size ** 0.5) * (block_raw + 1)):
		for col in range(int(size ** 0.5) * block_col, int(size ** 0.5) * (block_col + 1)):
			if BoardArray[raw][col] == m and raw != i and col != j:
				return False
	return True
