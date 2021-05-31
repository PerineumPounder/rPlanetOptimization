import pandas as pd


COLUMNS_NAMES = ["number", "first_tried", "id", "ing_1", "ing_2", "ing_3",
                 "ing_4", "result", "total_crafts", "aether_cost"]


class Database(object):

    def __init__(self, csv_path: str, simulated_element=None):
        self.df = pd.read_csv(csv_path, names=COLUMNS_NAMES)
        self.recipes = self._get_recipes()
        if simulated_element is not None:
            number = self.df[
                self.df.result == simulated_element
            ].number.to_list()[0]
            self.df = self.df[self.df.number < number]
        self.element_costs = self._get_element_costs()
        self.element_ids = list(self.element_costs.keys())
        self.failed_attempts = self._get_failed_attempts()

    def _get_element_costs(self):
        """Get discovered elements and aether costs."""
        discoveries = self.df[
            (self.df.result != "-") & (self.df.result != "=")
        ]
        costs = pd.Series(
            discoveries.aether_cost.values,
            index=discoveries.result
        ).to_dict()
        costs["WATER"] = 10000
        costs["EARTH"] = 10000
        costs["FIRE"] = 10000
        costs["AIR"] = 10000
        return costs

    def _get_failed_attempts(self):
        """Get failed attempts at discovering."""
        failures = self.df[
            (self.df.result == "-") | (self.df.result == "=")
        ]
        ing_1 = failures.ing_1.to_list()
        ing_2 = failures.ing_2.to_list()
        ing_3 = failures.ing_3.to_list()
        ing_4 = failures.ing_4.to_list()
        attempts = []
        for i1, i2, i3, i4 in zip(ing_1, ing_2, ing_3, ing_4):
            attempt = [i1, i2, i3, i4]
            attempt.sort()
            attempt = tuple(attempt)
            attempts.append(attempt)
        return attempts

    def _get_recipes(self):
        """Get recipes."""
        discoveries = self.df[
            (self.df.result != "-") & (self.df.result != "=")
        ]
        ing_1 = discoveries.ing_1.to_list()
        ing_2 = discoveries.ing_2.to_list()
        ing_3 = discoveries.ing_3.to_list()
        ing_4 = discoveries.ing_4.to_list()
        results = discoveries.result.to_list()
        recipes = {}
        for i1, i2, i3, i4, result in zip(ing_1, ing_2, ing_3, ing_4, results):
            attempt = [i1, i2, i3, i4]
            attempt.sort()
            attempt = tuple(attempt)
            recipes[result] = attempt
        return recipes
