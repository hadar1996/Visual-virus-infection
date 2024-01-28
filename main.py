import time

import numpy as np
import pygame as pg
from human import *
import random
import sys

# Initialize game window --------------------
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
# Colors of the grid:
WHITE = (255, 255, 255)  # Empty
GREEN = (127, 255, 0)  # Vaccine, 1
RED = (220, 60, 20)  # Sick, 2
BLUE = (0, 0, 255)  # Healthy, 3
N = 50
T = int(sys.argv[3])
# PV << PI, 0<P<1
PI = float(sys.argv[1])  # Probability that infected infect healthy
PV = float(sys.argv[2])  # Probability that infected infect vaccined
pg.init()
screenSize = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pg.display.set_mode(screenSize)
pg.display.set_caption("Covid-19")
screen.fill(WHITE)
pg.display.flip()


def drawGrid(matrix):
    blockSize = 10  # Set the size of the grid block
    i = 0  # Rows of matrix
    j = 0  # Columns of matrix
    for y in range(3, WINDOW_WIDTH, blockSize + 3):
        for x in range(3, WINDOW_HEIGHT, blockSize + 3):
            rect = pg.Rect(x, y, blockSize, blockSize)
            try:
                if matrix[i][j] == 0:
                    pg.draw.rect(screen, WHITE, rect)
                    pg.display.flip()
                elif matrix[i][j] == 1:
                    pg.draw.rect(screen, GREEN, rect)
                    pg.display.flip()
                elif matrix[i][j] == 2:
                    pg.draw.rect(screen, RED, rect)
                    pg.display.flip()
                elif matrix[i][j] == 3:
                    pg.draw.rect(screen, BLUE, rect)
                    pg.display.flip()
            except:
                pg.draw.rect(screen, WHITE, rect)

            j = j + 1
        j = 0
        i = i + 1


# Function to get the next step for each person
def get_next_location(matrix, current_loc, direction):
    if (current_loc[0] + direction[0]) < 0 or (current_loc[0] + direction[0]) >= len(matrix) or (
            current_loc[1] + direction[1]) < 0 or \
            (current_loc[1] + direction[1]) >= len(matrix) or (current_loc[0] + direction[1]) < 0 or \
            (current_loc[0] + direction[1]) >= len(matrix) or (current_loc[1] + direction[0]) < 0 or \
            (current_loc[1] + direction[0]) >= len(matrix):
        step = ((current_loc[0] + direction[1]) % len(matrix), (current_loc[1] + direction[0]) % len(matrix))
    else:
        step = ((current_loc[0] + direction[0]) % len(matrix), (current_loc[1] + direction[1]) % len(matrix))
    return step


# Function to update the matrix to each Generation
def update(matrix, people):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            curr_loc = (i, j)
            if matrix[curr_loc[0]][curr_loc[1]] != 0:
                # Check person with surroundings
                # 1, PI
                # 3, PV
                human = get_human_by_location(people, curr_loc)
                if human.state != STATE_SICK and is_infected(human, matrix):
                    # print("{} Got sick".format(human))
                    matrix[curr_loc[0]][curr_loc[1]] = STATE_SICK
                    human.state = STATE_SICK
                direction = (random.randrange(-1, 2), random.randrange(-1, 2))
                next_loc = get_next_location(matrix, curr_loc, direction)
                # This is to check that a person is not in a place (i,j)
                while matrix[next_loc[0]][next_loc[1]] != 0:
                    direction = (random.randrange(-1, 2), random.randrange(-1, 2))
                    next_loc = get_next_location(matrix, curr_loc, direction)
                matrix[curr_loc[0]][curr_loc[1]] = 0
                matrix[next_loc[0]][next_loc[1]] = human.state
                human.current_index = next_loc
                if human.t == T:
                    human.state = STATE_VACCINATED
                    matrix[next_loc[0]][next_loc[1]] = STATE_VACCINATED
                    human.t = 0
                if human.state == STATE_SICK:
                    human.t += 1

    # Todo: more checks for example T to get vaccinated
    # Todo: When to stop game percentage vaccined and print

    return matrix, people


def get_human_by_location(people, loc):
    humans = [human for human in people if human.current_index == loc]
    if len(humans) == 0:
        raise IndexError
    return humans[0]


def get_surroundings(human, matrix):
    indexes = [get_next_location(matrix, human.current_index, (1, 0)),
               get_next_location(matrix, human.current_index, (0, 1)),
               get_next_location(matrix, human.current_index, (1, 1)),
               get_next_location(matrix, human.current_index, (1, -1)),
               get_next_location(matrix, human.current_index, (-1, 1)),
               get_next_location(matrix, human.current_index, (-1, 0)),
               get_next_location(matrix, human.current_index, (0, -1)),
               get_next_location(matrix, human.current_index, (-1, -1))]
    return [matrix[index[0]][index[1]] for index in indexes]


def is_infected(human, matrix):
    """

    :param human:
    :param matrix:
    :return:
    """
    probability = 0
    if human.state == STATE_HEALTHY:
        probability = PI
    elif human.state == STATE_VACCINATED:
        probability = PV
    flag = 0
    surroundings = get_surroundings(human, matrix)
    probability *= 100
    for neighbor in surroundings:
        if neighbor == STATE_SICK:
            if random.randrange(1, 101) <= probability:
                flag = 1
    return flag == 1


if __name__ == '__main__':
    people = []
    numbers = [0, 1, 2, 3]
    c = 0
    matrix = [[np.random.choice(numbers) for y in range(N)] for x in range(N)]

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != 0:
                people.append(Human((i, j), matrix[i][j]))

    finish = False
    while not finish:
        vaccinated = [person for person in people if person.state == STATE_VACCINATED]
        ratio = len(vaccinated) / len(people)
        if ratio >= 0.8:
            print("Finished with ratio {}".format(ratio))
            print("Number of turns: {}".format(c))
            finish = True
        drawGrid(matrix)
        matrix, people = update(matrix, people)
        c += 1
        #time.sleep(1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finish = True
    pg.quit()

