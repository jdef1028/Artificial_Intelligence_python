__author__ = 'xiaolin'
execfile("SudokuStarter.py")
sb = init_board("input_puzzles/easy/9_9.sudoku")
sb.print_board()

fb = solve(sb, False, False, False, False)
fb.print_board()
