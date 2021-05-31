from collections import Counter
import argparse
import database
import itertools
import json


parser = argparse.ArgumentParser(description='Alchemy bitch.')
parser.add_argument("--path", type=str, help="Config file path.")
args, _ = parser.parse_known_args()


RECIPE_AMOUNT = 4
JSON_KEYS = [
    "inclusion_constraints",
    "exclusion_constraints",
    "quantity_constraints",
    "simulated_element"
]


def _find_subsets(ingredients, n):
    subsets = list(itertools.combinations(ingredients, n))
    for i, subset in enumerate(subsets):
        subsets[i] = list(subset)
        subsets[i].sort()
        subsets[i] = tuple(subsets[i])
    return list(set(subsets))


class AlchemyEngine(object):

    def __init__(self, db: database.Database):
        self.db = db
        self.quantity_constraints = []
        self.inclusion_constraints = []
        self.exclusion_constraints = []

    def add_quantity_constraint(self, eid: int,
                                lower_bound: int,
                                upper_bound: int):
        """Combinations contain a quantity element eid in bound."""
        self.quantity_constraints.append((eid, lower_bound, upper_bound))

    def add_inclusion_constraint(self, eids: tuple):
        """Combinations have to contain at least one element in eid tuple"""
        self.inclusion_constraints.append(eids)

    def add_exclusion_constraint(self, eids: tuple):
        """Combinations cannot contain all elements in eid tuple."""
        self.exclusion_constraints.append(eids)

    def solve(self):
        """Given constraints solve for possible combinations."""
        ingredients = []
        for eid, _, upper_bound in self.quantity_constraints:
            ingredients.extend([eid] * upper_bound)

        possibilities = _find_subsets(ingredients, RECIPE_AMOUNT)

        possibilities_temp = []
        for p in possibilities:
            if p not in self.db.failed_attempts:
                possibilities_temp.append(p)
        possibilities = possibilities_temp

        for eid, lower_bound, _ in self.quantity_constraints:
            possibilities_tmp = []
            for p in possibilities:
                counter = Counter(p)
                if counter[eid] >= lower_bound:
                    possibilities_tmp.append(p)
            possibilities = possibilities_tmp

        for eids in self.inclusion_constraints:
            possibilities_tmp = []
            for p in possibilities:
                if any([eid in p for eid in eids]):
                    possibilities_tmp.append(p)
            possibilities = possibilities_tmp

        for eids in self.exclusion_constraints:
            possibilities_tmp = []
            for p in possibilities:
                if not all([eid in p for eid in eids]):
                    possibilities_tmp.append(p)
            possibilities = possibilities_tmp

        return possibilities


def main():
    # Load config.
    config = json.load(open(args.path))
    assert all(key in config.keys() for key in JSON_KEYS)

    # Construct database.
    db = database.Database(
        csv_path="data/alchemy-table.csv",
        simulated_element=config["simulated_element"]
    )

    # Construct constraints.
    ae = AlchemyEngine(db)
    for constraint in config["inclusion_constraints"]:
        ae.add_inclusion_constraint(constraint)
    for constraint in config["exclusion_constraints"]:
        ae.add_exclusion_constraint(constraint)
    for eid, lb, ub in config["quantity_constraints"]:
        ae.add_quantity_constraint(eid, lb, ub)
    solutions = ae.solve()

    # Output possible solutions.
    for solution in solutions:
        cost = sum([db.element_costs[eid] for eid in solution])
        print(solution, "Cost: %d" % cost)


if __name__ == "__main__":
    main()
