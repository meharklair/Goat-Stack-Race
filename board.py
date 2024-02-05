#----------------------------------------------------
# Board implementation
#----------------------------------------------------

from .stack import Stack
from .goat import Goat


class Board:
  def __init__(self, width, height, obstacle_positions):
    ''' initializes the class'''
    board = []
    self.width = width
    self.height = height
    self.obstacle_positions = obstacle_positions
    for i in range(self.height):
        row = []
        for j in range(self.width):
            stack = Stack()
            row.append(stack)
        board.append(row) 
    self.check_obstacle_position()
    for item in self.obstacle_positions:
      board[item[0] - 1][ord(item[1])-65].push('x')
    self.board = board  
                
  def check_row(self,row):
    ''' checks if the given row is valid'''
    if row >= 1 and row <= self.height:
      pass
    else:
      raise Exception('row is outside of board')
  def check_col(self,col):
    ''' checks if the given column is valid'''
    if col >= 1 and col <= self.width:
      pass
      
    else:
        raise Exception('col is outside of board')
        
  def check_obstacle_position(self):
    ''' checks if the obstacle pos is valid'''
    for item in self.obstacle_positions:
        self.check_row(item[0])
        self.check_col(ord(item[1])-64)
            
  def get_width(self):
    ''' returns the width'''
    return self.width
    
  def get_height(self):
    ''' returns the height'''
    return self.height
    
  def get_board(self):
    ''' returns the board'''
    return self.board
    
  def __str__(self):
    ''' returns the string repr of board'''
    i = 0
    add = 0
    string = '     '
    final_str = ''
    current = self.board
    for j in range(self.width):
        string += chr(97 + i).upper() + '   '
        i = i + 1
    final_str += f'{string} \n'
    for a in range(self.height):
        row = ''
        ting = ('+---' * self.width)
        ting = '   ' + ting +'+'
        row += f'{a + 1:<2}' + ' '
        
        for i in range(self.width):
            if current[a][i].is_empty():
                row += (f"|   ")
            elif current[a][i].peek() == 'x':
                row += f"| {current[a][i].peek()} "
            else:
                row += f"| {current[a][i].peek().get_colour()[0]} "
            add = add + 1
        row += (f"|   ")
        final_str += f'{ting} \n'
        final_str += f'{row} \n'
        
    final_str += f'{ting} \n'
    return final_str
