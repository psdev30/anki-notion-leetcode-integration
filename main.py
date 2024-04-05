import os
import sys
from dotenv import load_dotenv
import requests


deck_name = "Leetcode"
# headers = {"X-Api-Key": os.getenv("ANKI-API-KEY")}


# Check if the required number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <Leetcode Question Name>")
    sys.exit(1)

# Get the command-line arguments
question = sys.argv[1]

# Use the arguments in your script
print(f"Argument 1: {question}")

load_dotenv()

params = {
    "action": "findCards",
    "version": 6,
    "params": {
        "query": f"deck:{deck_name} front:{question}"
    },
    "key": os.getenv("ANKI-API-KEY")
}

response = requests.post(
    f"http://{os.getenv('ANKI-BASE-URL')}:{os.getenv('ANKI-BASE-PORT')}",
    json=params
)

# Check if the request was successful
response.raise_for_status()

# Parse the response JSON
data = response.json()
print(data)