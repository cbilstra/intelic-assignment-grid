from copy import deepcopy
from numbers import Number
from itertools import product
import os
from typing import List, Optional, Tuple
from os.path import join


class Plane:
    def __init__(self, x: int, y: int, initial_value: Number):
        self.x = x
        self.y = y
        self.initial_value = initial_value
        self.current_value = self.initial_value

    def visit(self) -> Number:
        res = self.current_value
        self.current_value = 0
        return res

    def tick(self):
        self.current_value = min(self.initial_value, self.current_value + float(os.getenv("OBSERVATION_SCORE_RESTORATION")))

    def __str__(self):
        """Gives y, x (matrix) notation"""
        return f"({self.y},{self.x})"


class Move:
    def __init__(self, old_plane: Optional[Plane], new_plane: Plane, reward: Number):
        self.old_plane = old_plane
        self.new_plane = new_plane
        self.reward = reward

    
class Path:
    def __init__(self, moves: List[Move]):
        self.moves = moves
    
    def score(self) -> Number:
        return sum([move.reward for move in self.moves])
    
    def print(self):
        for move in self.moves:
            print(f"from {move.old_plane} to {move.new_plane} with reward {move.reward}")
        print(f"with a sub score of {self.score()}")


class Drone:
    def __init__(self, start_location: Plane):
        self.start_location = start_location
        self.current_plane = self.start_location
        # NOTE we assume we collect the reward for the start location as well
        self.moves: List[Move] = [Move(None, self.start_location, self.start_location.visit())]  

    def move(self, new_plane: Plane):
        reward = new_plane.visit()  # TODO check no double visit otherwhere
        self.moves.append(Move(self.current_plane, new_plane, reward))
        self.current_plane = new_plane

    @property
    def path(self) -> Path:
        return Path(self.moves)
    

class Grid:
    def __init__(self, planes: List[List[Plane]], drones: List[Drone]):
        self.planes: List[List[Plane]] = planes
        self.drones: List[Drone] = drones
        self.size = len(self.planes)

    def all_planes(self):
        # TODO test
        return [e for row in self.planes for e in row]
    
    def adjacent(self, plane: Plane) -> List[Plane]:
        x_diffs = [0]
        if plane.x != 0:
            x_diffs.append(-1)
        if plane.x != self.size - 1:
            x_diffs.append(1)
        
        y_diffs = [0]
        if plane.y != 0:
            y_diffs.append(-1)
        if plane.y != self.size - 1:
            y_diffs.append(1)

        res = []
        # Cartesian product
        for x_diff, y_diff in product(x_diffs, y_diffs):
            if not (x_diff == 0 and y_diff == 0):
                res.append(self.planes[plane.y + y_diff][plane.x + x_diff])

        # TODO we could test if another drone is not yet in that plane
        return res
    
    def tick(self):
        for plane in self.all_planes():
            plane.tick()

    
class GridFactory:
    def __init__(self, planes: List[List[Plane]], drones: List[Drone]):
        self.original_grid = Grid(planes, drones)

    def new_grid(self) -> Grid:
        return deepcopy(self.original_grid)

    @classmethod
    def from_file(cls, size: int, drone_locations: List[Tuple[int, int]]):
        with open(join('data', f'{size}.txt'), 'r') as file:
            lines = file.readlines()

        rows = []
        for y, line in enumerate(lines):
            if y < size:
                row = []
                elements = line.split(" ")
                for x, reward in enumerate(elements):
                    plane = Plane(x, y, float(reward))
                    row.append(plane)
                assert len(row) == size
                rows.append(row)

        assert len(rows) == size

        drones = [Drone(rows[y][x]) for x, y in drone_locations]
        return cls(rows, drones)
