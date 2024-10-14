from items import *

room_MessHall = {
    "name": "mess hall",
    
    "id": "Mess Hall",

    "description":
    """You are in the space station's main cafeteria, a large hall 
with overturned tables and chairs. The hall is dimly lit by 
a few flickering lights, accentuating its gloominess. You 
can go south to the escape pod, east to the medical bay, 
west to the living quarters, or north to the control centre. """,

    "exits": {"south": "Escape Pod", "east": "Medical Bay", "west": "Living Quarters", "north": "Control Centre"},

    "items": [item_small_oxygen_tank]
}

room_EscapePod = {
    "name": "escape pod",
    
    "id": "Escape Pod",

    "description":
    """You are leaning against the door of the escape pod. It 
hasn't been used in some time and it probably won't work as 
expected. There appears to be a concerning number of dents 
and scratches on the pod, but it's still your only hope of 
returning to the Earth. The exit leads you north to the 
airlock through which is the mess hall.""",

    "exits":  {"north": "Mess Hall"},

    "items": [item_escapepod]
}

room_Dorms = {
    "name": "your colleague's room",
    
    "id": "Living Quarters",

    "description":
    """You are in your deceased colleague's room. He's left a 
number of memoirs and trinkets lying around. All the other 
rooms lie in a similarly abandoned state, or have been 
locked by their owners only to never be unlocked again. You 
can go east to the mess hall, north to the cargo bay, south 
to the medical bay, or west to look inside his storage 
compartment.""",

    "exits": {"east": "Mess Hall", "north": "Cargo Bay", "south": "Medical Bay", "west": "Storage Cubby"}, #West for secret Closet

    "items": []
}

room_Power = {
    "name": "the power and engine room",
    
    "id": "Power",

    "description":
    """You are standing in the space station's power and engine 
room, surrounded by multi-coloured cables dangling from the 
mainframe computers. Some of the cables appear to be worn 
out, or even completely missing. The exit is south to the 
cargo bay. """,

    "exits": {"south": "Cargo Bay"},

    "items": [item_screwdriver, item_wirecutter, item_powersupply]
}

room_Control = {
    "name": "the control centre",
    
    "id": "Control Centre",

    "description":
    """You are standing in the control room. It's a large R&D 
facility filled with desks, expensive machinery and 
computers. You can go west to the cargo bay or south to the 
mess hall.""",

    "exits": {"west": "Cargo Bay", "south": "Mess Hall"},

    "items": [item_computer,item_medium_oxygen_tank]
}

room_CargoBay = {
    "name": "the cargo bay",
    
    "id": "Cargo Bay",

    "description":
    """The cargo bay is a dark, and cavernous chamber that hosts 
logistics, and storage pallets. There's a number of useful 
and not-so useful tools scattered about on the floor. You 
can go east to the control centre, north to power, or south 
to the living quarters.""",

    "exits": {"east": "Control Centre", "north": "Power", "south": "Living Quarters"},

    "items": [item_cables, item_fuses, item_welder]

}

room_MedicalBay = {
    "name": "the medical room",
    
    "id": "Medical Bay",

    "description":
    """You are in the medical facility, a large, brightly lit room 
crammed with beds and hospital machinery that no longer 
works. The sterile smell somehow continues to linger in the 
air. You can go west to the mess hall, or north to the 
living quarters.""",

    "exits": {"west": "Mess Hall", "north": "Living Quarters"},

    "items": [item_large_oxygen_tank]
}

room_compartment = {
     "name": "the storage cubby",
     
     "id": "Storage Cubby",

    "description":
    """You are looking inside your colleague's storage cubby. 
Annoyingly it's locked and your colleague has put a riddle as 
the password to the lock. You can go east to go back into the 
living quarters.""",

    "exits": {"east":"Living Quarters"},

    "items": [item_password]
}

rooms = {
    "Mess Hall": room_MessHall,
    "Escape Pod": room_EscapePod,
    "Power": room_Power,
    "Control Centre": room_Control,
    "Living Quarters": room_Dorms,
    "Storage Cubby": room_compartment,
    "Cargo Bay": room_CargoBay,
    "Medical Bay": room_MedicalBay
}