import pygame
import time
import pandas as pd

heart = """
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
    ye = True
    while ye:
        game = 0
        turn = True
        played = []
        protocol = {
            'game': game,
            'move': [],
            'time': []
        }
        tic_map = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]
        map = new_map(map_size, map_size)
        map = flip(map[:], import_art(heart))
        pygame.init()
        pygame.display.set_caption("TicTacToe")
        screen = pygame.display.set_mode((map_size * cell_size,
                                          map_size * cell_size))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    chosen = get_field(pygame.mouse.get_pos())
                    if played.count(chosen) <= 0:
                        map = place_mark(map[:],
                                         chosen,
                                         turn)
                        turn = update_turn(turn)
                        played.append(chosen)
                        protocol['move'].append(chosen)
                        protocol['time'].append(time.time())
                        tic_map = update_tic_map(tic_map[:],
                                                 chosen,
                                                 turn)
                        if win_cond(tic_map) == 1:
                            print(1)
                            running = False
                        elif win_cond(tic_map) == 2:
                            print(2)
                            running = False
            for i in range(map_size):
                for k in range(map_size):
                    color = white if map[i][k] else black
                    pygame.draw.rect(screen, color, (k * cell_size,
                                                     i * cell_size,
                                                     cell_size, cell_size))
            pygame.display.flip()
        export(protocol)
        game += 1
    pygame.quit()


def win_cond(tic_map: []):
    for i in range(3):
        if tic_map[i][0] == tic_map[i][1] == tic_map[i][2] != 0:
            return tic_map[i][0]
        if tic_map[0][i] == tic_map[1][i] == tic_map[2][i] != 0:
            return tic_map[0][i]

    if tic_map[0][0] == tic_map[1][1] == tic_map[2][2] != 0:
        return tic_map[0][0]
    if tic_map[0][2] == tic_map[1][1] == tic_map[2][0] != 0:
        return tic_map[0][2]
    return 0


def export(protocol):
    df = pd.DataFrame(protocol)
    df.to_csv('tic_data.csv', mode='a', header=False)


def update_turn(turn: bool):
    return not turn


def update_tic_map(tic_map: [], move: [], turn: bool):
    if turn:
        tic_map[move[0]][move[1]] = 2
    else:
        tic_map[move[0]][move[1]] = 1
    return tic_map


def new_map(size_x: int, size_y: int) -> []:
    grid = []
    for i in range(size_y):
        grid.append([])
        for k in range(size_x):
            grid[i].append(True)
    return grid


def flip(canvas: [], bit_map: []) -> []:
    for bit in bit_map:
        if canvas[bit[0]][bit[1]] is True:
            canvas[bit[0]][bit[1]] = False
        else:
            canvas[bit[0]][bit[1]] = True
    return canvas


def import_art(s):
    code = []
    rows = s.split('\n')
    rows = rows[1:-1]
    for x, row in enumerate(rows):
        for y, c in enumerate(row):
            if c == '#':
                code.append([x, y])
    return code


def get_field(coords: int):
    window_l = map_size * cell_size
    field = []
    for c in coords:
        for k in range(3):
            if c < window_l / 3 * (k + 1):
                field.append(k)
                break
    return field


def place_mark(map: [], coords: int, turn: bool):
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
