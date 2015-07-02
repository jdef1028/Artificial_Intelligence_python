__author__ = 'xiaolin'
execfile("xlo365.py")
sb = init_board("input_puzzles/easy/9_9.sudoku")
sb.print_board()

fb = solve(sb, False, False, False, False)
fb.print_board()
