item_screwdriver = {
    "id": "screwdriver",

    "name": "screwdriver",

    "description":
    "A flathead screwdriver.",
    
    "broken": False, # True if the item is broken
    
    "mobile": True, # True if the player should be able to carry the item, False if not

    "consumable": False, # True if the player should be able to consume the item
    
    "items to fix": [] # Items needed to fix this item
}

item_powersupply = {
    "id": "power supply",

    "name": "power supply",

    "description":
    "The main power supply that provides the space station with power.",

    "broken": True,

    "mobile": False,

    "consumable":False,

    "items to fix": ["screwdriver","cables","wire cutter","fuses"]
}

item_escapepod = {
    "id": "escape pod",

    "name": "escape pod",

    "description":
    "A compact, one-person escape pod designed for emergency evacuation from the space station.",

    "broken": True,

    "mobile": False,

    "consumable": False,

    "items to fix": ["screwdriver","cables","wire cutter"]
}
    
item_computer = {
    "id": "computer",

    "name": "computer",

    "description":
    "The space stations's main computer.",
    
    "broken": False,
    
    "mobile": False,

    "consumable": False,
    
    "items to fix": []
}

item_password = {
    "id": "password",

    "name": "password",

    "description":
    "A mysterious piece of paper with a password written on it. It might come in handy to contact authorities.",

    "broken": False,

    "mobile": True,

    "consumable": False,

    "items to fix": []
}

item_cables = {
    "id": "cables",

    "name": "cables",

    "description":
    "An assortment of different cables. Might be useful to repair electronic items.",

    "broken": False,

    "mobile": True,

    "consumable": False,

    "items to fix": []
}

item_small_oxygen_tank = {
    "id": "small oxygen tank",

    "name": "small oxygen tank",
    
    "description":
    "An oxygen tank that can give you 25 oxygen.",

    "broken": False,

    "mobile": True,

    "consumable": True,

    "items to fix": [],

    "oxygen": 25

}

item_medium_oxygen_tank = {
    "id": "medium oxygen tank",

    "name": "medium oxygen tank",
    
    "description":
    "An oxygen tank that can give you 50 oxygen.",

    "broken": False,

    "mobile": True,

    "consumable": True,

    "items to fix": [],

    "oxygen": 50

}

item_large_oxygen_tank = {
    "id": "large oxygen tank",

    "name": "large oxygen tank",

    "description":
    "An oxygen tank that can give you 75 oxygen.",

    "broken": False,

    "mobile": True,

    "consumable": True,

    "items to fix": [],

    "oxygen": 75
}

item_wirecutter = {
    "id": "wire cutter",

    "name": "wire cutter",

    "description":
    "A small tool used for easily cutting cables and wires.",

    "broken": False,

    "mobile": True,

    "consumable": False,

    "items to fix": []
}

item_welder = {
    "id": "welding device",

    "name": "welding device",

    "description":
    "Used to fuse pieces of metal together on the spaceship.",

    "broken": False,

    "mobile": True,

    "consumable": False,

    "items to fix": []
}

item_fuses = {
    "id": "fuses",

    "name": "fuses",
# This description is also from ChatGPT
    "description":
    "A set of electronic fuses that might be useful for fixing electrical systems on the spaceship.",

    "broken": False,

    "mobile": True,

    "consumable": False,

    "items to fix": []
}

items = {
    "computer": item_computer,
    "screwdriver": item_screwdriver,
    "password": item_password,
    "cables": item_cables,
    "small oxygen tank": item_small_oxygen_tank,
    "medium oxygen tank": item_medium_oxygen_tank,
    "large oxygen tank": item_large_oxygen_tank,
    "wire cutter": item_wirecutter,
    "welding device": item_welder,
    "fuses": item_fuses,
    "power supply": item_powersupply,
    "escape pod": item_escapepod
}