# Disaster Response Decision Support System using Case-Based Reasoning (CBR)
# CS0065 - Intelligent Systems | TA3
#

import json
from pathlib import Path

CASE_FILE = Path("disaster_cases.json")

# Step 1: Case Representation
# Each case stores the problem attributes and a previous response plan.
INITIAL_CASES = [
    {
        "case_id": 1,
        "name": "Typhoon Ursula - Sample Case",
        "problem": {
            "disaster_type": "typhoon",
            "flood_severity": "high",
            "location_type": "coastal",
            "affected_population": 3000
        },
        "solution": {
            "evacuation": "Evacuate residents in high-risk coastal and flood-prone zones.",
            "shelter": "Prepare temporary shelters and confirm safe capacity.",
            "resources": "Prioritize rescue boats, food, drinking water, and first-aid supplies."
        }
    },
    {
        "case_id": 2,
        "name": "Urban Flooding - Sample Case",
        "problem": {
            "disaster_type": "flood",
            "flood_severity": "high",
            "location_type": "urban",
            "affected_population": 5000
        },
        "solution": {
            "evacuation": "Move residents from deeply flooded streets and low-lying neighborhoods.",
            "shelter": "Open accessible evacuation centers and check their remaining capacity.",
            "resources": "Prioritize rescue vehicles, clean water, food packs, and medical supplies."
        }
    },
    {
        "case_id": 3,
        "name": "Rural River Flood - Sample Case",
        "problem": {
            "disaster_type": "flood",
            "flood_severity": "moderate",
            "location_type": "rural",
            "affected_population": 1200
        },
        "solution": {
            "evacuation": "Move households near the river to designated safe areas when advised by authorities.",
            "shelter": "Prepare a nearby community shelter and transport assistance.",
            "resources": "Prepare drinking water, food packs, first-aid kits, and transport support."
        }
    },
    {
        "case_id": 4,
        "name": "Coastal Storm Surge - Sample Case",
        "problem": {
            "disaster_type": "typhoon",
            "flood_severity": "moderate",
            "location_type": "coastal",
            "affected_population": 2200
        },
        "solution": {
            "evacuation": "Issue early warnings and move residents away from storm-surge risk areas.",
            "shelter": "Prepare inland evacuation centers and transportation.",
            "resources": "Prepare communication equipment, food, water, and first-aid supplies."
        }
    },
    {
        "case_id": 5,
        "name": "Low-Severity Urban Flood - Sample Case",
        "problem": {
            "disaster_type": "flood",
            "flood_severity": "low",
            "location_type": "urban",
            "affected_population": 800
        },
        "solution": {
            "evacuation": "Monitor flood-prone streets and advise residents to move if conditions worsen.",
            "shelter": "Identify a nearby safe location and keep evacuation centers on standby.",
            "resources": "Prepare warning messages, drinking water, basic first aid, and transport if needed."
        }
    }
]

SEVERITY_LEVELS = {"low": 1, "moderate": 2, "high": 3}
LOCATION_OPTIONS = {"urban", "rural", "coastal"}
DISASTER_OPTIONS = {"typhoon", "flood", "earthquake"}

# Weighted similarity: disaster type 35%, flood severity 30%,
# location type 20%, and population similarity 15%.
WEIGHTS = {
    "disaster_type": 0.35,
    "flood_severity": 0.30,
    "location_type": 0.20,
    "affected_population": 0.15
}


def load_cases():
    """Load retained cases from JSON, or start with the five sample cases."""
    if CASE_FILE.exists():
        try:
            with CASE_FILE.open("r", encoding="utf-8") as file:
                saved_cases = json.load(file)
            if isinstance(saved_cases, list) and saved_cases:
                return saved_cases
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read saved case file. Using sample cases.")
    return [case.copy() for case in INITIAL_CASES]


def save_cases(cases):
    """Save the full case base so retained cases remain available next run."""
    with CASE_FILE.open("w", encoding="utf-8") as file:
        json.dump(cases, file, indent=4)


def get_nonempty_input(prompt):
    """Keep asking until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value


def get_choice(prompt, choices):
    """Ask for a value from a fixed list of choices."""
    choices_text = "/".join(sorted(choices))
    while True:
        value = input(f"{prompt} ({choices_text}): ").strip().lower()
        if value in choices:
            return value
        print(f"Please enter one of these choices: {choices_text}")


def get_population():
    """Validate that the population is a positive whole number."""
    while True:
        try:
            population = int(input("Estimated affected population: ").strip())
            if population > 0:
                return population
            print("Population must be greater than zero.")
        except ValueError:
            print("Please enter a whole number, such as 2500.")


def collect_new_problem():
    """Collect the attributes of the new disaster case."""
    print("\n=== ENTER NEW DISASTER ===")
    name = get_nonempty_input("Case name (e.g., New Urban Typhoon): ")
    disaster_type = get_choice(
        "Disaster type", DISASTER_OPTIONS
    )
    flood_severity = get_choice(
        "Flood/impact severity", set(SEVERITY_LEVELS)
    )
    location_type = get_choice(
        "Location type", LOCATION_OPTIONS
    )
    affected_population = get_population()

    return {
        "case_id": None,
        "name": name,
        "problem": {
            "disaster_type": disaster_type,
            "flood_severity": flood_severity,
            "location_type": location_type,
            "affected_population": affected_population
        },
        "solution": {}
    }


def population_similarity(new_population, old_population):
    """Return a score from 0 to 1; closer population sizes score higher."""
    larger = max(new_population, old_population)
    difference = abs(new_population - old_population)
    return max(0.0, 1.0 - (difference / larger))


def calculate_similarity(new_case, old_case):
    """Calculate a weighted similarity score between 0 and 100."""
    new = new_case["problem"]
    old = old_case["problem"]

    scores = {
        "disaster_type": 1.0 if new["disaster_type"] == old["disaster_type"] else 0.0,
        "flood_severity": 1.0 if new["flood_severity"] == old["flood_severity"] else 0.0,
        "location_type": 1.0 if new["location_type"] == old["location_type"] else 0.0,
        "affected_population": population_similarity(
            new["affected_population"], old["affected_population"]
        )
    }

    weighted_score = sum(scores[key] * WEIGHTS[key] for key in WEIGHTS)
    return weighted_score * 100


def retrieve_similar_cases(new_case, cases):
    """Rank all previous cases from most similar to least similar."""
    ranked_cases = []
    for case in cases:
        score = calculate_similarity(new_case, case)
        ranked_cases.append((score, case))

    ranked_cases.sort(key=lambda item: item[0], reverse=True)
    return ranked_cases


def adapt_solution(new_case, retrieved_case):
    """Adapt the retrieved response plan using the new case's details."""
    problem = new_case["problem"]
    old_solution = retrieved_case["solution"]
    population = problem["affected_population"]
    severity = problem["flood_severity"]
    location = problem["location_type"]
    disaster = problem["disaster_type"]

    # Start with the retrieved case's solution, then tailor each recommendation.
    if severity == "high":
        evacuation = (
            f"Prioritize urgent evacuation from high-risk areas. Coordinate with "
            f"local emergency officials for approximately {population:,} potentially affected people."
        )
        shelter = (
            f"Urgently confirm sufficient shelter capacity for up to {population:,} people, "
            "including accessible facilities and safe transport."
        )
        resources = (
            "Prioritize rescue teams, safe transport, drinking water, food, first-aid supplies, "
            "and reliable emergency communications."
        )
    elif severity == "moderate":
        evacuation = (
            f"Prepare targeted evacuation for high-risk areas and issue clear warnings to "
            f"communities within the potentially affected population of {population:,}."
        )
        shelter = (
            f"Check nearby evacuation centers and available capacity for approximately "
            f"{population:,} potentially affected people."
        )
        resources = (
            "Stage drinking water, food packs, first-aid supplies, transport, and communication equipment."
        )
    else:
        evacuation = (
            "Monitor conditions, issue precautionary warnings, and prepare to move residents "
            "if official alerts or local conditions worsen."
        )
        shelter = (
            f"Identify safe locations and keep shelter arrangements ready for up to "
            f"{population:,} potentially affected people."
        )
        resources = (
            "Prepare warning messages, basic first-aid supplies, drinking water, and transport if needed."
        )

    if location == "coastal":
        evacuation += " Give particular attention to coastal and storm-surge risk zones."
    elif location == "urban":
        evacuation += " Prioritize low-lying streets, drainage bottlenecks, and densely populated areas."
    else:
        evacuation += " Pay attention to riverbanks, isolated communities, and access routes."

    if disaster == "typhoon":
        resources += " Monitor official typhoon, rainfall, and wind advisories."
    elif disaster == "earthquake":
        resources += " Follow official earthquake safety guidance and check buildings and routes for hazards."
    else:
        resources += " Monitor official rainfall, river-level, and flood advisories."

    return {
        "evacuation": evacuation,
        "shelter": shelter,
        "resources": resources,
        "adapted_from": retrieved_case["name"],
        "reference_solution": {
            "evacuation": old_solution.get("evacuation", ""),
            "shelter": old_solution.get("shelter", ""),
            "resources": old_solution.get("resources", "")
        }
    }


def display_case(case):
    """Print a case in a readable format."""
    problem = case["problem"]
    print(f"\nCase ID: {case['case_id']} | Name: {case['name']}")
    print(
        f"  Disaster: {problem['disaster_type'].title()} | "
        f"Severity: {problem['flood_severity'].title()} | "
        f"Location: {problem['location_type'].title()} | "
        f"Population: {problem['affected_population']:,}"
    )
    if case.get("solution"):
        solution = case["solution"]
        print(f"  Evacuation: {solution.get('evacuation', 'N/A')}")
        print(f"  Shelter: {solution.get('shelter', 'N/A')}")
        print(f"  Resources: {solution.get('resources', 'N/A')}")


def main():
    cases = load_cases()

    print("=" * 65)
    print(" DISASTER RESPONSE DECISION SUPPORT SYSTEM (CBR)")
    print("=" * 65)
    print(f"Current case base: {len(cases)} case(s)")
    print("\n=== EXISTING CASE BASE ===")
    for case in cases:
        display_case(case)

    new_case = collect_new_problem()

    # Step 2: Similarity Assessment and Retrieval
    ranked_cases = retrieve_similar_cases(new_case, cases)
    print("\n=== SIMILARITY ASSESSMENT ===")
    for rank, (score, case) in enumerate(ranked_cases, start=1):
        print(f"{rank}. {case['name']} - Similarity: {score:.2f}%")

    best_score, best_case = ranked_cases[0]
    print("\n=== RETRIEVED MOST SIMILAR CASE ===")
    display_case(best_case)
    print(f"Similarity score: {best_score:.2f}%")

    # Step 3: Case Adaptation
    print("\n=== ADAPTED RESPONSE PLAN ===")
    adapted_solution = adapt_solution(new_case, best_case)
    new_case["solution"] = adapted_solution
    print(f"Adapted from: {adapted_solution['adapted_from']}")
    print(f"1. Evacuation: {adapted_solution['evacuation']}")
    print(f"2. Shelter: {adapted_solution['shelter']}")
    print(f"3. Resources: {adapted_solution['resources']}")

    # Step 4: Learning / Retention
    new_case["case_id"] = max(
        (case.get("case_id", 0) for case in cases), default=0
    ) + 1
    cases.append(new_case)
    save_cases(cases)

    print("\n=== LEARNING / RETENTION ===")
    print("New case saved successfully!")
    print(f"Saved to: {CASE_FILE.resolve()}")
    print(f"Updated case base contains {len(cases)} case(s).")

    print("\n=== UPDATED CASE BASE ===")
    for case in cases:
        display_case(case)

    print("\nReminder: This is a classroom prototype. Follow official emergency")
    print("alerts and local emergency-management authorities in real situations.")


if __name__ == "__main__":
    main()
