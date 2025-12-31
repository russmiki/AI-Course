def score(food, goal):
    if goal == "lose_weight":
        return food["protein"] * 2 - food["calories"]
    if goal == "gain_weight":
        return food["calories"] + food["protein"]
    return food["protein"]
