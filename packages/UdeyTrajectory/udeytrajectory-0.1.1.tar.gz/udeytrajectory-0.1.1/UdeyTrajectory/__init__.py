import json

def get_trajectory(index):
    data = {}
    with open(f"./pattern{index}.json", "r") as f:
        data = json.load(f)

    return data

data = get_trajectory(1)
print(data)