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

def find_notion_problem_id(problem_title):
    query = {
        "filter": {
            "value": "page",
            "property": "object"
        }
    }

    # Send the POST request to the Notion API
    response = requests.post(f"{os.getenv('NOTION-BASE-URL')}/v1/search", 
        headers=notion_headers, json=query)


    # Check if the request was successful
    if response.status_code == 200:
        search_results = response.json()["results"]
        page_id = None
        for result in search_results:
            if result["properties"]["Name"]["title"][0]["text"]["content"].lower() == problem_title.lower():
                page_id = result["id"]
                print(page_id)
                return page_id
                
        if not page_id:
            print(f"No page found with the name '{problem_title}'")

    else:
        print(f"Error: {response.status_code}: {response.text}")

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
problem_title = sys.argv[1]

# Use the arguments in your script
print(f"Argument 1: {problem_title}")

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

def update_notion_problem_entry(problem_id, anki_card_id, next_review_date):
    query = {
        "properties": {
            "anki_card_id": {  "number": anki_card_id },
            "next_review": { 
                "date": { "start": next_review_date }
            }
        }
    }

    response = requests.patch(f"{os.getenv('NOTION-BASE-URL')}/v1/pages/{problem_id}",
        headers=notion_headers, json=query)
    
    print(response.text)
    if response.status_code == 200:
        search_results = response.json()
        print(search_results)

def 

if __name__ == "__main__":

    problem_id = find_notion_problem_id(problem_title=problem_title)
    update_notion_problem_entry(problem_id=problem_id, anki_card_id=1234, next_review_date="2024-03-04")
