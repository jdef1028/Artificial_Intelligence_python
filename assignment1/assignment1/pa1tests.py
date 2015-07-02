# Programming Assignment 1 Tests
# This file includes a set of tests to make sure that your code behaves as
#    expected. These tests are not at all intended to be exhaustive. You
#    should design more tests for your code in addition to these. 

print "\nProblem 1: \n"
        
print "twoToTheN test case #1: " + str(twoToTheN(3) == 8)
print "twoToTheN test case #2: " + str(twoToTheN(0) == 1)
print "twoToTheN test case #3: " + str(twoToTheN(10) == 1024)
print "twoToTheN test case #4: " + str(twoToTheN(5) == 32)
    
print "\nProblem 2: \n"

x = [5,1,-2,3,1]
y = [5,1,2,3,1,4]
z = [1.5,2.5,3.5,4.5]
print "mean test case #1: " + str(mean(x) == float(8)/float(5))
print "mean test case #2: " + str(mean(y) == float(16)/float(6))
print "mean test case #3: " + str(mean(z) == 3)
print "median test case #1: " + str(median(x) == 1)
print "median test case #2: " + str(median(y) == 2.5)
print "median test case #3: " + str(median(z) == 3)

print "\nProblem 3: \n"

myTree = [4, [1 ,[7,[23],[24]]],[2],[3,[4],[5,[6]]],[19]]
print "bfs test case #1: " + str(bfs(myTree, 10) == False)
print "bfs test case #2: " + str(bfs(myTree, 7) == True)
print "dfs test case #1: " + str(dfs(myTree, 1) == True)
print "dfs test case #2: " + str(dfs(myTree, 7) == True)

print "\nProblem 4: \n"
            
myB = TTTBoard()
print myB

myB.makeMove("X", 5)
myB.makeMove("O", 6)
myB.makeMove("X", 1)
myB.makeMove("O", 0)
print myB.gameOver()
myB.makeMove("X", 4)
myB.makeMove("O", 3)
print myB.gameOver()
print myB.makeMove("X", 3)
print myB.makeMove("X", 2)

print myB

print "tic tac toe test case #1: " + str(myB.hasWon("X") == False)
print "tic tac toe test case #2: " + str(myB.hasWon("O") == True)
