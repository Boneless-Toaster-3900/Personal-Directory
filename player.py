from items import *
from map import rooms

inventory = []

# Start game at the Mess Hall
current_room = rooms["Mess Hall"]

oxygen = 100

objectives = 0

start_values = {
    "inventory":[],
    "current room id":"Mess Hall",
    "oxygen":100,
    "objectives":0,
    "room item ids":{"Mess Hall":["small oxygen tank"],
                     "Escape Pod":["escape pod"],
                     "Living Quarters":[],
                     "Power":["screwdriver","wire cutter","power supply"],
                     "Control Centre":["computer","medium oxygen tank"],
                     "Cargo Bay":["cables","fuses","welding device"],
                     "Medical Bay":["large oxygen tank"],
                     "Storage Cubby":["password"]
                         },
    "broken items status":{"power supply":True,
                           "escape pod":True
                           },
    "time elapsed prev sessions":0,
                  }