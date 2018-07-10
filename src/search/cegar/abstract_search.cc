#include "abstract_search.h"

#include "abstract_state.h"
#include "transition_system.h"
#include "utils.h"

#include "../utils/memory.h"

#include <cassert>

using namespace std;

namespace cegar {
AbstractSearch::AbstractSearch(
    const vector<int> &operator_costs)
    : operator_costs(operator_costs) {
}

void AbstractSearch::reset(int num_states) {
    open_queue.clear();
    search_info.resize(num_states);
    for (AbstractSearchInfo &info : search_info) {
        info.reset();
    }
}

vector<int> AbstractSearch::get_g_values() const {
    vector<int> g_values;
    g_values.reserve(search_info.size());
    for (const AbstractSearchInfo &info : search_info) {
        g_values.push_back(info.get_g_value());
    }
    return g_values;
}

unique_ptr<Solution> AbstractSearch::find_solution(
    const vector<Transitions> &transitions,
    const AbstractStates &states, int init_id, const Goals &goal_ids) {
    assert(transitions.size() == states.size());
    int num_states = states.size();
    reset(num_states);
    for (int state_id = 0; state_id < num_states; ++state_id) {
        search_info[state_id].increase_h_value_to(
            states[state_id]->get_goal_distance_estimate());
    }
    search_info[init_id].decrease_g_value_to(0);
    open_queue.push(search_info[init_id].get_h_value(), init_id);
    int goal_id = astar_search(transitions, true, &goal_ids);
    open_queue.clear();
    bool has_found_solution = (goal_id != UNDEFINED);
    if (has_found_solution) {
        return extract_solution(init_id, goal_id);
    }
    return nullptr;
}

vector<int> AbstractSearch::compute_distances(
    const vector<Transitions> &transitions, const unordered_set<int> &start_ids) {
    reset(transitions.size());
    for (int goal_id : start_ids) {
        search_info[goal_id].decrease_g_value_to(0);
        open_queue.push(0, goal_id);
    }
    astar_search(transitions, false);
    open_queue.clear();
    return get_g_values();
}

int AbstractSearch::astar_search(
    const vector<Transitions> &transitions, bool use_h, const Goals *goals) {
    assert((use_h && goals) || (!use_h && !goals));
    while (!open_queue.empty()) {
        pair<int, int> top_pair = open_queue.pop();
        int old_f = top_pair.first;
        int state_id = top_pair.second;

        const int g = search_info[state_id].get_g_value();
        assert(0 <= g && g < INF);
        int new_f = g;
        if (use_h)
            new_f += search_info[state_id].get_h_value();
        assert(new_f <= old_f);
        if (new_f < old_f)
            continue;
        if (goals && goals->count(state_id) == 1) {
            open_queue.clear();
            return state_id;
        }
        assert(utils::in_bounds(state_id, transitions));
        for (const Transition &transition : transitions[state_id]) {
            int op_id = transition.op_id;
            int succ_id = transition.target_id;

            assert(utils::in_bounds(op_id, operator_costs));
            const int op_cost = operator_costs[op_id];
            assert(op_cost >= 0);
            int succ_g = (op_cost == INF) ? INF : g + op_cost;
            assert(succ_g >= 0);

            if (succ_g < search_info[succ_id].get_g_value()) {
                search_info[succ_id].decrease_g_value_to(succ_g);
                int f = succ_g;
                if (use_h) {
                    int h = search_info[succ_id].get_h_value();
                    if (h == INF)
                        continue;
                    f += h;
                }
                assert(f >= 0);
                assert(f != INF);
                open_queue.push(f, succ_id);
                search_info[succ_id].set_incoming_transition(Transition(op_id, state_id));
            }
        }
    }
    return UNDEFINED;
}

unique_ptr<Solution> AbstractSearch::extract_solution(int init_id, int goal_id) const {
    unique_ptr<Solution> solution = utils::make_unique_ptr<Solution>();
    int current_id = goal_id;
    while (current_id != init_id) {
        const Transition &prev = search_info[current_id].get_incoming_transition();
        solution->emplace_front(prev.op_id, current_id);
        assert(prev.target_id != current_id);
        current_id = prev.target_id;
    }
    return solution;
}
}
