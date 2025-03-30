import json

geyser_locations = [
    [196.7, 247.2, 269.7],
    [181.6, 276.9, 269.9],
    [193.8, 219.2, 269.8],
    [183.0, 235.2, 269.8],
    [165.2, 253.1, 269.9],
    [158.0, 280.9, 269.9],
    [178.8, 202.3, 269.9],
    [161.7, 228.7, 269.8],
    [145.9, 259.3, 269.8],
    [162.6, 200.3, 269.8],
    [145.5, 228.9, 269.8],
    [122.4, 249.6, 269.8],
    [136.7, 199.6, 269.8],
    [109.5, 218.6, 269.8],
]
geyser_markers = [
    "Spiral",
    "Triangle",
    "Circle",
    "Heart",
    "Cloud",
    "X",
    "Arrow",
    "Square",
    "Star",
    "Cat",
    "Fox",
    "Plus",
    "Frog",
    "Fish",
]
num_geysers = len(geyser_locations)
p1_start = 0
p2_start = 7
p3_start = 6

data = {
    "id": "haskha.ura.toxic",
    "name": "Ura LCM\nToxic Spawns",
    "category": "Raids",
    "description": "Automatically begins on fight start.\nAfter 70%, press trigger key 0 when the first toxic appears at square.\nPress trigger key 0 again at 40%",
    "author": "Haskha.7509",
    "map": 1564,
    "reset": {
        "position": [194.095, 403.29, 265.844],
        "radius": 15,
        "requireEntry": True,
    },
}


def get_phase_header(name):
    return {
        "name": name,
        "start": {
            "position": [145.639, 235.136, 269.928],
            "radius": 90,
            "requireEntry": True,
            "requireCombat": True,
        },
        "finish": {
            "position": [145.639, 235.136, 269.928],
            "radius": 200,
            "type": "key",
            "keyBind": "0",
        },
        "alerts": [],
        "directions": [],
    }


def get_alert(time: int, index: int):
    return {
        "warning": geyser_markers[index],
        "warningDuration": 12,
        "timestamps": [time],
        "icon": "Assets/" + geyser_markers[index] + ".png",
    }


def get_direction(time: int, index: int):
    return {
        "name": geyser_markers[index],
        "destination": geyser_locations[index],
        "animSpeed": 0,
        "texture": "Assets/ArrowTrail.png",
        "duration": 12,
        "timestamps": [time - 12],
    }


# P1
data["phases"] = []
data["phases"].append(get_phase_header("Ura LCM - Phase 1"))
time = 12
index = p1_start
while time < 150:
    data["phases"][0]["alerts"].append(get_alert(time, index))
    data["phases"][0]["directions"].append(get_direction(time, index))
    time += 12
    index = (index + 1) % num_geysers

# P2
data["phases"].append(get_phase_header("Ura LCM - Phase 2"))
time = -2
index = p2_start
while time < 300:
    data["phases"][1]["alerts"].append(get_alert(time, index))
    data["phases"][1]["directions"].append(get_direction(time, index))
    time += 12
    index = (index + 1) % num_geysers

# P3
data["phases"].append(get_phase_header("Ura LCM - Phase 3"))
time = -2
index = p3_start
while time < 300:
    data["phases"][2]["alerts"].append(get_alert(time, index))
    data["phases"][2]["directions"].append(get_direction(time, index))
    time += 12
    index = (index + 1) % num_geysers

# P4 (not existing, just end point for now)
data["phases"].append(
    {
        "name": "End",
        "start": {
            "position": [145.639, 235.136, 269.928],
            "radius": 90,
            "requireEntry": True,
            "requireCombat": True,
        },
    }
)

file = open("../ura_lcm_toxic_spawns.bhtimer", "w")
json.dump(data, file, indent=2)
file.close()
