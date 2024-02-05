#----------------------------------------------------
# Game implementation
#----------------------------------------------------

from typing import List
from .goat import Goat
from .board import Board
from .player import Player

GOATS_PER_PLAYER = 4
WINNING_NUMBER_GOATS = 3
VALID_COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
SIDE_JUMP_SIZE = 1
FORWARD_JUMP_SIZE = 1
class Game:
    '''
    Represents the Goat Race game
    '''
    ################################################
    #
    # The following methods MUST be in your solution
    # 
    ##############################################
    
    def __init__(self,width,height,obstacle_positions):
        ''' initializes the class'''
        self.width = width
        self.height = height
        self.obstacle_positions = obstacle_positions
        self.board = Board(width, height, obstacle_positions)
        self.turn = None
        self.player_list = []
        self.phase = 0
    def __str__(self): 
        ''' returns a string repr of game'''
        players = ''
        current = self.board.get_board()
        end_str = ''
        end_str += f'{str(self.board)} \n'
        for item in self.player_list:
            players += f'{item.get_colour()} '
        end_str += f'players: {players} \n'
        end_str += f'phase:{self.phase} \n'
        if self.phase == 1:
            end_str += f'players who turn it is: undefined \n'
        else:
            end_str += f'players who turn it is: {self.get_current_player().get_colour()} \n'
        return end_str
    def get_phase(self): 
        ''' gets current phase'''
        return self.phase
    
    def get_turn(self):
        ''' gets current turn'''
        return self.turn
    
    def get_current_player(self):
        ''' gets current player'''
        return self.player_list[self.get_turn()]    
    
    def set_phase(self, phase):
        ''' sets the phase'''
        self.phase = phase
        
    def set_turn(self, turn):
        '''  sets the turn'''
        self.turn = turn 
    
    def add_player(self, player):
        ''' adds a player'''
        
        self.player_list.append(player)
    
    def get_goats_blocked(self,player):
        ''' returns the number of goats blocked'''
        blocked = 0
        list = []
        goats = player.get_goats()
        board = self.board.get_board()
        for i in range(GOATS_PER_PLAYER):
            col = ord(goats[i].column) - 65
            if board[goats[i].row - 1][col].is_empty():
                pass
            else:
                top = board[goats[i].row - 1][col].peek()
                if goats[i].get_colour() != top.get_colour() or top in list:
                    blocked += 1
                list.append(top)
        return blocked
                

    def get_goats_per_player(self):
        ''' gets the number of goats per player'''
        goats_per = []
        for player in self.player_list:
            goats_per.append(player.get_length())
        return goats_per
    
    def add_goat(self,row,col):
        ''' adds a goat'''
        board = self.board.get_board()
        current = self.get_current_player()
        goat = Goat(self.get_current_player().get_colour(),row,col)
        col = ord(col) - 65
        current.add_goat(goat)
        self.board.check_row(row)    
        self.board.check_col(col + 1)
        board[row - 1][col].push(goat)
        
        
    def move_sideways(self, move):
        '''Executes sideways move if valid '''
        # start and end locations will be input A1A2
        player_colour = self.get_current_player().get_colour()
        board = self.board.get_board()
        if ord(move[0][1]) - 65 != ord(move[1][1]) - 65:
            raise Exception('cannot move forward in sideways jump')
        if move[0][0] - move[1][0] == 1 or move[0][0] - move[1][0] == -1:
            if board[move[0][0] - 1][ord(move[0][1]) - 65].is_empty():
                raise Exception('no goat at given position')
            elif board[move[0][0] - 1][ord(move[0][1]) - 65].peek() == 'x':
                raise Exception('cannot move obstacle')
            elif board[move[0][0] - 1][ord(move[0][1]) - 65].peek().get_colour() != player_colour:
                raise Exception('cannot move another players goat sideways')
            elif board[move[1][0] - 1][ord(move[1][1]) - 65].is_empty():
                
                goat = board[move[0][0] - 1][ord(move[0][1]) - 65].pop()
                goat.set_row(move[1][0])
                board[move[1][0] -1][ord(move[1][1]) - 65].push(goat)
                
            elif board[move[1][0] - 1][ord(move[1][1]) - 65].peek() == 'x':
                raise Exception('cannot jump onto obstacle')
            else:
                goat = board[move[0][0] - 1][ord(move[0][1]) - 65].pop()
                goat.set_row(move[1][0])
                board[move[1][0] -1][ord(move[1][1]) - 65].push(goat)                  
        else:
            raise Exception('cannot move more than one space up or down')
                    

    def move_forward(self, move, dice_outcome):
        '''Executes forward move if valid '''
        # forwards move of any goat eg A1B1
        board = self.board.get_board()
        count = 0
        add = 0
        if move[0][0] != dice_outcome or move[0][0] != dice_outcome:
            raise Exception('Cannot move in a row that was not rolled')
        if ord(move[1][1]) - ord(move[0][1]) != 1 or  ord(move[1][1]) - ord(move[0][1]) != 1:
            raise Exception('Cannot move more than one space forwards')
        if ord(move[1][1]) - ord(move[0][1]) != 1:
            raise Exception('Cannot move backwards')
        
       
        if board[move[0][0] - 1][ord(move[0][1]) - 65].is_empty():
            raise Exception('no goat at given position')
        else:
            if board[move[1][0] - 1][ord(move[1][1]) - 65].is_empty():
                goat = board[move[0][0] - 1][ord(move[0][1]) - 65].pop()
                goat.set_col(move[1][1])
                board[move[1][0] - 1][ord(move[1][1]) - 65].push(goat)
            elif board[move[1][0] - 1][ord(move[1][1]) - 65].peek() == 'x':
                raise Exception('cannot go forward obstacle there')
            else:
                # changes the pos of the goat
                goat = board[move[0][0] - 1][ord(move[0][1]) - 65].pop()
                goat.set_col(move[1][1])
                board[move[1][0] - 1][ord(move[1][1]) - 65].push(goat)
                                    
                
    def check_row(self, row: int) -> None:
        '''Checks if a row is valid'''
        if row >= 1 and row <= self.height:
            pass
        else:
            raise Exception    
        
    
    def check_valid_move_format(self, move: List) -> None:
        '''Checks if the given location is an appropriate list of tuples'''
        if len(move) == 2:
            for item in move:
                self.board.check_row(item[0])
                self.board.check_col((ord(item[1]) - 64))
      
        else:
            raise Exception('invalid tuple')
        

    def check_nonempty_row(self, row) -> bool:
        '''Returns whether there are non-blocked goats in a row'''
        board_list = []
        board = self.board.get_board()
        for item in board[row-1]:
            if item.is_empty():
                board_list.append(' ')
            else:
                board_list.append(item.peek())
        for i in range(len(board_list) - 1):
            if board_list[i] == ' ':
                pass
            elif board_list[i] != 'x':
                if i == len(board_list) - 1:
                    pass
                # checks if the next position is a obstacle
                elif board_list[i+1] == 'x':
                    pass
                else:
                    return  True
        return False
            
    
    def check_starting_goat_placement(self, row: int) -> bool:
        '''Checks that goat is not placed in a high stack'''
        board = self.board.get_board()
        smallest_stack = 1000
        for i in range(self.height):
            if board[i][0].size() < smallest_stack:
                smallest_stack = board[i][0].size()
        if board[row - 1][0].size() <= smallest_stack:
            return True
        else:
            return False
    
    def check_winner(self) -> bool:
        '''
            Returns whether one player has won by getting 
            the necessary goats to the Destination
        '''

        board = self.board.get_board()
        count_dict = {}
        col_check = chr(65 + (self.width -1))
        for item in self.player_list:
            count_dict[item] = 0
            goats = item.get_goats()
            for goat in goats:
                if goat.column == col_check:
                    count_dict[item] += 1 
        
        for value in count_dict.values(): 
            if value == 3:
                return True

        return False
        
    
    def check_tie(self) -> bool:
        '''
            Returns whether there is a tie since 
            no player has possible moves
        '''
        if self.phase == 3:
            for i in range(1,self.height + 1):
                if self.check_nonempty_row(i):
                    return False
            return True
        else:
            return False
            

    ################################################
    #
    # The following methods do NOT need to be
    # included in your solution, but they might
    # give you an idea of possible useful methods
    # to include.
    # 
    ################################################
    def get_goats_blocked_per_player(self) -> List[int]:
        '''
            Returns a list that contains the number 
            of goats blocked per player.
        '''
        pass

    def get_starting_gate_sizes(self) -> List[int]:
        '''
            Returns a list containing how many goats
            are in each row of the starting gate
        '''
        pass
    
    def get_top_goat(self, row : int, column : str) -> Goat:
        '''
            Obtains a goat at a specific location
            Inputs:
                - row: the row where the goat will be obtained from
                - column: the column where the goat will be obtained from
            Returns:
                The goat at the top of the stack in the specified location
        '''
        pass
   
    def get_goats_destination_per_player(self, destination: str) -> List[int]:
        '''
            Return a list that contains the number 
            of goats per player in the destination.
        '''
        pass

    def check_column(self, column: str) -> None:
        '''Checks if a column is valid'''

        pass
    
    def check_location(self, location) -> None:
        ''' Checks if location is in the board'''

        pass
    
    def check_jump(self, row: int, column: str) -> None:
        '''Checks if available stack to jump'''

        pass

    def check_forward_move(self, forward_move: List, dice_outcome: int) -> None:
        '''
            Checks if player can move goat forward
            Inputs:
                - forward_move: list with tuple of initial and final locations
                - dice_outcome: dice outcome (integer between 1 and 6)
        '''
        pass

    def check_sideways_move(self, sideways_move: List[tuple]) -> None:
        '''
            Checks if player can move goat sideways
            Inputs:
                - forward_move: list with tuple of initial and final locations
        '''
        pass

    def check_same_color(self, row: int, column: str) -> None:
        '''
            Checks if the color of the current 
            player and the goat on top coincide
        '''
        pass
    
    def move_goat(self, move: List) -> None:
        '''
            Lets a goat jump in the board
            Inputs:
                - move: list with tuple of initial and final locations
        '''
        pass
        
    

if __name__ == '__main__':

    pass