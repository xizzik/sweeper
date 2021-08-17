import numpy as np

def get_nbhd(arr,coord):
        return arr[(coord[0] if coord[0] == 0 else coord[0]-1):(coord[0]+2),
               (coord[1] if coord[1] == 0 else coord[1]-1):(coord[1]+2)]
    

class Sweeper():
    
    def __init__(self,game_size_x, game_size_y, nmines):
        self.game_size_x = game_size_x
        self.game_size_y = game_size_y
        self.game_size = self.game_size_x*self.game_size_y
        self.nmines = nmines
        self.array_hidden, self.where_bombs = self.initialize_board()
        self.array_visible = np.zeros((self.game_size_x, self.game_size_y)) - 2
        self.state = 'active'
        self.swept = set()
        

    def get_nbhd_coords(self,coord):
        c1,c2 = coord[0], coord[1]
        nbhd = set()
        for i in range(c1-1,c1+2):
            for j in range(c2-1,c2+2):
                if (0<=i<self.game_size_x)&(0<=j<self.game_size_y)*((i,j)!=coord):
                    nbhd.add((i,j))
        return nbhd
    
    def initialize_board(self):
        game_array = np.zeros(self.game_size)
        mines = np.random.choice(self.game_size, size = self.nmines, replace = False)
        game_array[mines] = -1
        game_array = game_array.reshape((self.game_size_x, self.game_size_y))
        bombs = tuple(map(tuple,np.argwhere(game_array == -1)))
        for bomb in bombs:
            nbhd = get_nbhd(game_array,bomb)
            nbhd += 1
        for bomb in bombs:
            game_array[bomb] = -1
        return game_array, bombs
    
    def sweep(self, coord):
        if self.state != 'over':
            if self.array_hidden[coord] == -1:
                self.array_visible[coord] = self.array_hidden[coord]
                self.state = 'over'
            elif coord not in self.swept:
                self.array_visible[coord] = self.array_hidden[coord]
                self.swept.add(coord)
                if self.array_hidden[coord] == 0:
                    nbhd = self.get_nbhd_coords(coord)
                    bombs_set = set(self.where_bombs)
                    for point in nbhd - bombs_set:
                        self.sweep(point)
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
            except:
                print('Unhandled error has occured!')
                break
        elif game.state == 'over':
            print(game.array_visible, '\n', 'Game over!')
            break
        elif game.state == 'won':
            print(game.array_visible, '\n', 'You won!')
            break
        else:
            print('An error has occured!')
            break