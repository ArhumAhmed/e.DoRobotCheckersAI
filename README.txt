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