OPTIMAL = True

SAS_FILE = "output.sas"

def get_pddl_features(task):
    has_axioms = False
    has_conditional_effects = False
    with open(task) as f:
        in_op = False
        for line in f:
            line = line.strip()
            if line == "begin_rule":
                has_axioms = True
            if line == "begin_operator":
                in_op = True
            elif line == "end_operator":
                in_op = False
            elif in_op:
                parts = line.split()
                if len(parts) >= 6 and all(p.lstrip('-').isdigit() for p in parts):
                    print(f"Task has at least one conditional effect: {line}")
                    has_conditional_effects = True
    return has_axioms, has_conditional_effects

has_axioms, has_conditional_effects = get_pddl_features(SAS_FILE)


if has_axioms:
    CONFIGS = [
    (
        1,
        ['--search', 'astar(blind())']
    )
]
else:
    if has_conditional_effects:
        ABSTRACTIONS = (
            "[projections(sys_scp(max_time=200,"
            " max_time_per_restart=10,create_complete_transition_system=true),create_complete_transition_system=true)]"
        )
    else:
        ABSTRACTIONS = (
            "[projections(sys_scp(max_time=200,"
            " max_time_per_restart=10)),cartesian(max_time=200,verbosity=silent)]"
        )
    CONFIGS = [
    (
        1,
        [
            "--search",
            f"astar(operatorcounting([pho_abstraction_constraints({ABSTRACTIONS},strategy=max_cluster)],cache_lp=true),verbosity=silent)",
        ],
    )
]
