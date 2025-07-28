print("Welcome To Recipe Collection.\n")


class Recipe:
    def __init__(self, name, ingredients, cooking_time, cooking_instructions):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.cooking_instructions = cooking_instructions

    def display_recipe(self):
        print(f"Name: {self.name}")
        print(f"Ingredients: {self.ingredients}")
        print(f"Cooking Time: {self.cooking_time}")
        print(f"Instructions: {self.cooking_instructions}")


Recipe_1 = Recipe(name=input("Enter recipe name: ")
                  , ingredients=input("Enter ingredients (comma-separated): ")
                  , cooking_time=input("Enter Cooking Time: ")
                  , cooking_instructions=input("Enter Cooking Instructions: "))

print("\nDisplaying recipe .......")
Recipe_1.display_recipe()
