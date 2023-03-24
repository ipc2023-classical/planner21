from lab.fetcher import Fetcher
import sys
from collections import defaultdict
from lab.reports import Attribute, geometric_mean, arithmetic_mean


def check_opcount_spho(exp):
    props = Fetcher().fetch_dir(exp.eval_dir)
    for prop in props:
        if "algorithm" in props[prop]:
            alg_data = props[prop]
            if (alg_data["algorithm"] in ["tuple", "flipped-tuple", "max_cluster"]):
                if (alg_data["cache_hits"] > alg_data["evaluations"]):
                    sys.exit("cache hits more than evaluation")
    print("all checks passed")


class DominanceFilters:
    algorithm_order = {"always": "always", "tuple": "tuple", "max_cluster": "tuple",
                       "range_sa": "max_cluster", "percent_sa": "range_sa"}

    def __init__(self, attribute, inverse_order=False):
        self.tasksalgs_to_property = defaultdict(
            lambda: sys.maxsize if inverse_order else 0)
        self.attribute = attribute
        self.key = f"{attribute}-ok"
        self.inverse_order = inverse_order

    def _get_task(self, run):
        return (run["domain"], run["problem"])

    def store_attribute(self, run):
        attr_value = run.get(self.attribute)
        if attr_value is not None:
            self.tasksalgs_to_property[(run.get("algorithm"),
                                        self._get_task(run))] = attr_value
        return True

    def compute_dominance(self, run):
        attr_value = run.get(self.attribute)
        if attr_value is not None:
            if not self.inverse_order:
                run[self.key] = run.get(self.attribute) >= self.tasksalgs_to_property[(
                    self.algorithm_order[run["algorithm"]], self._get_task(run))]
            else:
                run[self.key] = run.get(self.attribute) <= self.tasksalgs_to_property[(
                    self.algorithm_order[run["algorithm"]], self._get_task(run))]
        return run

    def get_attribute(self):
        return Attribute(self.key, absolute=True, min_wins=None, function=all)
