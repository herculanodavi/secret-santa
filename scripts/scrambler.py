import numpy as np
import logging
from person import Person
from typing import Callable


def bypass_shuffle(givers: list[Person]) -> dict[Person, Person]:
    return {el: el for el in givers}


def groups_shuffle(givers: list[Person]) -> dict[Person, Person]:
    assigned_givers = {}

    def find_random_match(giver: Person):
        shuffled = np.random.permutation(givers)
        for r in shuffled:
            if giver != r and len(giver.groups.intersection(r.groups)) != 0 and r not in assigned_givers:
                return r
        return None
    
    original_giver = np.random.choice(givers)
    giver = original_giver
    receiver = None

    while len(assigned_givers) < len(givers) - 1:
        receiver = find_random_match(giver)
        assigned_givers[giver] = receiver
        giver = receiver

    assigned_givers[giver] = original_giver

    return assigned_givers


def get_shuffler(name: str) -> Callable[[list[Person]], dict[Person, Person]]:
    if name == 'groups':
        return groups_shuffle
    elif name == 'bypass':
        return bypass_shuffle
    raise ValueError(f'Evaluator with name {name} is not implemented.')


def solve(people: list[Person], evaluator: str, num_retries=100) -> dict:
    receivers = people.copy()
    solver = get_shuffler(evaluator)

    for i in range(num_retries):
        logging.debug(f"Trying permutation {i + 1}")
        assignments = solver(receivers)
        if assignments is not None:
            return [{
                'giver': k,
                'receiver': v
            } for (k, v) in assignments.items()]

    raise RuntimeError(
        f"Algorithm did not find a solution. Try again with more retries than {num_retries} or change groups.")
