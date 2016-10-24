#ifndef COST_SATURATION_ABSTRACTION_GENERATOR_H
#define COST_SATURATION_ABSTRACTION_GENERATOR_H

#include "types.h"

#include <memory>
#include <vector>

class AbstractTask;

namespace cost_saturation {
class Abstraction;

class AbstractionGenerator {
public:
    virtual std::vector<AbstractionAndStateMap> generate_abstractions(
        const std::shared_ptr<AbstractTask> &task) = 0;
};
}

#endif
