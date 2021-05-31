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
        self.quantity_constraints.append((eid, lower_bound, upper_bound))

    def add_inclusion_constraint(self, eids: tuple):
        self.inclusion_constraints.append(eids)

    def add_exclusion_constraint(self, eids: tuple):
        self.exclusion_constraints.append(eids)

    def solve(self):
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

    import wikipedia
    print(wikipedia.page("barrel", auto_suggest=False).content)





    # elements = database.Database("alchemy-table.csv").element_ids
    #
    # for el in elements:
    #     db = database.Database("alchemy-table.csv", simulated_element=el)
    #     recipe = db.recipes[el]
    #     count = 0
    #     for attempt in db.failed_attempts:
    #         c = list((Counter(attempt) & Counter(recipe)).elements())
    #         if len(c) == 3:
    #             count += 1
    #     print(count, el, db.recipes[el])

    # db = database.Database("alchemy-table.csv", simulated_element="PAPER")
    # recipe = ("PLANT", "PLANT", "PRESS", "FOG")
    # count = 0
    # for attempt in db.failed_attempts:
    #     c = list((Counter(attempt) & Counter(recipe)).elements())
    #     if len(c) == 3:
    #         print(attempt)
    #         count += 1
    # print(count, recipe, (recipe in db.failed_attempts))

    # db = database.Database("alchemy-table.csv")
    # ae = AlchemyEngine(db)
    # ae.add_inclusion_constraint(("PAPER", "CLOTH"))
    # ae.add_quantity_constraint("WIND", 0, 3)
    # ae.add_quantity_constraint("SKY", 0, 3)
    # ae.add_quantity_constraint("TREE", 0, 3)
    # ae.add_quantity_constraint("KNIFE", 0, 1)
    # ae.add_quantity_constraint("PAINT", 0, 1)
    # ae.add_quantity_constraint("CLOTH", 0, 3)
    # ae.add_quantity_constraint("PAPER", 0, 3)
    # ae.add_quantity_constraint("RAINBOW", 0, 3)
    # solutions = ae.solve()
    # for recipe in solutions:
    #     count = 0
    #     for attempt in db.failed_attempts:
    #         c = list((Counter(attempt) & Counter(recipe)).elements())
    #         if len(c) == 3:
    #             count += 1
    #     print(count, recipe)
    # print(db.recipes)

    # -----------------------------------------------------------------------
    # GUN simulation, 8 results, success
    # -----------------------------------------------------------------------
    # db = database.Database("alchemy-table.csv", simulated_element="GUN")
    # ae = AlchemyEngine(db)
    # ae.add_inclusion_constraint(("METAL", "STEEL"))
    # ae.add_quantity_constraint("EXPLOSN", 1, 3)
    # ae.add_quantity_constraint("METAL", 0, 3)
    # ae.add_quantity_constraint("STEEL", 0, 3)
    # ae.add_quantity_constraint("BULLET", 1, 3)
    # ae.add_quantity_constraint("BARREL", 0, 1)
    # pprint.pprint(ae.solve())

    # [('BARREL', 'BULLET', 'EXPLOSN', 'STEEL'),
    #  ('BULLET', 'EXPLOSN', 'EXPLOSN', 'METAL'),
    #  ('BULLET', 'EXPLOSN', 'STEEL', 'STEEL'),
    #  ('BULLET', 'EXPLOSN', 'EXPLOSN', 'STEEL'),
    #  ('BARREL', 'BULLET', 'EXPLOSN', 'METAL'),
    #  ('BULLET', 'EXPLOSN', 'METAL', 'STEEL'),
    #  ('BULLET', 'BULLET', 'EXPLOSN', 'STEEL'),
    #  ('BULLET', 'BULLET', 'EXPLOSN', 'METAL')]

    # -----------------------------------------------------------------------
    # SALT simulation, wrecked
    # -----------------------------------------------------------------------
    # db = database.Database("alchemy-table.csv", simulated_element="SALT")
    # ae = AlchemyEngine(db)
    # ae.add_inclusion_constraint(("SEA", "OCEAN"))
    # ae.add_quantity_constraint("SUN", 0, 3)
    # ae.add_quantity_constraint("OCEAN", 0, 3)
    # ae.add_quantity_constraint("SEA", 0, 3)
    # ae.add_quantity_constraint("BEACH", 0, 1)
    # ae.add_quantity_constraint("TNPLT", 0, 1)
    # pprint.pprint(ae.solve())

    # -----------------------------------------------------------------------
    # VIRUS simulation, 10, success
    # -----------------------------------------------------------------------
    # db = database.Database("alchemy-table.csv", simulated_element="VIRUS")
    # ae = AlchemyEngine(db)
    # ae.add_inclusion_constraint(("HEAT", "SUN"))
    # ae.add_quantity_constraint("MICROSCOPE", 0, 1)
    # ae.add_quantity_constraint("GARBAGE", 1, 3)
    # ae.add_quantity_constraint("HEAT", 0, 2)
    # ae.add_quantity_constraint("SUN", 0, 2)
    # pprint.pprint(ae.solve())

    # -----------------------------------------------------------------------
    # PLASMA simulation, wrecked
    # -----------------------------------------------------------------------
    # db = database.Database("alchemy-table.csv", simulated_element="PLASMA")
    # ae = AlchemyEngine(db)
    # ae.add_exclusion_constraint(("FIRE", "HEAT"))
    # ae.add_quantity_constraint("BOILER", 0, 1)
    # ae.add_quantity_constraint("OXYGEN", 1, 3)
    # ae.add_quantity_constraint("HEAT", 0, 3)
    # ae.add_quantity_constraint("FIRE", 0, 3)
    # pprint.pprint(ae.solve())

    # db = database.Database("alchemy-table.csv")
    # ae = AlchemyEngine(db)
    # ae.add_exclusion_constraint(("FIRE", "HEAT"))
    # ae.add_inclusion_constraint(("CLAY", "DIAMOND"))
    # ae.add_exclusion_constraint(("CLAY", "DIAMOND"))
    # ae.add_quantity_constraint("DIAMOND", 0, 2)
    # ae.add_quantity_constraint("CLAY", 0, 2)
    # ae.add_quantity_constraint("HEAT", 0, 3)
    # ae.add_quantity_constraint("TIME", 0, 3)
    # ae.add_quantity_constraint("VACUUM", 0, 3)
    # pprint.pprint(ae.solve())


    # element = "BULLET"
    # db = database.Database("alchemy-table.csv", simulated_element=element)
    # ae = AlchemyEngine(db)
    # ae.add_quantity_constraint("STEEL", 0, 3)
    # ae.add_quantity_constraint("RING", 0, 2)
    # ae.add_quantity_constraint("METAL", 0, 2)
    # ae.add_quantity_constraint("GUNPWDR", 0, 3)
    # ae.add_quantity_constraint("EXPLOSN", 0, 3)
    # solutions = ae.solve()
    #
    # for recipe in solutions:
    #     count = 0
    #     for attempt in db.failed_attempts:
    #         c = list((Counter(attempt) & Counter(recipe)).elements())
    #         if len(c) == 3:
    #             count += 1
    #     cost = 0
    #     for eid in recipe:
    #         cost += db.element_costs[eid]
    #     print(count, recipe, cost)
    #
    # if db.recipes[element] in solutions:
    #     print(db.recipes[element])
    #     print("SUCCESS")
    # else:
    #     print(db.recipes[element])
    #     print("FAILURE")

    # 19('BOILER', 'PRESS', 'STEAM', 'STEAM')
    # 880000
    # 34('AIR', 'BOILER', 'FIRE', 'PRESS')
    # 820000
    # 31('AIR', 'BOILER', 'PRESS', 'STEAM')
    # 850000
    # 39('AIR', 'AIR', 'BOILER', 'PRESS')
    # 820000
    # 23('BOILER', 'PRESS', 'PRESS', 'STEAM')
    # 880000
    # 23('BOILER', 'FIRE', 'PRESS', 'STEAM')
    # 850000

    # 9('DEW', 'MNTAIN', 'MNTAIN', 'WIND')
    # 10('MNTAIN', 'MNTAIN', 'WATER', 'WIND')

    # element = None
    # db = database.Database("alchemy-table.csv", simulated_element=element)
    # ae = AlchemyEngine(db)
    # ae.add_inclusion_constraint(("AIR", "STEAM"))
    # ae.add_quantity_constraint("PRESS", 1, 3)
    # ae.add_quantity_constraint("AIR", 0, 2)
    # ae.add_quantity_constraint("STEAM", 0, 2)
    # ae.add_quantity_constraint("BOILER", 1, 1)
    # ae.add_quantity_constraint("FIRE", 0, 2)
    # solutions = ae.solve()

    # element = None
    # db = database.Database("alchemy-table.csv", simulated_element=element)
    # ae = AlchemyEngine(db)
    # ae.add_quantity_constraint("PAINT", 1, 3)
    # ae.add_quantity_constraint("PAPER", 1, 3)
    # ae.add_quantity_constraint("TREE", 0, 2)
    # ae.add_quantity_constraint("WALL", 0, 1)
    # solutions = ae.solve()

    # element = None
    # db = database.Database("alchemy-table.csv", simulated_element=element)
    # ae = AlchemyEngine(db)
    # ae.add_inclusion_constraint(("DEW", "WATER"))
    # ae.add_exclusion_constraint(("DEW", "WATER"))
    # ae.add_exclusion_constraint(("WIND", "ATMSPHE"))
    # ae.add_exclusion_constraint(("PLANT", "MOSS"))
    # ae.add_exclusion_constraint(("PLANT", "GRASS"))
    # ae.add_exclusion_constraint(("MOSS", "GRASS"))
    # ae.add_quantity_constraint("MNTAIN", 1, 3)
    # ae.add_quantity_constraint("DEW", 0, 2)
    # ae.add_quantity_constraint("FOG", 0, 2)
    # ae.add_quantity_constraint("WATER", 0, 2)
    # # ae.add_quantity_constraint("ATMSPHE", 0, 2)
    # ae.add_quantity_constraint("WIND", 0, 2)
    # # ae.add_quantity_constraint("PLANT", 0, 1)
    # # ae.add_quantity_constraint("MOSS", 0, 1)
    # # ae.add_quantity_constraint("GRASS", 0, 1)
    # solutions = ae.solve()
    #
    # for recipe in solutions:
    #     count = 0
    #     for attempt in db.failed_attempts:
    #         c = list((Counter(attempt) & Counter(recipe)).elements())
    #         if len(c) == 3:
    #             count += 1
    #     cost = 0
    #     for eid in recipe:
    #         cost += db.element_costs[eid]
    #     print(count, recipe, cost)
    #
    # if db.recipes[element] in solutions:
    #     print("SUCCESS")
    # else:
    #     print(db.recipes[element])
    #     print("FAILURE")



if __name__ == "__main__":
    main()
