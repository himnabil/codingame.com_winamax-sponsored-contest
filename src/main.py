import sys
import math
from functools import lru_cache
from typing import Iterable, Tuple
from collections.abc import Sequence
from copy import copy

def debug (msg):
    print(msg , file= sys.stderr )



directions_str = ('v', '<', '>' ,'^')
directions_diff = ((0,1), (-1,0), (1,0), (0,-1))
balls_str = "123456789"
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


Ball = Tuple[int, int, int, bool]
Mutation = Tuple[int, int, str]


width, height = [int(i) for i in input().split()]
grid_in = ""
balls_in = []

for y in range(height):
    row = input()
    debug(row)
    row_balls = [(x, y, int(row[x]), False) for x in range(len(row)) if row[x] in balls_str]
    balls_in += row_balls
    clean_row = "".join([ '.' if c in balls_str else c for c in row ])
    grid_in += clean_row + '\n'
balls_in.sort(key = lambda b: b[2] ,reverse= False)
balls_in = tuple(balls_in)


grid_out = ('.' * width + '\n') * height

@lru_cache(maxsize= None)
def grid_mutat( grid : str, mutations : Iterable[Mutation] ) -> str :
    l = list(grid)
    for mutation in mutations :
        x, y, c = mutation
        l[ y * (width + 1) + x] = c 
    return "".join(l)

    

@lru_cache(maxsize=None)
def grid_at( grid : str ) :
    @lru_cache(maxsize=None)
    def at(x: int, y: int) :
        return grid [ y*(width + 1) +x ]
    return at 

terrain_at = grid_at(grid_in)

@lru_cache(maxsize=None)
def ball_grid_of (balls: Iterable[Ball]) -> str:
    grid = ('.' * width + '\n') * height
    mutations = ((x, y ,"B") for (x, y,_,_) in balls )
    return grid_mutat(grid , mutations)

@lru_cache(maxsize=None)
def do_move (world: tuple[str, Sequence[Ball]] , m: tuple[int,int]):
    grid, balls = world
    ball_index , direction = m
    x, y, shot_counter, _ = balls [ball_index]
    dx , dy = directions_diff[direction]
    dirertion_str = directions_str[direction]
    
    target_x = x + shot_counter * dx
    target_y = y + shot_counter * dy

    if target_x >= width or target_x < 0 or target_y >= height or target_y < 0 :
        return None

    if terrain_at(target_x, target_y) == "X" :
        return None

    ball_grid = ball_grid_of(balls)
    ball_at = grid_at(ball_grid)
    path_at = grid_at(grid)
    
    mutations = []
    step = 1
    if not (path_at(x, y) == '.'):
        return None
        
    while step < shot_counter :
        if step > 0 and not (ball_at(x, y) == '.'):
            return None
        
        if not (path_at(x, y) == '.'):
            return None
        
        if terrain_at(x, y) ==  "H": 
            return None
        
        mutations.append((x, y, dirertion_str))
        step += 1
        x += dx
        y += dy
    
    ball_in_hole = terrain_at(x, y) == "H" and ball_at(x,y) == "."

    if shot_counter == 1 and not ball_in_hole :
        return None

    result_grid = grid_mutat(grid, tuple(mutations))
    result_balls = balls_mutat(balls, ball_index, (x, y, shot_counter - 1, ball_in_hole))

    return (result_grid, result_balls)

@lru_cache(maxsize=None)
def balls_mutat(balls: tuple[Ball], index: int, ball: Ball):
    balls_list = list(balls)
    balls_list[index] = ball
    balls_list.sort(key = lambda ball : ball[2] , reverse= False)
    return tuple(balls_list)

class Counter :
    def __init__(self):
        self.c = 0
    def __repr__(self) -> str:
        return f'{self.c}'
    def incr(self):
        self.c +=1

counter_solve = Counter()

@lru_cache(maxsize=None)
def solve(world: tuple[str, Sequence[Ball]]) :
    
    if counter_solve.c % 1000 == 0 :
        debug(counter_solve)
    counter_solve.incr()
    grid, balls = world
    balls_count = len(balls)
    #debug( solve.cache_info())
    if all([in_hole for (_,_,_, in_hole) in balls]) :
        return grid
    moves = [(i, d) for i in range(balls_count) if not balls[i][3] for d in range(4)]
    for move in moves :
        next_world = do_move(world , move)
        if next_world is None:
            continue
        result = solve(next_world)
        if result is not None:
            return result
        
    return None

fst_world = (grid_out, balls_in)

result = solve(fst_world)

print(result)
