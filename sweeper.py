import numpy as np

def get_neighbours_2d(arr,coord):
    return arr[(coord[0] if coord[0] == 0 else coord[0]-1):(coord[0]+2),
               (coord[1] if coord[1] == 0 else coord[1]-1):(coord[1]+2)]

class Sweeper():
    
    def __init__(self,game_size_x, game_size_y, nmines):
        self.game_size_x = game_size_x
        self.game_size_y = game_size_y
        self.game_size = self.game_size_x*self.game_size_y
        self.nmines = nmines
        game_array = np.zeros(self.game_size)
        rng = np.random.default_rng()
        mines = np.random.choice(self.game_size, size = nmines)
        game_array[mines] = -1
        
        self.array_hidden = game_array.reshape((self.game_size_x, self.game_size_y))
        self.array_visible = np.zeros((self.game_size_x, self.game_size_y)) - 2
        self.state = 'active'
        self.where_bombs = tuple(map(tuple,np.argwhere(self.array_hidden == -1)))
        self.swept = set()
        
        for bomb in self.where_bombs:
            nbhd = get_neighbours_2d(self.array_hidden,bomb)
            nbhd += 1
        for bomb in self.where_bombs:
            self.array_hidden[bomb] = -1
    
    def sweep(self, coord):
        if self.state != 'over':
            if self.array_hidden[coord] == -1:
                self.array_visible[coord] = self.array_hidden[coord]
                self.state = 'over'
            elif coord not in self.swept:
                self.array_visible[coord] = self.array_hidden[coord]
                self.swept.add(coord)
                if len(self.swept) == self.game_size - self.nmines:
                    self.state = 'won'

if __name__ == "__main__":
    game = Sweeper(10,8,10)
    while True:
        if game.state == 'active':
            print(game.array_visible)
            try:
                get_coord = input('Input your coordinate:')
                if get_coord == 'exit':
                    print('Exiting game.')
                    break
                coord = tuple(map(int, get_coord.split(',')))
                game.sweep(coord)
            except ValueError:
                print('That is not a correct coordinate (write ex. "1,2")')
            except IndexError:
                print('That is not a valid coordinate (make sure your coordinate is in range)')
        elif game.state == 'over':
            print(game.array_visible, '\n', 'Game over!')
            break
        elif game.state == 'won':
            print(game.array_visible, '\n', 'You won!')
            break

