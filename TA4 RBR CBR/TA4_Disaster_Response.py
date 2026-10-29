"""
TA4 - Knowledge Representation, Rule-Based Reasoning, and Case-Based Reasoning
Use case: Disaster Response Decision Support System

This educational prototype uses sample data only. It does not replace official
emergency services or real-time disaster information.
"""

from copy import deepcopy

# PART 1: KNOWLEDGE REPRESENTATION (KR)
# Facts are grouped into three categories: hazard, impact, and resources.
incident_facts = {
    "hazard": {
        "heavy_rain": True,
        "flood_level_cm": 65,
        "road_blocked": True,
    },
    "impact": {
        "people_needing_evacuation": 120,
        "injured_people": 4,
    },
    "resources": {
        "shelter_available": True,
        "rescue_vehicles_available": 2,
    },
}


# PART 2: RULE-BASED REASONING (RBR)
# Each function checks the knowledge base and returns an action if its rule fires.
def rule_flood_warning(facts):
    if facts["hazard"]["heavy_rain"] and facts["hazard"]["flood_level_cm"] >= 50:
        return "Issue a flood warning for the affected area."
    return None


def rule_road_closure(facts):
    if facts["hazard"]["road_blocked"]:
        return "Notify responders and mark the blocked road as inaccessible."
    return None


def rule_evacuation(facts):
    if facts["impact"]["people_needing_evacuation"] >= 50 and facts["resources"]["shelter_available"]:
        return "Coordinate evacuation and direct residents to the available shelter."
    return None


def rule_medical_support(facts):
    if facts["impact"]["injured_people"] > 0:
        return "Dispatch medical support for injured people."
    return None


def run_rbr(facts):
    """Inference engine: check every rule and collect all inferred actions."""
    rules = [rule_flood_warning, rule_road_closure, rule_evacuation, rule_medical_support]
    actions = []
    for rule in rules:
        action = rule(facts)
        if action:
            actions.append(action)
    return actions


# PART 3: CASE-BASED REASONING (CBR)
# Each case stores problem features and a solution from a previous incident.
case_base = [
    {
        "name": "Case 1 - Severe Flooding",
        "problem": {"heavy_rain": True, "flood_level_high": True, "road_blocked": True,
                    "many_evacuees": True, "injuries": True},
        "solution": "Issue a flood warning, close blocked roads, evacuate residents, and send medical support."
    },
    {
        "name": "Case 2 - Localized Road Flooding",
        "problem": {"heavy_rain": True, "flood_level_high": False, "road_blocked": True,
                    "many_evacuees": False, "injuries": False},
        "solution": "Warn nearby residents and reroute traffic away from the flooded road."
    },
    {
        "name": "Case 3 - Earthquake with Injuries",
        "problem": {"heavy_rain": False, "flood_level_high": False, "road_blocked": True,
                    "many_evacuees": True, "injuries": True},
        "solution": "Secure damaged roads, evacuate affected residents, and dispatch medical teams."
    },
]


def get_problem_features(facts):
    """Convert current facts to the same feature format used by stored cases."""
    return {
        "heavy_rain": facts["hazard"]["heavy_rain"],
        "flood_level_high": facts["hazard"]["flood_level_cm"] >= 50,
        "road_blocked": facts["hazard"]["road_blocked"],
        "many_evacuees": facts["impact"]["people_needing_evacuation"] >= 50,
        "injuries": facts["impact"]["injured_people"] > 0,
    }


def similarity(new_problem, old_problem):
    """Simple matching score: proportion of matching Boolean features."""
    matches = sum(new_problem[key] == old_problem[key] for key in new_problem)
    return matches / len(new_problem)


def retrieve_most_similar_case(new_problem, cases):
    best_case = None
    best_score = -1
    for case in cases:
        score = similarity(new_problem, case["problem"])
        if score > best_score:
            best_case = case
            best_score = score
    return best_case, best_score


def run_cbr(facts, cases):
    # RETRIEVE: find the case with the highest feature match.
    new_problem = get_problem_features(facts)
    matched_case, score = retrieve_most_similar_case(new_problem, cases)

    # REUSE: begin with the solution from the most similar past case.
    reused_solution = matched_case["solution"]

    # REVISE: a simple example of adapting the past solution to current facts.
    revised_solution = reused_solution
    if facts["resources"]["rescue_vehicles_available"] < 2:
        revised_solution += " Prioritize the highest-risk locations because rescue vehicles are limited."
    if not facts["resources"]["shelter_available"]:
        revised_solution += " Identify a safe temporary evacuation site."

    # RETAIN: store the current problem and revised solution as a new case.
    new_case = {
        "name": "New Case - Current Flood Incident",
        "problem": new_problem,
        "solution": revised_solution,
    }
    cases.append(new_case)
    return matched_case["name"], score, reused_solution, revised_solution, len(cases)


def main():
    print("=" * 66)
    print("TA4: DISASTER RESPONSE DECISION SUPPORT SYSTEM")
    print("=" * 66)

    print("\nPART 1 - KNOWLEDGE BASE")
    print("Categories: hazard, impact, resources")
    for category, facts in incident_facts.items():
        print(f"  {category.title()}: {facts}")

    print("\nPART 2 - RULE-BASED REASONING ACTIONS")
    actions = run_rbr(incident_facts)
    for action in actions:
        print(f"  - {action}")

    print("\nPART 3 - CASE-BASED REASONING")
    matched_name, score, reused, revised, count = run_cbr(incident_facts, case_base)
    print(f"  Retrieved case: {matched_name}")
    print(f"  Similarity score: {score:.0%}")
    print(f"  Reused solution: {reused}")
    print(f"  Revised solution: {revised}")
    print(f"  Retain step: new case added; case base now has {count} cases.")

    print("\nNote: This is a classroom prototype using sample data, not live emergency advice.")


if __name__ == "__main__":
    main()
