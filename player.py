#----------------------------------------------------
# Player implementation
#----------------------------------------------------

from .goat import Goat

class Player:
    def __init__(self, colour):
        self.colour = colour
        self.goat_list = []
        
    def add_goat(self, item):
        ''' adds a goat'''
        self.goat_list.append(item)
        
    def remove_goat(self):
        ''' removes a goat '''
        self.goat_list.pop()
        
    def get_goats(self):
        ''' returns the goat list'''
        return self.goat_list
        
    def get_colour(self):
        ''' gets colour'''
        return self.colour
    
    def get_length(self):
        ''' gets lengths of the goat list'''
        return len(self.goat_list)
    
    def __str__(self):
        ''' string repr of player'''
        print(self.colour)
        print('Goats:')
        for goat in self.goat_list:
            print(f'{goat.get_colour()} {str(goat)}')
        return''