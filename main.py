import argparse

def parse_starting_position(value: str):
    try:
        x_str, y_str = value.split(',')
        return int(x_str), int(y_str)
    except ValueError:
        raise argparse.ArgumentTypeError("Starting position must be in the format <int>,<int>")

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
        "starting_position",
        type=parse_starting_position,
        help="Starting position on the grid as <x>,<y> (e.g., 3,4)"
    )

    args = parser.parse_args()

    print(f"Grid size: {args.grid_size}")
    print(f"Number of steps: {args.num_steps}")
    print(f"Max duration: {args.max_duration}")
    print(f"Starting position: {args.starting_position}")

if __name__ == "__main__":
    main()
