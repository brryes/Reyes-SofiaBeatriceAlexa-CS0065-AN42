import agentpy as ap
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import Counter


# ---------------- AGENT ----------------

class RandomWalker(ap.Agent):

    def setup(self):
        self.path = []

    def step(self):
        x, y = self.position
        grid_width, grid_height = self.model.p.grid_size

        # Four possible movement directions
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # Preferred direction, if the scenario has one
        preferred = self.model.p.preferred_direction

        if preferred is not None:
            directions.remove(preferred)
            random.shuffle(directions)
            directions.insert(0, preferred)
        else:
            random.shuffle(directions)

        # Positions occupied by other agents
        occupied_positions = {
            tuple(other.position)
            for other in self.model.agents
            if other is not self
        }

        # Try each direction
        moved = False

        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            new_position = (new_x, new_y)

            inside_grid = (
                0 <= new_x < grid_width
                and 0 <= new_y < grid_height
            )

            if inside_grid and new_position not in occupied_positions:
                self.position = new_position
                moved = True
                break

        # If no valid position exists, remain in the same location
        if not moved:
            self.position = (x, y)

        # Record the new position
        self.path.append(tuple(self.position))


# ---------------- MODEL ----------------

class RandomWalkModel(ap.Model):

    def setup(self):
        self.agents = ap.AgentList(
            self,
            self.p.agents,
            RandomWalker
        )

        grid_width, grid_height = self.p.grid_size

        all_positions = [
            (x, y)
            for x in range(grid_width)
            for y in range(grid_height)
        ]

        # Give agents starting positions
        if self.p.agents <= len(all_positions):
            starting_positions = random.sample(
                all_positions,
                self.p.agents
            )
        else:
            starting_positions = [
                random.choice(all_positions)
                for _ in range(self.p.agents)
            ]

        for agent, position in zip(self.agents, starting_positions):
            agent.position = position
            agent.path = [position]

    def step(self):
        for agent in self.agents:
            agent.step()


# ---------------- SCENARIOS ----------------
# Change these values to experiment.

scenario_1 = {
    "agents": 5,
    "grid_size": (10, 10),
    "steps": 30,
    "preferred_direction": None
}

scenario_2 = {
    "agents": 10,
    "grid_size": (10, 10),
    "steps": 30,
    "preferred_direction": (1, 0)
    # (1, 0) means agents prefer moving to the right
}


# ---------------- CREATE MODELS ----------------

model_1 = RandomWalkModel(scenario_1)
model_1.setup()

model_2 = RandomWalkModel(scenario_2)
model_2.setup()

models = [model_1, model_2]
titles = [
    "Scenario 1: Random Movement",
    "Scenario 2: More Agents Moving Right"
]


# ---------------- DISPLAY SETUP ----------------

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

scatter_plots = []
path_lines = []

for ax, model, title in zip(axes, models, titles):
    grid_width, grid_height = model.p.grid_size

    ax.set_xlim(-1, grid_width)
    ax.set_ylim(-1, grid_height)
    ax.set_xticks(range(grid_width))
    ax.set_yticks(range(grid_height))
    ax.grid(True)
    ax.set_title(title)
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")

    x_positions = [agent.position[0] for agent in model.agents]
    y_positions = [agent.position[1] for agent in model.agents]

    scatter = ax.scatter(
        x_positions,
        y_positions,
        s=120,
        color="red"
    )

    lines = []

    for agent in model.agents:
        line, = ax.plot(
            [agent.position[0]],
            [agent.position[1]],
            linewidth=1
        )
        lines.append(line)

    scatter_plots.append(scatter)
    path_lines.append(lines)


# ---------------- ANIMATION ----------------

def update(frame):
    for model, scatter, lines in zip(
        models,
        scatter_plots,
        path_lines
    ):
        model.step()

        x_positions = [
            agent.position[0]
            for agent in model.agents
        ]

        y_positions = [
            agent.position[1]
            for agent in model.agents
        ]

        scatter.set_offsets(
            list(zip(x_positions, y_positions))
        )

        # Display the path of every agent
        for agent, line in zip(model.agents, lines):
            path_x = [position[0] for position in agent.path]
            path_y = [position[1] for position in agent.path]

            line.set_data(path_x, path_y)

    return scatter_plots + [
        line
        for lines in path_lines
        for line in lines
    ]


animation_object = animation.FuncAnimation(
    fig,
    update,
    frames=scenario_1["steps"],
    interval=200,
    repeat=False,
    blit=False
)

plt.tight_layout()
plt.show()


# ---------------- FINAL POSITION ANALYSIS ----------------

def display_analysis(model, scenario_name):
    print("\n" + "=" * 50)
    print(scenario_name)
    print("=" * 50)

    final_positions = [
        tuple(agent.position)
        for agent in model.agents
    ]

    print("Final positions:")

    for number, position in enumerate(final_positions, start=1):
        print(f"Agent {number}: {position}")

    position_counts = Counter(final_positions)

    print("\nPosition distribution:")

    for position, count in sorted(position_counts.items()):
        print(f"Position {position}: {count} agent(s)")

    unique_positions = len(position_counts)
    total_agents = len(final_positions)

    print(f"\nTotal agents: {total_agents}")
    print(f"Occupied grid positions: {unique_positions}")

    if unique_positions == total_agents:
        print("No agents share the same final position.")
    else:
        print("Some agents share the same final position.")


display_analysis(model_1, "Scenario 1 Analysis")
display_analysis(model_2, "Scenario 2 Analysis")