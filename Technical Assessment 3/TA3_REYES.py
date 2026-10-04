# TA3: Case-Based Reasoning System
# Case Study: Intelligent Tutoring System (ITS)

from pprint import pprint


# =====================================================
# PART 1: CASE BASE
# =====================================================

case_base = [
    {
        "problem": {
            "topic": "fractions",
            "error": "wrong_denominator",
            "level": "beginner",
            "attempts": 2
        },
        "solution": "Review how to find a common denominator."
    },
    {
        "problem": {
            "topic": "algebra",
            "error": "wrong_operation",
            "level": "beginner",
            "attempts": 3
        },
        "solution": "Review the basic operations used in solving equations."
    },
    {
        "problem": {
            "topic": "fractions",
            "error": "wrong_numerator",
            "level": "intermediate",
            "attempts": 2
        },
        "solution": "Practice multiplying numerators correctly."
    },
    {
        "problem": {
            "topic": "geometry",
            "error": "wrong_formula",
            "level": "intermediate",
            "attempts": 4
        },
        "solution": "Review the correct formula before solving the problem."
    },
    {
        "problem": {
            "topic": "algebra",
            "error": "wrong_operation",
            "level": "intermediate",
            "attempts": 2
        },
        "solution": "Practice balancing both sides of an equation."
    }
]


# =====================================================
# PART 2: NEW PROBLEM
# =====================================================

new_problem = {
    "topic": input("Enter the topic (fractions/algebra/geometry): ").lower(),
    "error": input(
        "Enter the error "
        "(wrong_denominator/wrong_numerator/wrong_operation/wrong_formula): "
    ).lower(),
    "level": input("Enter the student level (beginner/intermediate): ").lower(),
    "attempts": int(input("Enter the number of attempts: "))
}

print("\nNEW STUDENT PROBLEM")
pprint(new_problem)


# =====================================================
# PART 3: SIMILARITY ASSESSMENT
# =====================================================

def calculate_similarity(new_problem, old_problem):
    score = 0

    # Topic is highly important
    if new_problem["topic"] == old_problem["topic"]:
        score += 3

    # Error type is also highly important
    if new_problem["error"] == old_problem["error"]:
        score += 4

    # Student level
    if new_problem["level"] == old_problem["level"]:
        score += 1

    # Similar number of attempts
    if abs(new_problem["attempts"] - old_problem["attempts"]) <= 1:
        score += 1

    return score


def retrieve_case(new_problem, case_base):
    best_case = None
    highest_score = -1

    for case in case_base:
        score = calculate_similarity(
            new_problem,
            case["problem"]
        )

        print("Compared with case:", case["problem"])
        print("Similarity score:", score)

        if score > highest_score:
            highest_score = score
            best_case = case

    return best_case, highest_score


retrieved_case, similarity_score = retrieve_case(
    new_problem,
    case_base
)

print("\nRETRIEVED CASE")
pprint(retrieved_case)

print("\nHIGHEST SIMILARITY SCORE:", similarity_score)


# =====================================================
# PART 4: REUSE AND ADAPT THE SOLUTION
# =====================================================

adapted_solution = retrieved_case["solution"]

if new_problem["attempts"] >= 3:
    adapted_solution += (
        " The student should also complete additional practice exercises."
    )
else:
    adapted_solution += (
        " The student should answer guided practice questions."
    )

print("\nADAPTED SOLUTION")
print(adapted_solution)


# =====================================================
# PART 5: REVISE
# =====================================================

revision = input(
    "\nEnter a revised solution or press Enter to keep the adapted solution: "
)

if revision.strip() != "":
    final_solution = revision
    print("Solution revised.")
else:
    final_solution = adapted_solution
    print("Adapted solution retained.")


# =====================================================
# PART 6: RETAIN
# =====================================================

new_case = {
    "problem": new_problem,
    "solution": final_solution
}

case_base.append(new_case)

print("\nNEW CASE SAVED SUCCESSFULLY!")
print("\nUPDATED CASE BASE:")

for number, case in enumerate(case_base, start=1):
    print(f"\nCase {number}")
    pprint(case)