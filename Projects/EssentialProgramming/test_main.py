import json
from pprint import pprint

with open("biblioteca.json", "r") as file:
    pprint(json.load(file))
