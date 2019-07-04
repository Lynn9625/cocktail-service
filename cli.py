import os
import requests
import json
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO


load_dotenv()
apikey = os.environ.get("API_KEY")

    

def get_cocktail_ingredients(url):
    cocktail_response = requests.get(url)
    cocktail_parsed_response = json.loads(cocktail_response.text)
    cocktail_ingredients = []
    x = 1
    while cocktail_parsed_response["drinks"][0][f"strIngredient{x}"] != '':
        ingredient = cocktail_parsed_response["drinks"][0][f"strIngredient{x}"]
        measure = cocktail_parsed_response["drinks"][0][f"strMeasure{x}"]
        cocktail_ingredients.append(f"Ingredient{x}: {ingredient} {measure}")
        x += 1 
    return cocktail_ingredients
    
def get_cocktail_glass(url):
    cocktail_response = requests.get(url)
    cocktail_parsed_response = json.loads(cocktail_response.text)
    return cocktail_parsed_response["drinks"][0]["strGlass"]

def get_cocktail_instruction(url):
    cocktail_response = requests.get(url)
    cocktail_parsed_response = json.loads(cocktail_response.text)
    return cocktail_parsed_response["drinks"][0]["strInstructions"]

def get_cocktail_image(url):
    cocktail_response = requests.get(url)
    cocktail_parsed_response = json.loads(cocktail_response.text)
    image_url = cocktail_parsed_response["drinks"][0]["strDrinkThumb"]
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    image.show()



if __name__ == "__main__":
    ##1. Obtain a list of all ingredients
    pre_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/list.php?i=list"
    pre_response = requests.get(pre_url)
    pre_parsed_response = json.loads(pre_response.text)

    ingredients = []
    a = 0
    while a < len(pre_parsed_response["drinks"]):
        ingredient = pre_parsed_response["drinks"][a]["strIngredient1"]
        ingredients.append(ingredient)
        a += 1



    ##2. Get the user infomation input 
    ## (search cocktail by name; search cocktail by ingredient; get random recommendation)
    print("Hi, I'm your cocktail advisor. What do you want to know today?")
    print("--------------------------------------------------------------")
    print("FYI, you can input 'name' to search cocktail by name, 'ingredient' to search cocktail by ingredient, or 'random' to look for fun!")
    print("--------------------------------------------------------------")
    while True:
        selected_order = input("My choice is: ")
        if selected_order in ["name","ingredient","random"]:
            break
        else: 
            print("Oh, invaild value. Please try again!")
            next



    ##3. Compile and parse the URL
    if selected_order == "name":
        item = input("The cocktail I want to know is: ")
        variable = f"search.php?s={item}"
    elif selected_order == "ingredient":
        item = input("The ingredient I choose is (capitalize the first letter): ")
        if item in ingredients:
            variable = f"filter.php?i={item}"
        else:
            print("Oh, invalid value. Please try again!")
            exit()
    elif selected_order == "random":
        print("I'm recommending something new for you right now")
        variable = "random.php"

    request_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/{variable}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)



    ##4. Prevent an HTTP request if the cocktaili's name or ingredient that user searches not likely to be valid
    try:    
       parsed_response["drinks"][0]
    except:
       print('Oh no, something is wrong. Can we start over?')
       print('Shutting program down...')
       exit()



    ##5. Seach cocktail by name
    if "search.php" in request_url:    
        print("--------------------------------------------------------------")
        print(f"The following cocktails all contain '{item}' in their names:")
        b = 0
        cocktails = []  ## This is a list of cocktails whose names all contain the keyword that user inputs in the previous step
        while b < len(parsed_response["drinks"]):
            cocktail = parsed_response["drinks"][b]["strDrink"]
            cocktails.append(cocktail)
            b += 1
        for x in cocktails:
            print(x)
        print("--------------------------------------------------------------")
        cocktail_choice = input("Input the name of one listed cocktail to continue searching or 'DONE' to exit (case sensitive):")
        print("--------------------------------------------------------------") 
        if cocktail_choice in cocktails:
            name_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/search.php?s={cocktail_choice}"
            for p in get_cocktail_ingredients(name_url):
                print(p)
            print("--------------------------------------------------------------")
            print("Type of glass:",get_cocktail_glass(name_url))
            print("--------------------------------------------------------------")
            print("Instruction:",get_cocktail_instruction(name_url))
            get_cocktail_image(name_url)
        elif cocktail_choice == "DONE":
            pass
        else:
            print("Oh, invalid value. Please try again!")
            next



    ##6. Search cocktail by ingredient
    if "filter.php" in request_url: 
       print("--------------------------------------------------------------")
       print(f"The following cocktails all have the ingredient '{item}':")
       c = 0
       drinks = [] ## This is a list of cocktails containing the ingredient that user inputs in the previous step
       while c < len(parsed_response["drinks"]):
           drink = parsed_response["drinks"][c]["strDrink"]
           drinks.append(drink)
           c += 1
       for y in drinks:
        print(y)  
       print("--------------------------------------------------------------")
       drink_choice = input("Input the name of one listed cocktail to continue searching or 'DONE' to exit (case sensitive):")
       print("--------------------------------------------------------------")
       if drink_choice in drinks:
            ingr_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/search.php?s={drink_choice}"
            for p in get_cocktail_ingredients(ingr_url):
                print(p)
            print("--------------------------------------------------------------")
            print("Type of glass:",get_cocktail_glass(ingr_url))
            print("--------------------------------------------------------------")
            print("Instruction:",get_cocktail_instruction(ingr_url))
            get_cocktail_image(ingr_url)
       elif drink_choice == "DONE":
           pass
       else:
           print("Oh, invalid value. Please try again!")
           next



    ##7. Get random recommendation
    if "random.php" in request_url:
       print("--------------------------------------------------------------")
       print("The recommended cocktail is:",parsed_response["drinks"][0]["strDrink"])
       print("--------------------------------------------------------------")
       random_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/random.php"
       for p in get_cocktail_ingredients(random_url):
                print(p)
       print("--------------------------------------------------------------")
       print("Type of glass:",get_cocktail_glass(random_url))
       print("--------------------------------------------------------------")
       print("Instruction:",get_cocktail_instruction(random_url))
       get_cocktail_image(random_url)





