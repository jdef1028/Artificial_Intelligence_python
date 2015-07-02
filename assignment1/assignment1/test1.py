__author__ = 'xiaolin'


def dfs(tree, elem):
	flag = False
	root = tree.pop(0)
	print root
	if root == elem:
		return True
	for child in tree:
		flag = dfs(child, elem)
	return False


dfs([1, [2, [3]], [4]], 4)