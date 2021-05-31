from collections import Counter
import database
import itertools


RECIPE_AMOUNT = 4


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
