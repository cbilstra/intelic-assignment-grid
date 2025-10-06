import argparse
import time
import multiprocessing as mp
from typing import List, Tuple
from dotenv import load_dotenv
from os import getenv

from grid import GridFactory
from simulate import STRATEGY_MAP, Runner

load_dotenv()


def parse_starting_position(value: str) -> List[Tuple[int, int]]:
    try:
        tuples = value.split("%")
        res = []
        for tup in tuples:
            x_str, y_str = tup.split(',')
            res.append((int(x_str), int(y_str)))
        return res
    except:
        raise argparse.ArgumentTypeError("Starting position must be in the format <int>,<int>%<int>,<int>%...")

def main():
    parser = argparse.ArgumentParser(
        description="Simulate drone movement on a grid with defined number of steps and duration."
    )

    parser.add_argument(
        "grid_size",
        type=int,
        choices=[20,100,1000],
        help="Size of the grid (e.g., 20 for a 20x20 grid)"
    )

    parser.add_argument(
        "num_steps",
        type=int,
        help="Number of steps to simulate"
    )

    parser.add_argument(
        "max_duration",
        type=float,
        help="Maximum duration of the simulation in seconds"
    )

    parser.add_argument(
        "starting_positions",
        type=parse_starting_position,
        help="Starting position on the grid as <int>,<int>%<int>,<int>%.. (e.g., 3,4%4,5)"
    )

    parser.add_argument(
        '--strategy',
        choices=STRATEGY_MAP.keys(),
        required=True,
        help="Strategy to use: 'random', 'greedy', or 'smart'"
    )


    args = parser.parse_args()
    print(f"Grid size: {args.grid_size}")
    print(f"Number of steps: {args.num_steps}")
    print(f"Max duration: {args.max_duration}")
    print(f"Starting positions: {args.starting_positions}")
    print(f"Strategy: {args.strategy}")
    run(args)

def run(args):
    num_workers = int(getenv("NUM_WORKERS"))
    print(f"Num Workers: {num_workers}")

    t_0 = time.perf_counter()
    grid_factory = GridFactory.from_file(args.grid_size, args.starting_positions)
    runner = Runner(grid_factory, args.max_duration, args.num_steps, STRATEGY_MAP[args.strategy])
    pool = mp.Pool(num_workers)
    paths_per_worker = pool.map(runner.start, [t_0]*num_workers)

    max_score = 0
    for i, paths in enumerate(paths_per_worker):
        print(f"\nworker {i+1}")
        total_score = 0
        for path in paths:
            path.print()
            total_score += path.score()
            print()
        print(f'With a total score of {total_score}')

        if max_score < total_score:
            max_score = total_score

    print(f"And a max score of {max_score}")


if __name__ == "__main__":
    main()
