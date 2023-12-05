import pygame
import time
import os
import pandas as pd

grid = """
--#--#--
--#--#--
########
--#--#--
--#--#--
########
--#--#--
--#--#--
"""

tic = """
-#
#-
"""

tac = """
##
##
"""

white = (255, 255, 255)
black = (0, 0, 0)

map_size = 8
cell_size = 40


def main():
    main_loop = True
    game = get_game()
    while main_loop:
        endscreen = True
        game_running = True

        rounds = 0  # rounds since start of the game
        tic_or_toe = True  # whose turn is it
        played_moves = []  # which fields are occupied

        protocol = {
            'game': game,
            'move': [],
            'time': [],
            'winner': 0
        }

        tic_map = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]

        map = new_map(map_size, map_size)  # create new map
        map = flip(map[:], import_art(grid))  # flip ascii art as grid

        pygame.init()
        pygame.display.set_caption("TicTacToe")
        screen = pygame.display.set_mode((map_size * cell_size,
                                          map_size * cell_size))

        # start game
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endscreen = False
                    game_running = False
                    main_loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    chosen_field = get_field(pygame.mouse.get_pos())  # get which field was clicked on

                    if played_moves.count(chosen_field) <= 0:  # check if field is occupied
                        map = place_mark(map[:],  # place ascii art on map
                                         chosen_field,
                                         tic_or_toe)

                        # update needed variables
                        tic_or_toe = update_turn(tic_or_toe)
                        played_moves.append(chosen_field)
                        rounds += 1
                        tic_map = update_tic_map(tic_map[:],
                                                 chosen_field,
                                                 tic_or_toe)

                        # update protocol
                        protocol['move'].append(chosen_field)
                        protocol['time'].append(int(time.time()))

                        # check if a player has won
                        if win_cond(tic_map) == 1:
                            protocol['winner'] = 1
                            game_running = False
                        elif win_cond(tic_map) == 2:
                            protocol['winner'] = 2
                            game_running = False
                        elif rounds >= 9:  # tie
                            game_running = False

            for i in range(map_size): 
                for k in range(map_size):
                    color = white if map[i][k] else black
                    pygame.draw.rect(screen, color, (k * cell_size,
                                                     i * cell_size,
                                                     cell_size, cell_size))
            pygame.display.flip()
        
        game += 1  # update game id
        export(protocol)  # append to csv

        # endscreen holds frame till click
        while endscreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endscreen = False
                    game_running = False
                    main_loop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    endscreen = False
    pygame.quit()


def get_game():
    """get the last game id from the csv."""
    path = 'tic_data.csv'
    if not os.path.exists(path):
        return 0
    df = pd.read_csv(path)
    return df['game'].iloc[-1]


def win_cond(tic_map: []):
    """check if a player has won."""
    # rows and columns
    for i in range(3):
        if tic_map[i][0] == tic_map[i][1] == tic_map[i][2] != 0:
            return tic_map[i][0]
        if tic_map[0][i] == tic_map[1][i] == tic_map[2][i] != 0:
            return tic_map[0][i]

    # diagonal
    if tic_map[0][0] == tic_map[1][1] == tic_map[2][2] != 0:
        return tic_map[0][0]
    if tic_map[0][2] == tic_map[1][1] == tic_map[2][0] != 0:
        return tic_map[0][2]

    # no winner yet
    return 0


def export(protocol):
    """append to csv."""
    header = True
    path = 'tic_data.csv'
    if os.path.exists(path):
        header = False
    df = pd.DataFrame(protocol)
    df.to_csv(path, mode="a", index=False, header=header)


def update_turn(turn: bool):
    """flip whose turn it is."""
    return not turn


def update_tic_map(tic_map: [], move: [], turn: bool):
    """add last move to the tic map."""
    if turn:
        tic_map[move[0]][move[1]] = 2  # tic
    else:
        tic_map[move[0]][move[1]] = 1  # tac
    return tic_map


def new_map(size_x: int, size_y: int) -> []:
    """create new map."""
    grid = []
    for i in range(size_y):
        grid.append([])
        for k in range(size_x):
            grid[i].append(True)
    return grid


def flip(canvas: [], bit_map: []) -> []:
    """flip all pixel colors defined in the bitmap."""
    for bit in bit_map:
        if canvas[bit[0]][bit[1]] is True:
            canvas[bit[0]][bit[1]] = False
        else:
            canvas[bit[0]][bit[1]] = True
    return canvas


def import_art(s):
    """get bit map from ascii art."""
    bit_map = []
    rows = s.split('\n')
    rows = rows[1:-1]
    for x, row in enumerate(rows):
        for y, c in enumerate(row):
            if c == '#':
                bit_map.append([x, y])
    return bit_map


def get_field(coords: int):
    """get which field was clicked on."""
    window_l = map_size * cell_size
    field = []
    for c in coords:
        for k in range(3):
            if c < window_l / 3 * (k + 1):
                field.append(k)
                break
    return field


def place_mark(map: [], coords: int, turn: bool):
    """place bit_map at the specified field."""
    y = coords[0] * 3
    x = coords[1] * 3
    art = []

    if turn:
        art = import_art(tic)
    else:
        art = import_art(tac)

    for px in art:
        px[0] += x
        px[1] += y
    return flip(map[:], art)


if __name__ == "__main__":
    main()
