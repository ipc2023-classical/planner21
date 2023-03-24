from common_parser import CommonParser
from lab.reports import Attribute, geometric_mean, arithmetic_mean

CACHE_HITS = Attribute(
    "cache_hits", absolute=True, min_wins=False, function=geometric_mean, digits=1
)

CACHE_SIZE = Attribute(
    "cache_size", absolute=True, min_wins=False, function=geometric_mean, digits=1
)

ABS_EMPTY = Attribute(
    "abs_empty", absolute=True, min_wins=False, function=arithmetic_mean
)

ABS_DUP = Attribute(
    "abs_dup", absolute=True, min_wins=False, function=arithmetic_mean
)

ABS_USE = Attribute(
    "abs_useful", absolute=True, min_wins=False, function=arithmetic_mean
)


def main():
    parser = CommonParser()
    parser.add_bottom_up_pattern("cache_hits", r"cache hits: (\d+)")
    parser.add_bottom_up_pattern("cache_size", r"cache size: (\d+)")
    parser.add_pattern("abs_empty", r"Empty constraints: (\d+)")
    parser.add_pattern("abs_dup", r"Duplicate constraints: (\d+)")
    parser.add_pattern("abs_useful", r"Useful constraints: (\d+)")
    parser.parse()


if __name__ == "__main__":
    main()
