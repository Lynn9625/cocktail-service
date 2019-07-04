import os
import requests
import json
from dotenv import load_dotenv
from cli import get_cocktail_ingredients
from cli import get_cocktail_glass
from cli import get_cocktail_instruction

load_dotenv()
apikey = os.environ.get("API_KEY")

## In this test, I gather the infomation ahead of time about a specific cocktail "Margarita" (e.g. ingredients; type of glass; instruction) from the raw data in advance
## Then, my goal is to test whether functions in the "cocktail.py" file can return these desired information
def test_get_cocktail_ingredients():
    cocktail_choice = 'Margarita'
    test_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/search.php?s={cocktail_choice}"
    assert 'Ingredient1: Tequila 1 1/2 oz ' in get_cocktail_ingredients(test_url)
    assert 'Ingredient2: Triple sec 1/2 oz ' in get_cocktail_ingredients(test_url)
    assert 'Ingredient3: Lime juice 1 oz ' in get_cocktail_ingredients(test_url)
    assert 'Ingredient4: Salt ' in get_cocktail_ingredients(test_url)

def test_get_cocktail_glass():
    cocktail_choice = 'Margarita'
    test_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/search.php?s={cocktail_choice}"
    assert get_cocktail_glass(test_url) == "Cocktail glass"

def test_get_cocktail_instruction():
    cocktail_choice = 'Margarita'
    test_url = f"https://www.thecocktaildb.com/api/json/v1/{apikey}/search.php?s={cocktail_choice}"
    assert get_cocktail_instruction(test_url) == "Rub the rim of the glass with the lime slice to make the salt stick to it. Take care to moisten only the outer rim and sprinkle the salt on it. The salt should present to the lips of the imbiber and never mix into the cocktail. Shake the other ingredients with ice, then carefully pour into the glass."