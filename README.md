# Cocktail-Freestyle-Project
1) Fork the repo, then clone it to download it onto your own local computer and navigate there from the command-line:
Address: https://github.com/Lynn9625/Cocktail-Freestyle-Project
cd ~/Desktop/Cocktail-Freestyle-Project

2) Create and activate a new Anacona virtual environment named cocktail:
conda create -n cocktail-env python=3.7
conda activate cocktail-env

3) From within the virtual environment, install the required packages:
pip install requests 
pip install python-dotenv 

4) Get the API Key and create an ".env" file
Your repo should contain an ".env" file with your apikey (for this api, all users can use the developer key "1" as the API key, but if you have other api keys, please make sure that it just appears in the .env file )
API_KEY = "1"

5) From within the virtual environment, demonstrate your ability to run the Python script frm the command-line:
python cocktail.py