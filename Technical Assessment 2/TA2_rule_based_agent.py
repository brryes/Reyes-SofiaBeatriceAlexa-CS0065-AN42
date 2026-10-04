# Rule-Based Vacuum Cleaner Agent

# Task 1: Set up the environment
rooms = {
    "A": input("Is room A Dirty or Clean? (dirty/clean): ").lower(),
    "B": input("Is room B Dirty or Clean? (dirty/clean): ").lower()
}

# Check room conditions
def is_dirty(room):
    return rooms[room] == "dirty"

# Clean a room
def clean_room(room):
    rooms[room] = "clean"


# Task 2: Create the rule-based agent
class VacuumAgent:

    def __init__(self):
        self.current_room = "A"

    # Move between rooms
    def move(self):
        if self.current_room == "A":
            self.current_room = "B"
        else:
            self.current_room = "A"

    # Follow the rules
    def perceive_and_act(self):
        if is_dirty(self.current_room):
            clean_room(self.current_room)
            return "Cleaned the room"
        else:
            self.move()
            return "Moved to Room " + self.current_room


# Task 3: Run the simulation
agent = VacuumAgent()

steps = int(input("How many steps should the agent run?: "))

print("\nInitial Environment:")
print(rooms)

for step in range(1, steps + 1):
    action = agent.perceive_and_act()

    print("\nStep", step)
    print("Agent location:", agent.current_room)
    print("Action:", action)
    print("Environment:", rooms)

print("\nSimulation complete!")