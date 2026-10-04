# TA4: Knowledge Representation, RBR, and CBR
# Use Case: Weather Advice System

# =====================================================
# PART 1: KNOWLEDGE REPRESENTATION
# =====================================================

# Knowledge base with five facts
facts = {
    "temperature": 32,
    "is_raining": True,
    "humidity": 85,
    "wind_speed": 20,
    "sky": "cloudy"
}

# Three categories
categories = {
    "environment": ["temperature", "humidity"],
    "weather": ["is_raining", "sky"],
    "safety": ["wind_speed"]
}

print("KNOWLEDGE BASE")
print(facts)

print("\nCATEGORIES")
for category, items in categories.items():
    print(category, ":", items)


# =====================================================
# PART 2: RULE-BASED REASONING
# =====================================================

def rule_hot(facts):
    if facts["temperature"] >= 30:
        return "Drink plenty of water."


def rule_raining(facts):
    if facts["is_raining"]:
        return "Bring an umbrella."


def rule_humid(facts):
    if facts["humidity"] >= 80:
        return "Stay in a cool place."


def rule_windy(facts):
    if facts["wind_speed"] >= 25:
        return "Be careful because of strong winds."


# Inference engine
def inference_engine(facts, rules):
    actions = []

    for rule in rules:
        result = rule(facts)

        if result is not None:
            actions.append(result)

    return actions


rules = [
    rule_hot,
    rule_raining,
    rule_humid,
    rule_windy
]

rbr_actions = inference_engine(facts, rules)

print("\nRULE-BASED REASONING ACTIONS")

for action in rbr_actions:
    print("-", action)


# =====================================================
# PART 3: CASE-BASED REASONING
# =====================================================

# Three previous cases
case_base = [
    {
        "problem": {
            "hot": True,
            "raining": True,
            "humid": True,
            "windy": False
        },
        "solution": "Bring an umbrella and drink plenty of water."
    },
    {
        "problem": {
            "hot": False,
            "raining": True,
            "humid": False,
            "windy": True
        },
        "solution": "Bring an umbrella and avoid outdoor activities."
    },
    {
        "problem": {
            "hot": False,
            "raining": False,
            "humid": False,
            "windy": False
        },
        "solution": "The weather is comfortable for outdoor activities."
    }
]

# Convert current facts into problem features
new_problem = {
    "hot": facts["temperature"] >= 30,
    "raining": facts["is_raining"],
    "humid": facts["humidity"] >= 80,
    "windy": facts["wind_speed"] >= 25
}


# Calculate similarity
def calculate_similarity(problem1, problem2):
    score = 0

    for feature in problem1:
        if problem1[feature] == problem2[feature]:
            score += 1

    return score


# Retrieve the most similar case
def retrieve_case(new_problem, case_base):
    best_case = None
    highest_score = -1

    for case in case_base:
        score = calculate_similarity(
            new_problem,
            case["problem"]
        )

        if score > highest_score:
            highest_score = score
            best_case = case

    return best_case, highest_score


# Retrieve and reuse
similar_case, similarity_score = retrieve_case(
    new_problem,
    case_base
)

solution = similar_case["solution"]

print("\nCASE-BASED REASONING")
print("New problem:", new_problem)
print("Most similar case:", similar_case["problem"])
print("Similarity score:", similarity_score)
print("Reused solution:", solution)


# Revise
revision = input(
    "\nEnter a revised solution or press Enter to keep the original: "
)

if revision.strip() != "":
    solution = revision
    print("Solution revised.")
else:
    print("Original solution retained.")


# Retain
new_case = {
    "problem": new_problem,
    "solution": solution
}

case_base.append(new_case)

print("\nNew case added to the case base.")
print("Total cases:", len(case_base))

print("\nFINAL SOLUTION")
print(solution)