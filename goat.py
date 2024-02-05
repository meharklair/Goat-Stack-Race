#----------------------------------------------------
# Goat implementation
#----------------------------------------------------

class Goat:
    def __init__(self, colour, row, column):
        self.colour = colour
        self.row = row
        self.column = column
    def __str__(self):
        ''' returns a string repr of the goat'''
        return(f'{self.colour} {self.column}{self.row}')
    
    def get_colour(self):
        ''' returns goat colour'''
        return self.colour
    
    def set_row(self, new_row):
        ''' sets a new row'''
        self.row = new_row
        
    def set_col(self, new_col):
        ''' sets a new column'''
        self.column = new_col  