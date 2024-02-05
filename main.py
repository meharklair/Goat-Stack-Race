import time
from datetime import datetime
from pathlib import Path
from typing import List

from src.classes import Engine

PHASES = [1,2,3,4]
WAIT_TIME = 1
START_MESSAGE = "Let's have a goat race!"
END_MESSAGE = 'Game ended. Good bye.'


def should_print_game(phase: int, subphase: int):
    '''Returns true if a new phase and turn starts'''

    return (phase in PHASES[1:]) and (subphase == 0)

def display_log_game(engine: Engine, filename: str) -> None:
    '''Displays the game state and saves it in a log'''

    print(str(engine))
    if filename is not None:
        try:
            with open(filename, "a") as file:
                file.write(str(engine)+'\n')
        except:
            raise Exception(f'Invalid filename: {filename}') 

def generate_filename() -> str:
    '''Generates valid filename where to store the game log'''
    
    now = datetime.now()
    now = now.strftime("%Y-%m-%d_%H-%M-%S")
    Path('./savegame').mkdir(parents=True, exist_ok=True)
    filename = f'savegame/save_{now}.txt'
    return filename

def main(
        number_players: int, 
        obstacle_positions: List[int], 
        filename: str
    ) -> None:
    '''Executes game while not quit'''

    print(START_MESSAGE)
    time.sleep(WAIT_TIME)

    quit = False

    while not quit:
        # Create game engine
        engine = Engine(number_players, obstacle_positions)
        reset = False
        valid = True

        # Prints initial configuration
        display_log_game(engine, filename)
        
        while not (reset or quit):
            # Displays board and game info
            if valid and should_print_game(engine.get_phase(), engine.subphase):
                display_log_game(engine, filename)
            
            # Ask current player for input corresponding to current
            # phase and executes the corresponding action
            try:
                reset, quit = engine.game_step()                   
                valid = True

            except Exception as e:
                print(e)
                valid = False
            
    print(END_MESSAGE)


if __name__ == '__main__':

    filename = generate_filename()    
    number_players = 2
    obstacle_positions = [(3,'C'),(6,'D'),(4,'F'),(5,'E'),(4,'D')]

    main(number_players, obstacle_positions, filename)
    