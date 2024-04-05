import os
import sys
from dotenv import load_dotenv
import requests
import urllib.parse


load_dotenv()
# Define the Notion API endpoint and headers
notion_headers = {
    "Authorization": f"Bearer {os.getenv('NOTION-SECRET-KEY')}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_all_pages():
    query = {
        "filter": {
            "value": "page",
            "property": "object"
        }
    }

    # Send the POST request to the Notion API
    response = requests.post(f"{os.getenv('NOTION-BASE-URL')}/v1/search", headers=notion_headers, json=query)


    # Check if the request was successful
    if response.status_code == 200:
        search_results = response.json()["results"]
        # You can also print additional properties or the entire page object
        print(search_results)

    else:
        print(f"Error: {response.status_code} - {response.text}")

def get_notion_page(query):
    # Define the search query
    page_name = "Personal Home"
    # Encode special characters and remove leading/trailing whitespace
    encoded_page_name = urllib.parse.quote(page_name.strip())  
    query = {
        "query": encoded_page_name,
        "filter": {
            "value": "page",
            "property": "object"
        }
    }

    # Send the POST request to the Notion API
    response = requests.post(os.getenv("NOTION-BASE-URL"), headers=notion_headers, json=query)

    # Check if the request was successful
    if response.status_code == 200:
        search_results = response.json()["results"]

        # Iterate over the search results
        for result in search_results:
            page_id = result["id"]
            page_title = result["properties"]["title"]["title"][0]["text"]["content"]

            # Check if the page title matches the desired name (case-insensitive)
            if page_title.lower() == encoded_page_name.lower():
                print(f"Page found: {page_title} (ID: {page_id})")
                break
        else:
            print(f"No page found with the name '{page_name}'")
    else:
        print(f"Error: {response.status_code} - {response.text}")

deck_name = "Leetcode"

# Check if the required number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <Leetcode Question Name>")
    sys.exit(1)

# Get the command-line arguments
question = sys.argv[1]

# Use the arguments in your script
print(f"Argument 1: {question}")

def get_card(deck_name, question):
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


get_all_pages()