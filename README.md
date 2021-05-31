# rPlanetOptimization

Organize element search space and allow you to backtest strategies. Donate to help a guppy out at **dvuee.wam**

## Database
Wrapper on the csv file for attempts tried located here https://prospectors.online/alchemy/alchemy-table.csv. It is recommended that you keep this file up to date in your directory, just download it and replace the old one. To instantiate a database see below:
```python
db = Database(csv_path="data/alchemy_table.csv", simulated_element="FROST")
```
The database allows you to "simulate" the environment at the time of discovery for a certain element. It lets you access the following attributes:
```python
db.failed_attempts  # All the failed attempts (up to the simulated element).
db.element_costs  # Cost of each element discovered (up to the simulated element).
db.element_ids  # ID's (such as "FROST" or "PRESS") of elements discovered (up to the simulated element).
```
The database also has access to all discovered recipes, will contain all discovered recipes regardless of whether you are trying to simulate an element or not.

```python
db.recipes  # Dictionary containing recipes keyed by element ID.
```
To not simulate an element (if you are trying to discover new elements) simply pass in a null value. 
```python
db = Database(csv_path="data/alchemy_table.csv", simulated_element=None)
```

## Alchemy Engine
Given a set of constraints this will solve for all attempts that are still available to try.
```python
ae = AlchemyEngine(db=db)
```
Pass in a database with a "simulated_element" if you would like to backtest solutions.

### Constraints
The goal is to narrow down your search space. Constrain your search space with the following sets of rules.
```python
ae.add_inclusion_constraint(("WATER", "DEW"))  # All combinations must include a water OR a dew.
ae.add_exclusion_constraint(("WATER", "DEW"))  # All combinations must not include BOTH water AND dew.
ae.add_quantity_constraint("WATER", lower_bound=1, upper_bound=3)  # All combinations can have between 1 and 3 waters.
```
Once constraints are added call solve to get possible recipes that have NOT been tried.
```python
ae.solve()
```

## How To Use
Can run through configuration files. See example configs/frost.json file. Set **simulated_element to null** if you would like to NOT backtest (AKA you are trying for new elements that have not been discovered).

```json
{
    "simulated_element": "FROST",
    "inclusion_constraints": [
        ["WATER", "DEW"]
    ],
    "exclusion_constraints": [
        ["WATER", "DEW"]
    ],
    "quantity_constraints": [
        ["WATER", 0, 3],
        ["DEW", 0, 3],
        ["WIND", 0, 2],
        ["MNTAIN", 0, 2],
        ["ATMSPHE", 0, 2],
        ["AIR", 0, 2]
    ]
}
```
Then call the following to backtest your belief system.
```bash
python alchemy_engine.py --config=config/frost.json
```
Sample Output:
```bash
('BOILER', 'SWAMP', 'SWAMP', 'WATER') Cost: 1270000
('BOILER', 'PRESS', 'SWAMP', 'WATER') Cost: 1060000
('BOILER', 'SWAMP', 'WATER', 'WATER') Cost: 1030000
('BOILER', 'PRESS', 'PRESS', 'SWAMP') Cost: 1090000
```

