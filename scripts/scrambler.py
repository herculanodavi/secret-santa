import numpy as np
import logging
from person import Person
from typing import Callable


def evaluate_bypass(givers: list[Person], receivers: list[Person]) -> bool:
    return True


def evaluate_groups(givers: list[Person], receivers: list[Person]) -> bool:
    for (g, r) in zip(givers, receivers):
        if g == r:
            logging.debug(
                f"{g.name} and {r.name} are the same person.")
            return False
        if len(g.groups.intersection(r.groups)) == 0:
            logging.debug(
                f"{g.name} and {r.name} don't have a group in common.")
            return False
    return True


def get_evaluator(name: str) -> Callable[[list[Person], list[Person]], bool]:
    if name == 'groups':
        return evaluate_groups
    elif name == 'bypass':
        return evaluate_bypass
    raise ValueError(f'Evaluator with name {name} is not implemented.')


def scramble(people: list[Person], evaluator: str, num_retries=100) -> dict:
    receivers = people.copy()
    evaluate = get_evaluator(evaluator)

    for _ in range(num_retries):
        np.random.shuffle(receivers)
        if (evaluate(people, receivers)):
            return [{
                'giver': g,
                'receiver': r
            } for (g, r) in zip(people, receivers)]

    raise RuntimeError(
        f"Algorithm did not find a solution. Try again with more retries than {num_retries} or change groups.")
