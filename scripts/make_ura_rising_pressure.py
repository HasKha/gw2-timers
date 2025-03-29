import json

def get_rising_pressure_timestamps():
    timer = 0
    ret = []
    while timer < 600:
        timer += 8
        ret.append(timer)
    return ret

data = {
    "id": "haskha.ura.rp",
    "name": "Ura LCM\nRising Pressure",
    "category": "Raids",
    "description": "",
    "author": "Haskha.7509",
    "map": 1564,
    "reset": {
        "position": [194.095, 403.29, 265.844],
        "radius": 15,
        "requireEntry": True,
    },
}

data["phases"] = [
    {
        "name": "Ura LCM - Rising Pressure",
        "start": {
            "position": [145.639, 235.136, 269.928],
            "radius": 90,
            "requireEntry": True,
            "requireCombat": True,
        },
        "alerts": [
            {
                "warning": "Rising Pressure",
                "fillColor": [191, 115, 57, 0],
                "warningDuration": 8,
                "timestamps": get_rising_pressure_timestamps(),
                "icon": "Assets/Rising_Pressure.png",
            }
        ],
    }
]

file = open("../ura_lcm_rising_pressure.bhtimer", "w")
json.dump(data, file, indent=2)
file.close()
