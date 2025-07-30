import json

def get_trajectory(index):
    with open(f"pattern{index}.json", "r") as f:
        data = json.load(f)