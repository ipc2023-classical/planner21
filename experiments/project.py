from collections import namedtuple, defaultdict
from pathlib import Path
from lab import tools
from downward.reports.absolute import AbsoluteReport
from downward.reports import PlanningReport
import getpass
import platform
import os
import re
import subprocess
import sys

User = namedtuple("User", ["scp_login", "remote_repo"])

small_proj = User(
    scp_login="x_pauho@tetralith.nsc.liu.se",
    remote_repo="/proj/snic2021-22-825/users/x_pauho/downward-projects",
)

dfsplan = User(
    scp_login="x_pauho@tetralith.nsc.liu.se",
    remote_repo="/proj/dfsplan/users/x_pauho",
)

try:
    DOWNWARD_DIR = Path(os.environ["DOWNWARD_REPO"])
except KeyError:
    sys.exit(
        "Error: the DOWNWARD_REPO environment variable must point to a Fast Downward"
        " repo."
    )

try:
    SCORPION_DIR = Path(os.environ["SCORPION_REPO"])
except KeyError:
    sys.exit(
        "Error: the SCORPION_REPO environment variable must point to a SCORPION repo."
    )


def load_env_var(env_var):
    try:
        return os.environ[env_var]
    except KeyError:
        sys.exit(f"Error: the environment variable {env_var} is not defined")


def get_repo_base() -> Path:
    """Get base directory of the repository, as an absolute path.

    Search upwards in the directory tree from the main script until a
    directory with a subdirectory named ".git" is found.

    Abort if the repo base cannot be found."""
    path = Path(tools.get_script_path())
    while path.parent != path:
        if (path / ".git").is_dir():
            return path
        path = path.parent
    sys.exit("repo base could not be found")


DOMAINS_DIR = load_env_var("DOWNWARD_BENCHMARKS")


DIR = Path(__file__).resolve().parent
NODE = platform.node()
REMOTE = re.match(r"tetralith\d+\.nsc\.liu\.se|n\d+", NODE)

EXP_NAME = Path(__file__).stem

SAS_BENCHMARK_DIR = "/proj/dfsplan/ragnarok/sas"

SUITE_OPTIMAL_STRIPS = [
    "agricola-opt18-strips",
    "airport",
    "barman-opt11-strips",
    "barman-opt14-strips",
    "blocks",
    "childsnack-opt14-strips",
    "data-network-opt18-strips",
    "depot",
    "driverlog",
    "elevators-opt08-strips",
    "elevators-opt11-strips",
    "floortile-opt11-strips",
    "floortile-opt14-strips",
    "freecell",
    "ged-opt14-strips",
    "grid",
    "gripper",
    "hiking-opt14-strips",
    "logistics00",
    "logistics98",
    "miconic",
    "movie",
    "mprime",
    "mystery",
    "nomystery-opt11-strips",
    "openstacks-opt08-strips",
    "openstacks-opt11-strips",
    "openstacks-opt14-strips",
    "openstacks-strips",
    "organic-synthesis-opt18-strips",
    "organic-synthesis-split-opt18-strips",
    "parcprinter-08-strips",
    "parcprinter-opt11-strips",
    "parking-opt11-strips",
    "parking-opt14-strips",
    "pathways",
    "pegsol-08-strips",
    "pegsol-opt11-strips",
    "petri-net-alignment-opt18-strips",
    "pipesworld-notankage",
    "pipesworld-tankage",
    "psr-small",
    "rovers",
    "satellite",
    "scanalyzer-08-strips",
    "scanalyzer-opt11-strips",
    "snake-opt18-strips",
    "sokoban-opt08-strips",
    "sokoban-opt11-strips",
    "spider-opt18-strips",
    "storage",
    "termes-opt18-strips",
    "tetris-opt14-strips",
    "tidybot-opt11-strips",
    "tidybot-opt14-strips",
    "tpp",
    "transport-opt08-strips",
    "transport-opt11-strips",
    "transport-opt14-strips",
    "trucks-strips",
    "visitall-opt11-strips",
    "visitall-opt14-strips",
    "woodworking-opt08-strips",
    "woodworking-opt11-strips",
    "zenotravel",
]

SUITE_OPTIMAL_STRIPS_DEBUG = [
    "airport:p01-airport1-p1.pddl",
    "blocks:probBLOCKS-4-0.pddl",
    "data-network-opt18-strips:p01.pddl",
    "depot:p01.pddl",
    "driverlog:p01.pddl",
    "elevators-opt11-strips:p01.pddl",
    "freecell:p01.pddl",
    "ged-opt14-strips:d-1-2.pddl",
    "grid:prob01.pddl",
    "gripper:prob01.pddl",
    "hiking-opt14-strips:ptesting-1-2-3.pddl",
    "logistics00:probLOGISTICS-4-0.pddl",
    "miconic:s1-0.pddl",
    "mprime:prob01.pddl",
    "mystery:prob01.pddl",
    "organic-synthesis-opt18-strips:p01.pddl",
    "parcprinter-opt11-strips:p01.pddl",
    "pathways:p01.pddl",
    "pegsol-opt11-strips:p01.pddl",
    "petri-net-alignment-opt18-strips:p01.pddl",
    "pipesworld-notankage:p01-net1-b6-g2.pddl",
    "pipesworld-tankage:p01-net1-b6-g2-t50.pddl",
    "psr-small:p01-s2-n1-l2-f50.pddl",
    "rovers:p01.pddl",
    "satellite:p01-pfile1.pddl",
    "scanalyzer-opt11-strips:p01.pddl",
    "sokoban-opt11-strips:p01.pddl",
    "spider-opt18-strips:p01.pddl",
    "storage:p01.pddl",
    "termes-opt18-strips:p01.pddl",
    "tpp:p01.pddl",
    "transport-opt14-strips:p01.pddl",
    "trucks-strips:p01.pddl",
    "visitall-opt14-strips:p-1-5.pddl",
    "woodworking-opt11-strips:p01.pddl",
    "zenotravel:p01.pddl",
]


SUITE_TEST = [
    "agricola-opt18-strips",
    "airport",
    "barman-opt11-strips",
    "barman-opt14-strips",
    "blocks",
    "childsnack-opt14-strips",
    "data-network-opt18-strips",
    "depot",
    "driverlog",
    "elevators-opt08-strips",
    "elevators-opt11-strips",
    "floortile-opt11-strips",
    "floortile-opt14-strips",
    "freecell",
    "ged-opt14-strips",
    "grid",
    "gripper",
    "hiking-opt14-strips",
    "logistics00",
    "logistics98",
    "miconic",
    "movie",
    "mprime",
    "mystery",
    "nomystery-opt11-strips",
    "openstacks-opt08-strips",
    "openstacks-opt11-strips",
    "openstacks-opt14-strips",
    "openstacks-strips",
    "organic-synthesis-opt18-strips",
    "organic-synthesis-split-opt18-strips",
    "parcprinter-08-strips",
    "parcprinter-opt11-strips",
    "parking-opt11-strips",
    "parking-opt14-strips",
    "pathways",
    "pegsol-08-strips",
    "pegsol-opt11-strips",
    "petri-net-alignment-opt18-strips",
    "pipesworld-notankage",
    "pipesworld-tankage",
    "psr-small",
    "rovers",
    "satellite",
    "scanalyzer-08-strips",
    "scanalyzer-opt11-strips",
    "snake-opt18-strips",
    "sokoban-opt08-strips",
    "sokoban-opt11-strips",
    "spider-opt18-strips",
    "storage",
    "termes-opt18-strips",
    "tetris-opt14-strips",
    "tidybot-opt11-strips",
    "tidybot-opt14-strips",
    "tpp",
    "transport-opt08-strips",
    "transport-opt11-strips",
    "transport-opt14-strips",
    "trucks-strips",
    "visitall-opt11-strips",
    "visitall-opt14-strips",
    "woodworking-opt08-strips",
    "woodworking-opt11-strips",
    "zenotravel",
    "airport-adl",
    "caldera-split-opt18-adl",
]


def open_report(exp, outfile: Path):
    outfile = Path(exp.eval_dir) / outfile
    exp.add_step(
        f"open-{outfile.name.split('.')[0]}", subprocess.call, ["xdg-open", outfile]
    )


def _get_exp_dir_relative_to_repo():
    repo_name = get_repo_base().name
    script = Path(tools.get_script_path())
    script_dir = script.parent
    rel_script_dir = script_dir.relative_to(get_repo_base())
    expname = script.stem
    return repo_name / rel_script_dir / "data" / expname


def add_scp_step(exp, login, repos_dir):
    remote_exp = Path(repos_dir) / _get_exp_dir_relative_to_repo()
    exp.add_step(
        "scp-eval-dir",
        subprocess.call,
        [
            "scp",
            "-r",  # Copy recursively.
            "-C",  # Compress files.
            f"{login}:{remote_exp}-eval",
            f"{exp.path}-eval",
        ],
    )


def add_absolute_report(exp, *, name=None, outfile=None, **kwargs):
    report = AbsoluteReport(**kwargs)
    if name and not outfile:
        outfile = f"{name}.{report.output_format}"
    elif outfile and not name:
        name = Path(outfile).name
    elif not name and not outfile:
        name = f"{exp.name}-abs"
        outfile = f"{name}.{report.output_format}"

    if not Path(outfile).is_absolute():
        outfile = Path(exp.eval_dir) / outfile

    exp.add_report(report, name=name, outfile=outfile)
    if not REMOTE:
        exp.add_step(f"open-{name}", subprocess.call, ["xdg-open", outfile])


class Hardest10Report(PlanningReport):
    """
    Keep the 10 tasks from each domain that are solved by the fewest number of planners.
    """

    def get_text(self):
        solved_by = defaultdict(int)
        for run in self.props.values():
            if run.get("coverage"):
                solved_by[(run["domain"], run["problem"])] += 1
        hardest_tasks = {}
        for domain, problems in sorted(self.domains.items()):
            solved_problems = [
                problem for problem in problems if solved_by[(domain, problem)] > 0
            ]
            solved_problems.sort(key=lambda problem: solved_by[(domain, problem)])
            hardest_tasks[domain] = set(solved_problems[:10])
        for domain, problems in sorted(self.domains.items()):
            print(domain, len(problems), len(hardest_tasks[domain]))
        new_props = tools.Properties()
        for key, run in self.props.items():
            if run["problem"] in hardest_tasks[run["domain"]]:
                new_props[key] = run
        return str(new_props)
