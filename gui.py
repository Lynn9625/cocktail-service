import os
import requests
import json
import PySimpleGUI as sg
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


## ASK USERS WHAT FUNCTION THEY WHAT TO USE
if __name__ == "__main__":
    layout1 = [
    [sg.Text("Hi, I'm your cocktail expert")],
    [sg.Listbox(values=("search cocktail by name","search cocktail by ingredient","random recommendation"), size=(40, 5), select_mode="single")],
    [sg.OK(),sg.Cancel()],
    ]
    window1 = sg.Window("Cocktail Search Service").Layout(layout1)
    event,values = window1.Read()


## SEARCH COCKTAIL BY NAME
    if values == {0: ['search cocktail by name']} and event == "OK":
        layout2 = [
        [sg.Text("The cocktail I want to know is")],
        [sg.Input()],
        [sg.OK(),sg.Cancel()],
        ]
        window2 = sg.Window("Cocktail Search Service").Layout(layout2)
        event, values = window2.Read()
        if values[0] != ''and event == "OK":
            request_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/search.php?s={values[0]}"
            response = requests.get(request_url)
            parsed_response = json.loads(response.text)
            try:    
                parsed_response["drinks"][0]
            except:
                sg.Popup("Invalid input. Please try again")
                exit()
            x = 0
            cocktails = []  ## This is a list of cocktails whose names all contain the keyword that user inputs in the previous step
            while x < len(parsed_response["drinks"]):
                cocktail = parsed_response["drinks"][x]["strDrink"]
                cocktails.append(cocktail)
                x += 1
            layout3 = [
                [sg.Text(f"The following cocktails all contain '{values[0]}' in their names")],
                [sg.Text("Interested in one of the following cocktails? Input its name to continue searching (case sensitive)")],
                [sg.InputText()],
                [sg.Multiline("\n".join(cocktails), autoscroll=True)],
                [sg.OK(),sg.Cancel()],
            ]
            window3 = sg.Window("Cocktail Search Service").Layout(layout3)
            event, values = window3.Read()
            if values[0] in cocktails and event == "OK":
                message = f"Name of cocktail: {values[0]}"
                name_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/search.php?s={values[0]}"
                for p in get_cocktail_ingredients(name_url):
                    message += f"\n{p}"
                message += f"\nType of glass:{get_cocktail_glass(name_url)}"
                message += f"\nInstruction: {get_cocktail_instruction(name_url)}"
                get_cocktail_image(name_url)
                sg.PopupScrolled(message,title="Cocktail Search Service")
            elif values[0] not in cocktails and event == "OK":
                sg.Popup("Invalid input. Please try again",title="Cocktail Search Service")
            elif event is None or event == "Cancel":
                exit()
        elif values[0] == '' and event == "OK":
            sg.Popup("No received input. Please try again")    
        elif event is None or event == "Cancel":
            exit()


## SEARCH COCKTAIL BY INGREDIENT
    elif values == {0: ['search cocktail by ingredient']} and event == "OK":        
        layout4 = [
        [sg.Text("The ingredient I choose is (capitalize the first letter)")],
        [sg.Input()],
        [sg.OK(),sg.Cancel()],
        ]
        window4 = sg.Window("Cocktail Search Service").Layout(layout4)
        event, values = window4.Read()
        if values[0] != '' and event == "OK":
            request_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/filter.php?i={values[0]}"
            print(request_url)
            response = requests.get(request_url)
            try:    
                parsed_response = json.loads(response.text)
                parsed_response["drinks"][0]
            except:
                sg.Popup("Invalid input. Please try again")
                exit()
            x = 0
            drinks = []  ## This is a list of cocktails whose names all contain the keyword that user inputs in the previous step
            while x < len(parsed_response["drinks"]):
                drink = parsed_response["drinks"][x]["strDrink"]
                drinks.append(drink)
                x += 1
            layout5 = [
                [sg.Text(f"The following cocktails all contain '{values[0]}' in their ingredients")],
                [sg.Text("Interested in one of the following cocktails? Input its name to continue searching (case sensitive)")],
                [sg.InputText()],
                [sg.Multiline("\n".join(drinks),autoscroll=True)],
                [sg.OK(),sg.Cancel()],
            ]
            window5 = sg.Window("Cocktail Search Service").Layout(layout5)
            event, values = window5.Read()
            if values[0] in drinks and event == "OK":
                message = f"Name of cocktail: {values[0]}"
                ingr_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/search.php?s={values[0]}"
                for p in get_cocktail_ingredients(ingr_url):
                    message += f"\n{p}"
                message += f"\nType of glass:{get_cocktail_glass(ingr_url)}"
                message += f"\nInstruction: {get_cocktail_instruction(ingr_url)}"
                get_cocktail_image(ingr_url)
                sg.PopupScrolled(message,title="Cocktail Search Service")
            elif values[0] not in drinks and event == "OK":
                sg.Popup("Invalid input. Please try again",title="Cocktail Search Service")
            elif event is None or event == "Cancel":
                exit()
        elif values[0] == '' and event == "OK":
            sg.Popup("No received input. Please try again")    
        elif event is None or event == "Cancel":
            exit()


## RANDOM SELECTION
    elif values == {0: ['random recommendation']} and event == "OK":   
        random_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/random.php"
        cocktail_response = requests.get(random_url)
        cocktail_parsed_response = json.loads(cocktail_response.text)
        message = "The recommended cocktail: " + cocktail_parsed_response["drinks"][0]["strDrink"]
        for p in get_cocktail_ingredients(random_url):
            message += f"\n{p}"
        message += f"\nType of glass:{get_cocktail_glass(random_url)}"
        message += f"\nInstruction: {get_cocktail_instruction(random_url)}"
        get_cocktail_image(random_url)
        sg.PopupScrolled(message,title="Cocktail Search Service")



    elif len(values[0]) < 1 and event == "OK":
        sg.Popup("No received input. Please try again")
    elif event is None or event == "Cancel":
        exit()
