import operator
from dataclasses import dataclass
from functools import reduce

import common.input_data as input_data

@dataclass
class Meal:
    ingredients: set[str]
    allergens: set[str]

    def get_number_of_ingredients_matching(self, ingredients: set[str]) -> int:
        return len(ingredients & self.ingredients)

def to_meal(text: str) -> Meal:
    ingredients, allergens = text.strip(')').split(' (contains ')
    return Meal(set(ingredients.split(" ")), set(allergens.split(', ')))


def get_number_of_times_nonallergen_ingredients_appear(meals: list[Meal]) -> int:
    allergen_to_ingredient = get_allergen_ingredients(meals)
    non_allergen_ingredients = get_all_ingredients(meals) - set(allergen_to_ingredient.values())
    return sum([meal.get_number_of_ingredients_matching(non_allergen_ingredients)
                for meal in meals])

def get_stripped_meals(meals: list[Meal], ingredients: list[str]) -> list[Meal]:
    return [Meal(m.ingredients - set(ingredients), m.allergens) for m in meals]

def get_allergen_ingredients(meals: list[Meal]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    all_allergens = get_all_allergens(meals)
    while len(mapping) != len(all_allergens):
        possible_ingredients: dict[str, set[str]] = {}
        for meal in get_stripped_meals(meals, list(mapping.values())):
            for allergen in meal.allergens:
                if allergen not in possible_ingredients:
                    possible_ingredients[allergen] = set(meal.ingredients)
                else:
                    possible_ingredients[allergen] &= meal.ingredients
        mapping |= {allergen: ingredients.pop()
                    for allergen, ingredients in possible_ingredients.items()
                    if len(ingredients) == 1}
    return mapping

def get_all_allergens(meals: list[Meal]) -> set[str]:
    return reduce(operator.or_, [m.allergens for m in meals])

def get_all_ingredients(meals: list[Meal]) -> set[str]:
    return reduce(operator.or_, [m.ingredients for m in meals])

def get_canonically_dangerous_ingredient(meals: list[Meal]) -> str:
    allergen_to_ingredient = get_allergen_ingredients(meals)
    return ",".join(ingredient for _,ingredient in sorted(allergen_to_ingredient.items(),
                                                          key=operator.itemgetter(0)))

MEALS = input_data.read("input/input21.txt", to_meal)
if __name__ == "__main__":
    print(get_number_of_times_nonallergen_ingredients_appear(MEALS))
    print(get_canonically_dangerous_ingredient(MEALS))
