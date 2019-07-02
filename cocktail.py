import os
import requests
import json
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()
apikey = os.environ.get("API_KEY")

    
def get_cocktail_info(url):
    cocktail_response = requests.get(url)
    cocktail_parsed_response = json.loads(cocktail_response.text)
    x = 1
    while cocktail_parsed_response["drinks"][0][f"strIngredient{x}"] != '':
        ingredients = cocktail_parsed_response["drinks"][0][f"strIngredient{x}"]
        measures = cocktail_parsed_response["drinks"][0][f"strMeasure{x}"]
        print(f"Ingredient{x}: {ingredients}  {measures}")
        x += 1   
    print("--------------------------------------------------------------")
    print("Type of glass:",cocktail_parsed_response["drinks"][0]["strGlass"])
    print("--------------------------------------------------------------")
    print("Instruction:",cocktail_parsed_response["drinks"][0]["strInstructions"])
    image_url = cocktail_parsed_response["drinks"][0]["strDrinkThumb"]
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    image.show()




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
    cocktail_choice = input("Input the name of one listed cocktail to continue searching or 'DONE' to exit:")
    print("--------------------------------------------------------------") 
    if cocktail_choice in cocktails:
        name_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/search.php?s={cocktail_choice}"
        get_cocktail_info(name_url)
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
   drink_choice = input("Input the name of one listed cocktail to continue searching or 'DONE' to exit:")
   print("--------------------------------------------------------------")
   if drink_choice in drinks:
       ingr_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/search.php?s={drink_choice}"
       get_cocktail_info(ingr_url)
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
   get_cocktail_info(random_url)





