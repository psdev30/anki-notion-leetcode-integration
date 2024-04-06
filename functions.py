import os
from dotenv import load_dotenv
import requests

load_dotenv()


notion_headers = {
    "Authorization": f"Bearer {os.getenv('NOTION-SECRET-KEY')}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}


def find_card(deck_name, problem_title):
    params = {
        "action": "findCards",
        "version": 6,
        "params": {
            "query": f"deck:{deck_name} front:{problem_title}"
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
    return data

def find_next_review_date(anki_card_id):
    print(anki_card_id)
    params = {
        "action": "cardsInfo",
        "version": 6,
        "params": {
            "cards": [anki_card_id]
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
    return data

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
    
    if response.status_code == 200:
        search_results = response.json()
        print(search_results)
        return True