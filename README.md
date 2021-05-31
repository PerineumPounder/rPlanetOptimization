# rPlanetOptimization

Organize element search space and allow you to backtest strategies.

## Database
Wrapper on the csv file for attempts tried located here https://prospectors.online/alchemy/alchemy-table.csv. It is recommended that you keep this file up to date in your directory, just download it and replace the old one.
```python
db = Database(csv_path="data/alchemy_table.csv", simulated_element="FROST"
```

## Constraints

The goal is to narrow down your search space. in

## How To Backtest

```bash
python alchemy_engine.py --config=configs/frost.json
```
