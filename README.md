## Review The Rules of the Game
This should be a familiar game to you, I would just reintroduce the rules briefly. Each players can connect as many dots as they wish in a straight line, and they can only start from the end of the current game. The whole project had done by Mina, Han and me. Thanks for my team mates in participating in the development. Check my code at: https://github.com/Andyyesiyu/Hold_That_Line_Minimax

## From Sample Minimax to Practical Utilization
I used the code from https://github.com/Cledersonbc/tic-tac-toe-minimax to understand the implementation of Minimax algorithm and edited it to work in Hold The Line game. More analysis of the Minimax algorithm in Tic-Tac-Toe please refer to Mingyan’s report. Actually, I found that the Pseudocode in the blog is the most intuitive part and share it below.
```
minimax(state, depth, player)

	if (player = max) then
		best = [null, -infinity]
	else
		best = [null, +infinity]

	if (depth = 0 or gameover) then
		score = evaluate this state for player
		return [null, score]

	for each valid move m for player in state s do
		execute move m on s
		[move, score] = minimax(s, depth - 1, -player)
		undo move m on s

		if (player = max) then
			if score > best.score then best = [move, score]
		else
			if score < best.score then best = [move, score]

	return best
end
```
In the real code section, because it is the tic-tac-toe game, so it is easy to do the “execute move m on s” part by using the code: “state[x][y] = player”, and “undo move m on s” by “state[x][y] = 0”. But for our Hold The Line game, the situation is different, because the status is not that easy to reverse, we should consider this two parts of detail to implement Minimax in Hold The Line. For other logic the logic is similar to a large part, like using MAX in computer’s turn and use MIN in person’s turn. 

## Basic ideas of Hold That Line Minimax
As I discussed in previous part, the “execute move” and “undo move” part should be paid attention to. So I just use two class functions to process the m seperately. “Execute move” is the function *self.fillBoard*, and “Undo move” is the function *self.deleteBoard*.  I also set up a function *self.findAllValidPath* to find all feasible moves.
Apart from the calculation part, storing the status in hold that line is more difficult than the Tic-Tac-Toe (just two situations 1 or 0), I created three variables to store the status variable. The first one is the previousLines, which means previous existed lines in the game. The second one prevEnds means previous two end points (points can start drawing the line). The third fillpath records all the coordinates of the path that drew just now. By using all three variables, I can reverse to the previous game session. First *self.fillBoard* returned those three variables and parse them to *self.deleteBoard* as the parameters. 
Before explaining evaluation function part, I must define the “final status” of the game. In the algorithm, if there is no line to draw, the game is defined as “end”. Then, the *self.evaluate* is called before making the next step so if the *self.evaluate* is calling in the computer’s session, which means computer has no choice to draw and the person must put the final line. So person loses and computer wins, vice versa. In the Hold That Line Minimax, I define the score as 1,0,-1. One means computer win so it is the largest value and negative one means person win so it is the smallest one. Zero is in the middle, so it represents game is not over and we should stop here for computation complexity consideration. We will not choose zero if we have other choice. But if there is no better choice, the computer would just choose one of them not in the worst case (-1). Then there is another question, what happen if we have multiple choice?
To deal with the problem, I maintained a bestList array to store all the best steps in calculation. If a better step appeared, the bestList would be empty and change to that best step now. 
To decide the depth in minimax, I just tried it in several situations. In testing I found my computer can handle 5*5 board game in depth 3; and for smaller one like a game which weight and height all equals 3, the computer can hand Minimax in depth 4. I think because it is the exhaustive depth first search, so the calculation cost is high and there should have some optimization way. 
When we talk about time complexity of the code, I think for every step of minimax, we should first find all feasible map using *findAllValidPath*, which should scan all the empty points and judge whether they are conflict with the current line. So the time complexity of *findAllValidPath* is about `O(m*n*l)`, m is the width of the board; n is the height of the board and l is the number of turns. Because both *self.fillBoard* and *self.evaluate* will not  exceed the `O(m*n)`(at most draw a longest line in the board). So I can regard the single Minimax time complexity is `O(m*n*l)`. As I limited the depth it to 3, so the whole deduction algorithm time complexity will be `O(m*n*l)^3`. This is a super big time complexity so it is easy to understand why it would be really slow in depth 4.
Other details of the Hold That Line Minimax algorithm please refer to the code and I have added comments to nearly every line in the minimax function, which is really of detail and could help you guys to understand. 
## Other functions
Basically, our team’s project has three parts, handling inputs from users, judging whether lines would cross and the minimax deduction. 
## Code Review
It is a little bit awkward to review my own code, but from the current angle, I would try my best to review the code in several aspects below:
1. Code Duplication
There are some duplications in the code, like in the fillLine function, I just compare the data several times to choose the bigger one. Some time I sticked to use if else statement in one line and produce several duplication.
2. Styling
As the development habit in Java, I used  camel case in variable and function’s name. But after that, I heard that in python, we should use underscore naming, so this is a main flaw. 
There are some indents and empty lines not in right position, because I did use some automatic formatting extensions. I fixed nearly all of them after uploading the latest version.
Comments are brilliant with bilingual language support. 
3. Testing
No testing module