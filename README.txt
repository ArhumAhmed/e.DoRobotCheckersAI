INTRODUCTION:

In this project, our team programs an e.Do robotic arm to play checkers against a human opponent. The program consists of three components which are referenced by the main integration script. The first component is object detection. In our setup, we have a camera mounted above a checkerboard pointing down at it. Object detection reads the frames and determines what the board state is based on the location of circles and squares and what colors they are. The next component is the manipulation which control the motors in the 6-axis e.Do arm. Manipulation is what enables us to have the robot physically pickup a piece and move it around once a turn has been decided. The final component is the AI which computes the best possible move the robot can make using the minimax algorithm and heauristic. The heauristic assigns points to specific features of a board state it considers advantageous. The minimax algorithm looks a number of moves ahead and determines all possible moves and board states that are possible for every move it can make and references the heauristic to determine which move will yield the best possible end states. The integration script calls on the object detection to determine what the current board state is and passes it in form of an array to the AI. The framework for the AI was forked from https://github.com/THeK3nger/Cobra-Draughts. The AI validates if the board state is valid and if so, computes and returns the best possible move. The move is returned back to the integration script which passes the move intruction to manipulation to execute the physical movement to make that move. In addition, we also implemented a form of machine learning to improve the heauristic of the AI. This works by randomly increasing or decreasing one of the feature values in the heuristic whenever the AI loses against an opponent. Furthermore, we have developed an environment in which the AI can train against itself. One instance of the AI object is using the static default values whereas the other one is accessing an external file containing the heauristic value which is being modified when it loses. The idea is that given enough trials, the modified AI's heauristic will begin to aggregate towards an ideal ratio. 



SETUP:
* Make sure the checkerboard is the correct distance from the robot
and that the checkerboard is in the center of the cameras's view. You
can use programs such as guvcview to check this.


HOW TO RUN:
- run config.sh script to connect ros on the jetson to the robot
- enter 'roscd edo_checkers_final/src'
- enter 'python3 total_integration.py'


PLAYING A GAME:
* The robot will play a full game until it either wins or loses.

* Win conditions: the robot takes all of the opponents pieces or opponent has no more
valid moves

* Lose conditions: the robot loses all of its pieces or no longer has a valid move

* On loss or win the program will end on its own.

* If a valid move is not detected the robot will not make its move until a valid
move is made
