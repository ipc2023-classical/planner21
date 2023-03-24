from lab.reports import Attribute, geometric_mean, arithmetic_mean

EVALUATIONS_PER_TIME = Attribute(
    "evaluations_per_time", min_wins=False, function=geometric_mean, digits=1
)

CACHE_RATIO = Attribute(
    "cache_hits_ratio", absolute=True, min_wins=False, function=arithmetic_mean
)


def add_evaluations_per_time(run):
    evaluations = run.get("evaluations")
    time = run.get("search_time")
    if evaluations is not None and evaluations >= 100 and time:
        run["evaluations_per_time"] = evaluations / time
    return run


def cached_ratio(run):
    evaluations = run.get("evaluations")
    cache_hits = run.get("cache_hits")
    if evaluations is not None and cache_hits is not None and evaluations != 0:
        run["cache_hits_ratio"] = cache_hits / evaluations
    return run
