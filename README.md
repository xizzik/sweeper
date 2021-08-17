# sweeper
Minesweeper game in python (for reinforcement learning planned in future).

Currently the game runs in command line without GUI. You can input a coordinate (starting from 0) in the form ex. "1,2" then the game checks if there is a mine, if not it reveals the number of mines in the neighbourhood. Unswept coordinates are masked by "-2" and if you encounter a mine it will be "-1".

You can exit the game at any time by inputing "exit".
