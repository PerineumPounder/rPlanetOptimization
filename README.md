# rPlanetOptimization

Organize element search space and allow you to backtest strategies.

## Database
Wrapper on the csv file for attempts tried located here https://prospectors.online/alchemy/alchemy-table.csv. It is recommended that you keep this file up to date in your directory, just download it and replace the old one. To instantiate a database see below:
```python
db = Database(csv_path="data/alchemy_table.csv", simulated_element="FROST")
```
The database allows you to "simulate" the environment at the time of discovery for a certain element. It lets you access the following attributes:
```python
db.failed_attempts # All the failed attempts (up to the simulated element).
db.element_costs # Cost of each element discovered (up to the simulated element).
db.element_ids # ID's (such as "FROST" or "PRESS") of elements discovered (up to the simulated element).
```
The database also has access to all discovered recipes, will contain all discovered recipes regardless of whether you are trying to simulate an element or not.

```python
db.recipes # Dictionary containing recipes keyed by element ID.
```
To not simulate an element (if you are trying to discover new elements) simply pass in a null value. 
```python
db = Database(csv_path="data/alchemy_table.csv", simulated_element=None)
```

## Constraints

The goal is to narrow down your search space. in

## How To Backtest

```bash
python alchemy_engine.py --config=configs/frost.json
```
