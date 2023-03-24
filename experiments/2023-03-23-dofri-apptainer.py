from lab.experiment import Experiment
from downward.experiment import FastDownwardExperiment
from downward.suites import build_suite
from lab.environments import TetralithEnvironment, LocalEnvironment
import project
import shutil
import checks
import filters
from collections import namedtuple
import suite

SPhOConfig = namedtuple("SPhOConfig", "strategy cache debug")

USER = project.small_proj

if project.REMOTE:
    ENV = TetralithEnvironment(
        email="paul.hoft@liu.se",
        extra_options="#SBATCH -A snic2022-22-1074",
        memory_per_cpu="9G",
    )
    HOURS = 0
    MIN = 15
    TIME_LIMIT = int(HOURS * 60 + MIN)
    MEMORY_LIMIT = 8000
    SUITE = build_suite(project.SAS_BENCHMARK_DIR, project.SUITE_TEST)
else:
    ENV = LocalEnvironment(processes=5)
    HOURS = 0
    MIN = 2
    TIME_LIMIT = int(HOURS * 60 + MIN)
    MEMORY_LIMIT = 2048
    SUITE = build_suite(project.DOMAINS_DIR, project.SUITE_OPTIMAL_STRIPS_DEBUG)

exp = Experiment(environment=ENV)
# exp.add_parser("basic-parser.py")

# Add step that writes experiment files to disk.
exp.add_step("build", exp.build)

# Add step that executes all runs.
exp.add_step("start", exp.start_runs)

# Add step that collects properties from run directories and
# writes them to *-eval/properties.
exp.add_fetcher(name="fetch")

exp.add_parser(FastDownwardExperiment.EXITCODE_PARSER)
exp.add_parser(FastDownwardExperiment.SINGLE_SEARCH_PARSER)
exp.add_parser("basic-parser.py")

image = project.get_repo_base() / "Dofri"

exp.add_resource("dofri", image, symlink=True)
exp.add_resource("", "common_parser.py")


for task in SUITE:
    run = exp.add_run()
    run.add_resource("domain", task.domain_file)
    run.add_resource("problem", task.problem_file)
    run.add_command(
        "planner",
        ["{dofri}", "{domain}", "{problem}", "planfile.out"],
        memory_limit=MEMORY_LIMIT,
    )
    run.set_property("algorithm", "dofri")
    run.set_property("domain", task.domain)
    run.set_property("problem", task.problem)
    run.set_property("id", ["dofri", task.domain, task.problem])

ATTRIBUTES = [
    "error",
    "run_dir",
    "search_start_time",
    "search_start_memory",
    "total_time",
    "h_values",
    "coverage",
    "cost",
    "evaluations",
    "expansions",
    "expansions_until_last_jump",
    "memory",
]

project.add_absolute_report(
    exp, attributes=ATTRIBUTES, filter=[filters.add_evaluations_per_time]
)

exp.add_parse_again_step()


if not project.REMOTE:
    exp.add_step("remove-eval-dir", shutil.rmtree, exp.eval_dir, ignore_errors=True)
    project.add_scp_step(exp, USER.scp_login, USER.remote_repo)

# Parse the commandline and run the given steps.
exp.run_steps()
