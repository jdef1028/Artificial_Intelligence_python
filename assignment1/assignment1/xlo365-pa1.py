# name: Xiaolin Li
# netID: xlo365
def twoToTheN(n):
	"""
	Calculate the value of 2 to the n power
	:param n: the power of the exponentiation
	:return: the result of 2 to the n power
	"""
	if n == 0:
		return 1
	elif n % 2 == 0:  # if n is even, separate into 2 sets
		return twoToTheN(n / 2) ** 2
	else:  # if n is odd, leave one of the 2 out and then separate into 2 sets
		return 2 * twoToTheN((n - 1) / 2) ** 2


def mean(L):
	"""
	Calculate the mean of a list
	:param L: The list of number
	:return: The mean value
	"""
	s = 0
	# compute the sum of the list
	for i in L:
		s += i
	# Mean --> divide the sum by the number of elements in the list
	if s % len(L) == 0:
		return s / len(L)
	else:
		return float(s) / len(L)


def median(L):
	"""
	Calculate the median of a list
	:param L:
	:return:
	"""
	# record the length of the list. It will be used as the criteria in splitting cases in the following steps
	n = len(L)
	# sort the list in the increasing manner
	L.sort()
	# case 1: odd elements in the list, pick the middle one
	if n % 2 == 1:
		return L[(n - 1) / 2]
	# case 2: even elements in the list, take the average of the middle two.
	else:
		return 0.5 * (L[n / 2] + L[(n - 2) / 2])


def dfs(tree, elem):
	"""
	Depth First Searching Algorithm implementation
	:param tree: list containing the tree structure
	:param elem: the target element value
	:return: True: The element exists in the tree
			False: The element does not exist in the tree
	"""
	# initialize a flag to indicate whether the element exists in the tree
	flag = False
	# print the root element
	print tree[0]
	# judge whether the root element is the one to be found
	if tree[0] == elem:
		return True

	for i in range(len(tree)):
		if i != 0:
			flag |= dfs(tree[i], elem)
		if flag:
			break
	return flag


def bfs(tree, elem):
	"""
	Breath First Searching Algorithm implementation
	:param tree: list containing the tree structure
	:param elem: the target element value
	:return: True: The element exists in the tree
			False: The element does not exist in the tree
	"""

	def treecopy(tree, tree1):
		# implement deep copy of the tree. Then we will only 
		for j in tree:
			# if the element is not a sub-tree, then add to list
			if type([]) != type(j):
				tree1.append(j)
			else:  # else dig into the next level of depth
				tree1.append([])
				treecopy(j, tree1[-1])

	tree1 = []
	treecopy(tree, tree1)
	flag = False
	print tree1[0]
	if tree1[0] == elem:  # examine the root node
		return True
	tree1.pop(0)
	while len(tree1) != 0:
		print tree1[0][0]
		if tree1[0][0] == elem:  # examine the current node
			return True
		# if the target is found, no more searching then

		tree1[0].pop(0)
		if len(tree1[0]) == 0:
			tree1.pop(0)  # remove the examined node
		else:
			for i in tree1[0]:
				tree1.append(i)  # add the removed node's children (could be tree or nodes) to the end of the queue
			tree1.pop(0)  # delete the children
	return flag


class TTTBoard:
	"""
	Tic Tac Toe Game implementation
	"""

	def __init__(self):
		"""
		Initialize the game board
		:return: print a new board on the screen
		"""
		self.board = ['*'] * 9  # use 9 different chars to represent the state
		return

	def __str__(self):
		"""
		define the display style
		:return: display style
		"""
		self.display = ''
		for i in range(len(self.board)):
			if (i + 1) % 3 != 0:
				self.display += self.board[i] + ' '
			elif (i + 1) % 3 != 3:
				self.display += self.board[i] + '\n'
		return self.display

	def makeMove(self, player, position):
		"""
		either of the players makes a move here
		:param player: "X" or "O" represents the players
		:param position: the position that "X" or "O" will be placed
		:return: if this move is valid
		"""
		if player == 'X' or player == 'O':
			if '*' not in self.board:
				return False
			if self.board[position] == '*':
				self.board[position] = player
				return True
			else:
				return False

	def hasWon(self, player):
		"""
		Examine if the player win the game
		:param player: "X" or "O" representation of the players
		:return: Whether this player has won or not
		"""
		pos = []
		# extract all the square that has been occupied by this player
		for i in range(len(self.board)):
			if self.board[i] == player:
				pos.append(i)
		# enumerate all the winning states
		wins = [[0, 1, 2],
		        [3, 4, 5],
		        [6, 7, 8],
		        [0, 3, 6],
		        [1, 4, 7],
		        [2, 5, 8],
		        [0, 4, 8],
		        [2, 4, 6]]
		for i in wins:
			count = 0
			for j in i:
				if j in pos:
					count += 1
			if count == 3:
				# count is 3 means that it meets the winning criteria
				return True
		return False

	def gameOver(self):
		"""
		Examnie if the game is over (either of the players won or the board is full)
		:return: True: Game is over. False: it is not over
		"""
		if self.hasWon('X') or self.hasWon('O') or ('*' not in self.board):
			return True
		else:
			return False

	def clear(self):
		"""
		by calling this function, the board will be cleared
		:return: a cleared board
		"""
		self.__init__()
		return

