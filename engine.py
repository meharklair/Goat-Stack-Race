#----------------------------------------------------
# Game engine implementation
# 
# Author: Team CMPUT 175 Winter 2023 (FEB)
#----------------------------------------------------

from typing import List
import random
import time

from .game import Game
from .player import Player

WIDTH = 9
HEIGHT = 6
MIN_PLAYERS = 2
MAX_PLAYERS = 5
GOATS_PER_PLAYER = 4
PHASES = [1,2,3,4]
PLAYERS = ['WHITE', 'BLACK', 'RED', 'ORANGE', 'GREEN']
VALID_COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
RACE_KEYS = ['dice_outcome', 'sideways_move', 'forward_move']
SKIP_STRING = 'skip'
PASS_STRING = 'pass'
WAIT_TIME = 0.5


class Engine:
    '''
    Represents the Goat Race engine
    '''
    
    def __init__(self, number_players: int, obstacle_positions: List = []):
        '''Initializes the engine'''

        # Check if # of players between 2 and 5
        try:
            self.check_number_players(number_players)
            self.number_players = number_players
        except Exception as e:
            raise

        # Initialize game 
        self.game = Game(WIDTH, HEIGHT, obstacle_positions)
        self.game.set_phase(PHASES[0])
        self.order_phase_outcomes = []
        self.player_order = [i  for i in range(self.number_players)]
        self.initial_turn = 0
        self.dice_outcome = None
        self.subphase = 0
        
        # Add players
        for player_id in range(number_players):
            player_color = PLAYERS[player_id]
            player = Player(player_color)
            self.game.add_player(player)
    
    def check_number_players(self, n: int) -> None:
        '''Checks if number of players is valid'''

        if not isinstance(n, int) or (n < MIN_PLAYERS) or (n > MAX_PLAYERS):
            raise Exception(
                f'Invalid number of players: {n}' 
                + f'Should be between {MIN_PLAYERS} and {MAX_PLAYERS}'
            )
    
    def throw_dice(self, n_sides: int = 6) -> int:
        '''Generates a random number between 1 and 6'''

        print('The dice is rolling...')
        time.sleep(WAIT_TIME)
        dice_outcome = random.randint(1, n_sides)
        print(f'The dice stopped. The outcome is {dice_outcome}')
        time.sleep(WAIT_TIME)
        return dice_outcome

    def should_exit(self, command: str) -> bool:
        '''Returns True if quit command is typed'''

        if not isinstance(command, str):
            return False
        return command.lower() == 'q'
    
    def should_skip(self, command: str) -> bool:
        '''Returns True if skip command is typed'''

        if not isinstance(command, str):
            return False
        return command.lower() == 's'

    def process_throw(self, command: str) -> str:
        '''
            Checks that the user chose the throw 
            or quit commands and returns it
        '''
        if command.lower() in ['t', 'q']:
            return command.lower()
        else:
            raise Exception(f'Invalid command: {command}')

    def process_row(self, command: str) -> str:
        '''
            Checks that the row where a new goat 
            is added is valid and returns it
        '''
        if self.should_exit(command): 
            return command.lower()
        if len(command) == 1:        
            try:
                row = int(command)
            except:
                raise Exception('Invalid row input')
            
            self.game.check_row(row)
            return row
        else:
            raise Exception(f'Invalid command: {command}')        
    
    def process_restart(self, command: str) -> str:
        '''
            Checks that the user chose the restart 
            or quit commands and returns it
        '''
        if command.lower() in ['r', 'q']:
            return command.lower()
        else:
            raise Exception(f'Invalid command: {command}')

    def process_jump(self, command: str) -> List[tuple]:
        '''
            Checks the jump has a valid format and returns
            it in the format expected by the engine: 
                    
                [(init_location),(final_location)]
        '''
        if self.should_exit(command): 
            return command

        if len(command) == 4:
            try:                
                initial_column = command[0].upper()
                initial_row = int(command[1])
                final_column = command[2].upper()
                final_row = int(command[3])
                move = [
                    (initial_row, initial_column), 
                    (final_row, final_column)
                ]
            except:
                raise Exception('Invalid move input')
            
            self.game.check_valid_move_format(move)
            return move

        else:
            raise Exception(f'Invalid command: {command}')

    def process_sideways_jump(self, command: str) ->  List[tuple]:
        '''
            Checks the sideways jump has a valid format
        '''
        if self.should_skip(command): 
            return SKIP_STRING
        else: 
            return self.process_jump(command)

    def get_command(self):
        '''Returns the command input by the current player'''

        player = PLAYERS[self.get_turn()]
        phase = self.get_phase()

        if (phase == PHASES[0]) or ((phase == PHASES[2]) and (self.subphase == 0)):
            message = f'Player {player}, enter t to throw the dice, or q to end the game: '
            process = self.process_throw

        elif phase == PHASES[1]:
            message = f'Player {player}, enter the row where you want to place a new goat: '
            process = self.process_row

        elif (phase == PHASES[2]) and (self.subphase == 1):
            message = f'Player {player}, enter s to skip, or start and end locations of sideways jump (e.g., A2A1): '
            process = self.process_sideways_jump

        elif (phase == PHASES[2]) and (self.subphase == 2):
            message = f'Player {player}, enter the start and end locations of forward jump (e.g., A1B1): '
            process = self.process_jump

        elif phase == PHASES[3]:
            message = f'Enter r to restart the game, or q to end the game: '
            process = self.process_restart
        
        else:
            raise Exception(f'Invalid phase: {phase} or subphase: {self.subphase}')
        
        command = input(message)
        command = process(command)
        return command
    
    def should_get_command(self, row=None):
        '''If current phase is Race, checks if row has any goat'''

        phase = self.get_phase()

        if (phase == PHASES[2]) and (self.subphase == 2):
            goats_in_row = self.game.check_nonempty_row(row)
            return goats_in_row
        elif (phase == PHASES[2]) and (self.subphase == 1):
            player = self.game.get_current_player()
            goats_blocked = self.game.get_goats_blocked(player)
            return goats_blocked < GOATS_PER_PLAYER
        return True

    def run_order_phase_step(self) -> None:
        ''' Throws the dice and stores the result for ordering the players'''

        # Throw and store dice
        dice_outcome = self.throw_dice()
        self.order_phase_outcomes.append(dice_outcome)

        # Pass to next player    
        self.update_turn()
        
        # Updates phase if completed
        self.update_order_phase()        
    
    def update_order_phase(self) -> None:
        '''
            Checks if players finished throwing the initial
            dice and set turn according to order
        '''
        phase_done = self.check_all_players_throwed_dice()
        if phase_done:
            initial_turn = self.player_order[0]
            self.game.set_turn(initial_turn)
            self.update_phase()

    def run_placement_phase_step(self, chosen_goat_row: int):
        '''Adds goat in given row if possible'''

        # Validate if player can add goat in chosen row of the starting gate
        valid_row = self.game.check_starting_goat_placement(chosen_goat_row)
        if not valid_row:
            raise Exception(f'Stack in row {chosen_goat_row} is too high')
        
        # Add goat to board and player list
        starting_gate = VALID_COLUMNS[0]
        self.game.add_goat(chosen_goat_row, starting_gate)

        # Updates phase if completed
        self.update_placement_phase()

        # Pass to next player
        self.update_turn()

    def update_placement_phase(self) -> None:
        '''
            Checks if all players have the appropriate number
            of goats in the board to start the race
        '''
        # Obtain a list with number of goats per player
        goats_per_player = self.game.get_goats_per_player()
        
        # Loop through the list
        player_id = 0
        phase_done = True
        while phase_done and (player_id < self.number_players):
            goat_number = goats_per_player[player_id]
            if goat_number != GOATS_PER_PLAYER:
                phase_done = False
            player_id += 1

        if phase_done:
            self.update_phase()
  
    def update_turn(self) -> None:
        '''Update turn by moving one index in the player_order list.'''

        turn = self.game.get_turn()
        if turn is None:
            self.initial_turn = (
                (self.initial_turn + 1) % self.number_players)
        else:
            turn_index = self.player_order.index(turn)
            new_turn_index = (turn_index+1) % self.number_players
            new_turn = self.player_order[new_turn_index]
            self.game.set_turn(new_turn)

    def update_phase(self) -> bool:
        phase = self.get_phase()        
        new_phase = PHASES[PHASES.index(phase)+1]
        self.game.set_phase(new_phase)        

    def update_race_subphase(self):
        '''Cycles throgh the subphase numbers'''

        self.subphase = (self.subphase + 1) % 3
        
    def check_all_players_throwed_dice(self):
        ''' Checks that there is a dice ouctome for each player'''
        
        number_of_throws = len(self.order_phase_outcomes)
        if number_of_throws == self.number_players:
            self.player_order.sort( 
                key=lambda x: (self.order_phase_outcomes[x], x),
                reverse=True,
            )
            return True
        return False

    def get_turn(self) -> int:
        turn = self.game.get_turn()
        if turn is None:
            turn = self.initial_turn
        return turn
    
    def get_phase(self) -> int:
        return self.game.get_phase()

    def get_action(self):
        '''Obtain command from user if needed. Otherwise set action as pass'''

        if self.should_get_command(row=self.dice_outcome):
            command = self.get_command()
            quit = self.should_exit(command)  
        else:
            command = PASS_STRING
            quit = False
            print('Not available moves')
        return command, quit

    def check_endgame(self):
        reset = False
        quit = False

        # Check if winner or tie
        is_winner = self.game.check_winner()
        is_tie = self.game.check_tie()

        if is_winner or is_tie:
            self.update_phase()

            # Display endgame message
            if is_winner:
                turn = self.get_turn()
                turn_index = self.player_order.index(turn)
                previous_turn_index = (turn_index-1) % self.number_players
                previous_turn = self.player_order[previous_turn_index]
                print(f'Player {PLAYERS[previous_turn]} is the winner!')
            else:
                print(f"There are no more possible winners. It's a tie!")

            # Ask for reset
            command = self.get_command()
            if self.should_exit(command):
                quit = True
            else:
                reset = True

        return reset, quit

    def game_step(self):
        
        action, quit = self.get_action()
        reset = False

        if not quit:
            phase = self.get_phase()

            # Order
            if phase == PHASES[0]:
                # Throw and store dice
                self.run_order_phase_step()

            # Placement    
            elif phase == PHASES[1]:
                self.run_placement_phase_step(action)

            # Race 
            elif phase == PHASES[2]:                 
                if self.subphase == 0:
                    self.dice_outcome = self.throw_dice()                   
                
                elif (self.subphase == 1) and (action not in [PASS_STRING, SKIP_STRING]):
                    self.game.move_sideways(action)

                elif self.subphase == 2:
                    if action != PASS_STRING:
                        self.game.move_forward(action, self.dice_outcome)
                    self.update_turn()               
                
                self.update_race_subphase()
           
            reset, quit = self.check_endgame()
        
        return reset, quit
   
    def __str__(self) -> str:
        '''Returns a visual snapshot of the game'''

        return str(self.game)


if __name__ == '__main__':
    pass