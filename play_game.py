import json, os, time, random

def main():
    # TODO: allow them to choose from multiple JSON files?
    print("All files in the current directory:", os.listdir())
    json_games = []
    for i in os.listdir():
        if i[-4:] == 'json':
            json_games.append(i)
    print("The JSON files in this directory are", json_games)
    for i in range(len(json_games)):
               print(i+1, json_games[i])
    choice = int(input("What game would you like to play?"))
    game_choice = (json_games[choice - 1])
    game_thing = str(game_choice)
    
    
    with open(game_thing) as fp:
        game = json.load(fp)
    print(check_bridges(game))
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)

def find_non_win_rooms(game):
    keep = []
    for room_name in game.keys():
        # skip if it is the "fake" metadata room that has title & start
        if room_name == '__metadata__':
            continue
        # skip if it ends the game
        if game[room_name].get('ends_game', False):
            continue
        # keep everything else:
        keep.append(room_name)
    return keep
def check_bridges(game):
    for room in game:
        if room == '__metadata__':
            continue
        if room in game:
            pass
        if room not in game:
            return False

    return True
def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    begin = time.perf_counter()
    cat_place = random.choice(find_non_win_rooms(rooms))
    
    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])
        
        if current_place == cat_place:
            print("!!There's a cat in here!")
        
        if random.randint(0,2) == 1:
            cat_room = rooms[cat_place]
            cat_exit = random.choice(find_non_win_rooms(rooms))
            cat_place = cat_exit
        
        if here.get("visited", False):
            print("...You've been in this room before")
        here['visited'] = True

        # TODO: print any available items in the room...
        if len(here['items']) == 0:
            print("...There are no items in here")
        if len(here['items']) >= 1:
            print("Here are the items in the room:", here['items'])
        # e.g., There is a Mansion Key.
        if "Raw Fish" in stuff and current_place == cat_place:
            print("...The cat purrs! Maybe you have something it wants?")
        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        if action == "help":
            print_instructions()
            continue

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        if action == "stuff":
            if stuff == []:
                print("You have nothing")
                continue
            else:
                print(stuff)
                continue
        # TODO: if they type "take", grab any items in the room.
        if action == "take":
            for i in here['items']:
                stuff.append(i)
            here['items'].clear()
            continue 
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        if action == "search":
            for exit in here['exits']:
                if exit.get("hidden", True):
                    exit["hidden"] = False
            continue
        if action == "find":
            for exit in here['exits']:
                if exit.get("hidden", True):
                    exit["hidden"] = False
            continue
        if action == "drop":
            for i in range(len(stuff)):
               print(i+1, stuff[i])
            drop_item=int(input("Which item would you like to drop?"))
            here['items'].append(stuff[drop_item-1])
            stuff.pop(drop_item-1)
            continue
        if action == "time":
            current = time.perf_counter()
            print(f"You have spent {current - begin:0.2f} seconds in this game")
            continue
                    
                
                
                
        
        
            
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            if "Mansion Key" not in stuff:
                if current_place == "crypt":
                    break
            if "Mansion Key" not in stuff:
                if selected['destination'] == 'outside':
                    print("You try to open the door, but it's locked!")
                    continue
                    
                
            current_place = selected['destination']
            print("...")
            
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")

def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
            usable.append(exit)
            continue
        usable.append(exit)
    return usable
    

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'time' to see how many seconds you have spent in the game.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()
