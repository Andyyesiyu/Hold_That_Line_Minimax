from random import choice
import collections
class Solver:
    def __init__(self,m,n):
        self.board = [['' for _ in range(n)] for _ in range(m)]  # "." -> Empty, "#" -> Drew
        '''
        # self.board = [
        #     ['2','','1','',''],
        #     ['','','12','','']
        # ]
        # self.board = [
        #     ['0','','',''],
        #     ['','0','',''],
        #     ['','','0',''],
        #     ['','','','0']
        # ]
        '''
        self.lines = collections.defaultdict(list)  # {0:[(0,0),(3,3)],}
        self.ends = [] # Two end points of the game
        # self.ends = [(0,0),(3,3)]  # [(0,0),(3,3)]
        self.round = 0 # record the round number

    def printBoard(self):
        # print the whole board in a fancy way 
        for i in self.board:
            for j in i:
                if j=='':
                    print('N',end='\t')
                    # writetoFile('test','N','\t')
                else:
                    print(j,end='\t')
                    # writetoFile('test',j,'\t')
            print('\v')
            # writetoFile('test','\v')
    

    def fillBoard(self, from_, to_):
        # fill the board from from_ to to_ point. 
        # And, return the previous status of the game (important in minimax and dfs)

        # Always from from_ to to_, if not in the order, recursively call this function and reverse the order
        if to_ in self.ends:
            return self.fillBoard(to_,from_)

        self.round += 1

        # Copy status before handling fill board
        prevLines = self.lines.copy() 
        prevEnds = self.ends.copy()

        # Update game status variables
        self.lines[self.round] = [from_, to_]
        if len(self.ends) == 0:
            self.ends.append(from_)
            self.ends.append(to_)
        else:
            self.ends.pop(self.ends.index(from_))
            self.ends.append(to_)
        
        # fill line in the board and return this line
        lineToBeDelete = self.fillLine(from_, to_, self.round) 
        return prevLines,prevEnds,lineToBeDelete
        # for i in range(len(to_[0]-from_[0])):
            
    def deleteBoard(self, prevLines, prevEnds, fillpath):
        for deletei,deletej in fillpath:
            # self.board[deletei][deletej] = self.board[deletei][deletej][:-1*len(str(self.round))]
            self.board[deletei][deletej] = self.board[deletei][deletej][:-1]
        self.lines = prevLines 
        self.ends = prevEnds 
        self.round -= 1

    def isCross(self, line1, line2):
        # 判断是否相交，线用坐标list表示
        # return True if intersect, False if colinearity and not intersect
        # line -> [(0,0),(3,3)]
        # whether A,B,C in counter clock wise order
        l1 = sorted(line1)
        l2 = sorted(line2)
        def isinLine(A,B,C,D):
            if B[0]!=A[0]:
                k = (B[1]-A[1])/(B[0]-A[0])
                b = A[1] - k*A[0]
                if (C[0]*k + b == C[1] and min(A[0],B[0])<=C[0]<=max(A[0],B[0])) or (D[0]*k + b == D[1] and min(A[0],B[0])<=D[0]<=max(A[0],B[0])):
                    return True
                else:
                    return False
            else:
                return (C[0] == A[0] and min(A[1],B[1])<=C[1]<=max(A[1],B[1])) or (D[0] == A[0] and min(A[1],B[1])<=D[1]<=max(A[1],B[1]))
        def ccw(A,B,C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

        # Return true if line segments AB and CD intersect
        def intersect(A,B,C,D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
        
        return intersect(l1[0],l1[1],l2[0],l2[1]) or isinLine(l1[0],l1[1],l2[0],l2[1])
    
    def fillLine(self, first, second, role):
        # first -> (0,0); second -> (2,2); role -> 1,2,3
        # role = the round number
        # Fill the line in the board and return this line

        fillPath = []
        if first[0] == second[0]: # handle situations that k does not exists
            # small/big: the row number when col equals 
            small = first[1] if first[1] < second[1] else second[1]
            big = second[1] if first[1] < second[1] else first[1]
            for i in range(small, big+1):
                # fill the board, the string represents the round number 
                self.board[first[0]][i] += str(role)

                fillPath += [(first[0], i)]
        elif first[1] == second[1]: # same as above
            small = first[0] if first[0] < second[0] else second[0]
            big = second[0] if first[0] < second[0] else first[0]
            for i in range(small, big+1):
                self.board[i][first[1]] += str(role)
                fillPath += [(i,first[1])]
        else:
            # use linear algebra to fill the line
            k = (second[1] - first[1]) / (second[0] - first[0])
            b = first[1] - k * first[0]
            small = first[0] if first[0] < second[0] else second[0]
            big = second[0] if first[0] < second[0] else first[0]
            for x in range(small, big+1):
                y = k*x + b
                if int(y) == y:
                    self.board[int(x)][int(y)] += str(role)
                    fillPath += [(int(x),int(y))]
        # fillPath: all the coordinates of this path
        return fillPath


    def findValidPathFrom(self, end):
        res = []
        # Traverse all the cells in the board and check whether feasible 
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == '' :
                    ifvalid = True
                    for hist in self.lines:
                        currLine = self.lines[hist]
                        # print(end, (i,j),currLine)
                        if end in currLine:
                            continue
                        if self.isCross([end,(i,j)], currLine):
                            ifvalid = False
                        
                    if ifvalid:
                        res.append((i,j))
        return res

    def findAllValidPath(self):
        res1 = self.findValidPathFrom(self.ends[0]) # find valid from one ends
        res2 = self.findValidPathFrom(self.ends[1]) # find from anther ends
        res = []
        res += [(self.ends[0], i) for i in res1]
        res += [(self.ends[1], i) for i in res2]
        return [ele for ele in res if ele[1] not in self.ends]
        

    def evaluate(self, who):
        # COM = computer and PER = person
        # if in computer round, there is no lines to draw, 
        # which means computer win because the last line was drown by the person
        if who == 'COM': 
            res = 1
        elif who == 'PER':
            res = -1
        else:
            res = 0
        return res

    def ifFinal(self):
        # final means no line to draw
        if len(set(self.findValidPathFrom(self.ends[0]) + self.findValidPathFrom(self.ends[1]))) > 0:
            return False
        return True

    # depth: dfs depth
    # player: 'COM' or 'PER'
    # step：self.round
    def minimax(self,depth,player,step):
        """ Minimax Main Calculation
        
        Args:
            depth (int): depth of current calculation, for controling the calculation time
            player (str): 'COM' or 'PER', COM = computer, PER = person, which player plays now, then we can choose MIN or MAX
            step (int): current round(self.round) of the game
        
        Returns:
            [(int,int,int)]: (next_step x , next_step y, score: expected score in Minimax calculation )
        """
        inf = float('inf') 
        if player == 'COM': # if it is the compute's round, we should maxmize the score
            best = [-1, -1, -inf] # -1 to initialize and represent there is no possible step now
        else:  # if it is the person's round, we should minimize the score
            best = [-1, -1, inf]
        bestList = [] # all the best step we could have, because in this game, the best step could be multiple
        if depth == 0 or self.ifFinal(): # if this is the final step, or we reach the recursion bottom
            score = self.evaluate(player) # evaluate the final score
            return [-1, -1, score] # return final score, which is the base case of dfs
        validPath = self.findAllValidPath() # find all possible steps
        for start, end in validPath: # traverse all possible steps
            prevLines, prevEnds, fillpath = self.fillBoard(start, end) # fill the board and store previous status variables
            nextPlayer = 'COM' if player == 'PER' else 'PER' # switch role
            score = self.minimax(depth-1,nextPlayer,step+1) # recursively call current function 
            
            # use previous status variables to delete the path and try anther possible steps
            self.deleteBoard(prevLines, prevEnds, fillpath) 

            # fill the coordinate position
            score[0],score[1] = start,end


            if player == 'COM': # maxmize the score and store the best to bestList
                if score[2] > best[2]:
                    best = score
                    bestList = []
                if score[2] == best[2]:
                    bestList.append(score)
            else: # minimize the score store them
                if score[2] < best[2]:
                    best = score
                if score[2] == best[2]:
                    bestList.append(score)
        
        # random choose from all the best one
        return choice(bestList)

    def computeAndPlay(self):
        nextStep = self.minimax(3,'COM',self.round) # minimax enter point, use minimax calculate
        print('AI played at' + str(nextStep[0]) + ',' + str(nextStep[1]))
        # writetoFile('test','AI played at' + str(nextStep[0]) + ',' + str(nextStep[1])) # write profile
        self.fillBoard(nextStep[0],nextStep[1])

    #get the input from keyboard. If it is a valid input
    def getInput(self):
        line = input("Please input the coordinates:(Use 4 numbers to represent your line, split with commas)")
        line = line.replace('(','').replace(')','')
        while not self.isValidInput(line):
            line = input("Please input the coordinates:(Use 4 numbers to represent your line, split with commas)")
            
        return self.processInput(line)


    #if the input is valid, process it from str to list of coordinates
    def processInput(self,line):
        data = line.split(',')
        data = [int(x) for x in data]
        coor1 = (data[0], data[1])
        coor2 = (data[2], data[3])
        new_line = [coor1, coor2]
        # writetoFile('test','Person played at' + str(coor1) + ',' + str(coor2))
        self.fillBoard(coor1, coor2)
        return new_line

    #check whether it is valid
    def isValidInput(self,line):

        data = line.split(',')
        data = [int(x) for x in data]
        if len(data) != 4:
            return False
        coor1 = (data[0], data[1])
        coor2 = (data[2], data[3])
        if any(coor1+coor2)<0 or any(coor1+coor2)>=max(len(self.board),len(self.board[0])):
            return False
        if self.round == 0:
            return True
         #check whether the input contains the valid end
        checkends = [coor1, coor2]
        if not (coor1 in self.ends or coor2 in self.ends):
            return False
        end = coor1 if coor1 in self.ends else coor2
        another = coor2 if coor1 in self.ends else coor1
        all_possible_ends = self.findValidPathFrom(end)
        return another in all_possible_ends



def writetoFile(filename,content,end='\n'):
    # write to file automatically
    file = open('filename','a')
    file.write(content + end)
    file.close()

if __name__ == "__main__":
    solve = Solver(5,5)
    print(solve.isCross([(1,0),(2,0)],[(3,0),(4,0)]))
    # solve.fillLine((0,0),(2,1),'3
    print(solve.findValidPathFrom((0,2)))
    # get user input')
    # print(solve.mi

    # print(solve.findAllValidPath())
    # print(solve.minimax(3,'COM',3))

    # user input
    while True:
        # break
        solve.printBoard()
        print(solve.ends)
        print(solve.lines)
        try:
            print(solve.findAllValidPath())
        except:
            pass
        start, end = solve.getInput()

        if solve.ifFinal():
            print('computer win')
            # writetoFile('test','computer win')
            solve.printBoard()
            break
        solve.computeAndPlay()
        if solve.ifFinal():
            print('person win')
            # writetoFile('test','person win')
            solve.printBoard()
            break
    
