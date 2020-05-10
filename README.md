# cocktail service (using API TheCocktailDB to know more about cocktails)
1) Fork the repo, then clone it to download it onto your own local computer and navigate there from the command-line:
Address: https://github.com/Lynn9625/Cocktail-Freestyle-Project
cd ~/Desktop/Cocktail-Freestyle-Project

2) Create and activate a new Anacona virtual environment named cocktail:
conda create -n cocktail-env python=3.7；
conda activate cocktail-env

3) From within the virtual environment, install the required packages:
pip install requests；
pip install python-dotenv；
pip install pytest

4) Get the API Key and create an ".env" file
Your repo should contain an ".env" file with your API Key. You can get API key from https://www.thecocktaildb.com/api.php. For this API, all users can use the developer key "1" as the API Key, but if you have other API Key, please make sure that it just appears in the ".env" file：
API_KEY = "1"

5) From within the virtual environment, demonstrate your ability to run the Python script through the command-line:
python cli.py (for CLI)；
python gui.py (for GUI)

6) From within the virtual environment, demonstrate your ability to run the automated test:
pytest test_cocktail.py

Note: if your Python version is lower than 3.0, please import other corresponding version of the PySimpleGUI package

Note: because the "gui.py" file uses the same "def" functions in the "cli.py" file, so there is just one "test_cocktail.py" file to run the automated test
