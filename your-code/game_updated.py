# define rooms and items

door_a = {
    "name": "door a",
    "type": "door",
}

door_b = {
    "name": "door b",
    "type": "door",
}

door_c = {
    "name": "door c",
    "type": "door",
}

door_d = {
    "name": "door d",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

piano = {
    "name": "piano",
    "type": "furniture",
}

couch = {
    "name": "couch",
    "type": "furniture",
}

queen_bed = {
    "name": "queen bed",
    "type": "furniture",
}

double_bed = {
    "name": "double bed",
    "type": "furniture",
}

dresser = {
    "name": "dresser",
    "type": "furniture",
}

dinning_table = {
    "name": "dinning table",
    "type": "furniture",
}

musical_picture = {
    "name": "musical picture",
    "type": "furniture",
}

game_room = {
    "name": "game room",
    "type": "room",
}

bedroom1 = {
    "name": "bedroom 1",
    "type": "room",
}

bedroom2 = {
    "name": "bedroom 2",
    "type": "room",
}

living_room = {
    "name": "living room",
    "type": "room",
}


outside = {
  "name": "outside"
}

all_rooms = [game_room, bedroom1,bedroom2,living_room,outside]

all_doors = [door_a,door_b,door_c,door_d]

# define which items/rooms are related

object_relations = {
    "game room": [couch, piano, door_a,musical_picture],
    "bedroom 1": [queen_bed,door_a, door_b, door_c],
    "bedroom 2": [double_bed,dresser, door_b],
    "living room": [dinning_table,door_d, door_c],
    "outside": [door_d],
    "piano": [key_a],
    "queen bed":[key_b],
    "double bed":[key_c],
    "dresser":[key_d],
    "door a": [game_room, bedroom1],
    "door b": [bedroom2, bedroom1],
    "door c": [living_room, bedroom1],
    "door d": [outside, living_room]
}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game():
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"]) 
    
def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'a' to explore the room or 'b' to examine the objects in the room?").strip()
        if intended_action == "a":
            explore_room(room)
            play_room(room)
        elif intended_action == "b":
            examine_item(input("What object would you like to examine?").strip())
        else:
            print("Not sure what you mean. Type 'a' to explore the room or 'b' to examine the objects in the room?")
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            elif item["name"] == "musical picture":
                print("You're looking at the musical picture. Pay attention! It has 6 objects portraited: Giant, Aligator, Ant, Dice, Car, Fan")
            
            elif item["name"] == "piano":
                playtime= True
                while playtime== True:
                    print("You're facing the piano, please sit and play something.")
                    song_played=input("Can you play a 6 note song? ").replace(" ","")
                    if song_played.upper()=="GAADCF":
                        print("You're a musical genius! Wait, something was revealed.")
                        item_found = object_relations[item["name"]].pop()
                        game_state["keys_collected"].append(item_found)
                        print("You find key foor door a")
                        playtime= False
                    else:
                        print("That is not a great song, please try again. Remember the musical notes are: A B C D E F G. Maybe explore the room for inspiration \n")
                        another_try=input("Do you want to try again? Yes or No?")
                        if another_try.upper()== "NO":
                            playtime=False
                        else: 
                            continue


            
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")
    
    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
        play_room(next_room)
    else:
        play_room(current_room)

game_state = INIT_GAME_STATE.copy()

import tkinter as tk
import os, time
from threading import Thread


root = tk.Tk()
# set window size
root.geometry("500x200")

def start_timer(count):
    label = tk.Label(root)
    label.place(x=32, y=35)
    label.config(font=("Courier", 20))

    # change text in label   
    total_mins = count//60 # minutes left
    total_sec = count-(60*(total_mins)) #seconds left  
    if total_sec < 10:
        total_sec = f"0{total_sec}"
     
    label['text'] = '{min}:{sec}'.format(min=total_mins, sec=total_sec)

    if count > 0:
        # call countdown again after 1000ms (1s)
        root.after(1000, start_timer, count-1)
    if count == 0:
        label['text'] = 'GAME OVER'
        root.after(1000, start_timer, count-1)
    if count < 0:
        label['text'] = 'GAME OVER'
        time.sleep(2)
        root.destroy()
        return False



if __name__ == '__main__':
    game = Thread(target= start_game)
    game.start()

    timer = Thread(target= start_timer, args=(2,))
    timer.start()
    root.mainloop()

    timer.join()
    if timer.is_alive() == False:
        print("\n you are too slow! game over!")
        os._exit(0)
        

