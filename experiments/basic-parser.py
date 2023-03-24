from common_parser import CommonParser


def main():
    parser = CommonParser()
    parser.add_bottom_up_pattern(
        "search_start_time",
        r"\[t=(.+)s, \d+ KB\] g=0, 1 evaluated, 0 expanded",
        type=float,
    )
    parser.add_bottom_up_pattern(
        "search_start_memory",
        r"\[t=.+s, (\d+) KB\] g=0, 1 evaluated, 0 expanded",
        type=int,
    )
    parser.add_pattern(
        "initial_h_value",
        r"f = (\d+) \[1 evaluated, 0 expanded, t=.+s, \d+ KB\]",
        type=int,
    )
    parser.add_repeated_pattern(
        "h_values",
        r"New best heuristic value for .+: (\d+)\n",
        type=int,
    )
    parser.parse()


if __name__ == "__main__":
    main()
