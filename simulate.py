from abc import ABC, abstractmethod
from numbers import Number
import time
import random
from statistics import mean
from typing import List, Type
from grid import GridFactory, Drone, Path, Grid


class Strategy(ABC):
    @abstractmethod
    def tick(self, grid: Grid, drone: Drone) -> None:
        pass


class Greedy(Strategy):
    def tick(self, grid, drone):
        possible_planes = grid.adjacent(drone.current_plane)
        best_plane = None
        best_reward = 0
        for plane in possible_planes:
            reward = plane.current_value
            if reward > best_reward:
                best_reward = reward
                best_plane = plane
        drone.move(best_plane)


class Random(Strategy):
    def tick(self, grid, drone):
        possible_planes = grid.adjacent(drone.current_plane)
        chosen_plane = random.choice(possible_planes)
        drone.move(chosen_plane)


class LookAhead(Strategy):
    def tick(self, grid, drone):
        possible_planes = grid.adjacent(drone.current_plane)
        best_plane = None
        best_reward = 0
        for plane in possible_planes:
            reachable_next_tick = grid.adjacent(plane)
            reachable_values_next_tick = [e.value_next_tick() for e in reachable_next_tick]
            avg_value_for_plane = mean(reachable_values_next_tick) + plane.current_value
            if avg_value_for_plane > best_reward:
                best_reward = avg_value_for_plane
                best_plane = plane
        drone.move(best_plane)


class Runner:
    def __init__(self, grid_factory: GridFactory, max_time: Number, max_steps: int, strategy: Type[Strategy]):
        self.grid_factory = grid_factory
        self.max_time = max_time
        self.max_steps = max_steps
        self.strategy = strategy

    def start(self, t_0: float) -> List[Path]:
        grid = self.grid_factory.new_grid()
        num_steps = 0
        strategy = self.strategy()
        while time.perf_counter() - t_0 < self.max_time and num_steps < self.max_steps:
            for drone in grid.drones:
                strategy.tick(grid, drone)
            grid.tick()
            num_steps += 1 

        return [drone.path for drone in grid.drones]
    
STRATEGY_MAP = {
    'random': Random,
    'greedy': Greedy,
    'look-ahead': LookAhead,
}
